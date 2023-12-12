import json
import re
import sys


class UnknownToken(Exception):
    pass


def match_production(tokens, production):
    cursor = 0
    if not tokens and not production:
        return True
    for production_token in production:
        if production_token["type"] == "non_terminal":
            return True
        if cursor >= len(tokens):
            return False
        if tokens[cursor] != production_token:
            return False
        cursor += 1
    return False


def token_from_name(grammar, name):
    for token in grammar["tokens"]["terminal"]:
        if token["name"] == name:
            return {"name": name, "type": "terminal"}
    for token in grammar["tokens"]["non_terminal"]:
        if token == name:
            return {"name": name, "type": "non_terminal"}
    if name == grammar["newline_token"]:
        return {"name": name, "type": "terminal"}
    raise UnknownToken(f"Unknown token: {name}")


def parse(grammar, tokens):
    queue = [(tokens, grammar["start"])]

    while queue:
        current_tokens, current_stack = queue.pop()
        if not current_tokens and not current_stack:
            return True
        if not current_stack:
            continue
        for production in grammar["rules"][current_stack[-1]["name"]]:
            production = [token_from_name(grammar, name) for name in production]
            if match_production(current_tokens, production):
                new_tokens = current_tokens[
                    len(
                        [token for token in production if token["type"] == "terminal"]
                    ) :
                ]
                if not production or production[-1]["type"] == "terminal":
                    if not new_tokens:
                        return True
                    continue
                new_stack = current_stack[:-1] + production
                queue.append((new_tokens, new_stack))
    return False


def tokenize(grammar, word):
    for token in grammar["tokens"]["terminal"]:
        if re.match(token["regex"], word):
            return {"name": token["name"], "type": "terminal"}
    raise UnknownToken(f"Unknown token: {word}")


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 main.py <grammar_path> <file_path>")
        sys.exit(1)

    grammar_path = sys.argv[1]
    file_path = sys.argv[2]

    with open(grammar_path, "r") as file:
        grammar = json.load(file)

    with open(file_path, "r") as file:
        file_content = file.read()

    tokens = []
    for line in file_content.splitlines():
        for word in line.split(" "):
            if not word:
                continue
            token = tokenize(grammar, word)
            tokens.append(token)
        tokens.append({"name": grammar["newline_token"], "type": "terminal"})

    file_ok = parse(grammar, tokens)

    if file_ok:
        print("File is OK")
        print(*[token["name"] for token in tokens], sep="\n")
    else:
        print("File is not OK")


if __name__ == "__main__":
    main()
