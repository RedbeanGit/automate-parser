class Contact:
    TOKEN_NAME = "contact"

    def __init__(self, tx: str, rx: str, start: int, end: int) -> None:
        self.tx = tx
        self.rx = rx
        self.start = start
        self.end = end

    def __repr__(self) -> str:
        return f"Contact({self.tx}, {self.rx}, {self.start}, {self.end})"


class Rate:
    TOKEN_NAME = "rate"

    def __init__(self, frequency: int, start: int, end: int):
        self.frequency = frequency
        self.start = start
        self.end = end

    def __repr__(self) -> str:
        return f"Rate({self.frequency}, {self.start}, {self.end})"


class Delay:
    TOKEN_NAME = "delay"

    def __init__(self, duration: int, start: int, end: int):
        self.duration = duration
        self.start = start
        self.end = end

    def __repr__(self) -> str:
        return f"Delay({self.duration}, {self.start}, {self.end})"


type SpacecomObject = Contact | Rate | Delay
