from dataclasses import dataclass
from datetime import datetime
from .models import Cancha, HorarioReserva, Usuario


@dataclass(frozen=True)
class CrearReservaCommand:
    reserva_id: str
    usuario: Usuario
    cancha: Cancha
    inicio: datetime
    fin: datetime

    def horario(self) -> HorarioReserva:
        return HorarioReserva(self.inicio, self.fin)


@dataclass(frozen=True)
class RegistrarPagoCommand:
    reserva_id: str
    pago_id: str
    referencia_externa: str
