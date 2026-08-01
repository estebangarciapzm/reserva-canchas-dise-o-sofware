# Documento de Diseño UML
## Sistema de Reservas de Canchas Deportivas

## 1. Descripción general

El sistema permite gestionar reservas de canchas deportivas. La versión mínima funcional incluye tres casos de uso principales: consultar disponibilidad, crear reserva y cancelar reserva. También se registra un pago aprobado para confirmar la reserva.

El diseño UML se relaciona directamente con el código implementado en `models.py`, `services.py` y `repositories.py`.

---

## 2. Enfoque 4+1

### Vista lógica

La vista lógica representa las clases principales del sistema: `Usuario`, `Cancha`, `Reserva`, `Pago`, `EstadoReserva`, `EstadoPago`, `ServicioReservas` y `RepositorioReservasMemoria`.

### Vista de desarrollo

El proyecto está organizado en:

- `src/reservas/models.py`: modelos principales del dominio.
- `src/reservas/services.py`: lógica de aplicación y casos de uso.
- `src/reservas/repositories.py`: almacenamiento en memoria.
- `tests/test_reservas.py`: pruebas unitarias.
- `docs/`: documentación del diseño, diagnóstico e informe final.

### Vista de procesos

El flujo principal inicia cuando el usuario consulta disponibilidad. Luego puede crear una reserva pendiente, registrar un pago aprobado y confirmar la reserva. También puede cancelar una reserva existente.

### Vista física

La versión actual se ejecuta en GitHub Codespaces usando Python. El sistema no usa base de datos real; el almacenamiento se simula mediante un repositorio en memoria.

### Vista de escenarios

Los escenarios principales son:

1. Consultar disponibilidad.
2. Crear reserva.
3. Cancelar reserva.

---

## 3. Diagramas UML

- Diagrama de casos de uso: `diagrama_casos_uso_reservas.png`
- Diagrama de clases inicial: `diagrama_clases_reservas.png`
- Secuencia crear reserva: `diagrama_secuencia_crear_reserva.png`
- Secuencia cancelar reserva: `diagrama_secuencia_cancelar_reserva.png`

---

## 4. Patrón aplicado

El patrón aplicado es Repository Pattern, representado por la clase `RepositorioReservasMemoria`.

Este patrón permite separar la lógica de negocio de la forma en que se almacenan los datos. Actualmente las reservas se guardan en memoria, pero en el futuro se podría reemplazar este repositorio por una base de datos sin cambiar directamente la lógica principal de `ServicioReservas`.

---

## 5. Trazabilidad diseño-código

| Elemento UML | Archivo |
|---|---|
| Usuario | `src/reservas/models.py` |
| Cancha | `src/reservas/models.py` |
| Reserva | `src/reservas/models.py` |
| Pago | `src/reservas/models.py` |
| ServicioReservas | `src/reservas/services.py` |
| RepositorioReservasMemoria | `src/reservas/repositories.py` |
| Pruebas unitarias | `tests/test_reservas.py` |

---

## 6. Conclusión

El diseño inicial permite representar de forma clara los casos de uso principales del sistema. La separación entre modelos, servicios y repositorios facilita la prueba del código y deja una base preparada para la fase de refactorización.
