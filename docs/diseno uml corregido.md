# Documento de Diseño UML
## Sistema de Reservas de Canchas Deportivas

## 1. Descripción general del sistema

El sistema permite gestionar reservas de canchas deportivas de forma simple. La versión funcional mínima incluye tres casos de uso principales:

1. Consultar disponibilidad.
2. Crear una reserva.
3. Cancelar una reserva.

También se incluye el registro de un pago aprobado, el cual permite confirmar una reserva que inicialmente fue creada con estado pendiente.

El diseño UML se mantiene relacionado con el código implementado. Las clases, operaciones y relaciones descritas en este documento corresponden principalmente a los archivos `models.py`, `services.py` y `repositories.py`.

---

## 2. Alcance de la versión mínima

La aplicación permite:

- Verificar que una cancha esté activa.
- Consultar si una cancha está disponible en un horario.
- Evitar reservas confirmadas que se solapen.
- Calcular el precio según el número de horas.
- Crear una reserva en estado `PENDIENTE`.
- Registrar un pago aprobado.
- Confirmar una reserva después del pago.
- Cancelar una reserva.
- Guardar y consultar reservas mediante un repositorio en memoria.

No se incluyen todavía:

- Interfaz gráfica o aplicación web.
- Base de datos permanente.
- Autenticación de usuarios.
- Envío de notificaciones.
- Integración con una pasarela de pagos real.
- Reembolsos automáticos.

---

## 3. Enfoque 4+1

### 3.1 Vista lógica

La vista lógica representa los elementos principales del sistema y sus responsabilidades.

Las entidades centrales son:

- `Usuario`: representa a la persona que realiza una reserva.
- `Cancha`: representa una cancha deportiva que puede estar activa o inactiva.
- `Reserva`: conserva el usuario, la cancha, el horario, el precio y el estado.
- `Pago`: conserva la información del pago relacionado con una reserva.

También se utilizan:

- `EstadoReserva`: enumeración de estados de una reserva.
- `EstadoPago`: enumeración de estados de un pago.
- `ServicioReservas`: coordina los casos de uso.
- `RepositorioReservasMemoria`: almacena temporalmente las reservas.

### 3.2 Vista de desarrollo

El proyecto está organizado en los siguientes módulos:

```text
src/
└── reservas/
    ├── __init__.py
    ├── models.py
    ├── repositories.py
    └── services.py

tests/
└── test_reservas.py

docs/
├── diseno_uml.md
├── informe_malos_olores.md
└── evidencias/
```

Responsabilidades:

- `models.py`: entidades, enumeraciones y comportamiento del dominio.
- `services.py`: operaciones de disponibilidad, creación, pago y cancelación.
- `repositories.py`: almacenamiento de reservas en memoria.
- `tests/`: pruebas unitarias ejecutadas con `pytest`.
- `docs/`: documentación UML y evidencias del proyecto.

### 3.3 Vista de procesos

El sistema trabaja de forma síncrona y local.

El flujo principal es:

1. El usuario solicita una reserva.
2. `ServicioReservas` verifica que el horario sea válido.
3. El servicio consulta si la cancha está disponible.
4. El sistema calcula el precio total.
5. Se crea una reserva pendiente.
6. La reserva se guarda en memoria.
7. Cuando se registra un pago aprobado, la reserva cambia a confirmada.

Para cancelar:

1. El usuario proporciona el identificador de la reserva.
2. El servicio busca la reserva.
3. La reserva cambia su estado a cancelada.
4. El repositorio guarda el estado actualizado.

### 3.4 Vista física

La versión actual se ejecuta como una aplicación Python local dentro de GitHub Codespaces o en un computador que tenga Python instalado.

```text
Usuario
   |
   v
Aplicación Python
   |
   +-- ServicioReservas
   |
   +-- RepositorioReservasMemoria
           |
           v
     Diccionario en memoria
```

No existe todavía una base de datos externa ni un servidor web. Cuando termina la ejecución, los datos almacenados en memoria se pierden.

### 3.5 Vista de escenarios

Los escenarios principales son:

- Escenario 1: consultar la disponibilidad de una cancha.
- Escenario 2: crear una reserva pendiente.
- Escenario 3: registrar un pago aprobado y confirmar una reserva.
- Escenario 4: cancelar una reserva.
- Escenario alternativo: rechazar una reserva si existe un solapamiento.
- Escenario alternativo: mostrar un error cuando una reserva no existe.

---

## 4. Diagrama de casos de uso

