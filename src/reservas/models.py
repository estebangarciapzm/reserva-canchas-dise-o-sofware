from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional


class EstadoReserva(Enum):
    PENDIENTE = "PENDIENTE"
    CONFIRMADA = "CONFIRMADA"
    CANCELADA = "CANCELADA"


class EstadoPago(Enum):
    PENDIENTE = "PENDIENTE"
    APROBADO = "APROBADO"
    RECHAZADO = "RECHAZADO"
    REEMBOLSADO = "REEMBOLSADO"


@dataclass
class Usuario:
    id: str
    nombre: str
    email: str


@dataclass
class Cancha:
    id: str
    nombre: str
    ubicacion: str
    precio_por_hora: float
    activa: bool = True

    def esta_disponible_para_reservar(self) -> bool:
        return self.activa


@dataclass
class Pago:
    id: str
    reserva_id: str
    monto: float
    estado: EstadoPago = EstadoPago.PENDIENTE
    referencia_externa: Optional[str] = None


@dataclass
class Reserva:
    id: str
    usuario: Usuario
    cancha: Cancha
    inicio: datetime
    fin: datetime
    precio_total: float
    estado: EstadoReserva = EstadoReserva.PENDIENTE
    pago: Optional[Pago] = None

    def confirmar(self, pago: Pago) -> None:
        if pago.estado != EstadoPago.APROBADO:
            raise ValueError("La reserva solo puede confirmarse con un pago aprobado.")

        self.pago = pago
        self.estado = EstadoReserva.CONFIRMADA

    def cancelar(self) -> None:
        if self.estado == EstadoReserva.CANCELADA:
            raise ValueError("La reserva ya se encuentra cancelada.")

        self.estado = EstadoReserva.CANCELADA

    def se_solapa_con(self, cancha_id: str, inicio: datetime, fin: datetime) -> bool:
        misma_cancha = self.cancha.id == cancha_id
        reserva_activa = self.estado == EstadoReserva.CONFIRMADA
        horarios_solapados = self.inicio < fin and inicio < self.fin

        return misma_cancha and reserva_activa and horarios_solapados
