# Sistema de Reservas de Canchas Deportivas

Proyecto integrador de la asignatura Diseño de Software.

## Descripción

Este proyecto implementa una versión funcional mínima de un sistema de reservas de canchas deportivas.  
El sistema permite:

1. Consultar disponibilidad de una cancha.
2. Crear una reserva.
3. Registrar un pago aprobado para confirmar la reserva.
4. Cancelar una reserva.

El objetivo principal no es construir una aplicación grande, sino demostrar diseño orientado a objetos, pruebas unitarias, uso de Git y una base preparada para refactorización.

## Dominio elegido

D1. Sistema de reservas de canchas deportivas.

## Tecnologías utilizadas

- Python 3
- pytest
- GitHub
- GitHub Codespaces

## Estructura del proyecto

```text
src/
  reservas/
    models.py
    repositories.py
    services.py

tests/
  test_reservas.py

docs/
  notas_diseno.md

pip install -r requirements.txt
