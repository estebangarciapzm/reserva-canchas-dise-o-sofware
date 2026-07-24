# Documento de Diseño UML  
## Sistema de Reservas de Canchas Deportivas

## 1. Descripción general del sistema

El sistema permite gestionar reservas de canchas deportivas de forma simple. La versión funcional mínima incluye tres casos de uso principales: consultar disponibilidad, crear reserva y cancelar reserva. También se incluye el registro de pago aprobado como parte del flujo de confirmación de la reserva.

En esta parte entendí que el diseño UML no debe estar separado del código. Las clases del diagrama deben coincidir con lo que existe en `models.py`, `services.py` y `repositories.py`, porque así el diseño puede defenderse mejor durante una sustentación.

---

## 2. Enfoque 4+1

### Vista lógica

La vista lógica describe las clases principales del dominio. En este sistema aparecen entidades como `Usuario`, `Cancha`, `Reserva` y `Pago`. También se usan enumeraciones como `EstadoReserva` y `EstadoPago`.

### Vista de desarrollo

El código está organizado en tres módulos:

- `models.py`: clases del dominio.
- `services.py`: casos de uso y reglas de aplicación.
- `repositories.py`: almacenamiento en memoria.
- `tests/`: pruebas unitarias con pytest.

### Vista de procesos

El flujo principal ocurre cuando el usuario consulta disponibilidad, crea una reserva pendiente, registra un pago aprobado y luego la reserva queda confirmada.

### Vista física

La versión actual se ejecuta en GitHub Codespaces como una aplicación Python local. No usa base de datos real; el repositorio en memoria simula el almacenamiento para mantener el alcance controlado.

### Vista de escenarios

Los escenarios principales son:

1. Consultar disponibilidad de cancha.
2. Crear reserva.
3. Cancelar reserva.

---

## 3. Diagrama de casos de uso

```plantuml
@startuml
left to right direction

actor Usuario
actor Administrador

rectangle "Sistema de Reservas de Canchas" {
  usecase "Consultar disponibilidad" as UC1
  usecase "Crear reserva" as UC2
  usecase "Registrar pago aprobado" as UC3
  usecase "Cancelar reserva" as UC4
  usecase "Validar horario disponible" as UC5
  usecase "Calcular precio total" as UC6
  usecase "Notificar cancelación" as UC7
}

Usuario --> UC1
Usuario --> UC2
Usuario --> UC4

Administrador --> UC1

UC2 ..> UC1 : <<include>>
UC2 ..> UC5 : <<include>>
UC2 ..> UC6 : <<include>>
UC2 ..> UC3 : <<extend>>

UC4 ..> UC7 : <<extend>>

@enduml
cat > docs/diseno_uml.md <<'MD'
# Documento de Diseño UML
## Sistema de Reservas de Canchas Deportivas

## 1. Descripción general

El sistema permite gestionar reservas de canchas deportivas. La versión mínima funcional incluye tres casos de uso principales: consultar disponibilidad, crear reserva y cancelar reserva. También se registra un pago aprobado para confirmar la reserva.

En esta parte entendí que el diseño UML debe coincidir con el código. Por eso las clases del documento se relacionan con los archivos models.py, services.py y repositories.py.

## 2. Enfoque 4+1

### Vista lógica
Clases principales del dominio: Usuario, Cancha, Reserva, Pago, EstadoReserva y EstadoPago.

### Vista de desarrollo
El código se organiza en models.py, services.py, repositories.py y tests.

### Vista de procesos
El flujo principal es: consultar disponibilidad, crear reserva pendiente, registrar pago aprobado y confirmar reserva.

### Vista física
La versión actual se ejecuta en GitHub Codespaces. Usa Python y almacenamiento en memoria.

### Vista de escenarios
Los escenarios principales son consultar disponibilidad, crear reserva y cancelar reserva.

## 3. Casos de uso

Actores:
- Usuario
- Administrador

Casos principales:
- Consultar disponibilidad
- Crear reserva
- Registrar pago aprobado
- Cancelar reserva

Relaciones:
- Crear reserva incluye consultar disponibilidad.
- Crear reserva incluye calcular precio total.
- Crear reserva extiende registrar pago aprobado.
- Cancelar reserva puede extender notificar cancelación.

## 4. Clases del sistema

Clases:
- Usuario
- Cancha
- Reserva
- Pago
- EstadoReserva
- EstadoPago
- ServicioReservas
- RepositorioReservasMemoria

Relaciones:
- Un Usuario puede tener muchas Reservas.
- Una Cancha puede tener muchas Reservas.
- Una Reserva pertenece a una Cancha.
- Una Reserva pertenece a un Usuario.
- Una Reserva puede tener cero o un Pago.
- ServicioReservas usa RepositorioReservasMemoria.

## 5. Secuencias críticas

### Crear reserva
1. Usuario solicita crear reserva.
2. ServicioReservas valida disponibilidad.
3. ServicioReservas calcula precio.
4. ServicioReservas crea reserva pendiente.
5. RepositorioReservasMemoria guarda la reserva.

### Cancelar reserva
1. Usuario solicita cancelar reserva.
2. ServicioReservas busca la reserva.
3. Reserva cambia su estado a CANCELADA.
4. RepositorioReservasMemoria guarda la reserva actualizada.

## 6. Patrón aplicado

Se aplica el patrón Repository mediante RepositorioReservasMemoria. Este patrón separa la lógica de negocio del almacenamiento de datos.

En esta parte entendí que el repositorio permite que el servicio de reservas no dependa de cómo se guardan los datos. Hoy usamos memoria, pero después podría cambiarse por una base de datos.

## 7. Trazabilidad diseño-código

| Elemento | Archivo |
|---|---|
| Usuario | src/reservas/models.py |
| Cancha | src/reservas/models.py |
| Reserva | src/reservas/models.py |
| Pago | src/reservas/models.py |
| ServicioReservas | src/reservas/services.py |
| RepositorioReservasMemoria | src/reservas/repositories.py |
| Pruebas | tests/test_reservas.py |
