# Importa las herramientas de pruebas incluidas en Python.
import unittest

# Importa la clase que se evaluará.
from cliente import Cliente

# Importa la excepción esperada ante datos incorrectos.
from excepciones import DatosInvalidosError


# Agrupa las pruebas automáticas de clientes.
class TestCliente(unittest.TestCase):
    """Verifica registros válidos y rechazo de datos incorrectos."""

    # Prepara datos nuevos antes de cada prueba.
    def setUp(self):
        self.datos = {
            "identificador": 1,
            "nombre": "Ana Pérez",
            "documento": "1020304050",
            "correo": "ana@ejemplo.com",
            "telefono": "3001234567",
        }

    # Comprueba la creación y consulta de un cliente válido.
    def test_cliente_valido(self):
        cliente = Cliente(**self.datos)

        self.assertEqual(cliente.identificador, 1)
        self.assertEqual(cliente.nombre, "Ana Pérez")
        self.assertEqual(cliente.documento, "1020304050")
        self.assertEqual(cliente.correo, "ana@ejemplo.com")
        self.assertEqual(cliente.telefono, "3001234567")

    # Comprueba que se eliminen los espacios externos del nombre.
    def test_nombre_con_espacios_externos(self):
        self.datos["nombre"] = "  Ana Pérez  "

        cliente = Cliente(**self.datos)

        self.assertEqual(cliente.nombre, "Ana Pérez")

    # Comprueba que un nombre vacío sea rechazado.
    def test_nombre_vacio(self):
        self.datos["nombre"] = "   "

        with self.assertRaises(DatosInvalidosError):
            Cliente(**self.datos)

    # Comprueba que el documento no admita letras.
    def test_documento_con_letras(self):
        self.datos["documento"] = "123ABC"

        with self.assertRaises(DatosInvalidosError):
            Cliente(**self.datos)

    # Comprueba que un correo sin formato válido sea rechazado.
    def test_correo_invalido(self):
        self.datos["correo"] = "correo_invalido"

        with self.assertRaises(DatosInvalidosError):
            Cliente(**self.datos)

    # Comprueba que un teléfono demasiado corto sea rechazado.
    def test_telefono_corto(self):
        self.datos["telefono"] = "123"

        with self.assertRaises(DatosInvalidosError):
            Cliente(**self.datos)

    # Comprueba la validación del identificador heredada de Entidad.
    def test_identificador_negativo(self):
        self.datos["identificador"] = -1

        with self.assertRaises(DatosInvalidosError):
            Cliente(**self.datos)

    # Comprueba que un booleano no sea aceptado como identificador.
    def test_identificador_booleano(self):
        self.datos["identificador"] = True

        with self.assertRaises(DatosInvalidosError):
            Cliente(**self.datos)

    # Comprueba que los datos requeridos no puedan omitirse.
    def test_parametros_faltantes(self):
        with self.assertRaises(TypeError):
            Cliente(1, "Ana Pérez")

    # Comprueba que el nombre no admita asignación directa.
    def test_nombre_sin_asignacion_directa(self):
        cliente = Cliente(**self.datos)

        with self.assertRaises(AttributeError):
            cliente.nombre = "Otro nombre"


# Ejecuta las pruebas y muestra sus nombres y resultados.
if __name__ == "__main__":
    unittest.main(verbosity=2)