```plantuml
@startuml
left to right direction

actor Usuario

rectangle "Sistema de Reservas de Canchas" {
    usecase "Consultar\ndisponibilidad" as UC1
    usecase "Crear reserva" as UC2
    usecase "Registrar pago\naprobado" as UC3
    usecase "Cancelar reserva" as UC4

    usecase "Validar horario" as UC5
    usecase "Validar disponibilidad" as UC6
    usecase "Calcular precio total" as UC7
    usecase "Confirmar reserva" as UC8
}

Usuario --> UC1
Usuario --> UC2
Usuario --> UC3
Usuario --> UC4

UC2 ..> UC5 : <<include>>
UC2 ..> UC6 : <<include>>
UC2 ..> UC7 : <<include>>

UC3 ..> UC8 : <<include>>
UC8 ..> UC2 : <<extend>>

@enduml
```

### Explicación

- `Crear reserva` incluye validar el horario, validar disponibilidad y calcular el precio.
- `Registrar pago aprobado` incluye confirmar la reserva.
- `Confirmar reserva` extiende el proceso de creación, porque una reserva puede existir primero como pendiente y confirmarse posteriormente.
- `Cancelar reserva` es un caso independiente que modifica el estado de una reserva existente.

---

## 5. Diagrama de clases

```plantuml
@startuml
skinparam classAttributeIconSize 0

enum EstadoReserva {
    PENDIENTE
    CONFIRMADA
    CANCELADA
}

enum EstadoPago {
    PENDIENTE
    APROBADO
    RECHAZADO
    REEMBOLSADO
}

class Usuario {
    +id: str
    +nombre: str
    +email: str
}

class Cancha {
    +id: str
    +nombre: str
    +ubicacion: str
    +precio_por_hora: float
    +activa: bool
    +esta_disponible_para_reservar(): bool
}

class Pago {
    +id: str
    +reserva_id: str
    +monto: float
    +estado: EstadoPago
    +referencia_externa: Optional[str]
}

class Reserva {
    +id: str
    +usuario: Usuario
    +cancha: Cancha
    +inicio: datetime
    +fin: datetime
    +precio_total: float
    +estado: EstadoReserva
    +pago: Optional[Pago]
    +confirmar(pago: Pago): None
    +cancelar(): None
    +se_solapa_con(cancha_id: str, inicio: datetime, fin: datetime): bool
}

class ServicioReservas {
    -repositorio_reservas
    +consultar_disponibilidad(cancha, inicio, fin): bool
    +crear_reserva(reserva_id, usuario, cancha, inicio, fin): Reserva
    +registrar_pago_aprobado(reserva_id, pago_id, referencia_externa): Reserva
    +cancelar_reserva(reserva_id): Reserva
}

class RepositorioReservasMemoria {
    -_reservas: Dict[str, Reserva]
    +guardar(reserva: Reserva): Reserva
    +obtener_por_id(reserva_id: str): Optional[Reserva]
    +listar(): List[Reserva]
}

Usuario "1" -- "0..*" Reserva : realiza
Cancha "1" -- "0..*" Reserva : es reservada en
Reserva "1" o-- "0..1" Pago : contiene

Reserva --> EstadoReserva : usa
Pago --> EstadoPago : usa

ServicioReservas ..> Cancha : consulta
ServicioReservas ..> Reserva : crea y modifica
ServicioReservas ..> Pago : crea
ServicioReservas --> RepositorioReservasMemoria : usa

RepositorioReservasMemoria "1" o-- "0..*" Reserva : almacena

@enduml
```

### Relaciones y multiplicidades

- Un `Usuario` puede realizar cero o muchas reservas.
- Cada `Reserva` pertenece a un solo usuario.
- Una `Cancha` puede aparecer en cero o muchas reservas.
- Cada `Reserva` corresponde a una sola cancha.
- Una `Reserva` puede no tener pago o tener un solo pago.
- `ServicioReservas` utiliza `RepositorioReservasMemoria`.
- El repositorio puede almacenar cero o muchas reservas.

---

## 6. Diagrama de secuencia: crear reserva

```plantuml
@startuml
actor Usuario
participant ServicioReservas
participant Cancha
participant RepositorioReservasMemoria as Repositorio
participant Reserva

Usuario -> ServicioReservas: crear_reserva(id, usuario, cancha, inicio, fin)

alt inicio >= fin
    ServicioReservas --> Usuario: ValueError
else horario válido
    ServicioReservas -> Cancha: esta_disponible_para_reservar()
    Cancha --> ServicioReservas: activa

    alt cancha inactiva
        ServicioReservas --> Usuario: ValueError
    else cancha activa
        ServicioReservas -> Repositorio: listar()
        Repositorio --> ServicioReservas: lista de reservas

        loop por cada reserva
            ServicioReservas -> Reserva: se_solapa_con(cancha.id, inicio, fin)
            Reserva --> ServicioReservas: verdadero o falso
        end

        alt existe solapamiento
            ServicioReservas --> Usuario: ValueError
        else horario disponible
            ServicioReservas -> ServicioReservas: calcular horas y precio_total
            create Reserva
            ServicioReservas -> Reserva: Reserva(id, usuario, cancha,\ninicio, fin, precio_total)
            ServicioReservas -> Repositorio: guardar(reserva)
            Repositorio --> ServicioReservas: reserva guardada
            ServicioReservas --> Usuario: Reserva PENDIENTE
        end
    end
end

@enduml
```

