from __future__ import print_function, unicode_literals

import abc
import argparse
import ast
import json
import os
import re
import subprocess
import sys

from collections import defaultdict

from . import fnmatch
from ..localpaths import repo_root
from ..gitignore.gitignore import PathFilter

from manifest.sourcefile import SourceFile, js_meta_re, python_meta_re
from six import binary_type, iteritems, itervalues
from six.moves import range
from six.moves.urllib.parse import urlsplit, urljoin

here = os.path.abspath(os.path.split(__file__)[0])

ERROR_MSG = """You must fix all errors; for details on how to fix them, see
https://github.com/w3c/web-platform-tests/blob/master/docs/lint-tool.md

However, instead of fixing a particular error, it's sometimes
OK to add a line to the lint.whitelist file in the root of the
web-platform-tests directory to make the lint tool ignore it.

For example, to make the lint tool ignore all '%s'
errors in the %s file,
you could add the following line to the lint.whitelist file.

%s:%s"""

def all_filesystem_paths(repo_root):
    path_filter = PathFilter(repo_root, extras=[".git/*"])
    for dirpath, dirnames, filenames in os.walk(repo_root):
        for filename in filenames:
            path = os.path.relpath(os.path.join(dirpath, filename), repo_root)
            if path_filter(path):
                yield path
        dirnames[:] = [item for item in dirnames if
                       path_filter(os.path.relpath(os.path.join(dirpath, item) + "/",
                                                   repo_root))]

def check_path_length(repo_root, path, css_mode):
    if len(path) + 1 > 150:
        return [("PATH LENGTH", "/%s longer than maximum path length (%d > 150)" % (path, len(path) + 1), path, None)]
    return []


def check_worker_collision(repo_root, path, css_mode):
    endings = [(".any.html", ".any.js"),
               (".any.worker.html", ".any.js"),
               (".worker.html", ".worker.js")]
    for path_ending, generated in endings:
        if path.endswith(path_ending):
            return [("WORKER COLLISION",
                     "path ends with %s which collides with generated tests from %s files" % (path_ending, generated),
                     path,
                     None)]
    return []


def parse_whitelist(f):
    """
    Parse the whitelist file given by `f`, and return the parsed structure.
    """

    data = defaultdict(lambda:defaultdict(set))
    ignored_files = set()

    for line in f:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = [item.strip() for item in line.split(":")]
        if len(parts) == 2:
            parts.append(None)
        else:
            parts[-1] = int(parts[-1])

        error_type, file_match, line_number = parts
        file_match = os.path.normcase(file_match)

        if error_type == "*":
            ignored_files.add(file_match)
        else:
            data[error_type][file_match].add(line_number)

    return data, ignored_files


def filter_whitelist_errors(data, errors):
    """
    Filter out those errors that are whitelisted in `data`.
    """

    if not errors:
        return []

    whitelisted = [False for item in range(len(errors))]

    for i, (error_type, msg, path, line) in enumerate(errors):
        normpath = os.path.normcase(path)
        if error_type in data:
            wl_files = data[error_type]
            for file_match, allowed_lines in iteritems(wl_files):
                if None in allowed_lines or line in allowed_lines:
                    if fnmatch.fnmatchcase(normpath, file_match):
                        whitelisted[i] = True

    return [item for i, item in enumerate(errors) if not whitelisted[i]]

class Regexp(object):
    pattern = None
    file_extensions = None
    error = None
    _re = None

    def __init__(self):
        self._re = re.compile(self.pattern)

    def applies(self, path):
        return (self.file_extensions is None or
                os.path.splitext(path)[1] in self.file_extensions)

    def search(self, line):
        return self._re.search(line)

class TrailingWhitespaceRegexp(Regexp):
    pattern = b"[ \t\f\v]$"
    error = "TRAILING WHITESPACE"
    description = "Whitespace at EOL"

class TabsRegexp(Regexp):
    pattern = b"^\t"
    error = "INDENT TABS"
    description = "Tabs used for indentation"

class CRRegexp(Regexp):
    pattern = b"\r$"
    error = "CR AT EOL"
    description = "CR character in line separator"

class SetTimeoutRegexp(Regexp):
    pattern = b"setTimeout\s*\("
    error = "SET TIMEOUT"
    file_extensions = [".html", ".htm", ".js", ".xht", ".xhtml", ".svg"]
    description = "setTimeout used; step_timeout should typically be used instead"

