from ExpressionInterpreter import ExpressionInterpreter
from IdGenerator import IdGenerator
from IdMutator import IdMutator

if __name__ == '__main__':
    ei = ExpressionInterpreter()
    result = ei.compute("21^405")
    x = 0
    r = IdGenerator.generate_id(12)
    print(r)
    print('')
    id_mutator = IdMutator()
    while x < 300:
        id, pos, c, new_c = id_mutator.mutate_id(r, len(r))
        print(id + '  pos_to_mutate=' + str(pos) + '(' + c + '), mutated_to=' + new_c)
        x += 1
