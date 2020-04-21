from ExpressionInterpreter import ExpressionInterpreter
from IdsManager import random_id, mutate_id

if __name__ == '__main__':
    ei = ExpressionInterpreter()
    result = ei.compute("21^405")
    x = 0
    r = random_id(12)
    print(r)
    print('')
    while x < 300:
        id, pos, c, new_c = mutate_id(r)
        print(id + '  pos_to_mutate=' + str(pos) + '(' + c + '), mutated_to=' + new_c)
        x += 1