class W3CTestOrgRegexp(Regexp):
    pattern = b"w3c\-test\.org"
    error = "W3C-TEST.ORG"
    description = "External w3c-test.org domain used"

class Webidl2Regexp(Regexp):
    pattern = b"webidl2\.js"
    error = "WEBIDL2.JS"
    description = "Legacy webidl2.js script used"

class ConsoleRegexp(Regexp):
    pattern = b"console\.[a-zA-Z]+\s*\("
    error = "CONSOLE"
    file_extensions = [".html", ".htm", ".js", ".xht", ".xhtml", ".svg"]
    description = "Console logging API used"

class PrintRegexp(Regexp):
    pattern = b"print(?:\s|\s*\()"
    error = "PRINT STATEMENT"
    file_extensions = [".py"]
    description = "Print function used"

regexps = [item() for item in
           [TrailingWhitespaceRegexp,
            TabsRegexp,
            CRRegexp,
            SetTimeoutRegexp,
            W3CTestOrgRegexp,
            Webidl2Regexp,
            ConsoleRegexp,
            PrintRegexp]]

def check_regexp_line(repo_root, path, f, css_mode):
    errors = []

    applicable_regexps = [regexp for regexp in regexps if regexp.applies(path)]

    for i, line in enumerate(f):
        for regexp in applicable_regexps:
            if regexp.search(line):
                errors.append((regexp.error, regexp.description, path, i+1))

    return errors

def check_parsed(repo_root, path, f, css_mode):
    source_file = SourceFile(repo_root, path, "/", contents=f.read())

    errors = []

    if css_mode or path.startswith("css/"):
        if (source_file.type == "support" and
            not source_file.name_is_non_test and
            not source_file.name_is_reference):
            return [("SUPPORT-WRONG-DIR", "Support file not in support directory", path, None)]

    if source_file.name_is_non_test or source_file.name_is_manual:
        return []

    if source_file.markup_type is None:
        return []

    if source_file.root is None:
        return [("PARSE-FAILED", "Unable to parse file", path, None)]

    if source_file.type == "manual" and not source_file.name_is_manual:
        return [("CONTENT-MANUAL", "Manual test whose filename doesn't end in '-manual'", path, None)]

    if source_file.type == "visual" and not source_file.name_is_visual:
        return [("CONTENT-VISUAL", "Visual test whose filename doesn't end in '-visual'", path, None)]

    for reftest_node in source_file.reftest_nodes:
        href = reftest_node.attrib.get("href", "")
        parts = urlsplit(href)
        if parts.scheme or parts.netloc:
            errors.append(("ABSOLUTE-URL-REF",
                     "Reference test with a reference file specified via an absolute URL: '%s'" % href, path, None))
            continue

        ref_url = urljoin(source_file.url, href)
        ref_parts = urlsplit(ref_url)

        if source_file.url == ref_url:
            errors.append(("SAME-FILE-REF",
                           "Reference test which points at itself as a reference",
                           path,
                           None))
            continue

        assert ref_parts.path != ""

        reference_file = os.path.join(repo_root, ref_parts.path[1:])
        reference_rel = reftest_node.attrib.get("rel", "")

        if not os.path.isfile(reference_file):
            errors.append(("NON-EXISTENT-REF",
                     "Reference test with a non-existent '%s' relationship reference: '%s'" % (reference_rel, href), path, None))

    if len(source_file.timeout_nodes) > 1:
        errors.append(("MULTIPLE-TIMEOUT", "More than one meta name='timeout'", path, None))

    for timeout_node in source_file.timeout_nodes:
        timeout_value = timeout_node.attrib.get("content", "").lower()
        if timeout_value != "long":
            errors.append(("INVALID-TIMEOUT", "Invalid timeout value %s" % timeout_value, path, None))

    if source_file.testharness_nodes:
        if len(source_file.testharness_nodes) > 1:
            errors.append(("MULTIPLE-TESTHARNESS",
                           "More than one <script src='/resources/testharness.js'>", path, None))

        testharnessreport_nodes = source_file.root.findall(".//{http://www.w3.org/1999/xhtml}script[@src='/resources/testharnessreport.js']")
        if not testharnessreport_nodes:
            errors.append(("MISSING-TESTHARNESSREPORT",
                           "Missing <script src='/resources/testharnessreport.js'>", path, None))
        else:
            if len(testharnessreport_nodes) > 1:
                errors.append(("MULTIPLE-TESTHARNESSREPORT",
                               "More than one <script src='/resources/testharnessreport.js'>", path, None))

        testharnesscss_nodes = source_file.root.findall(".//{http://www.w3.org/1999/xhtml}link[@href='/resources/testharness.css']")
        if testharnesscss_nodes:
            errors.append(("PRESENT-TESTHARNESSCSS",
                           "Explicit link to testharness.css present", path, None))

        for element in source_file.variant_nodes:
            if "content" not in element.attrib:
                errors.append(("VARIANT-MISSING",
                               "<meta name=variant> missing 'content' attribute", path, None))
            else:
                variant = element.attrib["content"]
                if variant != "" and variant[0] not in ("?", "#"):
                    errors.append(("MALFORMED-VARIANT",
                               "%s <meta name=variant> 'content' attribute must be the empty string or start with '?' or '#'" % path, None))

        seen_elements = {"timeout": False,
                         "testharness": False,
                         "testharnessreport": False}
        required_elements = [key for key, value in {"testharness": True,
                                                    "testharnessreport": len(testharnessreport_nodes) > 0,
                                                    "timeout": len(source_file.timeout_nodes) > 0}.items()
                             if value]

        for elem in source_file.root.iter():
            if source_file.timeout_nodes and elem == source_file.timeout_nodes[0]:
                seen_elements["timeout"] = True
                if seen_elements["testharness"]:
                    errors.append(("LATE-TIMEOUT",
                                   "<meta name=timeout> seen after testharness.js script", path, None))

            elif elem == source_file.testharness_nodes[0]:
                seen_elements["testharness"] = True

            elif testharnessreport_nodes and elem == testharnessreport_nodes[0]:
                seen_elements["testharnessreport"] = True
                if not seen_elements["testharness"]:
                    errors.append(("EARLY-TESTHARNESSREPORT",
                                   "testharnessreport.js script seen before testharness.js script", path, None))

            if all(seen_elements[name] for name in required_elements):
                break


    for element in source_file.root.findall(".//{http://www.w3.org/1999/xhtml}script[@src]"):
        src = element.attrib["src"]
        for name in ["testharness", "testharnessreport"]:
            if "%s.js" % name == src or ("/%s.js" % name in src and src != "/resources/%s.js" % name):
                errors.append(("%s-PATH" % name.upper(), "%s.js script seen with incorrect path" % name, path, None))


    return errors

