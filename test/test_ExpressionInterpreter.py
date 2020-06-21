import unittest
from main.ExpressionInterpreter import ExpressionInterpreter


class ExpressionInterpreterTest(unittest.TestCase):

    def test_compute(self):

        compute = ExpressionInterpreter.compute

        # Addition
        self.assertEqual(compute("1+1"), 2)
        self.assertEqual(compute("100+(100+34)"), 234)
        self.assertEqual(compute("(3+14)+(3+4)"), 24)
        self.assertEqual(compute("1+2+(3+4+(5+(6+7)+8))+9"), 45)

        # Subtraction
        self.assertEqual(compute("1-2"), -1)
        self.assertEqual(compute("100-(100-20)"), 20)
        self.assertEqual(compute("(30-1)-(3-4)"), 30)
        self.assertEqual(compute("1-2-(3-4-(5-(6-7)-8))-9"), -11)

        # Negation
        self.assertEqual(compute("-17"), -17)
        self.assertEqual(compute("4/-2"), -2)

        # Mix
        self.assertEqual(compute("-13+(-(4+5-7))"), -15)


if __name__ == "__main__":
    unittest.main()
