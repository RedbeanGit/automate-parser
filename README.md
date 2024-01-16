# Automate parser

Check a file from a given grammar.

## Requirements

- Python 3.12 or higher
- Pipenv (optional)

## Usage

```bash
python src/main.py <token_defs_path> <rules_path> <file_path> [-v]
```

Where:

- `token_defs_path` is the path to the file containing the token definitions. This file **must** be a valid JSON file.
- `rules_path` is the path to the file containing the grammar rules. This file **must** follow the format specified in the [Grammar](#grammar) section.
- `file_path` is the path to the file to be checked.

You can find some examples of token definitions, grammar and sample file in the `examples` folder.

## Grammar

The grammar file must follow this format:

```
<non-terminal-1> -> <production-1> | <production-2> | ...
<non-terminal-2> -> <production-1> | <production-2> | ...
```

Where:

- `<non-terminal>` is a non-terminal symbol.
- `<production>` is a production rule. It can be a terminal symbol, a non-terminal symbol or a sequence of symbols.

The grammar needs at least one non-terminal symbol "S" (start symbol).