class ASTCheck(object):
    __metaclass__ = abc.ABCMeta
    error = None
    description = None

    @abc.abstractmethod
    def check(self, root):
        pass

class OpenModeCheck(ASTCheck):
    error = "OPEN-NO-MODE"
    description = "File opened without providing an explicit mode (note: binary files must be read with 'b' in the mode flags)"

    def check(self, root):
        errors = []
        for node in ast.walk(root):
            if isinstance(node, ast.Call):
                if hasattr(node.func, "id") and node.func.id in ("open", "file"):
                    if (len(node.args) < 2 and
                        all(item.arg != "mode" for item in node.keywords)):
                        errors.append(node.lineno)
        return errors

ast_checkers = [item() for item in [OpenModeCheck]]

def check_python_ast(repo_root, path, f, css_mode):
    if not path.endswith(".py"):
        return []

    try:
        root = ast.parse(f.read())
    except SyntaxError as e:
        return [("PARSE-FAILED", "Unable to parse file", path, e.lineno)]

    errors = []
    for checker in ast_checkers:
        for lineno in checker.check(root):
            errors.append((checker.error, checker.description, path, lineno))
    return errors


broken_js_metadata = re.compile(b"//\s*META:")
broken_python_metadata = re.compile(b"#\s*META:")


def check_script_metadata(repo_root, path, f, css_mode):
    if path.endswith((".worker.js", ".any.js")):
        meta_re = js_meta_re
        broken_metadata = broken_js_metadata
    elif path.endswith(".py"):
        meta_re = python_meta_re
        broken_metadata = broken_python_metadata
    else:
        return []

    done = False
    errors = []
    for idx, line in enumerate(f):
        assert isinstance(line, binary_type), line

        m = meta_re.match(line)
        if m:
            key, value = m.groups()
            if key == b"timeout":
                if value != b"long":
                    errors.append(("UNKNOWN-TIMEOUT-METADATA", "Unexpected value for timeout metadata", path, idx + 1))
            elif key == b"script":
                pass
            else:
                errors.append(("UNKNOWN-METADATA", "Unexpected kind of metadata", path, idx + 1))
        else:
            done = True

        if done:
            if meta_re.match(line):
                errors.append(("STRAY-METADATA", "Metadata comments should start the file", path, idx + 1))
            elif meta_re.search(line):
                errors.append(("INDENTED-METADATA", "Metadata comments should start the line", path, idx + 1))
            elif broken_metadata.search(line):
                errors.append(("BROKEN-METADATA", "Metadata comment is not formatted correctly", path, idx + 1))

    return errors


