import json
import os
import re

from automate.types import Grammar, TokenDef, Token
from automate.exceptions import (
    LoaderException,
    RulesLoaderException,
    TokensLoaderException,
)
from automate.utils import log


def _read_file(file_path: str) -> str:
    if not os.path.exists(file_path):
        raise LoaderException(f"File not found: {file_path}")
    if not os.path.isfile(file_path):
        raise LoaderException(f"Not a file: {file_path}")
    with open(file_path, "r") as file:
        return file.read()


def _parse_rule_token(rule_token_raw: str, token_defs: list[TokenDef]) -> Token:
    if re.match(r"^\[.*\]$", rule_token_raw):
        return Token(rule_token_raw[1:-1].strip(), False)

    if rule_token_raw == "newline":
        return Token(rule_token_raw, True)

    token_def = next((td for td in token_defs if td.name == rule_token_raw), None)
    if token_def:
        return Token(token_def.name, True)

    raise RulesLoaderException(f"Unknown token: {rule_token_raw}")


def _parse_rule_alternative(
    rule_alternative_raw: str, token_defs: list[TokenDef]
) -> list[Token]:
    return [
        _parse_rule_token(token, token_defs)
        for token in re.split(r"\s+", rule_alternative_raw.strip())
        if token
    ]


# = Public functions ==========================================================
def load_token_defs(token_defs_path: str, verbose: bool) -> list[TokenDef]:
    log(f"=> Loading token definitions from {token_defs_path}", verbose)
    token_defs_raw = _read_file(token_defs_path)
    # create a list of TokenDef from the JSON string
    return [
        TokenDef(token_def["name"], token_def["regex"])
        for token_def in json.loads(token_defs_raw)
    ]


def load_rules(rules_path: str, token_defs: list[TokenDef], verbose: bool) -> Grammar:
    log(f"=> Loading rules from {rules_path}", verbose)
    # create a Grammar from the rules string
    rules: Grammar = {}
    rules_raw = _read_file(rules_path)

    for rule_raw in rules_raw.splitlines():
        if "->" not in rule_raw:
            raise RulesLoaderException(f"'->' is missing: {rule_raw}")

        rule_name, rule_body = map(str.strip, rule_raw.split("->"))
        rules[rule_name] = [
            _parse_rule_alternative(alt, token_defs) for alt in rule_body.split("|")
        ]

    # check if the grammar has an "S" rule (start rule)
    if "S" not in rules:
        raise RulesLoaderException("No 'S' rule")

    return rules


def load_tokens(
    file_path: str, token_defs: list[TokenDef], verbose: bool
) -> list[Token]:
    log(f"=> Loading tokens from {file_path}", verbose)
    file_content = _read_file(file_path)
    tokens: list[Token] = []

    for line in file_content.split("\n"):
        for word in line.split(" "):
            if not word:
                continue
            for token_def in token_defs:
                if re.match(token_def.regex, word):
                    tokens.append(Token(token_def.name, True))
                    break
            else:
                raise TokensLoaderException(f"{word} cannot be recognized")
        tokens.append(Token("newline", True))
    return tokens[:-1]
