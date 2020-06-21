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

        # Multiplication
        self.assertEqual(compute("1*1"), 1)
        self.assertEqual(compute("2*(3*4)"), 24)
        self.assertEqual(compute("(3*4)*2"), 24)

        # Division
        self.assertEqual(compute("1/2"), 0.5)
        self.assertEqual(compute("4/(1/2)"), 8)
        """
        Any number divided by zero in the expression will automatically return 0 as result.
        """
        self.assertEqual(compute("2/(5/0)"), 0)
        self.assertEqual(compute("((1/(1/1)/1/1)/1)/2/1/2"), 0.25)

        # Modulus
        self.assertEqual(compute("1%3"), 1)
        self.assertEqual(compute("5%2%(7)"), 1)
        self.assertEqual(compute("-3%8%3"), 2)

        # Exponential
        self.assertEqual(compute("2^3"), 8)
        self.assertEqual(compute("4^(1/2)"), 2)
        self.assertEqual(compute("10^6"), 1000000)

        # Logarithm
        self.assertEqual(compute("2L2"), 1)
        self.assertEqual(compute("2L16L2"), 0.5)
        """
        Any value or base of a logarithm equal to zero in the expression will automatically return 0 as result.
        """
        self.assertEqual(compute("3L0"), 0)
        self.assertEqual(compute("(0L4)+1"), 0)

        # Negation
        self.assertEqual(compute("-17"), -17)
        self.assertEqual(compute("4/-2"), -2)
        self.assertEqual(compute("2*-(-(-2))"), -4)
        self.assertEqual(compute("-((3%-2))"), 1)

        # Mix
        self.assertEqual(compute("-13+(-(4+5-7))"), -15)
        self.assertEqual(compute("-(4*-1+((2^-3)%2)/(1/4))*2"), 31)


if __name__ == "__main__":
    unittest.main()