def check_path(repo_root, path, css_mode):
    """
    Runs lints that check the file path.

    :param repo_root: the repository root
    :param path: the path of the file within the repository
    :param css_mode: whether we're in CSS testsuite mode
    :returns: a list of errors found in ``path``
    """

    errors = []
    for path_fn in path_lints:
        errors.extend(path_fn(repo_root, path, css_mode))
    return errors


def check_file_contents(repo_root, path, f, css_mode):
    """
    Runs lints that check the file contents.

    :param repo_root: the repository root
    :param path: the path of the file within the repository
    :param f: a file-like object with the file contents
    :param css_mode: whether we're in CSS testsuite mode
    :returns: a list of errors found in ``f``
    """

    errors = []
    for file_fn in file_lints:
        errors.extend(file_fn(repo_root, path, f, css_mode))
        f.seek(0)
    return errors


def output_errors_text(errors):
    for error_type, description, path, line_number in errors:
        pos_string = path
        if line_number:
            pos_string += ":%s" % line_number
        print("%s: %s (%s)" % (pos_string, description, error_type))

def output_errors_json(errors):
    for error_type, error, path, line_number in errors:
        print(json.dumps({"path": path, "lineno": line_number,
                          "rule": error_type, "message": error}))

def output_error_count(error_count):
    if not error_count:
        return

    by_type = " ".join("%s: %d" % item for item in error_count.items())
    count = sum(error_count.values())
    if count == 1:
        print("There was 1 error (%s)" % (by_type,))
    else:
        print("There were %d errors (%s)" % (count, by_type))

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="*",
                        help="List of paths to lint")
    parser.add_argument("--json", action="store_true",
                        help="Output machine-readable JSON format")
    parser.add_argument("--css-mode", action="store_true",
                        help="Run CSS testsuite specific lints")
    return parser.parse_args()

def main(force_css_mode=False):
    args = parse_args()
    paths = args.paths if args.paths else all_filesystem_paths(repo_root)
    return lint(repo_root, paths, args.json, force_css_mode or args.css_mode)

def lint(repo_root, paths, output_json, css_mode):
    error_count = defaultdict(int)
    last = None

    with open(os.path.join(repo_root, "lint.whitelist")) as f:
        whitelist, ignored_files = parse_whitelist(f)

    if output_json:
        output_errors = output_errors_json
    else:
        output_errors = output_errors_text

    def process_errors(errors):
        """
        Filters and prints the errors, and updates the ``error_count`` object.

        :param errors: a list of error tuples (error type, message, path, line number)
        :returns: ``None`` if there were no errors, or
                  a tuple of the error type and the path otherwise
        """

        errors = filter_whitelist_errors(whitelist, errors)

        if not errors:
            return None

        output_errors(errors)
        for error_type, error, path, line in errors:
            error_count[error_type] += 1

        return (errors[-1][0], path)

    for path in paths[:]:
        abs_path = os.path.join(repo_root, path)
        if not os.path.exists(abs_path):
            paths.remove(path)
            continue

        if any(fnmatch.fnmatch(path, file_match) for file_match in ignored_files):
            paths.remove(path)
            continue

        errors = check_path(repo_root, path, css_mode)
        last = process_errors(errors) or last

        if not os.path.isdir(abs_path):
            with open(abs_path, 'rb') as f:
                errors = check_file_contents(repo_root, path, f, css_mode)
                last = process_errors(errors) or last

    if not output_json:
        output_error_count(error_count)
        if error_count:
            print(ERROR_MSG % (last[0], last[1], last[0], last[1]))
    return sum(itervalues(error_count))

path_lints = [check_path_length, check_worker_collision]
file_lints = [check_regexp_line, check_parsed, check_python_ast, check_script_metadata]

if __name__ == "__main__":
    error_count = main()
    if error_count > 0:
        sys.exit(1)
