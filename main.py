from ExpressionInterpreter import ExpressionInterpreter

if __name__ == '__main__':
    ei = ExpressionInterpreter()
    result = ei.compute("(10/2)*((6*(2/4))+2)")
    a = result
