class Token:
    def __init__(self, name: str, terminal: bool):
        self.name = name
        self.terminal = terminal

    def __repr__(self):
        return f"Token(name={self.name}, terminal={self.terminal})"


class TokenDef:
    def __init__(self, name: str, regex: str):
        self.name = name
        self.regex = regex

    def __repr__(self):
        return f"TokenDef(name={self.name}, regex={self.regex})"


type RuleAlternative = list[Token]
type Rule = list[RuleAlternative]
type Grammar = dict[str, Rule]
