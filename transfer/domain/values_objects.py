import dataclasses

import uuid
from enum import Enum


class DonorType(Enum):
    INDIVIDUAL = 'individual'
    COMPANY = 'company'


class DoneeType(Enum):
    PROJECT = 'PROJ'
    FUNDRAISER = 'FUND'


@dataclasses.dataclass(frozen=True)
class Donor:
    id: uuid.UUID
    name: str
    email: str
    donor_type: DonorType


@dataclasses.dataclass(frozen=True)
class Donee:
    id: uuid.UUID
    name: str
    donee_type: DoneeType

