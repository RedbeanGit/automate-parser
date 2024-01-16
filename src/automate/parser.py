from automate.exceptions import ParserException
from automate.types import Grammar, Token
from automate.utils import log


def parse(tokens: list[Token], grammar: Grammar, verbose: bool) -> bool:
    def parse_rec(rule_name: str, cursor: int) -> int:
        if rule_name not in grammar:
            raise ParserException(f"Unknown rule: {rule_name}")

        log(f"=> Checking rule {rule_name}", verbose)

        # for each production of the rule
        # try to parse the tokens
        for production in grammar[rule_name]:
            # keep track of the cursor for each production
            production_cursor = cursor
            for rule_token in production:
                # if the rule's token is terminal, increment the cursor
                # and check if the token matches the current rule's token
                if rule_token.terminal:
                    production_cursor += 1

                    if production_cursor >= len(tokens):
                        break
                    if rule_token.name != tokens[production_cursor].name:
                        break
                else:
                    # if the rule's token is non-terminal, try to parse it
                    sub_rule_cursor = parse_rec(rule_token.name, production_cursor)

                    # maybe the sub-rule failed to parse
                    # so we try the next production
                    if sub_rule_cursor == -1:
                        break
                    production_cursor = sub_rule_cursor
            else:
                # if we reached the end of the production without breaking
                # it means that the production matched the tokens
                log(
                    f"<= Matched rule {rule_name} (cursor={production_cursor})",
                    verbose,
                )
                return production_cursor

        # if we reached the end of the rule without returning
        # it means that no production matched the tokens
        log(f"<= Bad rule {rule_name} (cursor=-1)", verbose)
        return -1

    # check if we parsed all tokens
    return parse_rec("S", -1) == len(tokens) - 1
