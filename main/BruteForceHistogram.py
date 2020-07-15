import math

from classes.Symbol import Symbol
from classes.Id import Id
from classes.AdjacencyMatrix import AdjacencyMatrix
from main.DegreeAndDiameterCalculator import DegreeAndDiameterCalculator
from misc.config import wanted_length, number_of_nodes

num = 0
results = {}


def recursively_create_ids(i: int, symbols_to_check: list, symbols: list):
    global num, results, test
    for symbol in symbols_to_check:
        if Symbol.check(symbols[-1] if len(symbols) > 0 else None, symbol):
            symbols.append(symbol)
            if i + 1 == wanted_length:
                id = Id(symbols)
                if id.check() is None:
                    # print(str(id))
                    adj_matrix = AdjacencyMatrix.parse(id)
                    if adj_matrix.is_connected():
                        score = DegreeAndDiameterCalculator.calculate(adj_matrix)
                        score = score[0] + score[1]
                    else:
                        score = ((number_of_nodes - 1) * 2) + (
                                    number_of_nodes - adj_matrix.get_number_of_elements_from_biggest_component())
                    for substring_len in range(1, len(id) + 1):
                        for j in range(len(id) - substring_len + 1):
                            chars = str(Id(symbols[j:j+substring_len]))
                            if chars in results:
                                results[chars][0] += 1
                                results[chars][1] += score
                            else:
                                results[chars] = [1, score]
                            # print(" " + str(Id(chars)))
                num += 1
            else:
                recursively_create_ids(i + 1, Symbol.symbols() if i + 2 < wanted_length else Symbol.ending_symbols(),
                                       symbols)
            symbols.pop()


if __name__ == '__main__':

    # from classes.numbers.variables.AxisY import AxisY
    # from classes.numbers.variables.AxisX import AxisX
    # from classes.interpretable_symbols.functions.operators.Subtraction import Subtraction
    # from classes.numbers.constants.Two import Two
    # score = DegreeAndDiameterCalculator.calculate(AdjacencyMatrix.parse(Id([AxisY(), Subtraction(), Two(), Subtraction(), AxisX()])))

    symbols = Symbol.symbols()
    num_symbols = len(symbols)
    n = int(math.pow(num_symbols, wanted_length))

    print("Number of iterations: " + str(n))

    chars = " " * wanted_length

    for i in range(n):
        if i % num_symbols == 0:
            pass

    recursively_create_ids(0, Symbol.starting_symbols(), [])
    print("")
    print("Number of created ids: " + str(num))
    ordered_results = []
    ordered_results_by_length = [[] for a in range(wanted_length)]
    for key in results:
        score = results[key][1] / results[key][0]
        result_pair = [key, score]
        not_inserted = True
        for i in range(len(ordered_results)):
            result = ordered_results[i]
            if score < result[1]:
                ordered_results.insert(i, result_pair)
                not_inserted = False
                break
        if not_inserted:
            ordered_results.append(result_pair)
        not_inserted = True
        pos = len(key) - 1
        for i in range(len(ordered_results_by_length[pos])):
            result = ordered_results_by_length[pos][i]
            if score < result[1]:
                ordered_results_by_length[pos].insert(i, result_pair)
                not_inserted = False
                break
        if not_inserted:
            ordered_results_by_length[pos].append(result_pair)

    for i in range(len(ordered_results) - 1, 0, -1):
        result = ordered_results[i]
        print(result[0] + ": " + str(result[1]))
        # for ordered_list in ordered_results_by_length:
        #     if i < len(ordered_list):
        #         print("| " + ordered_list[i][0] + ": " + str(ordered_list[i][1]), end=" ")
        # print("")
    for i in range(len(ordered_results_by_length)):
        print("")
        for j in range(len(ordered_results_by_length[i]) - 1, 0, -1):
            result = ordered_results_by_length[i][j]
            print(result[0] + ": " + str(result[1]))
