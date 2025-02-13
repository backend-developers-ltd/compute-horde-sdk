# Compute Horde SDK

## `compute_horde_sdk.v1` module

### *class* ComputeHordeClient(hotkey: Keypair, compute_horde_validator_hotkey: str, job_queue: str | None = None, facilitator_url: str = 'https://facilitator.computehorde.io/api/v1/')

Bases: `object`

The class used to communicate with the Compute Horde.

#### *async* create_job(executor_class: ExecutorClass, job_namespace: str, docker_image: str, args: Sequence[str] | None = None, env: Mapping[str, str] | None = None, artifacts_dir: str | None = None, input_volumes: Mapping[str, [HuggingfaceInputVolume](#compute_horde_sdk._internal.models.HuggingfaceInputVolume) | [HTTPInputVolume](#compute_horde_sdk._internal.models.HTTPInputVolume)] | None = None, output_volumes: Mapping[str, [HTTPOutputVolume](#compute_horde_sdk._internal.models.HTTPOutputVolume)] | None = None, run_cross_validation: bool = False, trusted_output_volumes: Mapping[str, [HTTPOutputVolume](#compute_horde_sdk._internal.models.HTTPOutputVolume)] | None = None) → [ComputeHordeJob](#ComputeHordeJob)

Create a new job to run in the Compute Horde.

* **Parameters:**
  * **executor_class** – Class of the executor machine to run the job on.
  * **job_namespace** – Specifies where the job comes from.
    The recommended format is the subnet number and version, like e.g. `"SN123.0"`.
  * **docker_image** – Docker image of the job, in the form of `user/image:tag`.
  * **args** – Positional arguments and flags to run the job with.
  * **env** – Environment variables to run the job with.
  * **artifacts_dir** – Path of the directory that the job will write its results to.
    Contents of files found in this directory will be returned after the job completes
    as a part of the job result. It should be an absolute path (starting with `/`).
  * **input_volumes** – The data to be made available to the job in Docker volumes.
    The keys should be absolute file/directory paths under which you want your data to be available.
    The values should be `InputVolume` instances representing how to obtain the input data.
    For now, input volume paths must start with `/volume/`.
  * **output_volumes** – The data to be read from the Docker volumes after job completion
    and uploaded to the described destinations. Use this for outputs that are too big
    or too unstable to be treated as `artifacts`.
    The keys should be absolute file paths under which job output data will be available.
    The values should be `OutputVolume` instances representing how to handle the output data.
    For now, output volume paths must start with `/output/`.
  * **run_cross_validation** – Whether to run cross validation on a trusted miner.
  * **trusted_output_volumes** – Output volumes for cross validation on a trusted miner.
    If these are omitted then cross validating on a trusted miner will not result in any uploads.
* **Returns:**
  A `ComputeHordeJob` class instance representing the created job.

#### *async* get_job(job_uuid: str) → [ComputeHordeJob](#ComputeHordeJob)

Retrieve information about a job from the Compute Horde.

* **Parameters:**
  **job_uuid** – The UUID of the job to retrieve.
* **Returns:**
  A `ComputeHordeJob` instance representing this job.
* **Raises:**
  [**ComputeHordeNotFoundError**](#compute_horde_sdk._internal.exceptions.ComputeHordeNotFoundError) – If the job with this UUID does not exist.

#### *async* iter_jobs() → AsyncIterator[[ComputeHordeJob](#ComputeHordeJob)]

Retrieve information about your jobs from the Compute Horde.

* **Returns:**
  An async iterator of `ComputeHordeJob` instances representing your jobs.

Usage:

```default
async for job in client.iter_jobs():
    process(job)
```

### *class* ComputeHordeJob(client: [ComputeHordeClient](#ComputeHordeClient), uuid: str, status: [ComputeHordeJobStatus](#compute_horde_sdk._internal.models.ComputeHordeJobStatus), result: [ComputeHordeJobResult](#compute_horde_sdk._internal.models.ComputeHordeJobResult) | None = None)

Bases: `object`

The class representing a job running on the Compute Horde.

#### *async* wait(timeout: float | None = None) → None

Wait for this job to complete or fail.

* **Parameters:**
  **timeout** – Maximum number of seconds to wait for.
* **Raises:**
  [**ComputeHordeJobTimeoutError**](#compute_horde_sdk._internal.exceptions.ComputeHordeJobTimeoutError) – If the job does not complete within `timeout` seconds.
