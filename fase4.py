# Importa las clases principales del sistema.
from cliente import Cliente
from servicios import ReservaSala, AlquilerEquipo, AsesoriaEspecializada
from reserva import Reserva

# Importa las excepciones controladas.
from excepciones import ErrorSoftwareFJ, DatosInvalidosError

# Importa las funciones de registro.
from registrador import registrar_evento, registrar_error


# Administra las listas internas de objetos.
class SistemaSoftwareFJ:
    """Agrupa clientes, servicios y reservas sin usar bases de datos."""

    # Crea las colecciones en memoria.
    def __init__(self):
        self.clientes = []
        self.servicios = []
        self.reservas = []

    # Registra objetos evitando identificadores repetidos.
    def _agregar(self, coleccion, objeto):
        """Agrega un objeto si su identificador no existe."""

        # Revisa los identificadores de la colección correspondiente.
        if any(
            existente.identificador == objeto.identificador
            for existente in coleccion
        ):
            raise DatosInvalidosError(
                f"El identificador {objeto.identificador} ya existe."
            )

        # Almacena el objeto validado.
        coleccion.append(objeto)

        # Registra el evento sin incluir datos personales.
        registrar_evento(
            f"Registro de {type(objeto).__name__} "
            f"con identificador {objeto.identificador}."
        )

        # Devuelve una descripción del objeto.
        return objeto.describir()

    # Crea y almacena un cliente.
    def registrar_cliente(self, *datos):
        return self._agregar(self.clientes, Cliente(*datos))

    # Crea y almacena un servicio especializado.
    def registrar_servicio(self, clase, *datos):
        return self._agregar(self.servicios, clase(*datos))

    # Busca un objeto por su identificador.
    def _buscar(self, coleccion, identificador):
        """Devuelve el objeto solicitado o genera un error."""

        # Recorre los objetos almacenados.
        for objeto in coleccion:
            if objeto.identificador == identificador:
                return objeto

        # Rechaza referencias inexistentes.
        raise DatosInvalidosError(
            f"No existe un registro con identificador {identificador}."
        )

    # Permite obtener un servicio para calcular sus costos.
    def buscar_servicio(self, identificador):
        return self._buscar(self.servicios, identificador)

    # Permite consultar una reserva.
    def buscar_reserva(self, identificador):
        return self._buscar(self.reservas, identificador)

    # Crea una reserva relacionando objetos ya registrados.
    def crear_reserva(self, identificador, cliente_id, servicio_id, horas):
        """Busca cliente y servicio antes de crear la reserva."""

        # Obtiene las referencias válidas.
        cliente = self._buscar(self.clientes, cliente_id)
        servicio = self._buscar(self.servicios, servicio_id)

        # Construye y almacena la reserva pendiente.
        reserva = Reserva(identificador, cliente, servicio, horas)
        return self._agregar(self.reservas, reserva)

    # Procesa una reserva existente.
    def procesar_reserva(self, identificador, **opciones):
        return self.buscar_reserva(identificador).procesar(**opciones)

    # Cancela una reserva existente.
    def cancelar_reserva(self, identificador):
        return self.buscar_reserva(identificador).cancelar()


