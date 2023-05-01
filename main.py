"""
Pablo Valencia A01700912
Compilers
Grammar Parser
Detecting terminals and non-terminals
Creating first and follow sets
April 30, 2023
"""


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
                symbols_graph[non_terminal].append(symbol)
            else:
                symbols_graph[non_terminal] = [symbol]

            if symbol != ' ' and symbol not in symbols_graph:
                symbols_graph[symbol] = []

    terminals, non_terminals = [], []
    for symbol, productions in symbols_graph.items():
        # If a symbol is a leaf, then it is terminal
        if len(productions) == 0:
            terminals.append(symbol)
        else:
            non_terminals.append(symbol)

    return {
        'graph': symbols_graph,
        'terminals': set(terminals),
        'non_terminals': set(non_terminals)
    }


def get_first(current, grammar, firsts, non_terminals, visited):
    """
    get_first receives a symbol of a grammar and returns the set that contains
    the possible first terminals.
    :param current: the symbol used to obtain the first set.
    :param grammar: a dictionary where the keys are non-terminals and the values
     are arrays containing the productions of the non-terminals.
    :param firsts: a dictionary where the keys are non-terminals and the values
    are the corresponding first sets.
    :param non_terminals: a set containing all non-terminals in the grammar.
    :return: A set that contains the firsts of the current symbol.
    """
    # If it is terminal symbol
    if current not in non_terminals:
        return {current}

    # If this first of current is already calculated
    if current in firsts:
        return firsts[current]

    for i, production in enumerate(grammar[current]):
        complete_production = f'{current} -> {" ".join(production)}'
        if complete_production in visited:
            continue

        visited.add(complete_production)
        current_first = get_first(production[0], grammar, firsts,
                                  non_terminals, visited)
        # If the current first has epsilon, repeat the process with the next
        # symbol
        if ' ' in current_first:
            i = 1
            while i < len(production):
                next_symbol = get_first(production[i], grammar,
                                        firsts, non_terminals, visited)
                current_first = current_first.union(next_symbol)
                if ' ' not in next_symbol:
                    break
                i += 1

        if current not in firsts:
            firsts[current] = set()
        firsts[current] = firsts[current].union(current_first)
    return firsts[current]


def get_follow(current, grammar, follows, firsts, non_terminals):
    """
    get_follow receives a symbol of a grammar and returns the set that contains
    all the possible follow terminals.
    :param current: the symbol used to obtain the follow set.
    :param grammar: a dictionary where the keys are non-terminals and the values
    are arrays containing the productions of the non-terminals.
    :param follows: a dictionary where the keys are non-terminals and the values
    are the corresponding follow sets.
    :param firsts: a dictionary where the keys are non-terminals and the values
    are the corresponding first sets.
    :param non_terminals: a set containing all non-terminals in the grammar.
    :return: a set that contains the follows of the current symbol.
    """
    for production in grammar:
        production_list = production.split()
        non_terminal = production_list[0]

        # Get the idx of the current symbol everytime it appears in a production
        current_idx = [i + 2 for i, symbol in enumerate(production_list[2:])
                       if symbol == current]
        for idx in current_idx:
            # If the current idx is the last symbol
            if idx == len(production_list) - 1:
                if non_terminal == production_list[idx]:
                    continue
                # Recursively get the follow of the current non-terminal
                follows[current] = follows[current].union(follows[non_terminal])
            # If it is a terminal we add it to the set
            elif production_list[idx + 1] not in non_terminals:
                follows[current].add(production_list[idx + 1])
            # If it is not that last symbol of the production we get the first
            else:
                follows[current] = follows[current].union(
                    firsts[production_list[idx + 1]])
                # If the first has epsilon repeat the process with the next
                # symbol
                if ' ' in follows[current]:
                    i = idx + 1
                    while ' ' in follows[current]:
                        follows[current].remove(' ')
                        if i == len(production_list) - 1:
                            follows[current] = follows[current].union(
                                follows[non_terminal])
                            break
                        if production_list[idx] not in non_terminals:
                            follows[current].add(production_list[i])
                            break
                        follows[current] = follows[current].union(
                            firsts[production_list[i]])
                        i += 1


def process_grammar(grammar):
    """
    process_grammar receives a list of strings, where each string is a
    production, and returns a dictionary.
    :param grammar: a list where each element is a string that represents a
    production.
    :return: a dictionary where the keys are non-terminals and the values are
    arrays of arrays. Each array is a production of the non-terminal.
    """
    processed_grammar = {}
    for production in grammar:
        production_list = production.split()
        non_terminal = production_list[0]

        if non_terminal not in processed_grammar:
            processed_grammar[non_terminal] = []

        current_production = []
        for symbol in production_list[2:]:
            if symbol == "'":
                symbol = ' '

            if symbol == ' ' and symbol in current_production:
                continue
            current_production.append(symbol)
        processed_grammar[non_terminal].append(current_production)
    return processed_grammar


def main():

    grammar = read_lines()
    symbols = get_symbols(grammar)
    processed_grammar = process_grammar(grammar)

    print("------ TERMINALS AND NON TERMINALS ------")
    print("Terminal: " + ", ".join(symbols['terminals']))
    print("Non terminal: " + ", ".join(symbols['non_terminals']))
    print("------ FIRST AND FOLLOWS ------")

    first_dict = {}
    follow_dict = {}
    for non_terminal in processed_grammar:
        follow_dict[non_terminal] = set()
        get_first(non_terminal, processed_grammar, first_dict,
                  symbols['non_terminals'], set())

    follow_dict[grammar[0].split()[0]].add('$')
    while True:
        previous_dict = follow_dict.copy()
        for non_terminal in processed_grammar:
            get_follow(non_terminal, grammar, follow_dict, first_dict,
                       symbols['non_terminals'])
        if previous_dict == follow_dict:
            break

    for non_terminal in first_dict:
        print(f'{non_terminal} => FIRST = {first_dict[non_terminal]}, '
              f'FOLLOW = {follow_dict[non_terminal]}')


if __name__ == '__main__':
    main()
