import sys

from automate.loader import load_rules, load_token_defs, load_tokens
from automate.parser import parse
from automate.utils import log
from spacecom.handler import SpacecomHandler


def main() -> None:
    if len(sys.argv) < 3:
        print(
            f"Usage: python {sys.argv[0]} <token_defs_path> <rules_path> <file_path> [-v]"
        )
        sys.exit(1)

    token_defs_path = sys.argv[1]
    rules_path = sys.argv[2]
    file_path = sys.argv[3]

    # enable verbose mode if -v is passed
    if len(sys.argv) > 3:
        verbose = "-v" in sys.argv[4:]
    else:
        verbose = False

    # load token definitions, rules and tokens
    token_defs = load_token_defs(token_defs_path, verbose)
    log(f"<= Loaded {len(token_defs)} token definitions", verbose)

    rules = load_rules(rules_path, token_defs, verbose)
    log(f"<= Loaded {len(rules)} rules", verbose)

    tokens = load_tokens(file_path, token_defs, verbose)
    log(f"<= Loaded {len(tokens)} tokens", verbose)

    # parse file
    file_ok = parse(tokens, rules, verbose)

    # show result
    if file_ok:
        print("File is OK")
    else:
        print("File is not OK")
        return None

    # handle tokens
    spacecome_handler = SpacecomHandler()
    spacecome_handler.handle(tokens)

    print("Parsed objects:")
    print(" -", "\n - ".join(str(o) for o in spacecome_handler.objects))


if __name__ == "__main__":
    main()
