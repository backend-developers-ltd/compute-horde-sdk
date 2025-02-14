API Reference
=============

.. tip::
   :ref:`Pinning versions <semantic_versioning>` properly ensures the stability of your application.

SDK
---

.. autoclass:: compute_horde_sdk.v1.ComputeHordeClient()
    :inherited-members:
    :special-members: __init__

.. autoclass:: compute_horde_sdk.v1.ComputeHordeJob()
    :inherited-members:

.. autoclass:: compute_horde_sdk.v1.ComputeHordeJobStatus()
    :members:

Volumes
-------

.. autoclass:: compute_horde_sdk.v1.HTTPInputVolume()

Exceptions
---------

.. autoexception:: compute_horde_sdk.v1.ComputeHordeError()

.. autoexception:: compute_horde_sdk.v1.ComputeHordeNotFoundError()

.. autoexception:: compute_horde_sdk.v1.ComputeHordeJobTimeoutError()
