# Software FJ — Gestión de Clientes, Servicios y Reservas

## Autoría
- Estudiante: [Leidy Gomez].
- Actividad: Fase 4.
- Modalidad: trabajo individual autorizado por el docente.

## Descripción
Aplicación de consola en Python que gestiona clientes, servicios y
reservas mediante objetos y listas, sin utilizar bases de datos.

Incluye reserva de salas, alquiler de equipos y asesorías especializadas.

## Funcionalidades
- Registro y validación de clientes.
- Cálculo de costos con impuestos y descuentos opcionales.
- Creación, confirmación y cancelación de reservas.
- Clases abstractas, herencia, polimorfismo y encapsulación.
- Excepciones personalizadas y registro de eventos y errores.

## Ejecución
Proyecto probado con Python 3.14 en Windows, sin paquetes externos.

Desde la carpeta del proyecto, ejecutar:

```bash
python fase4.py
```

## Resultados de la simulación
- 22 operaciones: 12 exitosas y 10 errores controlados.
- 0 errores inesperados en la ejecución realizada.
- 2 clientes, 3 servicios y 3 reservas registrados.

## Consideraciones
Los datos se conservan únicamente durante la ejecución.
Los eventos y errores se registran en `sistema.log`.
El sistema ejecuta una simulación automática, sin menú interactivo
ni calendario de reservas.

## Pruebas automáticas
El proyecto incluye 40 pruebas de clientes, servicios y reservas.

Para ejecutarlas desde la carpeta del proyecto:

```bash
python -m unittest discover -v
```

Resultado esperado: 40 pruebas ejecutadas y estado `OK`.
