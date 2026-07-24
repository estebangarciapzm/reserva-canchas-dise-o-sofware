from datetime import datetime
from .models import Cancha, EstadoPago, Pago, Reserva, Usuario


class ServicioReservas:
    def __init__(self, repositorio_reservas):
        self.repositorio_reservas = repositorio_reservas

    def consultar_disponibilidad(self, cancha: Cancha, inicio: datetime, fin: datetime) -> bool:
        if not cancha.esta_disponible_para_reservar():
            return False

        for reserva in self.repositorio_reservas.listar():
            if reserva.se_solapa_con(cancha.id, inicio, fin):
                return False

        return True

    def crear_reserva(self, reserva_id: str, usuario: Usuario, cancha: Cancha, inicio: datetime, fin: datetime) -> Reserva:
        if inicio >= fin:
            raise ValueError("La hora de inicio debe ser menor que la hora de fin.")

        if not self.consultar_disponibilidad(cancha, inicio, fin):
            raise ValueError("La cancha no está disponible en ese horario.")

        horas = (fin - inicio).total_seconds() / 3600
        precio_total = horas * cancha.precio_por_hora

        reserva = Reserva(
            id=reserva_id,
            usuario=usuario,
            cancha=cancha,
            inicio=inicio,
            fin=fin,
            precio_total=precio_total,
        )

        return self.repositorio_reservas.guardar(reserva)

    def registrar_pago_aprobado(self, reserva_id: str, pago_id: str, referencia_externa: str) -> Reserva:
        reserva = self.repositorio_reservas.obtener_por_id(reserva_id)

        if reserva is None:
            raise ValueError("No existe una reserva con ese ID.")

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
            raise ValueError("No existe una reserva con ese ID.")

        reserva.cancelar()
        return self.repositorio_reservas.guardar(reserva)
