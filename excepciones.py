# Define los errores específicos del sistema Software FJ.


# Todas las excepciones del proyecto heredarán de esta clase.
class ErrorSoftwareFJ(Exception):
    """Representa un error controlado del sistema Software FJ."""
    pass


# Identifica datos personales o parámetros que no son válidos.
class DatosInvalidosError(ErrorSoftwareFJ):
    """Indica que un dato no cumple las reglas del sistema."""
    pass


# Identifica servicios que no se pueden reservar.
class ServicioNoDisponibleError(ErrorSoftwareFJ):
    """Indica que el servicio solicitado no está disponible."""
    pass


# Identifica problemas con la creación o procesamiento de reservas.
class ReservaInvalidaError(ErrorSoftwareFJ):
    """Indica que una reserva contiene datos o condiciones inválidas."""
    pass


# Identifica acciones que no están permitidas según el estado actual.
class OperacionNoPermitidaError(ErrorSoftwareFJ):
    """Indica que la operación solicitada no está permitida."""
    pass