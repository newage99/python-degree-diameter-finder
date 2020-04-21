from IdsManager import random_id, mutate_id
from global_variables import *

if __name__ == '__main__':

    ids_lengths = [3, 5, 10, 25, 100]
    number_of_mutation_per_id = 10
    ids_per_length = 4

    for length in ids_lengths:
        for i in range(1, ids_per_length + 1):
            id = random_id(length)
            print('Testing ' + str(number_of_mutation_per_id) + ' mutations on id #' + str(i) + ' (' + id + ') of length ' + str(length) + '...', end=" ")
            for i in range(number_of_mutation_per_id):
                mutated_id, pos, c, new_c = mutate_id(id)
                mutated_id_len = len(mutated_id)
                parenthesis_counter = 0
                for j in range(mutated_id_len):
                    if j > 0 and mutated_id[j-1] in forbidden_left_chars[mutated_id[j]]:
                        print('')
                        print(mutated_id)
                        print(('' * j) + '^  char ' + mutated_id[j] + ' must not be preceded by char ' + mutated_id[j-1])
                        exit(0)
                    elif j+1 < mutated_id_len and mutated_id[j+1] in forbidden_right_chars[mutated_id[j]]:
                        print('')
                        print(mutated_id)
                        print(('' * j) + '^  char ' + mutated_id[j] + ' must not be followed by char ' + mutated_id[j+1])
                        exit(0)
                if parenthesis_counter != 0:
                    print('')
                    print('Incorrect number of parenthesis.')
                    exit(0)
            print(' OK')