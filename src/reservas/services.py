from datetime import datetime
from .availability import ServicioDisponibilidad
from .commands import CrearReservaCommand, RegistrarPagoCommand
from .exceptions import HorarioInvalidoError, ReservaNoDisponibleError, ReservaNoEncontradaError
from .models import Cancha, HorarioReserva, Pago, Reserva, Usuario
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
        comando = CrearReservaCommand(
            reserva_id=reserva_id,
            usuario=usuario,
            cancha=cancha,
            inicio=inicio,
            fin=fin,
        )
        return self.crear_reserva_desde_comando(comando)

    def crear_reserva_desde_comando(self, comando: CrearReservaCommand) -> Reserva:
        horario = comando.horario()
        if not horario.es_valido():
            raise HorarioInvalidoError("La hora de inicio debe ser menor que la hora de fin.")
        if not self.servicio_disponibilidad.consultar(comando.cancha, horario):
            raise ReservaNoDisponibleError("La cancha no está disponible en ese horario.")

        precio_total = self.calculador_precio.calcular(comando.cancha, horario)
        reserva = Reserva(
            id=comando.reserva_id,
            usuario=comando.usuario,
            cancha=comando.cancha,
            horario=horario,
            precio_total=precio_total,
        )
        return self.repositorio_reservas.guardar(reserva)

    def registrar_pago_aprobado(self, reserva_id: str, pago_id: str, referencia_externa: str) -> Reserva:
        comando = RegistrarPagoCommand(
            reserva_id=reserva_id,
            pago_id=pago_id,
            referencia_externa=referencia_externa,
        )
        return self.registrar_pago_desde_comando(comando)

    def registrar_pago_desde_comando(self, comando: RegistrarPagoCommand) -> Reserva:
        reserva = self.repositorio_reservas.obtener_por_id(comando.reserva_id)
        if reserva is None:
            raise ReservaNoEncontradaError("No existe una reserva con ese ID.")

        pago = Pago.aprobado(
            pago_id=comando.pago_id,
            reserva_id=comando.reserva_id,
            monto=reserva.precio_total,
            referencia_externa=comando.referencia_externa,
        )
        reserva.confirmar(pago)
        return self.repositorio_reservas.guardar(reserva)

    def cancelar_reserva(self, reserva_id: str) -> Reserva:
        reserva = self.repositorio_reservas.obtener_por_id(reserva_id)
        if reserva is None:
            raise ReservaNoEncontradaError("No existe una reserva con ese ID.")
        reserva.cancelar()
        return self.repositorio_reservas.guardar(reserva)
