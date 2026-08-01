# Informe final de refactorización

## Sistema de Reservas de Canchas Deportivas

## 1. Contexto

Después de la primera versión funcional del sistema, se aplicó un proceso disciplinado de refactorización. Antes de iniciar los cambios, la suite de pruebas se ejecutó en verde. Luego, cada refactorización se realizó en un commit independiente y se volvieron a ejecutar las pruebas.

El objetivo de esta fase fue mejorar la mantenibilidad, la separación de responsabilidades y la expresividad del diseño sin cambiar el comportamiento funcional del sistema.

---

## 2. Evidencia general de pruebas

Las pruebas se guardaron en:

- `docs/evidencias/fase3/pruebas_antes_refactorizacion.txt`
- `docs/evidencias/fase3/pruebas_refactor_01.txt`
- `docs/evidencias/fase3/pruebas_refactor_02.txt`
- `docs/evidencias/fase3/pruebas_refactor_03.txt`
- `docs/evidencias/fase3/pruebas_refactor_04.txt`
- `docs/evidencias/fase3/pruebas_refactor_05.txt`
- `docs/evidencias/fase3/pruebas_refactor_06.txt`

Todas muestran las pruebas en verde.

---

## 3. Refactorizaciones aplicadas

| # | Nivel cubierto | Técnica aplicada | Problema original | Cambio aplicado | Commit |
|---|---|---|---|---|---|
| 1 | Datos | Introduce Value Object | Las fechas inicio y fin se manejaban como datos sueltos. | Se creó `HorarioReserva` para encapsular inicio, fin, duración y solapamiento. | 98c89f4 |
| 2 | Métodos | Extract Method / Extract Class | El cálculo de precio estaba dentro de `ServicioReservas`. | Se creó `CalculadorPrecio`. | 2e9ae95 |
| 3 | Condicionales | Replace Error Code / Domain Exceptions | Se usaban `ValueError` genéricos. | Se crearon excepciones específicas del dominio. | 1fc3ab1 |
| 4 | Clases y objetos | Extract Class | `ServicioReservas` concentraba demasiada lógica. | Se creó `ServicioDisponibilidad`. | 305dd43 |
| 5 | Clases y objetos | Factory Method | La creación de pagos aprobados estaba dentro del servicio. | Se agregó `Pago.aprobado(...)`. | ab87bb5 |
| 6 | Datos / métodos | Introduce Parameter Object | Los casos de uso recibían muchos parámetros sueltos. | Se crearon `CrearReservaCommand` y `RegistrarPagoCommand`. | 7e6fd9c |

---

## 4. Detalle de las refactorizaciones

### Refactorización 1: HorarioReserva

Antes, los métodos recibían `inicio` y `fin` como parámetros independientes. Esto generaba un olor de datos sueltos y repetición de lógica temporal.

Después, se creó `HorarioReserva`, que valida si el horario es correcto, calcula la duración en horas y revisa solapamientos.

Beneficio: el código expresa mejor el dominio y reduce la duplicación de lógica relacionada con fechas.

---

### Refactorización 2: CalculadorPrecio

Antes, el cálculo del precio total estaba dentro de `ServicioReservas`.

Después, se creó la clase `CalculadorPrecio`.

Beneficio: el servicio de reservas queda más enfocado en coordinar el caso de uso, mientras que la regla de precio queda separada.

---

### Refactorización 3: Excepciones del dominio

Antes, los errores del sistema se lanzaban con `ValueError` genéricos.

Después, se crearon excepciones específicas:

- `HorarioInvalidoError`
- `ReservaNoDisponibleError`
- `ReservaNoEncontradaError`
- `PagoNoAprobadoError`
- `ReservaYaCanceladaError`

Beneficio: los errores son más expresivos y fáciles de mantener.

---

### Refactorización 4: ServicioDisponibilidad

Antes, `ServicioReservas` calculaba disponibilidad, creaba reservas, registraba pagos y cancelaba reservas.

Después, se extrajo la lógica de disponibilidad a `ServicioDisponibilidad`.

Beneficio: mejora la separación de responsabilidades y reduce el tamaño conceptual de `ServicioReservas`.

---

### Refactorización 5: Pago.aprobado

Antes, `ServicioReservas` construía directamente un pago aprobado.

Después, la clase `Pago` tiene un método fábrica `aprobado`.

Beneficio: la lógica de creación de pagos queda más cerca del modelo correspondiente.

---

### Refactorización 6: Commands de entrada

Antes, algunos métodos recibían varios parámetros sueltos.

Después, se crearon `CrearReservaCommand` y `RegistrarPagoCommand`.

Beneficio: mejora la organización de los datos de entrada y prepara el sistema para crecer sin aumentar demasiado las firmas de los métodos.

---

## 5. Diagrama de clases actualizado

El diagrama actualizado se encuentra en:

`docs/diagramas/diagrama_clases_refactorizado.puml`

Este diagrama muestra la evolución del diseño después de agregar `HorarioReserva`, `CalculadorPrecio`, `ServicioDisponibilidad`, comandos de entrada y excepciones del dominio.

---

## 6. Demostración ejecutable

Se agregó el archivo:

`demo.py`

Ejecución:

```bash
PYTHONPATH=src python demo.py
```

La salida esperada muestra disponibilidad inicial, creación de reserva, confirmación por pago y cancelación.

---

## 7. Conclusión

La refactorización permitió conservar el comportamiento funcional del sistema, pero mejorar la organización interna del código. Las pruebas unitarias sirvieron como red de seguridad para verificar que cada cambio no rompiera los casos principales. Además, el historial Git evidencia una evolución progresiva del diseño mediante commits separados.
