"""
Pablo Valencia A01700912
Compilers
Grammar Parser
Detecting terminals and non-terminals
March 19, 2023
"""

import sys
import re


def read_lines(file_path):
    """
    read_lines open the file in file_path and reads the first line. The first
    line is converted to an integer and determines the number of lines to read
    below. Each line is added to a list.

    :param file_path: the relative or absolute path of the file to read.
    :return: a list where each element is a line of the file.
    """
    lines = []
    with open(file_path, 'r') as f:
        num_lines = int(f.readline())
        for _ in range(num_lines):
            lines.append(f.readline())
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

    # The program must receive the path of the file to read as an arg
    if len(sys.argv) != 2:
        print(f'Usage: {sys.argv[0]} <input file>')
        exit(1)

    file_path = sys.argv[1]

    try:
        grammar = read_lines(file_path)
    except FileNotFoundError:
        print(f'Error: File {file_path} not found')
        exit(2)
    except Exception as e:
        print(f'Error: {e}')
        exit(3)

    symbols = get_symbols(grammar)
    print("Terminal: " + ", ".join(symbols['terminals']))
    print("Non terminal: " + ", ".join(symbols['non_terminals']))


if __name__ == '__main__':
    main()
