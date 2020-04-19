from ExpressionInterpreter import ExpressionInterpreter
from IdsManager import random_id

if __name__ == '__main__':
    ei = ExpressionInterpreter()
    result = ei.compute("21^405")
    x = 0
    while x < 20:
        print(random_id(9))
        x += 1
