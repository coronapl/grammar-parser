# SLR Table

- Pablo Valencia A01700912
- Compilers
- Detecting terminals and non-terminals
- Creating first and follow sets
- June 4, 2023

## Requirements

- Python 3

## Usage

- `python3 main.py`
  - The first line must be number that determines the number of productions to read.
- `git clone https://github.com/coronapl/grammar-parser.git && cd grammar-parser && chmod +x run.sh && ./run.sh`
- If you want add another test, you can include it in the `test_cases` directory. After that, you need to include the
relative path of the test case in the `test_cases` list inside the `run.sh` script.

## Examples

```
python3 main.py
8 3
E -> T EPrime
EPrime -> + T EPrime
EPrime -> ' '
T -> F TPrime
TPrime -> * F TPrime
TPrime -> ' '
F -> ( E )
F -> id
id + id * id
id * id + ( id * id + id )
id +
------ TERMINALS AND NON TERMINALS ------
Terminal: *, id, ), +, (
Non terminal: EPrime, T, TPrime, E, F
------ FIRST AND FOLLOWS ------
F => FIRST = {'(', 'id'}, FOLLOW = {'+', '*', '$', ')'}
T => FIRST = {'(', 'id'}, FOLLOW = {'+', '$', ')'}
E => FIRST = {'(', 'id'}, FOLLOW = {'$', ')'}
EPrime => FIRST = {'+', ' '}, FOLLOW = {'$', ')'}
TPrime => FIRST = {'*', ' '}, FOLLOW = {'+', '$', ')'}
```
