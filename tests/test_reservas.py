from datetime import datetime

import pytest

from reservas.models import Cancha, EstadoReserva, Usuario
from reservas.repositories import RepositorioReservasMemoria
from reservas.services import ServicioReservas


def crear_servicio():
    repositorio = RepositorioReservasMemoria()
    return ServicioReservas(repositorio)


def crear_usuario():
    return Usuario(
        id="U1",
        nombre="Esteban Garcia",
        email="esteban@email.com",
    )


def crear_cancha():
    return Cancha(
        id="C1",
        nombre="Cancha Samanes 1",
        ubicacion="Parque Samanes",
        precio_por_hora=20.0,
    )


def test_consultar_disponibilidad_en_cancha_libre():
    servicio = crear_servicio()
    cancha = crear_cancha()

    inicio = datetime(2026, 7, 25, 18, 0)
    fin = datetime(2026, 7, 25, 19, 0)

    disponible = servicio.consultar_disponibilidad(cancha, inicio, fin)

    assert disponible is True


def test_crear_reserva_pendiente_con_precio_correcto():
    servicio = crear_servicio()
    usuario = crear_usuario()
    cancha = crear_cancha()

    inicio = datetime(2026, 7, 25, 18, 0)
    fin = datetime(2026, 7, 25, 20, 0)

    reserva = servicio.crear_reserva("R1", usuario, cancha, inicio, fin)

    assert reserva.id == "R1"
    assert reserva.estado == EstadoReserva.PENDIENTE
    assert reserva.precio_total == 40.0


def test_no_permite_reserva_solapada_confirmada():
    servicio = crear_servicio()
    usuario = crear_usuario()
    cancha = crear_cancha()

    inicio = datetime(2026, 7, 25, 18, 0)
    fin = datetime(2026, 7, 25, 19, 0)

    servicio.crear_reserva("R1", usuario, cancha, inicio, fin)
    servicio.registrar_pago_aprobado("R1", "PAGO1", "TX-001")

    with pytest.raises(ValueError):
        servicio.crear_reserva("R2", usuario, cancha, inicio, fin)


def test_confirmar_reserva_con_pago_aprobado():
    servicio = crear_servicio()
    usuario = crear_usuario()
    cancha = crear_cancha()

    inicio = datetime(2026, 7, 25, 18, 0)
    fin = datetime(2026, 7, 25, 19, 0)

    servicio.crear_reserva("R1", usuario, cancha, inicio, fin)
    reserva = servicio.registrar_pago_aprobado("R1", "PAGO1", "TX-001")

    assert reserva.estado == EstadoReserva.CONFIRMADA
    assert reserva.pago is not None
    assert reserva.pago.referencia_externa == "TX-001"


def test_cancelar_reserva():
    servicio = crear_servicio()
    usuario = crear_usuario()
    cancha = crear_cancha()

    inicio = datetime(2026, 7, 25, 18, 0)
    fin = datetime(2026, 7, 25, 19, 0)

    servicio.crear_reserva("R1", usuario, cancha, inicio, fin)
    reserva = servicio.cancelar_reserva("R1")

    assert reserva.estado == EstadoReserva.CANCELADA
