from types import NoneType


class Token:
    def __init__(self, name: str, terminal: bool, value: str | NoneType = None):
        self.name = name
        self.terminal = terminal
        self.value = value

    def __repr__(self):
        return f"Token(name={self.name}, terminal={self.terminal})"


class TokenDef:
    def __init__(self, name: str, regex: str):
        self.name = name
        self.regex = regex

    def __repr__(self):
        return f"TokenDef(name={self.name}, regex={self.regex})"


type Production = list[Token]
type Rule = list[Production]
type Grammar = dict[str, Rule]
