from typing import Dict, List, Optional
from .models import Reserva


class RepositorioReservasMemoria:
    def __init__(self):
        self._reservas: Dict[str, Reserva] = {}

    def guardar(self, reserva: Reserva) -> Reserva:
        self._reservas[reserva.id] = reserva
        return reserva

    def obtener_por_id(self, reserva_id: str) -> Optional[Reserva]:
        return self._reservas.get(reserva_id)

    def listar(self) -> List[Reserva]:
        return list(self._reservas.values())
