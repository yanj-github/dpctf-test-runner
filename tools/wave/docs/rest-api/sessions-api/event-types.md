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

DPCTF only

**Type identifier**: `test_ready`  

**Payload**:

An object, that contains information of the test case that finished loading.

```json
{
  "path": "<String>",
  "title": "<String>",
  "description": "<String>",
  "params": "<Object>",
  "observations": [
    {
      "id": "<String>",
      "name": "<String>",
      "description": "<String>",
    },
    ...
  ]
}
```

- **path**: The path of the test, relative to the DPCTF Test Runner root
- **title**: The name of the test
- **description**: A description of the test
- **params**: A key-value object containing all query parameters and its values
- **observations**: A list of observation that are required for this test
  - **id**: A unique identifier for the observation
  - **name**: The name of the observation
  - **description**: Details on how to perform the observation

**Description**: Triggered by a test that is done loading and waits for the 
observation framework to be ready.

## Observation Ready

DPCTF only

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

DPCTF only

**Type identifier**: `observation_completed`  

**Payload**:

The payload contains all results of the observation.

```json
[
  {
    "id": "<String>",
    "name": "<String>",
    "status": "Enum['PASS', 'FAIL', 'TIMEOUT', 'NOT_RUN']",
    "message": "<String>"
  },
  ...
]
```
- **id**: The id of the observation
- **name**: The name of the test.
- **status**: The status of the result:
  - **PASS**: The test was executed successfully.
  - **FAIL**: The test did not meet at least one assertion.
  - **TIMEOUT**: It took too long for this test to execute.
  - **NOT_RUN**: This test was skipped.
- **message** contains the reason for the tests failure. `null` if the test passed

**Description**: Triggered by an external framework that completed processing 
a requested observation.

## Playback event

DPCTF only

**Type identifier**: `playback`

**Payload**:

The payload contains the type of event that was triggered by the video. See 
[MediaElement Events](https://developer.mozilla.org/en-US/docs/Web/API/HTMLMediaElement#Events).
The payload is any data related to that event.

```json
{
  "type": "<String>",
  "data": "<Object|String|Number>",
}
```

**Description**: The playback events are video element events that are 
forwared to the session event channel.
