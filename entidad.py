# Importa las herramientas para definir clases abstractas.
from abc import ABC, abstractmethod

# Importa la excepción utilizada para rechazar datos inválidos.
from excepciones import DatosInvalidosError


# Define una base común para las entidades del sistema.
class Entidad(ABC):
    """Establece un identificador y comportamientos comunes."""

    # Inicializa el identificador de la entidad.
    def __init__(self, identificador):
        """Acepta únicamente identificadores enteros positivos."""

        # Rechaza valores de otros tipos, incluidos los booleanos.
        if type(identificador) is not int:
            raise DatosInvalidosError(
                "El identificador debe ser un número entero."
            )

        # Rechaza identificadores iguales a cero o negativos.
        if identificador <= 0:
            raise DatosInvalidosError(
                "El identificador debe ser mayor que cero."
            )

        # Guarda el identificador en un atributo privado.
        self.__identificador = identificador

    # Permite consultar el identificador mediante una propiedad. 
    @property
    def identificador(self):
        """Devuelve el identificador sin permitir su asignación directa."""
        return self.__identificador

    # Obliga a las clases hijas a definir sus validaciones.
    @abstractmethod
    def validar_datos(self):
        """Comprueba los datos específicos de cada entidad."""
        pass

    # Obliga a las clases hijas a definir su descripción.
    @abstractmethod
    def describir(self):
        """Devuelve una descripción de la entidad."""
        pass