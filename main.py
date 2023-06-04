"""
Pablo Valencia A01700912
Compilers
Grammar Parser
Detecting terminals and non-terminals
Creating first and follow sets
Creating SLR table
June 4, 2023
"""


def read_lines():
    """
    read_lines is a function that reads multiple lines of input from the user
    and stores them in a list. The first line is a number that determines the
    number of lines to read.

    :return: list where each element is a production.
    """
    lines = []
    strings = []
    first_line = input().split()
    grammar_lines, strings_lines = int(first_line[0]), int(first_line[1])

    for _ in range(grammar_lines):
        production = input()
        lines.append(production)

    for _ in range(strings_lines):
        string = input()
        strings.append(string)

    return lines, strings


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


class Node:
    def __init__(self, idx, kernel = None, productions = None) -> None:
        self.idx = idx
        self.next = {}
        self.kernel = kernel
        self.productions = productions


def get_complete_grammar(kernel, processed_grammar):
    """
    get_complete_grammar function takes in two parameters, kernel and processed_grammar,
    and returns a set of complete productions.
    :param kernel: A set representing the kernel.
    :param processed_grammar: A dictionary where the keys are non-terminals and the values are arrays of arrays,
    each representing a production of the non-terminal.
    :return: A set of complete productions.
    """
    queue = list(kernel)
    result = set()

    while len(queue) > 0:
        current_production = queue.pop(0)
        result.add(current_production)

        production_list = current_production.split()
        reading_index = production_list.index('.')

        if reading_index == len(production_list) - 1:
            continue

        reading_symbol = production_list[reading_index + 1]
        if reading_symbol not in processed_grammar:
            continue

        for next_production in processed_grammar[reading_symbol]:
            complete = reading_symbol + ' ->' + ' . ' + ' '.join(next_production)
            queue.append(complete)
    return result


def create_slr_graph(grammar, processed_grammar, non_terminals, terminals, follows):
    """
    create_slr_graph function takes in several parameters and returns a table and the number of states.
    :param grammar: A list of strings representing the grammar.
    :param processed_grammar: A dictionary where the keys are non-terminals and the values are arrays of arrays, each representing a production of the non-terminal.
    :param non_terminals: A set of non-terminal symbols.
    :param terminals: A set of terminal symbols.
    :param follows: A dictionary where the keys are non-terminals and the values are sets of symbols that can follow the non-terminal.
    :return: A table representing the SLR parser's parsing table, and the number of states.
    """
    global_kernels = {}
    next_state = 0

    first_production = grammar[0]
    first_non_terminal = first_production.split()[0]
    extended_production = f'ExtGrammar -> . {first_non_terminal}'

    node = Node(next_state)
    node.kernel = set([extended_production])
    node.productions = get_complete_grammar(node.kernel, processed_grammar)

    global_kernels[next_state] = node
    next_state += 1

    symbols = non_terminals | terminals

    queue = [node]

    while len(queue) > 0:
        current = queue.pop(0)

        for symbol in symbols:
            next_node = Node(next_state)
            next_node.kernel = set()

            for production in current.productions:
                production_list = production.split()
                reading_index = production_list.index('.')

                if reading_index == len(production_list) - 1:
                    continue

                reading_symbol = production_list[reading_index + 1]
                if reading_symbol == symbol:
                    production_list[reading_index] = reading_symbol
                    production_list[reading_index + 1] = '.'
                    next_node.kernel.add(' '.join(production_list))

            if len(next_node.kernel) > 0:
                same_kernel = False
                for _, state_node in global_kernels.items():
                    if state_node.kernel == next_node.kernel:
                        current.next[symbol] = state_node
                        same_kernel = True
                        break

                if not same_kernel:
                    global_kernels[next_state] = next_node
                    current.next[symbol] = next_node
                    next_node.productions = get_complete_grammar(next_node.kernel, processed_grammar)
                    next_state += 1
                    queue.append(next_node)

    new_queue = [global_kernels[0]]
    visited = set()
    while len(new_queue) > 0:
        current = new_queue.pop(0)

        if current in visited:
            continue

        visited.add(current)

        for _, neighbor in current.next.items():
            new_queue.append(neighbor)

    table = {}
    table['$'] = [None] * next_state
    for symbol in symbols:
        table[symbol] = [None] * next_state

    for state in range(next_state):
        current_state = global_kernels[state]
        for symbol in table:
            if symbol == '$':
                continue

            if symbol in current_state.next:
                action = 's'
                if symbol in non_terminals:
                    action = 'g'
                if table[symbol][state] is not None:
                    raise Exception('ERROR: invalid grammar')
                table[symbol][state] = (action, current_state.next[symbol].idx)

        for production in current_state.productions:
            production = production.strip()
            production_list = production.split()
            non_terminal = production_list[0]
            if production[-1] != '.':
                continue

            production = production[:-1].strip()
            if production not in grammar:
                if non_terminal == 'ExtGrammar':
                    table['$'][current_state.idx] = True
                    continue
                production = f"{production_list[0]} -> ' '"

            reduce_state = grammar.index(production) + 1
            for follow in follows[non_terminal]:
                if table[follow][current_state.idx] is not None:
                    raise Exception('ERROR: invalid grammar')
                table[follow][current_state.idx] = ('r', reduce_state)

    return table, next_state


