import unittest
from mathematical_expression_interpreter.MathematicalExpressionInterpreter import ExpressionInterpreter


class ExpressionInterpreterTest(unittest.TestCase):

    def test__process_negations(self):

        # TEST SUBTRACTION DOESN'T MODIFY THE EXPRESSION
        expr = "2-5-((4-3)-3)-88-(3-(543-((5-2)/3)-4)/3)-1"
        self.assertEqual(ExpressionInterpreter.process_negations(expr), expr)

        # NEGATION WHEN POS=0
        self.assertEqual(ExpressionInterpreter.process_negations("-2"), "0-2")
        self.assertEqual(ExpressionInterpreter.process_negations("-(1%1)"), "0-(1%1)")

        # NEGATION WHEN NEXT CHAR IS NUMBER
        self.assertEqual(ExpressionInterpreter.process_negations("2/-2"), "2/(0-2)")
        self.assertEqual(ExpressionInterpreter.process_negations("(1+9*-4%2)"), "(1+9*(0-4)%2)")
        self.assertEqual(ExpressionInterpreter.process_negations("(2+1)%-17-(3+2)"), "(2+1)%(0-17)-(3+2)")

        # NEGATION WHEN NEXT CHAR IS OPEN PARENTHESIS
        self.assertEqual(ExpressionInterpreter.process_negations("3+4*-(2%4)+3"), "3+4*(0-(2%4))+3")
        self.assertEqual(ExpressionInterpreter.process_negations("3L-((456-44)/3)+(24*7)"), "3L(0-((456-44)/3))+(24*7)")

    def test_compute(self):

        ei = ExpressionInterpreter()
        self.assertEqual(ei.compute("2^3-1"), 7)
        self.assertEqual(ei.compute("2L8"), 3)
        self.assertEqual(ei.compute("2-((5%2+1)^4-3)"), -11)


if __name__ == "__main__":
    unittest.main()
