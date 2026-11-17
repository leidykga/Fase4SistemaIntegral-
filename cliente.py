# Importa herramientas para validar el formato de los datos.
import re

# Importa la clase abstracta de la que heredará Cliente.
from entidad import Entidad

# Importa la excepción para datos incorrectos.
from excepciones import DatosInvalidosError


# Define un cliente como una entidad especializada del sistema.
class Cliente(Entidad):
    """Representa un cliente con datos personales validados."""

    # Recibe el identificador y los datos personales del cliente.
    def __init__(self, identificador, nombre, documento, correo, telefono):
        """Inicializa los atributos y valida los datos recibidos."""

        # Valida y almacena el identificador mediante la clase padre.
        super().__init__(identificador)

        # Guarda el nombre sin espacios sobrantes si es texto.
        self.__nombre = nombre.strip() if isinstance(nombre, str) else nombre

        # Guarda el documento sin espacios sobrantes si es texto.
        self.__documento = (
            documento.strip() if isinstance(documento, str) else documento
        )

        # Guarda el correo sin espacios sobrantes si es texto.
        self.__correo = correo.strip() if isinstance(correo, str) else correo

        # Guarda el teléfono sin espacios sobrantes si es texto.
        self.__telefono = (
            telefono.strip() if isinstance(telefono, str) else telefono
        )

        # Impide crear el cliente si alguno de sus datos es inválido.
        self.validar_datos()

    # Permite consultar el nombre sin modificarlo directamente.
    @property
    def nombre(self):
        """Devuelve el nombre del cliente."""
        return self.__nombre

    # Permite consultar el documento sin modificarlo directamente.
    @property
    def documento(self):
        """Devuelve el documento del cliente."""
        return self.__documento

    # Permite consultar el correo sin modificarlo directamente.
    @property
    def correo(self):
        """Devuelve el correo electrónico del cliente."""
        return self.__correo

    # Permite consultar el teléfono sin modificarlo directamente.
    @property
    def telefono(self):
        """Devuelve el teléfono del cliente."""
        return self.__telefono

    # Implementa la validación exigida por la clase Entidad.
    def validar_datos(self):
        """Verifica tipos, contenido y formatos de los datos personales."""

        # Comprueba que el nombre sea texto y tenga al menos dos caracteres.
        if not isinstance(self.__nombre, str) or len(self.__nombre) < 2:
            raise DatosInvalidosError(
                "El nombre debe ser un texto de al menos dos caracteres."
            )

        # Comprueba que el nombre contenga al menos una letra.
        if not any(caracter.isalpha() for caracter in self.__nombre):
            raise DatosInvalidosError(
                "El nombre debe contener al menos una letra."
            )

        # Comprueba que el documento sea texto compuesto por dígitos.
        if (
            not isinstance(self.__documento, str)
            or re.fullmatch(r"[0-9]{5,15}", self.__documento) is None
        ):
            raise DatosInvalidosError(
                "El documento debe contener entre 5 y 15 dígitos."
            )

        # Comprueba un formato básico de correo sin espacios.
        if (
            not isinstance(self.__correo, str)
            or re.fullmatch(
                r"[^@\s]+@[^@\s]+\.[^@\s]+", self.__correo
            ) is None
        ):
            raise DatosInvalidosError(
                "El correo debe tener un formato como nombre@dominio.com."
            )

        # Comprueba que el teléfono sea texto de entre 7 y 15 dígitos.
        if (
            not isinstance(self.__telefono, str)
            or re.fullmatch(r"[0-9]{7,15}", self.__telefono) is None
        ):
            raise DatosInvalidosError(
                "El teléfono debe contener entre 7 y 15 dígitos."
            )

    # Implementa la descripción exigida por la clase Entidad.
    def describir(self):
        """Devuelve una descripción sin mostrar documento ni teléfono."""
        return f"Cliente {self.identificador}: {self.__nombre}"