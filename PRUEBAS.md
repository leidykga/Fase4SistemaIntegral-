# Plan y resultados de pruebas — Software FJ

## Objetivo
Verificar registros, cálculos y reservas, comprobando que los errores
controlados no interrumpan las operaciones siguientes.

## Procedimiento
Ejecutar `python fase4.py`, revisar los resultados de la terminal
y consultar los eventos y errores en `sistema.log`.

## Casos ejecutados

| N.º | Operación | Resultado observado |
|---|---|---|
| 1 | Registrar cliente válido | Cliente registrado. |
| 2 | Registrar cliente con correo inválido | Error controlado. |
| 3 | Registrar otro cliente válido | Cliente registrado después del error anterior. |
| 4 | Registrar identificador de cliente repetido | Error controlado. |
| 5 | Crear sala con tarifa válida | Servicio registrado. |
| 6 | Crear servicio con tarifa negativa | Error controlado. |
| 7 | Crear equipo con tarifa válida | Servicio registrado. |
| 8 | Crear asesoría con tarifa válida | Servicio registrado. |
| 9 | Calcular equipo con seguro, impuesto y descuento | Total: 53550.00. |
| 10 | Aplicar descuento superior al 100 % | Error controlado. |
| 11 | Crear reserva con duración negativa | Error controlado. |
| 12 | Crear reserva válida de sala | Reserva 2 pendiente. |
| 13 | Procesar reserva de sala | Reserva 2 confirmada. Total: 107100.00. |
| 14 | Crear otra solicitud para la misma sala | Reserva 3 pendiente. |
| 15 | Procesar solicitud con sala ocupada | Error controlado. |
| 16 | Cancelar la reserva confirmada | Reserva 2 cancelada y sala liberada. |
| 17 | Procesar una reserva cancelada | Error controlado. |
| 18 | Procesar la solicitud pendiente tras liberar la sala | Reserva 3 confirmada. Total: 50000.00. |
| 19 | Crear solicitud de asesoría de media hora | Reserva 4 pendiente. |
| 20 | Procesar asesoría menor de una hora | Error controlado. |
| 21 | Crear reserva con cliente inexistente | Error controlado. |
| 22 | Crear cliente con parámetros faltantes | Error controlado. |

## Resumen observado
- Operaciones realizadas: 22.
- Operaciones exitosas: 12.
- Errores controlados: 10.
- Errores inesperados: 0.
- Clientes registrados: 2.
- Servicios registrados: 3.
- Reservas registradas: 3.

## Estados finales
- Reserva 2: cancelada.
- Reserva 3: confirmada.
- Reserva 4: pendiente por rechazo de la duración al procesarse.

## Conclusión
La ejecución terminó después de procesar las 22 operaciones.
Los errores previstos fueron manejados sin impedir las operaciones
posteriores. Estos resultados corresponden a los casos ejecutados
y no garantizan el comportamiento ante todas las entradas posibles.