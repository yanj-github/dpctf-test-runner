#!/bin/bash

BRANCHORCOMMITID=4bdeca6b451519a7f60f592468600e0a6cbfc42b

WPTBASEDIR=`pwd`

echo "Removing all test files ..."
rm -rf $WPTBASEDIR/2dcontext
rm -rf $WPTBASEDIR/accelerometer
rm -rf $WPTBASEDIR/accname
rm -rf $WPTBASEDIR/acid
rm -rf $WPTBASEDIR/ambient-light
rm -rf $WPTBASEDIR/animation-worklet
rm -rf $WPTBASEDIR/annotation-model
rm -rf $WPTBASEDIR/annotation-protocol
rm -rf $WPTBASEDIR/annotation-vocab
rm -rf $WPTBASEDIR/apng
rm -rf $WPTBASEDIR/appmanifest
rm -rf $WPTBASEDIR/async-local-storage
rm -rf $WPTBASEDIR/audio-output
rm -rf $WPTBASEDIR/background-fetch
rm -rf $WPTBASEDIR/BackgroundSync
rm -rf $WPTBASEDIR/badging
rm -rf $WPTBASEDIR/battery-status
rm -rf $WPTBASEDIR/beacon
rm -rf $WPTBASEDIR/bluetooth
rm -rf $WPTBASEDIR/clear-site-data
rm -rf $WPTBASEDIR/client-hints
rm -rf $WPTBASEDIR/clipboard-apis
rm -rf $WPTBASEDIR/compat
rm -rf $WPTBASEDIR/compression
rm -rf $WPTBASEDIR/conformance-checkers
rm -rf $WPTBASEDIR/console
rm -rf $WPTBASEDIR/content-dpr
rm -rf $WPTBASEDIR/content-security-policy
rm -rf $WPTBASEDIR/contenteditable
rm -rf $WPTBASEDIR/cookies
rm -rf $WPTBASEDIR/cookie-store
rm -rf $WPTBASEDIR/core-aam
rm -rf $WPTBASEDIR/cors
rm -rf $WPTBASEDIR/credential-management
rm -rf $WPTBASEDIR/css
rm -rf $WPTBASEDIR/custom-elements
rm -rf $WPTBASEDIR/delegated-ink
rm -rf $WPTBASEDIR/device-memory
rm -rf $WPTBASEDIR/document-policy
rm -rf $WPTBASEDIR/dom
rm -rf $WPTBASEDIR/domparsing
rm -rf $WPTBASEDIR/domxpath
rm -rf $WPTBASEDIR/dpctf
rm -rf $WPTBASEDIR/dpub-aam
rm -rf $WPTBASEDIR/dpub-aria
rm -rf $WPTBASEDIR/editing
rm -rf $WPTBASEDIR/element-timing
rm -rf $WPTBASEDIR/encoding
rm -rf $WPTBASEDIR/encoding-detection
rm -rf $WPTBASEDIR/encrypted-media
rm -rf $WPTBASEDIR/entries-api
rm -rf $WPTBASEDIR/eventsource
rm -rf $WPTBASEDIR/event-timing
rm -rf $WPTBASEDIR/feature-policy
rm -rf $WPTBASEDIR/fetch
rm -rf $WPTBASEDIR/FileAPI
rm -rf $WPTBASEDIR/forced-colors-mode
rm -rf $WPTBASEDIR/fullscreen
rm -rf $WPTBASEDIR/gamepad
rm -rf $WPTBASEDIR/generic-sensor
rm -rf $WPTBASEDIR/geolocation-API
rm -rf $WPTBASEDIR/geolocation-sensor
rm -rf $WPTBASEDIR/graphics-aam
rm -rf $WPTBASEDIR/gyroscope
rm -rf $WPTBASEDIR/hit-test
rm -rf $WPTBASEDIR/hr-time
rm -rf $WPTBASEDIR/html
rm -rf $WPTBASEDIR/html-longdesc
rm -rf $WPTBASEDIR/html-media-capture
rm -rf $WPTBASEDIR/idle-detection
rm -rf $WPTBASEDIR/imagebitmap-renderingcontext
rm -rf $WPTBASEDIR/import-maps
rm -rf $WPTBASEDIR/IndexedDB
rm -rf $WPTBASEDIR/inert
rm -rf $WPTBASEDIR/infrastructure
rm -rf $WPTBASEDIR/input-device-capabilities
rm -rf $WPTBASEDIR/input-events
rm -rf $WPTBASEDIR/intersection-observer
rm -rf $WPTBASEDIR/js
rm -rf $WPTBASEDIR/js-self-profiling
rm -rf $WPTBASEDIR/keyboard-lock
rm -rf $WPTBASEDIR/keyboard-map
rm -rf $WPTBASEDIR/largest-contentful-paint
rm -rf $WPTBASEDIR/layout-instability
rm -rf $WPTBASEDIR/lifecycle
rm -rf $WPTBASEDIR/loading
rm -rf $WPTBASEDIR/longtask-timing
rm -rf $WPTBASEDIR/magnetometer
rm -rf $WPTBASEDIR/manifest
rm -rf $WPTBASEDIR/mathml
rm -rf $WPTBASEDIR/media-capabilities
rm -rf $WPTBASEDIR/mediacapture-depth
rm -rf $WPTBASEDIR/mediacapture-fromelement
rm -rf $WPTBASEDIR/mediacapture-image
rm -rf $WPTBASEDIR/mediacapture-record
rm -rf $WPTBASEDIR/mediacapture-streams
rm -rf $WPTBASEDIR/mediasession
rm -rf $WPTBASEDIR/media-source
rm -rf $WPTBASEDIR/mimesniff
rm -rf $WPTBASEDIR/mixed-content
rm -rf $WPTBASEDIR/mst-content-hint
rm -rf $WPTBASEDIR/native-file-system
rm -rf $WPTBASEDIR/native-io
rm -rf $WPTBASEDIR/navigation-timing
rm -rf $WPTBASEDIR/netinfo
rm -rf $WPTBASEDIR/network-error-logging
rm -rf $WPTBASEDIR/notifications
rm -rf $WPTBASEDIR/offscreen-canvas
rm -rf $WPTBASEDIR/old-tests
rm -rf $WPTBASEDIR/orientation-event
rm -rf $WPTBASEDIR/orientation-sensor
rm -rf $WPTBASEDIR/origin-isolation
rm -rf $WPTBASEDIR/origin-policy
rm -rf $WPTBASEDIR/page-lifecycle
rm -rf $WPTBASEDIR/page-visibility
rm -rf $WPTBASEDIR/paint-timing
rm -rf $WPTBASEDIR/payment-handler
rm -rf $WPTBASEDIR/payment-method-basic-card
rm -rf $WPTBASEDIR/payment-method-id
rm -rf $WPTBASEDIR/payment-request
rm -rf $WPTBASEDIR/performance-timeline
rm -rf $WPTBASEDIR/PeriodicBackgroundSync
rm -rf $WPTBASEDIR/periodic-background-sync
rm -rf $WPTBASEDIR/permissions
rm -rf $WPTBASEDIR/permissions-request
rm -rf $WPTBASEDIR/permissions-revoke
rm -rf $WPTBASEDIR/picture-in-picture
rm -rf $WPTBASEDIR/pointerevents
rm -rf $WPTBASEDIR/pointerlock
rm -rf $WPTBASEDIR/portals
rm -rf $WPTBASEDIR/preload
rm -rf $WPTBASEDIR/presentation-api
rm -rf $WPTBASEDIR/printing
rm -rf $WPTBASEDIR/priority-hints
rm -rf $WPTBASEDIR/proximity
rm -rf $WPTBASEDIR/push-api
rm -rf $WPTBASEDIR/quirks
rm -rf $WPTBASEDIR/referrer-policy
rm -rf $WPTBASEDIR/remote-playback
rm -rf $WPTBASEDIR/reporting
rm -rf $WPTBASEDIR/requestidlecallback
rm -rf $WPTBASEDIR/resize-observer
rm -rf $WPTBASEDIR/resource-timing
rm -rf $WPTBASEDIR/screen-capture
rm -rf $WPTBASEDIR/screen_enumeration
rm -rf $WPTBASEDIR/screen-orientation
rm -rf $WPTBASEDIR/screen-wake-lock
rm -rf $WPTBASEDIR/scroll-animations
rm -rf $WPTBASEDIR/scroll-to-text-fragment
rm -rf $WPTBASEDIR/secure-contexts
rm -rf $WPTBASEDIR/selection
rm -rf $WPTBASEDIR/serial
rm -rf $WPTBASEDIR/server-timing
rm -rf $WPTBASEDIR/service-workers
rm -rf $WPTBASEDIR/shadow-dom
rm -rf $WPTBASEDIR/shape-detection
rm -rf $WPTBASEDIR/signed-exchange
rm -rf $WPTBASEDIR/sms
rm -rf $WPTBASEDIR/speech-api
rm -rf $WPTBASEDIR/storage
rm -rf $WPTBASEDIR/streams
rm -rf $WPTBASEDIR/subresource-integrity
rm -rf $WPTBASEDIR/svg
rm -rf $WPTBASEDIR/svg-aam
rm -rf $WPTBASEDIR/timing-entrytypes-registry
rm -rf $WPTBASEDIR/touch-events
rm -rf $WPTBASEDIR/trust-tokens
rm -rf $WPTBASEDIR/trusted-types
rm -rf $WPTBASEDIR/uievents
rm -rf $WPTBASEDIR/upgrade-insecure-requests
rm -rf $WPTBASEDIR/url
rm -rf $WPTBASEDIR/user-timing
rm -rf $WPTBASEDIR/vibration
rm -rf $WPTBASEDIR/video-raf
rm -rf $WPTBASEDIR/video-rvfc
rm -rf $WPTBASEDIR/visual-viewport
rm -rf $WPTBASEDIR/wai-aria
rm -rf $WPTBASEDIR/wake-lock
rm -rf $WPTBASEDIR/wasm
rm -rf $WPTBASEDIR/web-animations
rm -rf $WPTBASEDIR/web-bundle
rm -rf $WPTBASEDIR/webaudio
rm -rf $WPTBASEDIR/webauthn
rm -rf $WPTBASEDIR/WebCryptoAPI
rm -rf $WPTBASEDIR/webdriver
rm -rf $WPTBASEDIR/webgl
rm -rf $WPTBASEDIR/webgpu
rm -rf $WPTBASEDIR/wave-extra
rm -rf $WPTBASEDIR/WebIDL
rm -rf $WPTBASEDIR/web-locks
rm -rf $WPTBASEDIR/webmessaging
rm -rf $WPTBASEDIR/webmidi
rm -rf $WPTBASEDIR/web-nfc
rm -rf $WPTBASEDIR/webrtc
rm -rf $WPTBASEDIR/webrtc-extensions
rm -rf $WPTBASEDIR/webrtc-identity
rm -rf $WPTBASEDIR/webrtc-insertable-streams
rm -rf $WPTBASEDIR/webrtc-priority
rm -rf $WPTBASEDIR/webrtc-quic
rm -rf $WPTBASEDIR/webrtc-stats
rm -rf $WPTBASEDIR/webrtc-svc
rm -rf $WPTBASEDIR/web-share
rm -rf $WPTBASEDIR/websockets
rm -rf $WPTBASEDIR/webstorage
rm -rf $WPTBASEDIR/webtransport
rm -rf $WPTBASEDIR/webusb
rm -rf $WPTBASEDIR/webvr
rm -rf $WPTBASEDIR/webvtt
rm -rf $WPTBASEDIR/webxr
rm -rf $WPTBASEDIR/workers
rm -rf $WPTBASEDIR/worklets
rm -rf $WPTBASEDIR/x-frame-options
rm -rf $WPTBASEDIR/xhr

# delete old MANIFEST.json
rm MANIFEST.json

branch="master"

if [[ -n "$1" ]]; then
	branch="$1";
fi;

echo ""
echo "Importing WAVE SMTS Devices tests ..."
git clone -b $branch --single-branch https://github.com/yanj-github/dpctf-tests dpctf
mv dpctf/generated/* .
mv dpctf/test-config.json .
rm -rf dpctf

# build the MANIFEST.json
# echo ""
# echo "Building MANIFEST.json ..."
# ./wpt manifest -r --no-download

echo ""
echo "Start WAVE server using ./wpt serve-wave"