def evaluate_string(grammar, table, input):
    """
    evaluate_string function takes in a grammar, parsing table, and input string, and evaluates whether the input string is
    valid according to the grammar and the given parsing table.
    :param grammar: A list of strings representing the grammar.
    :param table: A parsing table represented as a dictionary of dictionaries, where the keys are input symbols
    and state indices, and the values are actions or next states.
    :param input: The input string to be evaluated.
    :return: True if the input string is valid according to the grammar and parsing table, False otherwise.
    """
    first_non_terminal = grammar[0].split()[0]
    stack = [first_non_terminal, 0]
    string = input.split() + ['$']

    while True:
        action = table[string[0]][stack[-1]]

        if action is True:
            return True
        if action is None:
            return False

        if action[0] == 's':
            stack.append(string.pop(0))
            stack.append(action[1])
        if action[0] == 'r':
            production = grammar[action[1] - 1]

            production_list = production.split()
            production_nt = production_list[0]

            if production.find("' '") == -1:
                num_symbols = len(production_list[2:]) * 2
            else:
                num_symbols = 0

            for _ in range(num_symbols):
                stack.pop()

            next_state = table[production_nt][stack[-1]]
            stack.append(production_nt)
            stack.append(next_state[1])


def create_html_table(table, terminals, non_terminals, num_states, evaluated_strings):
    """
    create_html_table function takes in a parsing table, terminals, non-terminals, number of states, and evaluated strings, and generates an HTML representation of the parsing table with the evaluated strings.
    :param table: A parsing table represented as a dictionary of dictionaries, where the keys are symbols and state indices, and the values are actions or next states.
    :param terminals: A set of terminal symbols.
    :param non_terminals: A set of non-terminal symbols.
    :param num_states: The number of states in the parsing table.
    :param evaluated_strings: A list of strings that were evaluated using the parsing table.
    :return: None
    """
    header = list(terminals) + ['$'] + list(non_terminals)
    html = '<table style="border: 1px solid black; width: 500px;">'

    html += '<tr style="border: 1px solid black;">'
    html += '<th style="border: 1px solid black;">State</th>'
    for symbol in header:
        html += '<th style="border: 1px solid black;">'
        html += symbol
        html += '</th>'
    html += '</tr>'

    for i in range(num_states):
        html += '<tr style="border: 1px solid black;">'
        html += '<td style="border: 1px solid black;">' + str(i) + '</td>'
        for symbol in header:
            html += '<td style="border: 1px solid black;">'
            if table[symbol][i] is not None:
                if table[symbol][i] is True:
                    html += 'Accepted'
                else:
                    html += table[symbol][i][0] + str(table[symbol][i][1])
            html += '</td>'
        html += '</tr>'
    html += '</table>'

    for i in range(len(evaluated_strings)):
        html += '<p>' + evaluated_strings[i] + '</p>'

    with open("table.html", "w") as text_file:
        text_file.write(html)

def main():

    grammar, strings = read_lines()
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

    table, num_states = create_slr_graph(grammar, processed_grammar, symbols['non_terminals'], symbols['terminals'], follow_dict)
    evaluated_strings = []
    for string in strings:
        evaluated_strings.append(f'{string} - ACCEPTED? {evaluate_string(grammar, table, string)}')
    create_html_table(table, symbols['terminals'], symbols['non_terminals'], num_states, evaluated_strings)

if __name__ == '__main__':
    main()