# Ejecuta la simulación completa.
def main():
    """Prueba registros, cálculos y reservas válidas e inválidas."""

    # Presenta el programa.
    print("=" * 65)
    print("SOFTWARE FJ - CLIENTES, SERVICIOS Y RESERVAS")
    print("=" * 65)

    # Crea las listas del sistema.
    sistema = SistemaSoftwareFJ()

    # Prepara operaciones independientes para continuar tras cada error.
    operaciones = [
        (
            "Registrar cliente válido",
            lambda: sistema.registrar_cliente(
                1, "Ana Pérez", "1020304050",
                "ana@ejemplo.com", "3001234567"
            ),
        ),
        (
            "Rechazar cliente con correo inválido",
            lambda: sistema.registrar_cliente(
                2, "Luis Gómez", "1020304051",
                "correo_invalido", "3007654321"
            ),
        ),
        (
            "Registrar otro cliente válido",
            lambda: sistema.registrar_cliente(
                3, "Marta Ruiz", "1020304052",
                "marta@ejemplo.com", "3101234567"
            ),
        ),
        (
            "Rechazar identificador de cliente repetido",
            lambda: sistema.registrar_cliente(
                1, "Pedro Ruiz", "1020304053",
                "pedro@ejemplo.com", "3201234567"
            ),
        ),
        (
            "Crear sala válida",
            lambda: sistema.registrar_servicio(
                ReservaSala, 1, "Sala de reuniones", 50000
            ),
        ),
        (
            "Rechazar servicio con tarifa negativa",
            lambda: sistema.registrar_servicio(
                ReservaSala, 2, "Sala inválida", -5000
            ),
        ),
        (
            "Crear equipo válido",
            lambda: sistema.registrar_servicio(
                AlquilerEquipo, 3, "Video proyector", 20000
            ),
        ),
        (
            "Crear asesoría válida",
            lambda: sistema.registrar_servicio(
                AsesoriaEspecializada, 4, "Asesoría en Python", 80000
            ),
        ),
        (
            "Calcular equipo con seguro, impuesto y descuento",
            lambda: sistema.buscar_servicio(3).calcular_costo(
                2, impuesto=19, descuento=10, seguro=True
            ),
        ),
        (
            "Rechazar descuento superior al 100 por ciento",
            lambda: sistema.buscar_servicio(1).calcular_costo(
                2, descuento=120
            ),
        ),
        (
            "Rechazar reserva con duración negativa",
            lambda: sistema.crear_reserva(1, 1, 1, -2),
        ),
        (
            "Crear reserva válida de sala",
            lambda: sistema.crear_reserva(2, 1, 1, 2),
        ),
        (
            "Procesar y confirmar la reserva de sala",
            lambda: sistema.procesar_reserva(
                2, impuesto=19, descuento=10
            ),
        ),
        (
            "Crear otra solicitud para la misma sala",
            lambda: sistema.crear_reserva(3, 3, 1, 1),
        ),
        (
            "Rechazar procesamiento porque la sala está ocupada",
            lambda: sistema.procesar_reserva(3),
        ),
        (
            "Cancelar la reserva confirmada y liberar la sala",
            lambda: sistema.cancelar_reserva(2),
        ),
        (
            "Rechazar procesamiento de una reserva cancelada",
            lambda: sistema.procesar_reserva(2),
        ),
        (
            "Procesar la reserva pendiente con la sala liberada",
            lambda: sistema.procesar_reserva(3),
        ),
        (
            "Crear reserva de asesoría de media hora",
            lambda: sistema.crear_reserva(4, 1, 4, 0.5),
        ),
        (
            "Rechazar asesoría por duración mínima",
            lambda: sistema.procesar_reserva(4),
        ),
        (
            "Rechazar una reserva con cliente inexistente",
            lambda: sistema.crear_reserva(5, 999, 3, 2),
        ),
        (
            "Rechazar creación de cliente con parámetros faltantes",
            lambda: sistema.registrar_cliente(9, "Cliente incompleto"),
        ),
    ]

    # Inicializa los contadores del resumen.
    exitosas = 0
    controladas = 0
    inesperadas = 0

    # Registra el inicio de la simulación.
    registrar_evento("Inicio de la simulación completa.")

    # Ejecuta las operaciones de forma secuencial.
    for numero, (descripcion, operacion) in enumerate(operaciones, start=1):
        # Presenta la operación actual.
        print(f"\n{numero}. {descripcion}")

        # Aísla cada operación para no detener las siguientes.
        try:
            resultado = operacion()

        # Controla errores del proyecto y parámetros faltantes.
        except (ErrorSoftwareFJ, TypeError) as error:
            controladas += 1
            registrar_error(f"Operación {numero} rechazada: {error}")
            print(f"ERROR CONTROLADO: {error}")

        # Aísla fallos no previstos en el límite de la simulación.
        except Exception as error:
            inesperadas += 1
            registrar_error(f"Fallo inesperado en operación {numero}: {error}")
            print("ERROR INESPERADO: consulte sistema.log.")

        # Registra y muestra únicamente los resultados exitosos.
        else:
            exitosas += 1
            registrar_evento(f"Operación {numero} completada.")
            print(f"CORRECTO: {resultado}")

        # Registra el cierre de cada intento.
        finally:
            registrar_evento(f"Finalizó la operación {numero}.")

    # Presenta el resumen de ejecución.
    print("\n" + "=" * 65)
    print("RESUMEN DE LA SIMULACIÓN")
    print(f"Operaciones realizadas: {len(operaciones)}")
    print(f"Operaciones exitosas: {exitosas}")
    print(f"Errores controlados: {controladas}")
    print(f"Errores inesperados: {inesperadas}")
    print(f"Clientes registrados: {len(sistema.clientes)}")
    print(f"Servicios registrados: {len(sistema.servicios)}")
    print(f"Reservas registradas: {len(sistema.reservas)}")

    # Demuestra el uso de métodos polimórficos.
    print("\nSERVICIOS:")
    for servicio in sistema.servicios:
        print(f"- {servicio.describir()}")

    # Muestra el estado final de las reservas.
    print("\nRESERVAS:")
    for reserva in sistema.reservas:
        print(f"- {reserva.describir()}")

    # Confirma que se alcanzó el final de la simulación.
    print("\nSimulación finalizada. Revise sistema.log.")

    # Registra el cierre.
    registrar_evento("Fin de la simulación completa.")


# Ejecuta la aplicación.
if __name__ == "__main__":
    main()
