from expression_interpreter.ExpressionInterpreter import ExpressionInterpreter
from id_manager.IdGenerator import IdGenerator
from id_manager.IdMutator import IdMutator

if __name__ == '__main__':
    ei = ExpressionInterpreter()
    result = ei.compute("(-3)")
    x = 0
    r = IdGenerator.generate_id(12)
    print(r)
    print('')
    id_mutator = IdMutator()
    while x < 300:
        id, pos, c, new_c = id_mutator.mutate_id(r, len(r))
        print(id + '  pos_to_mutate=' + str(pos) + '(' + c + '), mutated_to=' + new_c)
        x += 1
