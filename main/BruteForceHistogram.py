from symbols.Symbol import Symbol
from test.test_IdGenerator import check_id
from misc.config import wanted_length


if __name__ == '__main__':
    symbol_chars = list(Symbol.symbols_dict().keys())
    starting_symbols = Symbol.starting_symbols()
    ending_symbols = Symbol.ending_symbols()
    num = 0
    for start_symbol in starting_symbols:
        for symbol_char in symbol_chars:
            symbol = Symbol.parse(symbol_char, start_symbol)
            if symbol:
                for end_symbol in ending_symbols:
                    end_symbol = Symbol.parse(end_symbol.symbol(), symbol)
                    if end_symbol:
                        id = start_symbol.symbol() + symbol_char + end_symbol.symbol()
                        print(id)
                        num += 1
    print("")
    print(num)
