from automate.types import Token


class AbstractHandler:
    def handle(self, tokens: list[Token]) -> None:
        raise NotImplementedError
