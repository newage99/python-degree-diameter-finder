from classes.Symbol import Symbol
from classes.Id import Id
from classes.AdjacencyMatrix import AdjacencyMatrix
from main.DegreeAndDiameterCalculator import DegreeAndDiameterCalculator
from math import pow
from misc.config import wanted_length, number_of_nodes
from time import time

num = 0
results = {}


def recursively_create_ids(i: int, symbols_to_check: list, symbols: list):
    global num, results
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


def compute_id_results(id: Id):
    adj_matrix = AdjacencyMatrix.parse(id)
    if adj_matrix.is_connected():
        score = DegreeAndDiameterCalculator.calculate(adj_matrix)
        score = score[0] + score[1]
    else:
        score = ((number_of_nodes - 1) * 2) + (
                number_of_nodes - adj_matrix.get_number_of_elements_from_biggest_component())
    for substring_len in range(1, len(id) + 1):
        for j in range(len(id) - substring_len + 1):
            chars = str(Id(symbols[j:j + substring_len]))
            if chars in results:
                results[chars][0] += 1
                results[chars][1] += score
            else:
                results[chars] = [1, score]


def order_results(results):
    ordered_results = []
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
    return ordered_results


if __name__ == '__main__':

    # from classes.numbers.variables.AxisY import AxisY
    # from classes.numbers.variables.AxisX import AxisX
    # from classes.interpretable_symbols.functions.operators.Subtraction import Subtraction
    # from classes.numbers.constants.Two import Two
    # adjacency_matrix = AdjacencyMatrix.parse(Id([AxisY(), Subtraction(), Two(), Subtraction(), AxisX()]))
    # score = DegreeAndDiameterCalculator.calculate(adjacency_matrix)

    all_symbols = Symbol.symbols()
    num_symbols = len(all_symbols)
    symbols = [None for s in range(wanted_length)]
    n = int(pow(num_symbols, wanted_length))
    pows = [pow(num_symbols, wanted_length - i) for i in range(wanted_length + 1)]
    c = 0

    start = time()

    for i in range(n):
        symbols[0] = all_symbols[int((i % n) / pows[1])]
        char = str(symbols[0])
        parenthesis_counter = 1 if char == "(" else (-1 if char == ")" else 0)
        if symbols[0].starting_symbol and parenthesis_counter >= 0:
            for j in range(1, wanted_length - 1):
                if i % pows[j + 1] == 0:
                    symbols[j] = all_symbols[int((i % pows[j]) / pows[j + 1])]
            symbols[-1] = all_symbols[int(i % pows[-2])]
            if symbols[-1].ending_symbol:
                valid = True
                for j in range(1, wanted_length):
                    char = str(symbols[j])
                    parenthesis_counter = parenthesis_counter + (1 if char == "(" else (-1 if char == ")" else 0))
                    if not Symbol.check(symbols[j-1], symbols[j]) or parenthesis_counter < 0:
                        valid = False
                        break
                if valid and parenthesis_counter == 0:
                    id = Id(symbols)
                    compute_id_results(id)
                    # print(str(id))
                    c += 1

    midpoint = time()
    print("Ids creation time elapsed: " + str(midpoint - start) + " seconds")

    ordered_results = order_results(results)

    end = time()
    print("Results list ordering time elapsed: " + str(end - midpoint) + " seconds")

    # print("")
    # for i in range(len(ordered_results) - 1, 0, -1):
    #     print(ordered_results[i][0] + ": " + str(ordered_results[i][1]))
    # print("")

    print("Number of iterations: " + str(n))
    print("Number of created ids: " + str(c))
    print("Ordered results len: " + str(len(ordered_results)))




















def old():
    recursively_create_ids(0, Symbol.starting_symbols(), [])
    print("")
    print("Number of created ids: " + str(num))
    ordered_results_by_length = [[] for a in range(wanted_length)]
    ordered_results = []
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
    for i in range(len(ordered_results_by_length)):
        print("")
        for j in range(len(ordered_results_by_length[i]) - 1, 0, -1):
            result = ordered_results_by_length[i][j]
            print(result[0] + ": " + str(result[1]))