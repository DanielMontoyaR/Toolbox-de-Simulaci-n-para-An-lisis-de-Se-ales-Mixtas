
import unittest
from tests.plant_tester import predefined_plant_tester as PredefinedTester
from tests.plant_tester import personalized_plant_tester as PersonalizedTester

class PlantTester:
    def run_all_tests(self, verbosity=2):
        loader = unittest.TestLoader()
        suite = unittest.TestSuite()

        suite.addTests(loader.loadTestsFromTestCase(PredefinedTester.PredefinedPlantTester))
        suite.addTests(loader.loadTestsFromTestCase(PersonalizedTester.PersonalizedPlantTester))

        runner = unittest.TextTestRunner(verbosity=verbosity)
        runner.run(suite)
