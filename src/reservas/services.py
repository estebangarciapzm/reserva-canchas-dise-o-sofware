from datetime import datetime
from .availability import ServicioDisponibilidad
from .exceptions import HorarioInvalidoError, ReservaNoDisponibleError, ReservaNoEncontradaError
from .models import Cancha, EstadoPago, HorarioReserva, Pago, Reserva, Usuario
from .pricing import CalculadorPrecio


class ServicioReservas:
    def __init__(self, repositorio_reservas, servicio_disponibilidad=None, calculador_precio=None):
        self.repositorio_reservas = repositorio_reservas
        self.servicio_disponibilidad = servicio_disponibilidad or ServicioDisponibilidad(repositorio_reservas)
        self.calculador_precio = calculador_precio or CalculadorPrecio()

    def consultar_disponibilidad(self, cancha: Cancha, inicio: datetime, fin: datetime) -> bool:
        horario = HorarioReserva(inicio, fin)
        return self.servicio_disponibilidad.consultar(cancha, horario)

    def crear_reserva(self, reserva_id: str, usuario: Usuario, cancha: Cancha, inicio: datetime, fin: datetime) -> Reserva:
        horario = HorarioReserva(inicio, fin)
        if not horario.es_valido():
            raise HorarioInvalidoError("La hora de inicio debe ser menor que la hora de fin.")
        if not self.servicio_disponibilidad.consultar(cancha, horario):
            raise ReservaNoDisponibleError("La cancha no está disponible en ese horario.")

        precio_total = self.calculador_precio.calcular(cancha, horario)
        reserva = Reserva(
            id=reserva_id,
            usuario=usuario,
            cancha=cancha,
            horario=horario,
            precio_total=precio_total,
        )
        return self.repositorio_reservas.guardar(reserva)

    def registrar_pago_aprobado(self, reserva_id: str, pago_id: str, referencia_externa: str) -> Reserva:
        reserva = self.repositorio_reservas.obtener_por_id(reserva_id)
        if reserva is None:
            raise ReservaNoEncontradaError("No existe una reserva con ese ID.")
        pago = Pago(
            id=pago_id,
            reserva_id=reserva_id,
            monto=reserva.precio_total,
            estado=EstadoPago.APROBADO,
            referencia_externa=referencia_externa,
        )
        reserva.confirmar(pago)
        return self.repositorio_reservas.guardar(reserva)

    def cancelar_reserva(self, reserva_id: str) -> Reserva:
        reserva = self.repositorio_reservas.obtener_por_id(reserva_id)
        if reserva is None:
            raise ReservaNoEncontradaError("No existe una reserva con ese ID.")
        reserva.cancelar()
        return self.repositorio_reservas.guardar(reserva)
