import unittest
from main.ExpressionInterpreter import ExpressionInterpreter


class ExpressionInterpreterTest(unittest.TestCase):

    def test_compute(self):

        compute = ExpressionInterpreter.compute

        # OPERATOR TESTS
        self.assertEqual(compute("1+1"), 2)
        self.assertEqual(compute("1-1"), 0)
        self.assertEqual(compute("2*7"), 14)
        self.assertEqual(compute("6/2"), 3)
        self.assertEqual(compute("4%2"), 0)

        # FUNCTION TESTS
        self.assertEqual(compute("-3"), -3)
        self.assertEqual(compute("-(5)"), -5)


if __name__ == "__main__":
    unittest.main()
