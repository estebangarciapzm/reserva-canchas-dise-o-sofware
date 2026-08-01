from datetime import datetime
from reservas.models import Cancha, Usuario
from reservas.repositories import RepositorioReservasMemoria
from reservas.services import ServicioReservas


repositorio = RepositorioReservasMemoria()
servicio = ServicioReservas(repositorio)

usuario = Usuario(id="U1", nombre="Esteban Garcia", email="esteban@email.com")
cancha = Cancha(id="C1", nombre="Cancha Samanes 1", ubicacion="Parque Samanes", precio_por_hora=20.0)

inicio = datetime(2026, 7, 25, 18, 0)
fin = datetime(2026, 7, 25, 20, 0)

print("Disponibilidad inicial:", servicio.consultar_disponibilidad(cancha, inicio, fin))

reserva = servicio.crear_reserva("R1", usuario, cancha, inicio, fin)
print("Reserva creada:", reserva.id, reserva.estado.value, "Precio:", reserva.precio_total)

reserva = servicio.registrar_pago_aprobado("R1", "PAGO1", "TX-001")
print("Reserva confirmada:", reserva.estado.value)

reserva = servicio.cancelar_reserva("R1")
print("Reserva cancelada:", reserva.estado.value)
