from classes.Symbol import Symbol
from classes.Id import Id
from misc.config import wanted_length

num = 0


def recursively_create_ids(i: int, symbols_to_check: list, symbols: list):
    global num
    for symbol in symbols_to_check:
        if Symbol.check(symbols[-1] if len(symbols) > 0 else None, symbol):
            symbols.append(symbol)
            if i + 1 == wanted_length:
                id = Id(symbols)
                if id.check() is None:
                    print(str(id))
                num += 1
            else:
                recursively_create_ids(i + 1, Symbol.symbols() if i + 2 < wanted_length else Symbol.ending_symbols(),
                                       symbols)
            symbols.pop()


if __name__ == '__main__':
    recursively_create_ids(0, Symbol.starting_symbols(), [])
    print("")
    print("Number of created ids: " + str(num))
