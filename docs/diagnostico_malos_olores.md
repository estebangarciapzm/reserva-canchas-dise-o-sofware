# Informe de diagnóstico de malos olores

## Contexto

Este diagnóstico corresponde a la primera versión funcional mínima del sistema de reservas de canchas deportivas. El código ya permite consultar disponibilidad, crear reservas, registrar pagos aprobados y cancelar reservas. Además, las pruebas unitarias se ejecutan en verde con pytest.

En esta parte entendí que un mal olor no significa necesariamente que el programa falle. Más bien es una señal de que, si el proyecto crece, el diseño podría volverse difícil de mantener, probar o modificar.

---

## Mal olor 1: Obsesión por tipos primitivos

**Ubicación:** `src/reservas/models.py`, clases `Usuario`, `Cancha`, `Pago` y `Reserva`.

**Evidencia:** revisar `docs/evidencias/models_con_lineas.txt`.

**Descripción:**  
El código usa varios campos de tipo `str` para representar identificadores como `usuario.id`, `cancha.id`, `reserva.id` y `pago.id`. También el correo electrónico se maneja como una cadena simple.

**Por qué es un problema:**  
Aunque funciona en esta versión inicial, todos los identificadores se comportan igual para Python. Esto podría permitir errores como enviar un `cancha_id` donde se esperaba un `reserva_id`.

**Posible refactorización:**  
Crear objetos de valor como `UsuarioId`, `CanchaId`, `ReservaId` y `Email`.

---

## Mal olor 2: Servicio con muchas responsabilidades

**Ubicación:** `src/reservas/services.py`, clase `ServicioReservas`.

**Evidencia:** revisar `docs/evidencias/services_con_lineas.txt`.

**Descripción:**  
La clase `ServicioReservas` se encarga de consultar disponibilidad, crear reservas, calcular precios, registrar pagos aprobados y cancelar reservas.

**Por qué es un problema:**  
Para una versión mínima es aceptable, pero si el sistema crece esta clase puede convertirse en una clase grande. También mezcla reglas de disponibilidad, cálculo de precio y confirmación por pago.

**Posible refactorización:**  
Separar responsabilidades en `ServicioDisponibilidad`, `CalculadorPrecio` y `ServicioPagos`.

---

## Mal olor 3: Lista larga de parámetros

**Ubicación:** `src/reservas/services.py`, métodos `crear_reserva` y `registrar_pago_aprobado`.

**Evidencia:** revisar `docs/evidencias/services_con_lineas.txt`.

**Descripción:**  
Los métodos reciben varios datos sueltos, por ejemplo `reserva_id`, `usuario`, `cancha`, `inicio` y `fin`.

**Por qué es un problema:**  
A medida que el caso de uso crezca, la firma del método puede aumentar y volverse más difícil de leer. También puede facilitar errores en el orden de los argumentos.

**Posible refactorización:**  
Crear objetos de entrada como `CrearReservaCommand` y `RegistrarPagoCommand`.

---

## Mal olor 4: Mensajes de error quemados en el código

**Ubicación:** `src/reservas/models.py` y `src/reservas/services.py`, líneas donde aparece `raise ValueError`.

**Evidencia:** revisar `docs/evidencias/ubicaciones_malos_olores.txt`.

**Descripción:**  
Los mensajes de error están escritos directamente dentro de los métodos usando `ValueError`.

**Por qué es un problema:**  
Si el proyecto crece, será más difícil mantener mensajes consistentes. También limita la posibilidad de usar excepciones específicas para distintos errores del dominio.

**Posible refactorización:**  
Crear excepciones propias como `ReservaNoDisponibleError`, `ReservaNoEncontradaError` y `PagoNoAprobadoError`.

---

## Mal olor 5: Modelo Pago demasiado pasivo

**Ubicación:** `src/reservas/models.py`, clase `Pago`; `src/reservas/services.py`, método `registrar_pago_aprobado`.

**Evidencia:** revisar `docs/evidencias/models_con_lineas.txt` y `docs/evidencias/services_con_lineas.txt`.

**Descripción:**  
La clase `Pago` actualmente solo almacena datos. La creación de un pago aprobado se realiza dentro de `ServicioReservas`.

**Por qué es un problema:**  
Si después se agregan pagos rechazados, pagos pendientes, reembolsos o validación con una pasarela externa, la lógica de pagos puede mezclarse demasiado con la lógica de reservas.

**Posible refactorización:**  
Crear un `ServicioPagos` o un método de fábrica como `Pago.aprobado(...)`.

---

## Conclusión del diagnóstico

El código base cumple con los tres casos de uso principales y las pruebas unitarias se ejecutan correctamente. Sin embargo, este diagnóstico muestra que la versión inicial todavía puede mejorar en separación de responsabilidades, expresividad del dominio y manejo de errores. En mi interpretación, estos malos olores son útiles porque permiten planificar una refactorización gradual sin romper el sistema. La suite de pruebas en verde sirve como red de seguridad para realizar esos cambios con menor riesgo.
