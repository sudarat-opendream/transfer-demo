import datetime
from enum import Enum

from transfer.values_objects import Donor, Donee


class TransferDonationStatus(Enum):
    WAIL_FOR_TRANSFER = 'wait_for_transfer'
    WAIL_FOR_APPROVE = 'wait_for_approve'

    PAID = 'paid'
    FAILED = 'failed'
    CANCELLED = 'cancelled'


class TransferTransactionStatus(Enum):
    PENDING = 'pending'

    PAID = 'paid'
    FAILED = 'failed'
    CANCELLED = 'cancelled'


class TransferDonation:
    id: int

    donor: Donor
    donee: Donee
    donation_number: str

    expect_amount: float
    status: TransferDonationStatus = TransferDonationStatus.WAIL_FOR_TRANSFER

    date_confirmed: datetime

    created: datetime
    modified: datetime

    notes: list['TransferDonationNote'] = []
    transactions: list['TransferTransaction'] = []

    def __init__(self,
                 donor,
                 donee,
                 expect_amount,
                 created=datetime.datetime.now(),
                 modified=datetime.datetime.now()):
        self.id = TransferDonation.next_id()
        self.donor = donor
        self.donee = donee
        self.expect_amount = expect_amount

        self.donation_number = f'{donor.id}-{donee.id}-{self.id}'

        self.notes = []
        self.transactions = []

        self.created = created
        self.modified = modified

    @classmethod
    def next_id(cls):
        return 1

    @classmethod
    def add_note(cls, donation, note):
        transaction = TransferTransaction(donation,
                                          note,
                                          note.amount,
                                          status=TransferTransactionStatus.PENDING,
                                          created=note.date_confirmed,
                                          modified=note.date_confirmed)

        donation.notes.append(note)
        TransferDonation.set_to_wait_for_approve(donation, transaction)

    @classmethod
    def set_to_wait_for_approve(cls, donation, transaction):
        donation.transactions.append(transaction)
        donation.status = TransferDonationStatus.WAIL_FOR_APPROVE

    @classmethod
    def set_to_paid(cls, donation, transaction, date_confirmed=None):
        transaction.status = TransferTransactionStatus.PAID

        donation.date_confirmed = date_confirmed or transaction.created
        donation.amount = transaction.amount

        donation.status = TransferDonationStatus.PAID

    @classmethod
    def set_to_cancelled(cls, donation):
        donation.status = TransferDonationStatus.CANCELLED

    @classmethod
    def set_to_failed(cls, donation):
        donation.status = TransferDonationStatus.FAILED


class TransferDonationNote:
    id: int
    file_url: str

    amount: float
    date_confirmed: datetime

    note: str

    created: datetime
    modified: datetime

    donation: TransferDonation

    def __init__(self,
                 amount,
                 date_confirmed,
                 file_url,
                 note,
                 donation,
                 created=datetime.datetime.now(),
                 modified=datetime.datetime.now()
                 ):
        self.id = TransferDonationNote.next_id()

        self.amount = amount
        self.date_confirmed = date_confirmed

        self.file_url = file_url
        self.note = note

        self.donation = donation

        self.created = created
        self.modified = modified

    @classmethod
    def next_id(cls):
        return 1


class TransferTransaction:
    id: int
    amount: float

    status: TransferTransactionStatus
    created: datetime
    modified: datetime

    donation: TransferDonation
    note: TransferDonationNote

    def __init__(self,
                 donation,
                 note,
                 amount,
                 status=TransferTransactionStatus.PENDING,
                 created=datetime.datetime.now(),
                 modified=datetime.datetime.now()):
        self.id = TransferTransaction.next_id()
        self.status = status
        self.donation = donation
        self.note = note
        self.amount = amount
        self.created = created
        self.modified = modified

    @classmethod
    def next_id(cls):
        return 1

    @classmethod
    def set_to_paid(cls, transaction):
        transaction.status = TransferTransactionStatus.PAID

    @classmethod
    def set_to_cancelled(cls, transaction):
        transaction.status = TransferTransactionStatus.CANCELLED

    @classmethod
    def set_to_failed(cls, transaction):
        transaction.status = TransferTransactionStatus.FAILED

