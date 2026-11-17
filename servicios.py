# Importa herramientas para clases abstractas.
from abc import abstractmethod

# Importa una función para rechazar infinito y valores no numéricos.
from math import isfinite

# Importa la entidad base.
from entidad import Entidad

# Importa las excepciones de validación.
from excepciones import DatosInvalidosError, ServicioNoDisponibleError


# Centraliza la validación de cantidades numéricas.
def validar_numero(valor, nombre, minimo=0, estricto=False):
    """Comprueba tipo, finitud y límite inferior de una cantidad."""

    # Rechaza booleanos, textos y otros tipos no admitidos.
    if isinstance(valor, bool) or not isinstance(valor, (int, float)):
        raise DatosInvalidosError(f"{nombre} debe ser numérico.")

    # Convierte el dato para comprobar su finitud de manera controlada.
    try:
        numero = float(valor)

    # Conserva la causa de una conversión imposible.
    except (OverflowError, ValueError) as error:
        raise DatosInvalidosError(
            f"{nombre} está fuera del rango permitido."
        ) from error

    # Rechaza infinito y NaN.
    if not isfinite(numero):
        raise DatosInvalidosError(f"{nombre} debe ser finito.")

    # Aplica el límite inferior indicado.
    if numero < minimo or (estricto and numero == minimo):
        comparacion = "mayor que" if estricto else "mayor o igual que"
        raise DatosInvalidosError(
            f"{nombre} debe ser {comparacion} {minimo}."
        )

    # Devuelve el número validado.
    return numero


# Define la clase abstracta para los servicios.
class Servicio(Entidad):
    """Representa un recurso reservable con tarifa por hora."""

    # Inicializa los atributos compartidos por los servicios.
    def __init__(self, identificador, nombre, tarifa_hora):
        super().__init__(identificador)

        # Normaliza el nombre si es texto.
        self.__nombre = nombre.strip() if isinstance(nombre, str) else nombre

        # Conserva la tarifa recibida para validarla.
        self.__tarifa_hora = tarifa_hora

        # Cada objeto representa un recurso individual disponible.
        self.__disponible = True

        # Comprueba los datos generales.
        self.validar_datos()

    # Permite consultar el nombre.
    @property
    def nombre(self):
        return self.__nombre

    # Permite consultar la tarifa.
    @property
    def tarifa_hora(self):
        return self.__tarifa_hora

    # Permite consultar la disponibilidad.
    @property
    def disponible(self):
        return self.__disponible

    # Implementa la validación requerida por Entidad.
    def validar_datos(self):
        """Valida el nombre y la tarifa del servicio."""

        # Rechaza nombres vacíos o tipos incorrectos.
        if not isinstance(self.__nombre, str) or not self.__nombre:
            raise DatosInvalidosError("El servicio necesita un nombre.")

        # Guarda una tarifa positiva validada.
        self.__tarifa_hora = validar_numero(
            self.__tarifa_hora, "La tarifa", estricto=True
        )

    # Cambia la disponibilidad al confirmar una reserva.
    def ocupar(self):
        """Marca el recurso como ocupado si estaba disponible."""

        # Evita reservar dos veces un mismo recurso.
        if not self.__disponible:
            raise ServicioNoDisponibleError(
                f"El servicio '{self.nombre}' está ocupado."
            )

        # Actualiza el estado después de validar.
        self.__disponible = False

    # Restablece la disponibilidad al cancelar.
    def liberar(self):
        """Deja el recurso disponible nuevamente."""
        self.__disponible = True

    # Centraliza los cálculos compartidos.
    def _calcular_total(self, horas, impuesto, descuento, recargo=0):
        """Calcula el total aplicando descuento e impuesto porcentuales."""

        # Valida una duración positiva.
        horas = validar_numero(horas, "La duración", estricto=True)

        # Valida los porcentajes y el recargo.
        impuesto = validar_numero(impuesto, "El impuesto")
        descuento = validar_numero(descuento, "El descuento")
        recargo = validar_numero(recargo, "El recargo")

        # Impide porcentajes fuera del rango admitido.
        if impuesto > 100 or descuento > 100:
            raise DatosInvalidosError(
                "El impuesto y el descuento deben estar entre 0 y 100."
            )

        # Calcula el subtotal antes de aplicar porcentajes.
        subtotal = self.tarifa_hora * horas + recargo

        # Aplica primero descuento y después impuesto.
        total = subtotal * (1 - descuento / 100) * (1 + impuesto / 100)

        # Rechaza resultados inconsistentes o desbordados.
        if not isfinite(total) or total < 0:
            raise DatosInvalidosError("El costo calculado es inconsistente.")

        # Redondea el resultado monetario a dos decimales.
        return round(total, 2)

    # Obliga a cada servicio especializado a calcular su costo.
    @abstractmethod
    def calcular_costo(self, horas, impuesto=0, descuento=0):
        """Calcula el valor según las reglas del servicio."""
        pass


# Especializa el servicio para una sala individual.
class ReservaSala(Servicio):
    """Representa una sala con tarifa por hora."""

    # Sobrescribe el cálculo para el alquiler de salas.
    def calcular_costo(self, horas, impuesto=0, descuento=0):
        return self._calcular_total(horas, impuesto, descuento)

    # Sobrescribe la descripción requerida por Entidad.
    def describir(self):
        return f"Sala: {self.nombre}. Tarifa por hora: {self.tarifa_hora:.2f}"


# Especializa el servicio para un equipo individual.
class AlquilerEquipo(Servicio):
    """Representa un equipo con seguro opcional por reserva."""

    # Agrega una regla específica para el seguro.
    def calcular_costo(self, horas, impuesto=0, descuento=0, seguro=False):
        # Rechaza valores ambiguos para el seguro.
        if not isinstance(seguro, bool):
            raise DatosInvalidosError("El seguro debe ser True o False.")

        # Aplica un recargo fijo cuando se solicita seguro.
        recargo = 10000 if seguro else 0

        # Delega los cálculos y validaciones compartidos.
        return self._calcular_total(horas, impuesto, descuento, recargo)

    # Describe este tipo particular de servicio.
    def describir(self):
        return f"Equipo: {self.nombre}. Tarifa por hora: {self.tarifa_hora:.2f}"


# Especializa el servicio para una asesoría.
class AsesoriaEspecializada(Servicio):
    """Representa una asesoría con duración mínima de una hora."""

    # Agrega una restricción específica de duración.
    def calcular_costo(self, horas, impuesto=0, descuento=0):
        # Valida el dato antes de compararlo.
        horas = validar_numero(horas, "La duración", estricto=True)

        # Aplica la regla particular de las asesorías.
        if horas < 1:
            raise DatosInvalidosError(
                "La asesoría debe durar al menos una hora."
            )

        # Calcula el valor con las reglas generales.
        return self._calcular_total(horas, impuesto, descuento)

    # Describe este tipo particular de servicio.
    def describir(self):
        return (
            f"Asesoría: {self.nombre}. "
            f"Tarifa por hora: {self.tarifa_hora:.2f}"
        )