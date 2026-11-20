# Importa las herramientas de pruebas automáticas.
import unittest

# Importa los servicios que se evaluarán.
from servicios import (
    Servicio,
    ReservaSala,
    AlquilerEquipo,
    AsesoriaEspecializada,
)

# Importa las excepciones esperadas.
from excepciones import (
    DatosInvalidosError,
    ServicioNoDisponibleError,
)


# Agrupa las pruebas de los servicios.
class TestServicios(unittest.TestCase):
    """Comprueba cálculos, validaciones y disponibilidad."""

    # Crea objetos independientes antes de cada prueba.
    def setUp(self):
        self.sala = ReservaSala(1, "Sala de reuniones", 50000)
        self.equipo = AlquilerEquipo(2, "Video proyector", 20000)
        self.asesoria = AsesoriaEspecializada(
            3, "Asesoría en Python", 80000
        )

    # Comprueba el costo básico de una sala durante dos horas.
    def test_costo_sala(self):
        total = self.sala.calcular_costo(2)

        self.assertAlmostEqual(total, 100000.00, places=2)

    # Comprueba descuento del 10 % e impuesto del 19 %.
    def test_sala_con_impuesto_y_descuento(self):
        total = self.sala.calcular_costo(
            2, impuesto=19, descuento=10
        )

        self.assertAlmostEqual(total, 107100.00, places=2)

    # Comprueba el alquiler sin seguro.
    def test_equipo_sin_seguro(self):
        total = self.equipo.calcular_costo(2)

        self.assertAlmostEqual(total, 40000.00, places=2)

    # Comprueba el recargo fijo del seguro.
    def test_equipo_con_seguro(self):
        total = self.equipo.calcular_costo(2, seguro=True)

        self.assertAlmostEqual(total, 50000.00, places=2)

    # Comprueba el seguro junto con impuesto y descuento.
    def test_equipo_con_seguro_impuesto_y_descuento(self):
        total = self.equipo.calcular_costo(
            2, impuesto=19, descuento=10, seguro=True
        )

        self.assertAlmostEqual(total, 53550.00, places=2)

    # Comprueba una asesoría que cumple la duración mínima.
    def test_asesoria_valida(self):
        total = self.asesoria.calcular_costo(1)

        self.assertAlmostEqual(total, 80000.00, places=2)

    # Comprueba el rechazo de asesorías inferiores a una hora.
    def test_asesoria_demasiado_corta(self):
        with self.assertRaises(DatosInvalidosError):
            self.asesoria.calcular_costo(0.5)

    # Comprueba el rechazo de tarifas negativas.
    def test_tarifa_negativa(self):
        with self.assertRaises(DatosInvalidosError):
            ReservaSala(4, "Sala inválida", -5000)

    # Comprueba el rechazo de una duración igual a cero.
    def test_duracion_cero(self):
        with self.assertRaises(DatosInvalidosError):
            self.sala.calcular_costo(0)

    # Comprueba el rechazo de descuentos superiores al límite.
    def test_descuento_fuera_de_rango(self):
        with self.assertRaises(DatosInvalidosError):
            self.sala.calcular_costo(2, descuento=120)

    # Comprueba el rechazo de impuestos negativos.
    def test_impuesto_negativo(self):
        with self.assertRaises(DatosInvalidosError):
            self.sala.calcular_costo(2, impuesto=-1)

    # Comprueba que no se admitan cantidades infinitas.
    def test_duracion_infinita(self):
        with self.assertRaises(DatosInvalidosError):
            self.sala.calcular_costo(float("inf"))

    # Comprueba que el seguro requiera un valor booleano.
    def test_seguro_invalido(self):
        with self.assertRaises(DatosInvalidosError):
            self.equipo.calcular_costo(2, seguro="si")

    # Comprueba los cambios de disponibilidad del recurso.
    def test_ocupar_y_liberar(self):
        self.assertTrue(self.sala.disponible)

        self.sala.ocupar()
        self.assertFalse(self.sala.disponible)

        self.sala.liberar()
        self.assertTrue(self.sala.disponible)

    # Comprueba que un recurso ocupado no pueda ocuparse nuevamente.
    def test_ocupar_servicio_ya_ocupado(self):
        self.sala.ocupar()

        with self.assertRaises(ServicioNoDisponibleError):
            self.sala.ocupar()

    # Comprueba que Servicio siga siendo una clase abstracta.
    def test_servicio_abstracto(self):
        with self.assertRaises(TypeError):
            Servicio(4, "Servicio genérico", 10000)


# Ejecuta las pruebas y muestra el resultado de cada una.
if __name__ == "__main__":
    unittest.main(verbosity=2)