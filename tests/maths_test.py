import unittest
# import our `pybind11`-based extension module from package MonteCarlo
from MonteCarlo import MonteCarlo


class MainTest(unittest.TestCase):
    def test_add(self):
        # test that 1 + 1 = 2
        self.assertEqual(MonteCarlo.add(1, 1), 2)

    def test_subtract(self):
        # test that 1 - 1 = 0
        self.assertEqual(MonteCarlo.subtract(1, 1), 0)

    # TODO this test fails
    # def test_hello_world(self):
    #    # test that you python functions to
    #    self.assertEqual(MonteCarlo.hello_world(), "Hello, World!")


if __name__ == '__main__':
    unittest.main()
