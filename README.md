# Grammar Parser

- Pablo Valencia A01700912  
- Compilers  
- Detecting terminals and non-terminals  
- March 19, 2023  

## Requirements

- Python 3

## Usage

- `python3 main.py`
  - The first line must be number that determines the number of productions to read.
- `git clone https://github.com/coronapl/grammar-parser.git && cd grammar-parser && chmod +x run.sh && ./run.sh`

## Examples

```
python3 main.py
8
E -> T EPrime
EPrime -> + T EPrime
EPrime -> ' '
T -> F TPrime
TPrime -> * F TPrime
TPrime -> ' '
F -> ( E )
F -> id
Terminal: +, *, (, ), id
Non terminal: E, T, EPrime, F, TPrime
```

```
python3 main.py
6
E -> E + T
E -> T
T -> T * F
T -> F
F -> id
F -> ( E )
Terminal: +, *, id, (, )
Non terminal: E, T, F
```

