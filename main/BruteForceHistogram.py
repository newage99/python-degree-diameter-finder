from symbols.Symbol import Symbol
from misc.config import wanted_length


if __name__ == '__main__':
    symbols = list(Symbol.symbols_dict().keys())
    starting_symbols = Symbol.starting_symbols()
    ending_symbols = Symbol.ending_symbols()
    num = 0
    for start_symbol_char in starting_symbols:
        for symbol_char in symbols:
            symbol = Symbol.parse(symbol_char, start_symbol_char)
            if symbol:
                for end_symbol_char in ending_symbols:
                    end_symbol = Symbol.parse(end_symbol_char, symbol)
                    if end_symbol:
                        id = start_symbol_char + symbol_char + end_symbol_char
                        print(id)
                        num += 1
    print("")
    print(num)
