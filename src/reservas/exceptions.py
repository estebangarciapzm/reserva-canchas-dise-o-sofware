class ReservaError(ValueError):
    pass


class HorarioInvalidoError(ReservaError):
    pass


class ReservaNoDisponibleError(ReservaError):
    pass


class ReservaNoEncontradaError(ReservaError):
    pass


class PagoNoAprobadoError(ReservaError):
    pass


class ReservaYaCanceladaError(ReservaError):
    pass
