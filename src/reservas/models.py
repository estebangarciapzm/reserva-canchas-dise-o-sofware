from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional
from .exceptions import PagoNoAprobadoError, ReservaYaCanceladaError


class EstadoReserva(Enum):
    PENDIENTE = "PENDIENTE"
    CONFIRMADA = "CONFIRMADA"
    CANCELADA = "CANCELADA"


class EstadoPago(Enum):
    PENDIENTE = "PENDIENTE"
    APROBADO = "APROBADO"
    RECHAZADO = "RECHAZADO"
    REEMBOLSADO = "REEMBOLSADO"


@dataclass(frozen=True)
class HorarioReserva:
    inicio: datetime
    fin: datetime

    def es_valido(self) -> bool:
        return self.inicio < self.fin

    def duracion_horas(self) -> float:
        return (self.fin - self.inicio).total_seconds() / 3600

    def se_solapa_con(self, otro: "HorarioReserva") -> bool:
        return self.inicio < otro.fin and otro.inicio < self.fin


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

    @classmethod
    def aprobado(cls, pago_id: str, reserva_id: str, monto: float, referencia_externa: str) -> "Pago":
        return cls(
            id=pago_id,
            reserva_id=reserva_id,
            monto=monto,
            estado=EstadoPago.APROBADO,
            referencia_externa=referencia_externa,
        )


@dataclass
class Reserva:
    id: str
    usuario: Usuario
    cancha: Cancha
    horario: HorarioReserva
    precio_total: float
    estado: EstadoReserva = EstadoReserva.PENDIENTE
    pago: Optional[Pago] = None

    @property
    def inicio(self) -> datetime:
        return self.horario.inicio

    @property
    def fin(self) -> datetime:
        return self.horario.fin

    def confirmar(self, pago: Pago) -> None:
        if pago.estado != EstadoPago.APROBADO:
            raise PagoNoAprobadoError("La reserva solo puede confirmarse con un pago aprobado.")
        self.pago = pago
        self.estado = EstadoReserva.CONFIRMADA

    def cancelar(self) -> None:
        if self.estado == EstadoReserva.CANCELADA:
            raise ReservaYaCanceladaError("La reserva ya se encuentra cancelada.")
        self.estado = EstadoReserva.CANCELADA

    def se_solapa_con(self, cancha_id: str, inicio: datetime, fin: datetime) -> bool:
        misma_cancha = self.cancha.id == cancha_id
        reserva_activa = self.estado == EstadoReserva.CONFIRMADA
        horario_consultado = HorarioReserva(inicio, fin)
        horarios_solapados = self.horario.se_solapa_con(horario_consultado)
        return misma_cancha and reserva_activa and horarios_solapados
