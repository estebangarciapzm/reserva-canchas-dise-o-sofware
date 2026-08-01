from .models import Cancha, HorarioReserva


class ServicioDisponibilidad:
    def __init__(self, repositorio_reservas):
        self.repositorio_reservas = repositorio_reservas

    def consultar(self, cancha: Cancha, horario: HorarioReserva) -> bool:
        if not cancha.esta_disponible_para_reservar():
            return False

        for reserva in self.repositorio_reservas.listar():
            if reserva.se_solapa_con(cancha.id, horario.inicio, horario.fin):
                return False

        return True
