"""
Pablo Valencia A01700912
Compilers
Grammar Parser
Detecting terminals and non-terminals
March 19, 2023
"""
import re


def read_lines():
    """
    read_lines is a function that reads multiple lines of input from the user
    and stores them in a list. The first line is a number that determines the
    number of lines to read.

    :return: list where each element is a production.
    """
    lines = []
    lines_to_read = int(input())

    for _ in range(lines_to_read):
        production = input()
        lines.append(production)
    return lines


def get_symbols(grammar):
    """
    get_symbols receives a list of productions. The function determines which
    symbols are terminals and non_terminals.

    :param grammar: a list where each element is a production of the grammar.
    :return: a dictionary with two keys (terminals and non_terminals) each key
    stores a list of symbols.
    """

    # A graph is used to determine if a symbol is a terminal or a non-terminal
    symbols_graph = {}

    for production in grammar:
        production_list = production.split()
        non_terminal = production_list[0]
        for symbol in production_list[2:]:
            if symbol == "'":
                symbol = ' '

            if non_terminal in symbols_graph:
                symbols_graph[non_terminal].add(symbol)
            else:
                symbols_graph[non_terminal] = {symbol}

            if symbol != ' ' and symbol not in symbols_graph:
                symbols_graph[symbol] = set()

    terminals, non_terminals = [], []
    for symbol, productions in symbols_graph.items():
        # If a symbol is a leaf, then it is terminal
        if len(productions) == 0:
            terminals.append(symbol)
        else:
            # Using a regex to verify valid characters in a non-terminal
            if not re.match(r"^[a-zA-Z_-]+$", symbol):
                raise Exception('Error: invalid character found.')
            non_terminals.append(symbol)

    return {
        'terminals': terminals,
        'non_terminals': non_terminals
    }


def main():

    grammar = read_lines()
    symbols = get_symbols(grammar)
    print("Terminal: " + ", ".join(symbols['terminals']))
    print("Non terminal: " + ", ".join(symbols['non_terminals']))


if __name__ == '__main__':
    main()
