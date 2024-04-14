import unittest

from turbobus.constants import Provider


class SimulatedCommand:
            pass

class SimulatedHandler:
    pass

# Set up some sample providers for testing
Provider.set(SimulatedCommand, SimulatedHandler)
Provider.set(int, "Integer provider")


class TestProvider(unittest.TestCase):

    def test_set(self):
        Provider.set(float, "Float provider")
        self.assertEqual(Provider._providers[float.__name__], "Float provider")

    def test_get_existing_provider(self):
        Provider.set(str.__name__, "String provider")

        result = Provider.get(str.__name__)
        self.assertEqual(result, "String provider")

    def test_get_nonexistent_provider(self):
        result = Provider.get("nonexistent")
        self.assertIsNone(result)

    def test_get_non_string_key(self):
        result = Provider.set(int, "Integer provider")
        result = Provider.get(int)
        self.assertEqual(result, "Integer provider")
