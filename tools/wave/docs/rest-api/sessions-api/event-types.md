# Session Event Types - [Sessions API](../README.md#sessions-api)

Session events are events that are triggered by actions related to sessions. 
The [`event`](./events.md) functions of the sessions API make use of these events.

## Status change

**Type identifier**: `status`  

**Payload**: `"<String>"`  
Possible Values: `paused`, `running`, `completed`, `aborted`  

**Description**: Triggered once the status of the session changes.

## Resume 

**Type identifier**: `resume`  

**Payload**: `"<String>"`  
Contains the token of the session to resume.

**Description**: Triggered when a specific session is supposed to be resumed. 
This will discard the current session and continue executing the session with 
the provided token.

## Test Completed 

**Type identifier**: `test_completed`  

**Payload**: `"<String>"`  
Contains the test case that completed.

**Description**: Triggered when the test runner received a result for a test.

## Test Ready

**Type identifier**: `test_ready`  

**Payload**:

An object, that contains information of the test case that finished loading.

```json
{
  "test_path": "<String>",
  "test_name": "<String>",
  "test_description": "<String"
}
```

- **test_path**: The path of the test, relative to the DPCTF Test Runner root
- **test_name**: The name of the test
- **test_description**: A description of the test

**Description**: Triggered by a test that is done loading and waits for the 
observation framework to be ready.

## Observation Ready

**Type identifier**: `observation_ready`  

**Payload**:

An object, that contains the path of the test that the observation framework 
is ready to observe.

```json
{
  "test_path": "<String>"
}
```

- **test_path**: The path of the test, relative to the DPCTF Test Runner root

**Description**: Triggered by an external framework that is ready to perform 
observations for a specific test.

## Observation Completed

**Type identifier**: `observation_completed`  

**Payload**:

The payload contains all results of the observation.

```json
[
  {
    "name": "String",
    "status": "Enum['PASS', 'FAIL', 'TIMEOUT', 'NOT_RUN']",
    "message": "String"
  },
  ...
]
```
- **name**: The name of the test.
- **status**: The status of the result:
  - **PASS**: The test was executed successfully.
  - **FAIL**: The test did not meet at least one assertion.
  - **TIMEOUT**: It took too long for this test to execute.
  - **NOT_RUN**: This test was skipped.
- **message** contains the reason for the tests failure. `null` if the test passed

**Description**: Triggered by an external framework that completed processing 
a requested observation.
