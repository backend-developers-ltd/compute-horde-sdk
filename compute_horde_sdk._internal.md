# compute_horde_sdk._internal package

## Submodules

## compute_horde_sdk._internal.exceptions module

### *exception* compute_horde_sdk._internal.exceptions.ComputeHordeError

Bases: `Exception`

Something went wrong on the Compute Horde side.

### *exception* compute_horde_sdk._internal.exceptions.ComputeHordeJobTimeoutError

Bases: [`ComputeHordeError`](#compute_horde_sdk._internal.exceptions.ComputeHordeError), `TimeoutError`

Compute Horde job timed out.

### *exception* compute_horde_sdk._internal.exceptions.ComputeHordeNotFoundError

Bases: [`ComputeHordeError`](#compute_horde_sdk._internal.exceptions.ComputeHordeError)

The requested resource was not found in Compute Horde.

## compute_horde_sdk._internal.models module

### *class* compute_horde_sdk._internal.models.AbstractInputVolume

Bases: `ABC`

#### get_volume_relative_path(mount_path: str) → str

#### *abstract* to_compute_horde_volume(mount_path: str) → Annotated[InlineVolume | ZipUrlVolume | SingleFileVolume | MultiVolume | HuggingfaceVolume, FieldInfo(annotation=NoneType, required=True, discriminator='volume_type')]

### *class* compute_horde_sdk._internal.models.ComputeHordeJobResult(stdout: str)

Bases: `object`

#### stdout *: str*

### *class* compute_horde_sdk._internal.models.ComputeHordeJobStatus(value, names=None, \*, module=None, qualname=None, type=None, start=1, boundary=None)

Bases: `StrEnum`

#### ACCEPTED *= 'Accepted'*

#### COMPLETED *= 'Completed'*

#### FAILED *= 'Failed'*

#### REJECTED *= 'Rejected'*

#### SENT *= 'Sent'*

#### is_in_progress() → bool

### *class* compute_horde_sdk._internal.models.FacilitatorJobResponse(\*, uuid: str, executor_class: str, created_at: str, status: [ComputeHordeJobStatus](#compute_horde_sdk._internal.models.ComputeHordeJobStatus), docker_image: str, args: str, env: dict, stdout: str, volumes: list = [], uploads: list = [])

Bases: `BaseModel`

#### args *: str*

#### created_at *: str*

#### docker_image *: str*

#### env *: dict*

#### executor_class *: str*

#### model_config *: ClassVar[ConfigDict]* *= {}*

Configuration for the model, should be a dictionary conforming to [ConfigDict][pydantic.config.ConfigDict].

#### status *: [ComputeHordeJobStatus](#compute_horde_sdk._internal.models.ComputeHordeJobStatus)*

#### stdout *: str*

#### uploads *: list*

#### uuid *: str*

#### volumes *: list*

### *class* compute_horde_sdk._internal.models.FacilitatorJobsResponse(\*, count: int, next: str | None = None, previous: str | None = None, results: list[[FacilitatorJobResponse](#compute_horde_sdk._internal.models.FacilitatorJobResponse)])

Bases: `BaseModel`

#### count *: int*

#### model_config *: ClassVar[ConfigDict]* *= {}*

Configuration for the model, should be a dictionary conforming to [ConfigDict][pydantic.config.ConfigDict].

#### next *: str | None*

#### previous *: str | None*

#### results *: list[[FacilitatorJobResponse](#compute_horde_sdk._internal.models.FacilitatorJobResponse)]*

### *class* compute_horde_sdk._internal.models.HTTPInputVolume(\*, url: str)

Bases: `BaseModel`, [`AbstractInputVolume`](#compute_horde_sdk._internal.models.AbstractInputVolume)

Volume for downloading files from the Internet via HTTP.

#### model_config *: ClassVar[ConfigDict]* *= {}*

Configuration for the model, should be a dictionary conforming to [ConfigDict][pydantic.config.ConfigDict].

#### to_compute_horde_volume(mount_path: str) → SingleFileVolume

#### url *: str*

The URL to download the file from.

### *class* compute_horde_sdk._internal.models.HTTPOutputVolume(\*, http_method: Literal['POST', 'PUT'], url: str, form_fields: Mapping[str, str] | None = None, signed_headers: Mapping[str, str] | None = None)

Bases: `BaseModel`

#### form_fields *: Mapping[str, str] | None*

#### get_volume_relative_path(mount_path: str) → str

#### http_method *: Literal['POST', 'PUT']*

HTTP method to use, can be POST or PUT.

#### model_config *: ClassVar[ConfigDict]* *= {}*

Configuration for the model, should be a dictionary conforming to [ConfigDict][pydantic.config.ConfigDict].

#### signed_headers *: Mapping[str, str] | None*

#### to_compute_horde_output_upload(mount_path: str) → Annotated[SingleFilePostUpload | SingleFilePutUpload | ZipAndHttpPostUpload | ZipAndHttpPutUpload | MultiUpload, FieldInfo(annotation=NoneType, required=True, discriminator='output_upload_type')]

#### url *: str*

The URL to upload the file to.

### *class* compute_horde_sdk._internal.models.HuggingfaceInputVolume(\*, repo_id: str, repo_type: str | None = None, revision: str | None = None, allow_patterns: str | list[str] | None = None)

Bases: `BaseModel`, [`AbstractInputVolume`](#compute_horde_sdk._internal.models.AbstractInputVolume)

Volume for downloading resources from Huggingface.

By default, it downloads the entire repository and copier its structure.
To narrow it down, use the `allow_patterns` field.
If a file is inside a subfolder, it will be placed under the same path in the volume.

#### allow_patterns *: str | list[str] | None*

If provided, only files matching at least one pattern are downloaded.

#### model_config *: ClassVar[ConfigDict]* *= {}*

Configuration for the model, should be a dictionary conforming to [ConfigDict][pydantic.config.ConfigDict].

#### repo_id *: str*

Huggingface repository ID, in the format “namespace/name”.

#### repo_type *: str | None*

Set to “dataset” or “space” for a dataset or space, None or “model” for a model.

#### revision *: str | None*

Git revision ID: branch name / tag / commit hash.

#### to_compute_horde_volume(mount_path: str) → HuggingfaceVolume

### compute_horde_sdk._internal.models.OutputVolume

alias of [`HTTPOutputVolume`](#compute_horde_sdk._internal.models.HTTPOutputVolume)

## compute_horde_sdk._internal.sdk module

### *class* compute_horde_sdk._internal.sdk.ComputeHordeClient(hotkey: Keypair, compute_horde_validator_hotkey: str, job_queue: str | None = None, facilitator_url: str = 'https://facilitator.computehorde.io/api/v1/')

Bases: `object`

The class used to communicate with the Compute Horde.

#### *async* create_job(executor_class: ExecutorClass, job_namespace: str, docker_image: str, args: Sequence[str] | None = None, env: Mapping[str, str] | None = None, artifacts_dir: str | None = None, input_volumes: Mapping[str, [HuggingfaceInputVolume](#compute_horde_sdk._internal.models.HuggingfaceInputVolume) | [HTTPInputVolume](#compute_horde_sdk._internal.models.HTTPInputVolume)] | None = None, output_volumes: Mapping[str, [HTTPOutputVolume](#compute_horde_sdk._internal.models.HTTPOutputVolume)] | None = None, run_cross_validation: bool = False, deposition_comparison_method: str | None = None, trusted_output_volumes: Mapping[str, [HTTPOutputVolume](#compute_horde_sdk._internal.models.HTTPOutputVolume)] | None = None) → [ComputeHordeJob](#compute_horde_sdk._internal.sdk.ComputeHordeJob)

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
  * **deposition_comparison_method** – The method to use to compare the original job result
    with the one obtained from the trusted miner.
  * **trusted_output_volumes** – Output volumes for cross validation on a trusted miner.
    If these are omitted then cross validating on a trusted miner will not result in any uploads.
* **Returns:**
  A `ComputeHordeJob` class instance representing the created job.

#### *async* get_job(job_uuid: str) → [ComputeHordeJob](#compute_horde_sdk._internal.sdk.ComputeHordeJob)

Retrieve information about a job from the Compute Horde.

* **Parameters:**
  **job_uuid** – The UUID of the job to retrieve.
* **Returns:**
  A `ComputeHordeJob` instance representing this job.
* **Raises:**
  [**ComputeHordeNotFoundError**](#compute_horde_sdk._internal.exceptions.ComputeHordeNotFoundError) – If the job with this UUID does not exist.

#### *async* get_jobs(page: int = 1, page_size: int = 10) → list[[ComputeHordeJob](#compute_horde_sdk._internal.sdk.ComputeHordeJob)]

Retrieve information about your jobs from the Compute Horde.

* **Parameters:**
  * **page** – The page number.
  * **page_size** – The page size.
* **Returns:**
  A list of `ComputeHordeJob` instances representing your jobs.
* **Raises:**
  [**ComputeHordeNotFoundError**](#compute_horde_sdk._internal.exceptions.ComputeHordeNotFoundError) – If the requested page does not exist.

#### *async* iter_jobs() → AsyncIterator[[ComputeHordeJob](#compute_horde_sdk._internal.sdk.ComputeHordeJob)]

Retrieve information about your jobs from the Compute Horde.

* **Returns:**
  An async iterator of `ComputeHordeJob` instances representing your jobs.

Usage:

```default
async for job in client.iter_jobs():
    process(job)
```

### *class* compute_horde_sdk._internal.sdk.ComputeHordeJob(client: [ComputeHordeClient](#compute_horde_sdk._internal.sdk.ComputeHordeClient), uuid: str, status: [ComputeHordeJobStatus](#compute_horde_sdk._internal.models.ComputeHordeJobStatus), result: [ComputeHordeJobResult](#compute_horde_sdk._internal.models.ComputeHordeJobResult) | None = None)

Bases: `object`

The class representing a job running on the Compute Horde.

#### *async* refresh_from_facilitator() → None

#### *async* wait(timeout: float | None = None) → None

Wait for this job to complete or fail.

* **Parameters:**
  **timeout** – Maximum number of seconds to wait for.
* **Raises:**
  [**ComputeHordeJobTimeoutError**](#compute_horde_sdk._internal.exceptions.ComputeHordeJobTimeoutError) – If the job does not complete within `timeout` seconds.

## Module contents

Internal implementation of compute_horde_sdk.

This project uses ApiVer, and as such, all imports should be done from v\* submodules.
