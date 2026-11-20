# Importa las herramientas de pruebas automáticas.
import unittest

# Importa las clases utilizadas en las reservas.
from cliente import Cliente
from servicios import ReservaSala, AsesoriaEspecializada
from reserva import Reserva

# Importa las excepciones esperadas.
from excepciones import (
    DatosInvalidosError,
    ReservaInvalidaError,
    OperacionNoPermitidaError,
    ServicioNoDisponibleError,
)


# Agrupa las pruebas de creación, procesamiento y cancelación.
class TestReservas(unittest.TestCase):
    """Comprueba estados, costos y disponibilidad de las reservas."""

    # Prepara objetos nuevos antes de cada prueba.
    def setUp(self):
        # Crea un cliente válido.
        self.cliente = Cliente(
            1,
            "Ana Pérez",
            "1020304050",
            "ana@ejemplo.com",
            "3001234567",
        )

        # Crea una sala disponible con tarifa de 50000 por hora.
        self.sala = ReservaSala(1, "Sala de reuniones", 50000)

        # Crea una reserva pendiente de dos horas.
        self.reserva = Reserva(1, self.cliente, self.sala, 2)

    # Comprueba las condiciones iniciales de una reserva.
    def test_estado_inicial(self):
        self.assertEqual(self.reserva.estado, "pendiente")
        self.assertIsNone(self.reserva.total)
        self.assertTrue(self.sala.disponible)

    # Comprueba cálculo, confirmación y ocupación del recurso.
    def test_procesar_reserva(self):
        self.reserva.procesar(impuesto=19, descuento=10)

        self.assertEqual(self.reserva.estado, "confirmada")
        self.assertAlmostEqual(
            self.reserva.total, 107100.00, places=2
        )
        self.assertFalse(self.sala.disponible)

    # Comprueba que cancelar una solicitud pendiente no ocupe la sala.
    def test_cancelar_reserva_pendiente(self):
        self.reserva.cancelar()

        self.assertEqual(self.reserva.estado, "cancelada")
        self.assertTrue(self.sala.disponible)

    # Comprueba que cancelar una reserva confirmada libere la sala.
    def test_cancelar_reserva_confirmada(self):
        self.reserva.procesar()
        self.reserva.cancelar()

        self.assertEqual(self.reserva.estado, "cancelada")
        self.assertTrue(self.sala.disponible)

    # Comprueba que una reserva no pueda cancelarse dos veces.
    def test_cancelar_dos_veces(self):
        self.reserva.cancelar()

        with self.assertRaises(OperacionNoPermitidaError):
            self.reserva.cancelar()

    # Comprueba el rechazo del procesamiento de reservas canceladas.
    def test_procesar_reserva_cancelada(self):
        self.reserva.cancelar()

        with self.assertRaises(ReservaInvalidaError):
            self.reserva.procesar()

        self.assertEqual(self.reserva.estado, "cancelada")
        self.assertTrue(self.sala.disponible)

    # Comprueba que no se confirme sin calcular antes el costo.
    def test_confirmar_sin_procesar(self):
        with self.assertRaises(OperacionNoPermitidaError):
            self.reserva.confirmar()

        self.assertEqual(self.reserva.estado, "pendiente")
        self.assertTrue(self.sala.disponible)

    # Comprueba que no se procese nuevamente una reserva confirmada.
    def test_procesar_dos_veces(self):
        self.reserva.procesar()

        with self.assertRaises(ReservaInvalidaError):
            self.reserva.procesar()

        self.assertEqual(self.reserva.estado, "confirmada")
        self.assertFalse(self.sala.disponible)

    # Comprueba el rechazo de otra reserva sobre un recurso ocupado.
    def test_servicio_ocupado(self):
        self.reserva.procesar()

        otra_reserva = Reserva(2, self.cliente, self.sala, 1)

        with self.assertRaises(ReservaInvalidaError) as contexto:
            otra_reserva.procesar()

        self.assertEqual(otra_reserva.estado, "pendiente")

        # Comprueba que se conserve la causa original del error.
        self.assertIsInstance(
            contexto.exception.__cause__,
            ServicioNoDisponibleError,
        )

    # Comprueba que una reserva pendiente funcione al liberarse la sala.
    def test_reservar_despues_de_liberar(self):
        self.reserva.procesar()

        otra_reserva = Reserva(2, self.cliente, self.sala, 1)

        with self.assertRaises(ReservaInvalidaError):
            otra_reserva.procesar()

        self.reserva.cancelar()
        otra_reserva.procesar()

        self.assertEqual(self.reserva.estado, "cancelada")
        self.assertEqual(otra_reserva.estado, "confirmada")
        self.assertAlmostEqual(
            otra_reserva.total, 50000.00, places=2
        )
        self.assertFalse(self.sala.disponible)

    # Comprueba que se exija un objeto Cliente válido.
    def test_cliente_invalido(self):
        with self.assertRaises(ReservaInvalidaError):
            Reserva(2, None, self.sala, 1)

    # Comprueba que se exija un objeto Servicio válido.
    def test_servicio_invalido(self):
        with self.assertRaises(ReservaInvalidaError):
            Reserva(2, self.cliente, None, 1)

    # Comprueba que una duración negativa sea rechazada al crear.
    def test_duracion_negativa(self):
        with self.assertRaises(DatosInvalidosError):
            Reserva(2, self.cliente, self.sala, -1)

    # Comprueba la duración mínima y el encadenamiento del error.
    def test_asesoria_corta_conserva_causa(self):
        asesoria = AsesoriaEspecializada(
            2, "Asesoría en Python", 80000
        )

        reserva = Reserva(2, self.cliente, asesoria, 0.5)

        with self.assertRaises(ReservaInvalidaError) as contexto:
            reserva.procesar()

        self.assertIsInstance(
            contexto.exception.__cause__,
            DatosInvalidosError,
        )
        self.assertEqual(reserva.estado, "pendiente")
        self.assertIsNone(reserva.total)
        self.assertTrue(asesoria.disponible)


# Ejecuta las pruebas mostrando el resultado de cada una.
if __name__ == "__main__":
    unittest.main(verbosity=2)