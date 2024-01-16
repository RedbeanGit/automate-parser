from automate.exceptions import ParserException
from automate.types import Grammar, Token
from automate.utils import log


def parse(tokens: list[Token], grammar: Grammar, verbose: bool) -> bool:
    def parse_rec(rule_name: str, cursor: int) -> int:
        if rule_name not in grammar:
            raise ParserException(f"Unknown rule: {rule_name}")

        log(f"=> Checking rule {rule_name}", verbose)

        # for each alternative of the rule
        # try to parse the tokens
        for rule_alternative in grammar[rule_name]:
            # keep track of the cursor for each alternative
            rule_alternative_cursor = cursor
            for rule_token in rule_alternative:
                # if the rule's token is terminal, increment the cursor
                # and check if the token matches the current rule's token
                if rule_token.terminal:
                    rule_alternative_cursor += 1

                    if rule_alternative_cursor >= len(tokens):
                        break
                    if rule_token.name != tokens[rule_alternative_cursor].name:
                        break
                else:
                    # if the rule's token is non-terminal, try to parse it
                    sub_rule_cursor = parse_rec(
                        rule_token.name, rule_alternative_cursor
                    )

                    # maybe the sub-rule failed to parse
                    # so we try the next alternative
                    if sub_rule_cursor == -1:
                        break
                    rule_alternative_cursor = sub_rule_cursor
            else:
                # if we reached the end of the alternative without breaking
                # it means that the alternative matched the tokens
                log(
                    f"<= Matched rule {rule_name} (cursor={rule_alternative_cursor})",
                    verbose,
                )
                return rule_alternative_cursor

        # if we reached the end of the rule without returning
        # it means that no alternative matched the tokens
        log(f"<= Bad rule {rule_name} (cursor=-1)", verbose)
        return -1

    # check if we parsed all tokens
    return parse_rec("S", -1) == len(tokens) - 1
