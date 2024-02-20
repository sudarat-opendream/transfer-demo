import dataclasses


@dataclasses.dataclass(frozen=True)
class Money:
    amount: float
    currency: str
