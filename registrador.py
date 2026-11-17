# Importa las herramientas para registrar eventos y errores.
import logging

# Importa una herramienta para construir rutas de archivos.
from pathlib import Path


# Obtiene la carpeta donde está guardado este archivo.
CARPETA_PROYECTO = Path(__file__).resolve().parent

# Define la ubicación del archivo que almacenará los registros.
ARCHIVO_LOG = CARPETA_PROYECTO / "sistema.log"

# Crea un registrador identificado con el nombre del proyecto.
logger = logging.getLogger("software_fj")

# Permite registrar eventos informativos y errores.
logger.setLevel(logging.INFO)

# Evita enviar los mismos mensajes a otros registradores.
logger.propagate = False

# Evita agregar varias veces el mismo manejador de archivo.
if not logger.handlers:
    # Abre el archivo para agregar registros sin borrar los anteriores.
    manejador = logging.FileHandler(
        ARCHIVO_LOG,
        mode="a",
        encoding="utf-8"
    )

    # Define cómo se verá cada registro.
    formato = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s"
    )

    # Aplica el formato al manejador del archivo.
    manejador.setFormatter(formato)

    # Conecta el archivo con el registrador.
    logger.addHandler(manejador)


# Define cómo registrar una operación normal.
def registrar_evento(mensaje):
    """Guarda un evento informativo en sistema.log."""
    logger.info(mensaje)


# Define cómo registrar un error.
def registrar_error(mensaje):
    """Guarda un error y, si está siendo manejado, su detalle técnico."""
    logger.error(mensaje, exc_info=True)