---

## 7. Diagrama de secuencia: cancelar reserva

```plantuml
@startuml
actor Usuario
participant ServicioReservas
participant RepositorioReservasMemoria as Repositorio
participant Reserva

Usuario -> ServicioReservas: cancelar_reserva(reserva_id)
ServicioReservas -> Repositorio: obtener_por_id(reserva_id)
Repositorio --> ServicioReservas: reserva o None

alt reserva no encontrada
    ServicioReservas --> Usuario: ValueError
else reserva encontrada
    ServicioReservas -> Reserva: cancelar()

    alt reserva ya cancelada
        Reserva --> ServicioReservas: ValueError
        ServicioReservas --> Usuario: ValueError
    else reserva activa
        Reserva -> Reserva: estado = CANCELADA
        Reserva --> ServicioReservas: cancelación completada
        ServicioReservas -> Repositorio: guardar(reserva)
        Repositorio --> ServicioReservas: reserva actualizada
        ServicioReservas --> Usuario: Reserva CANCELADA
    end
end

@enduml
```

---

## 8. Patrón de diseño aplicado

### Patrón Repository

El patrón principal aplicado es **Repository**, representado por la clase `RepositorioReservasMemoria`.

Su responsabilidad es centralizar las operaciones de almacenamiento:

- Guardar una reserva.
- Buscar una reserva por identificador.
- Listar todas las reservas.

`ServicioReservas` no administra directamente el diccionario de datos. En su lugar, utiliza los métodos del repositorio.

### Beneficios

- Separa la lógica de aplicación del almacenamiento.
- Evita que `ServicioReservas` manipule directamente la estructura interna de datos.
- Facilita las pruebas unitarias.
- Permite reemplazar posteriormente el repositorio en memoria por una base de datos.
- Reduce el impacto de cambios en la persistencia.

En la versión actual, el patrón se aplica de manera básica porque solo existe una implementación concreta en memoria. Una evolución futura podría introducir una interfaz o clase abstracta para el repositorio.

---

## 9. Trazabilidad entre diseño y código

| Elemento del diseño | Ubicación en el código |
|---|---|
| `Usuario` | `src/reservas/models.py` |
| `Cancha` | `src/reservas/models.py` |
| `Reserva` | `src/reservas/models.py` |
| `Pago` | `src/reservas/models.py` |
| `EstadoReserva` | `src/reservas/models.py` |
| `EstadoPago` | `src/reservas/models.py` |
| `ServicioReservas` | `src/reservas/services.py` |
| `RepositorioReservasMemoria` | `src/reservas/repositories.py` |
| Pruebas unitarias | `tests/test_reservas.py` |

---

## 10. Correspondencia entre casos de uso y métodos

| Caso de uso | Método principal |
|---|---|
| Consultar disponibilidad | `ServicioReservas.consultar_disponibilidad()` |
| Crear reserva | `ServicioReservas.crear_reserva()` |
| Registrar pago aprobado | `ServicioReservas.registrar_pago_aprobado()` |
| Confirmar reserva | `Reserva.confirmar()` |
| Cancelar reserva | `ServicioReservas.cancelar_reserva()` |
| Validar solapamiento | `Reserva.se_solapa_con()` |
| Guardar reserva | `RepositorioReservasMemoria.guardar()` |
| Buscar reserva | `RepositorioReservasMemoria.obtener_por_id()` |

---

## 11. Decisiones de diseño

### Uso de entidades con `dataclass`

Las clases `Usuario`, `Cancha`, `Pago` y `Reserva` utilizan `dataclass` para reducir código repetitivo y mantener una estructura clara.

### Reglas dentro del dominio

Las operaciones `confirmar()`, `cancelar()` y `se_solapa_con()` se encuentran dentro de `Reserva`, porque modifican o consultan directamente su estado.

### Servicio de aplicación

`ServicioReservas` coordina las diferentes entidades y el repositorio. Allí se implementan los pasos completos de los casos de uso.

### Repositorio en memoria

La persistencia se realiza con un diccionario porque el objetivo de esta fase es demostrar diseño orientado a objetos, UML, pruebas y refactorización sin agregar la complejidad de una base de datos.

---

## 12. Conclusión

El diseño presenta una separación básica entre el modelo del dominio, los casos de uso y el almacenamiento. Los diagramas representan la implementación actual y permiten observar cómo colaboran `Usuario`, `Cancha`, `Reserva`, `Pago`, `ServicioReservas` y `RepositorioReservasMemoria`.

La solución es pequeña, pero permite aplicar posteriormente refactorizaciones en métodos, clases y objetos, datos y condicionales, manteniendo las pruebas unitarias como mecanismo de seguridad.
