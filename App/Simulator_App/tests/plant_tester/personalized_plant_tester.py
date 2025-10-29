from unittest import TestCase
from simulation_components.plant import get_plant

class PersonalizedPlantTester(TestCase):

    def setUp(self):
        # Initialize predefined plants for testing
        self.plant = get_plant("Personalized Plant")
        self.plant.set_parameters(Numerator=(1.0,3.0,4.0), Denominator=(1.0,5.0))  # Example parameters s^2 + 3s + 4 / s + 5

    def test_plant_initialization(self):
        self.assertEqual(self.plant.get_parameters()['Numerator'], (1.0,3.0,4.0))
        self.assertEqual(self.plant.get_parameters()['Denominator'], (1.0,5.0))

    def test_plant_transfer_function(self):
        tf = self.plant.get_transfer_function()
        self.assertIsInstance(tf, object)  # Assuming the transfer function is returned as an object

    def test_plant_invalid_denominator(self): # Denominator cannot be zero
        self.plant.set_parameters(Denominator=(0.0))
        tf = self.plant.get_transfer_function()
        self.assertIsInstance(tf, str)
        self.assertIn("Denominator cannot be all zeros", tf)
