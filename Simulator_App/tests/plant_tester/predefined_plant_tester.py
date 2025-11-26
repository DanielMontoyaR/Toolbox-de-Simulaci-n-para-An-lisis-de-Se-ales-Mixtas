from unittest import TestCase
from simulation_components.plant import get_plant
import control as ctrl

class PredefinedPlantTester(TestCase):

    def setUp(self):
        # Initialize predefined plants for testing
        self.plants = {
            "Ball and Beam": get_plant("Ball and Beam"),
            "DC Motor Speed Control": get_plant("DC Motor Speed Control"),
            "DC Motor Position Control": get_plant("DC Motor Position Control"),
        }
        self.plants["Ball and Beam"].set_parameters(m=1.0, R=0.05, d=0.5, g=-9.81, L=1.0, J=0.02)
        self.plants["DC Motor Speed Control"].set_parameters(J=0.01, b=0.1, K=0.01, R=1.0, L=0.5)
        self.plants["DC Motor Position Control"].set_parameters(J=0.02, b=0.2, K=0.02, R=2.0, L=1.0)


    # Ball and Beam Tests

    def test_ball_and_beam_plant_initialization(self):
        self.assertEqual(self.plants["Ball and Beam"].get_parameters()['m'], 1.0)
        self.assertEqual(self.plants["Ball and Beam"].get_parameters()['R'], 0.05)
        self.assertEqual(self.plants["Ball and Beam"].get_parameters()['d'], 0.5)
        self.assertEqual(self.plants["Ball and Beam"].get_parameters()['g'], -9.81)
        self.assertEqual(self.plants["Ball and Beam"].get_parameters()['L'], 1.0)
        self.assertEqual(self.plants["Ball and Beam"].get_parameters()['J'], 0.02)

    
    def test_ball_and_beam_transfer_function(self):
        tf = self.plants["Ball and Beam"].get_transfer_function()
        self.assertIsInstance(tf, ctrl.TransferFunction)
        
    def test_ball_and_beam_invalid_mass(self):
        self.plants["Ball and Beam"].set_parameters(m=-1.0)
        tf = self.plants["Ball and Beam"].get_transfer_function()
        self.assertIsInstance(tf, str)
        self.assertIn("Mass m must be positive", tf)

    def test_ball_and_beam_invalid_radius(self):
        #print("Testing Ball and Beam invalid radius...")
        self.plants["Ball and Beam"].set_parameters(R=-0.05)
        tf = self.plants["Ball and Beam"].get_transfer_function()
        self.assertIsInstance(tf, str)
        self.assertIn("Radius R must be positive", tf)

    def test_ball_and_beam_invalid_length(self):
        #print("Testing Ball and Beam invalid length...")
        self.plants["Ball and Beam"].set_parameters(L=-1.0)
        tf = self.plants["Ball and Beam"].get_transfer_function()
        self.assertIsInstance(tf, str)
        self.assertIn("Length L must be positive", tf)

    def test_ball_and_beam_invalid_gravity(self):
        #print("Testing Ball and Beam invalid gravity...")
        self.plants["Ball and Beam"].set_parameters(g=9.81)
        tf = self.plants["Ball and Beam"].get_transfer_function()
        self.assertIsInstance(tf, str)
        self.assertIn("Gravity g must be negative", tf)

    def test_ball_and_beam_invalid_distance(self):
        #print("Testing Ball and Beam invalid distance...")
        self.plants["Ball and Beam"].set_parameters(d=-0.5)
        tf = self.plants["Ball and Beam"].get_transfer_function()
        self.assertIsInstance(tf, str)
        self.assertIn("Distance d must be positive", tf)

    def test_ball_and_beam_invalid_inertia(self):
        #print("Testing Ball and Beam invalid inertia...")
        self.plants["Ball and Beam"].set_parameters(J=-0.02)
        tf = self.plants["Ball and Beam"].get_transfer_function()
        self.assertIsInstance(tf, str)
        self.assertIn("Moment of inertia J must be non-negative", tf)



    # DC Motor Speed Control Tests


    def test_dc_motor_speed_control_plant_initialization(self):
        self.assertEqual(self.plants["DC Motor Speed Control"].get_parameters()['J'], 0.01)
        self.assertEqual(self.plants["DC Motor Speed Control"].get_parameters()['b'], 0.1)
        self.assertEqual(self.plants["DC Motor Speed Control"].get_parameters()['K'], 0.01)
        self.assertEqual(self.plants["DC Motor Speed Control"].get_parameters()['R'], 1.0)
        self.assertEqual(self.plants["DC Motor Speed Control"].get_parameters()['L'], 0.5)

    def test_dc_motor_speed_control_transfer_function(self):
        tf = self.plants["DC Motor Speed Control"].get_transfer_function()
        self.assertIsInstance(tf, ctrl.TransferFunction)
    

    def test_dc_motor_speed_control_inertia(self):
        #print("Testing DC Motor Speed Control invalid inertia...")
        self.plants["DC Motor Speed Control"].set_parameters(J=-0.01)
        tf = self.plants["DC Motor Speed Control"].get_transfer_function()
        self.assertIsInstance(tf, str)
        self.assertIn("Moment of inertia J must be positive", tf)
    

    def test_dc_motor_speed_control_friction(self):
        #print("Testing DC Motor Speed Control invalid friction...")
        self.plants["DC Motor Speed Control"].set_parameters(b=-0.1)
        tf = self.plants["DC Motor Speed Control"].get_transfer_function()
        self.assertIsInstance(tf, str)
        self.assertIn("Motor viscous friction constant b must be non-negative", tf)

    def test_dc_motor_speed_control_electromotive_force(self):
        #print("Testing DC Motor Speed Control invalid electromotive force constant...")
        self.plants["DC Motor Speed Control"].set_parameters(K=-0.01)
        tf = self.plants["DC Motor Speed Control"].get_transfer_function()
        self.assertIsInstance(tf, str)
        self.assertIn("Electromotive force constant K must be non-negative", tf)

    def test_dc_motor_speed_control_resistance(self):
        #print("Testing DC Motor Speed Control invalid resistance...")
        self.plants["DC Motor Speed Control"].set_parameters(R=-1.0)
        tf = self.plants["DC Motor Speed Control"].get_transfer_function()
        self.assertIsInstance(tf, str)
        self.assertIn("Electric resistance R must be non-negative", tf)

    def test_dc_motor_speed_control_inductance(self):
        #print("Testing DC Motor Speed Control invalid inductance...")
        self.plants["DC Motor Speed Control"].set_parameters(L=-0.5)
        tf = self.plants["DC Motor Speed Control"].get_transfer_function()
        self.assertIsInstance(tf, str)
        self.assertIn("Electric inductance L must be non-negative", tf)




    # DC Motor Position Control Tests

    def test_dc_motor_position_control_plant_initialization(self):
        self.assertEqual(self.plants["DC Motor Position Control"].get_parameters()['J'], 0.02)
        self.assertEqual(self.plants["DC Motor Position Control"].get_parameters()['b'], 0.2)
        self.assertEqual(self.plants["DC Motor Position Control"].get_parameters()['K'], 0.02)
        self.assertEqual(self.plants["DC Motor Position Control"].get_parameters()['R'], 2.0)
        self.assertEqual(self.plants["DC Motor Position Control"].get_parameters()['L'], 1.0)

    def test_dc_motor_position_control_transfer_function(self):
        tf = self.plants["DC Motor Position Control"].get_transfer_function()
        self.assertIsInstance(tf, ctrl.TransferFunction)

    def test_dc_motor_position_control_inertia(self):
        #print("Testing DC Motor Position Control invalid inertia...")
        self.plants["DC Motor Position Control"].set_parameters(J=-0.02)
        tf = self.plants["DC Motor Position Control"].get_transfer_function()
        self.assertIsInstance(tf, str)
        self.assertIn("Moment of inertia J must be positive", tf)

    def test_dc_motor_position_control_friction(self):
        #print("Testing DC Motor Position Control invalid friction...")
        self.plants["DC Motor Position Control"].set_parameters(b=-0.2)
        tf = self.plants["DC Motor Position Control"].get_transfer_function()
        self.assertIsInstance(tf, str)
        self.assertIn("Motor viscous friction constant b must be non-negative", tf)

    def test_dc_motor_position_control_electromotive_force(self):
        #print("Testing DC Motor Position Control invalid electromotive force constant...")
        self.plants["DC Motor Position Control"].set_parameters(K=-0.02)
        tf = self.plants["DC Motor Position Control"].get_transfer_function()
        self.assertIsInstance(tf, str)
        self.assertIn("Electromotive force constant K must be non-negative", tf)

    def test_dc_motor_position_control_resistance(self):
        #print("Testing DC Motor Position Control invalid resistance...")
        self.plants["DC Motor Position Control"].set_parameters(R=-2.0)
        tf = self.plants["DC Motor Position Control"].get_transfer_function()
        self.assertIsInstance(tf, str)
        self.assertIn("Electric resistance R must be non-negative", tf)

    def test_dc_motor_position_control_inductance(self):
        #print("Testing DC Motor Position Control invalid inductance...")
        self.plants["DC Motor Position Control"].set_parameters(L=-1.0)
        tf = self.plants["DC Motor Position Control"].get_transfer_function()
        self.assertIsInstance(tf, str)
        self.assertIn("Electric inductance L must be non-negative", tf)



