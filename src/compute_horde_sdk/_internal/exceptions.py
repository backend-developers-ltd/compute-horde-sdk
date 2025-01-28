class ComputeHordeError(Exception):
    """Something went wrong on the Compute Horde side."""


class ComputeHordeJobTimeoutError(ComputeHordeError, TimeoutError):
    """Compute Horde job timed out."""
