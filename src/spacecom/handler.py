import spacecom.types as spt

from automate.handler import AbstractHandler
from automate.types import Token
from spacecom.exceptions import HandlerException
from spacecom.types import Contact, Delay, Rate, SpacecomObject


class SpacecomHandler(AbstractHandler):
    END_OF_OBJECT_TOKEN = "newline"

    def __init__(self) -> None:
        self.objects: list[SpacecomObject] = []
        self.current_object_cls: type[SpacecomObject] | None = None
        self.current_object_args: list[str] = []

    def handle(self, tokens: list[Token]) -> None:
        for token in tokens:
            self.handle_token(token)

    def handle_token(self, token: Token) -> None:
        match token.name:
            case Contact.TOKEN_NAME:
                self.current_object_cls = Contact
            case Rate.TOKEN_NAME:
                self.current_object_cls = Rate
            case Delay.TOKEN_NAME:
                self.current_object_cls = Delay
            case self.END_OF_OBJECT_TOKEN:
                self._build_object()
            case _:
                if self.current_object_cls is None:
                    raise HandlerException(f"Unknown object type {token.value}")
                if token.value:
                    self.current_object_args.append(token.value)
                else:
                    self.current_object_args.append(token.name)

    def _build_object(self) -> None:
        match self.current_object_cls:
            case spt.Contact:
                if len(self.current_object_args) != 4:
                    raise HandlerException("A contact object needs exactly 4 arguments")

                tx = self.current_object_args[0]
                rx = self.current_object_args[1]
                start = int(self.current_object_args[2])
                end = int(self.current_object_args[3])

                self.objects.append(Contact(tx, rx, start, end))

            case spt.Rate:
                if len(self.current_object_args) != 3:
                    raise HandlerException("A rate object needs exactly 3 arguments")

                frequency = int(self.current_object_args[0])
                start = int(self.current_object_args[1])
                end = int(self.current_object_args[2])

                self.objects.append(Rate(frequency, start, end))

            case spt.Delay:
                if len(self.current_object_args) != 3:
                    raise HandlerException("A delay object needs exactly 3 arguments")

                duration = int(self.current_object_args[0])
                start = int(self.current_object_args[1])
                end = int(self.current_object_args[2])

                self.objects.append(Delay(duration, start, end))

            case _:
                raise HandlerException(
                    "End of instruction reached before object creation"
                )
        self.current_object_cls = None
        self.current_object_args = []
