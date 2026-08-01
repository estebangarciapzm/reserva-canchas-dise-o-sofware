from .models import Cancha, HorarioReserva


class CalculadorPrecio:
    def calcular(self, cancha: Cancha, horario: HorarioReserva) -> float:
        return horario.duracion_horas() * cancha.precio_por_hora
