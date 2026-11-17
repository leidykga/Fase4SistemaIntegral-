# Importa las clases que participan en una reserva.
from entidad import Entidad
from cliente import Cliente
from servicios import Servicio, validar_numero

# Importa las excepciones del proyecto.
from excepciones import (
    ErrorSoftwareFJ,
    ReservaInvalidaError,
    OperacionNoPermitidaError,
    ServicioNoDisponibleError,
)

# Importa el registro de eventos.
from registrador import registrar_evento


# Integra cliente, servicio, duración y estado.
class Reserva(Entidad):
    """Representa una reserva pendiente, confirmada o cancelada."""

    # Inicializa una reserva pendiente.
    def __init__(self, identificador, cliente, servicio, horas):
        super().__init__(identificador)

        # Guarda los objetos y la duración recibidos.
        self.__cliente = cliente
        self.__servicio = servicio
        self.__horas = horas

        # Define el estado inicial y el costo aún no procesado.
        self.__estado = "pendiente"
        self.__total = None

        # Rechaza datos incorrectos antes de terminar la creación.
        self.validar_datos()

    # Permite consultar el estado.
    @property
    def estado(self):
        return self.__estado

    # Permite consultar el total.
    @property
    def total(self):
        return self.__total

    # Implementa las validaciones de Entidad.
    def validar_datos(self):
        """Comprueba cliente, servicio y duración."""

        # Comprueba que se recibió un objeto Cliente.
        if not isinstance(self.__cliente, Cliente):
            raise ReservaInvalidaError(
                "La reserva necesita un objeto Cliente válido."
            )

        # Comprueba que se recibió un servicio concreto.
        if not isinstance(self.__servicio, Servicio):
            raise ReservaInvalidaError(
                "La reserva necesita un objeto Servicio válido."
            )

        # Revalida los datos de los objetos relacionados.
        self.__cliente.validar_datos()
        self.__servicio.validar_datos()

        # Valida y guarda la duración.
        self.__horas = validar_numero(
            self.__horas, "La duración", estricto=True
        )

    # Confirma únicamente una reserva pendiente.
    def confirmar(self):
        """Ocupa el servicio y cambia el estado de la reserva."""

        # Evita confirmar reservas canceladas o ya confirmadas.
        if self.__estado != "pendiente":
            raise OperacionNoPermitidaError(
                "Solo se puede confirmar una reserva pendiente."
            )

        # Exige calcular el costo antes de confirmar.
        if self.__total is None:
            raise OperacionNoPermitidaError(
                "Primero debe procesar la reserva."
            )

        # Ocupa el servicio; puede fallar si otra reserva lo utiliza.
        self.__servicio.ocupar()

        # Actualiza el estado después de ocupar el recurso.
        self.__estado = "confirmada"

        # Registra la confirmación.
        registrar_evento(f"Reserva {self.identificador} confirmada.")

    # Cancela una reserva y libera el recurso si corresponde.
    def cancelar(self):
        """Cancela una reserva pendiente o confirmada."""

        # Impide cancelar nuevamente la misma reserva.
        if self.__estado == "cancelada":
            raise OperacionNoPermitidaError(
                "La reserva ya está cancelada."
            )

        # Libera solamente el servicio ocupado por esta reserva.
        if self.__estado == "confirmada":
            self.__servicio.liberar()

        # Actualiza el estado.
        self.__estado = "cancelada"

        # Registra la cancelación.
        registrar_evento(f"Reserva {self.identificador} cancelada.")

        # Devuelve un mensaje para mostrar el resultado.
        return f"Reserva {self.identificador} cancelada correctamente."

    # Calcula y confirma utilizando manejo avanzado de excepciones.
    def procesar(self, impuesto=0, descuento=0):
        """Calcula el costo y confirma conservando la causa de los fallos."""

        # Inicia el procesamiento controlado.
        try:
            # Comprueba que la reserva todavía puede procesarse.
            if self.__estado != "pendiente":
                raise OperacionNoPermitidaError(
                    "Solo se puede procesar una reserva pendiente."
                )

            # Revalida sus datos antes de operar.
            self.validar_datos()

            # Detecta recursos ocupados antes del cálculo.
            if not self.__servicio.disponible:
                raise ServicioNoDisponibleError(
                    "El servicio solicitado no está disponible."
                )

            # Utiliza polimorfismo para calcular el costo.
            self.__total = self.__servicio.calcular_costo(
                self.__horas,
                impuesto=impuesto,
                descuento=descuento,
            )

            # Confirma la reserva después de calcular el valor.
            self.confirmar()

        # Convierte el fallo en un error de procesamiento de reserva.
        except ErrorSoftwareFJ as error:
            # Conserva la excepción original como causa.
            raise ReservaInvalidaError(
                f"No se pudo procesar la reserva {self.identificador}: {error}"
            ) from error

        # Devuelve el resultado únicamente si no hubo errores.
        else:
            return self.describir()

        # Registra el fin del intento, exitoso o fallido.
        finally:
            registrar_evento(
                f"Fin del procesamiento de reserva {self.identificador}. "
                f"Estado: {self.__estado}."
            )

    # Describe la reserva sin exponer documento ni teléfono.
    def describir(self):
        """Devuelve un resumen de la reserva."""

        # Prepara el costo para mostrarlo.
        costo = "sin calcular" if self.__total is None else f"{self.__total:.2f}"

        # Devuelve el resumen.
        return (
            f"Reserva {self.identificador} | "
            f"Cliente: {self.__cliente.nombre} | "
            f"Servicio: {self.__servicio.nombre} | "
            f"Horas: {self.__horas:g} | "
            f"Estado: {self.__estado} | Total: {costo}"
        )