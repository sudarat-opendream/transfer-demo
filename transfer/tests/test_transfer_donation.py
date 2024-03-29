from datetime import datetime

from common.domain.value_objects import Money
from transfer.domain.entities import TransferDonation, TransferDonationStatus, TransferDonationNote, \
    TransferTransactionStatus
from transfer.tests.test_value_objects import donor_individual, donee_project


def test_donation(donor_individual, donee_project):
    donation = TransferDonation(donor_individual, donee_project, Money(100, "THB"))
    assert donation.donor == donor_individual
    assert donation.donee == donee_project
    assert donation.expect_amount.amount == 100
    assert donation.expect_amount.currency == "THB"
    assert donation.status == TransferDonationStatus.WAIL_FOR_TRANSFER


def test_donation_add_note(donor_individual, donee_project):
    donation = TransferDonation(donor_individual, donee_project, Money(100, "THB"))

    note = TransferDonationNote(Money(100, "THB"),
                                datetime.strptime('2021-01-01', '%Y-%m-%d'),
                                'test note.jpg',
                                'test note',
                                donation)
    TransferDonation.add_note(donation, note)

    assert len(donation.notes) == 1
    assert donation.notes[0].file_url == 'test note.jpg'
    assert donation.notes[0].note == 'test note'
    assert donation.notes[0].donation == donation

    assert len(donation.transactions) == 1
    assert donation.transactions[0].note == note
    assert donation.transactions[0].status == TransferTransactionStatus.PENDING
    assert donation.transactions[0].amount.amount == 100
    assert donation.transactions[0].amount.currency == "THB"

    assert donation.status == TransferDonationStatus.WAIL_FOR_APPROVE


def test_donation_add_2_note(donor_individual, donee_project):
    donation = TransferDonation(donor_individual, donee_project, Money(100, "THB"))

    note1 = TransferDonationNote(Money(100, "THB"),
                                 datetime.strptime('2021-01-01',
                                                   '%Y-%m-%d'),
                                 'test note1.jpg',
                                 'test note1',
                                 donation)
    TransferDonation.add_note(donation, note1)

    assert len(donation.notes) == 1

    assert donation.notes[0].amount.amount == 100
    assert donation.notes[0].amount.currency == "THB"
    assert donation.notes[0].date_confirmed == datetime.strptime('2021-01-01',
                                                                 '%Y-%m-%d')
    assert donation.notes[0].file_url == 'test note1.jpg'
    assert donation.notes[0].note == 'test note1'
    assert donation.notes[0].donation == donation

    assert donation.status == TransferDonationStatus.WAIL_FOR_APPROVE

    note2 = TransferDonationNote(Money(200, "THB"),
                                 datetime.strptime('2022-01-01',
                                                   '%Y-%m-%d'),
                                 'test note2.jpg',
                                 'test note2',
                                 donation)
    TransferDonation.add_note(donation, note2)

    assert len(donation.notes) == 2

    assert donation.notes[1].amount.amount == 200
    assert donation.notes[1].date_confirmed == datetime.strptime('2022-01-01',
                                                                 '%Y-%m-%d')
    assert donation.notes[1].file_url == 'test note2.jpg'
    assert donation.notes[1].note == 'test note2'
    assert donation.notes[1].donation == donation

    assert len(donation.transactions) == 2
    assert donation.status == TransferDonationStatus.WAIL_FOR_APPROVE

    assert donation.transactions[0].amount.amount == 100
    assert donation.transactions[0].amount.currency == "THB"

    assert donation.transactions[1].amount.amount == 200
    assert donation.transactions[1].amount.currency == "THB"

    donation1 = TransferDonation(donor_individual, donee_project, Money(100, "THB"))
    note3 = TransferDonationNote(Money(300, "THB"),
                                 datetime.strptime('2023-01-01',
                                                   '%Y-%m-%d'),
                                 'test note3.jpg',
                                 'test note3',
                                 donation)

    TransferDonation.add_note(donation1, note3)

    assert len(donation1.notes) == 1
    assert len(donation1.transactions) == 1


def test_donation_set_to_paid(donor_individual, donee_project):
    donation = TransferDonation(donor_individual, donee_project, Money(100, "THB"))

    note = TransferDonationNote(Money(100, "THB"),
                                datetime.strptime('2021-01-01', '%Y-%m-%d'),
                                'test note.jpg',
                                'test note',
                                donation)
    TransferDonation.add_note(donation, note)

    assert donation.status == TransferDonationStatus.WAIL_FOR_APPROVE

    transaction = donation.transactions[0]
    TransferDonation.set_to_paid(donation, transaction)

    assert transaction.status == TransferTransactionStatus.PAID

    assert donation.expect_amount.amount == 100
    assert donation.expect_amount.currency == "THB"

    assert donation.date_confirmed == datetime.strptime('2021-01-01', '%Y-%m-%d')
    assert donation.status == TransferDonationStatus.PAID


def test_donation_set_to_paid_2_note(donor_individual, donee_project):
    donation = TransferDonation(donor_individual, donee_project, Money(100, "THB"))

    note1 = TransferDonationNote(Money(100, "THB"),
                                 datetime.strptime('2021-01-01', '%Y-%m-%d'),
                                 'test note1.jpg',
                                 'test note1',
                                 donation)
    TransferDonation.add_note(donation, note1)

    assert len(donation.notes) == 1

    assert donation.notes[0].amount.amount == 100
    assert donation.notes[0].amount.currency == "THB"
    assert donation.notes[0].date_confirmed == datetime.strptime('2021-01-01',
                                                                 '%Y-%m-%d')
    assert donation.notes[0].file_url == 'test note1.jpg'
    assert donation.notes[0].note == 'test note1'
    assert donation.notes[0].donation == donation

    assert donation.status == TransferDonationStatus.WAIL_FOR_APPROVE

    note2 = TransferDonationNote(Money(200, "USD"),
                                 datetime.strptime('2022-01-01', '%Y-%m-%d'),
                                 'test note2.jpg',
                                 'test note2',
                                 donation)
    TransferDonation.add_note(donation, note2)

    assert len(donation.notes) == 2

    assert donation.notes[1].amount.amount == 200
    assert donation.notes[1].amount.currency == "USD"
    assert donation.notes[1].date_confirmed == datetime.strptime('2022-01-01',
                                                                 '%Y-%m-%d')
    assert donation.notes[1].file_url == 'test note2.jpg'
    assert donation.notes[1].note == 'test note2'
    assert donation.notes[1].donation == donation

    assert len(donation.transactions) == 2
    assert donation.status == TransferDonationStatus.WAIL_FOR_APPROVE

    assert donation.transactions[0].amount.amount == 100
    assert donation.transactions[1].amount.amount == 200

    transaction1 = donation.transactions[0]
    transaction2 = donation.transactions[1]

    TransferDonation.set_to_paid(donation, transaction2)

    assert transaction1.status == TransferTransactionStatus.PENDING
    assert transaction2.status == TransferTransactionStatus.PAID

    assert donation.expect_amount.amount == 200
    assert donation.expect_amount.currency == "USD"
    assert donation.date_confirmed == datetime.strptime('2022-01-01', '%Y-%m-%d')
    assert donation.status == TransferDonationStatus.PAID


def test_donation_set_to_cancelled(donor_individual, donee_project):
    donation = TransferDonation(donor_individual, donee_project, Money(100, "THB"))

    note = TransferDonationNote(Money(100, "THB"),
                                datetime.strptime('2021-01-01', '%Y-%m-%d'),
                                'test note.jpg',
                                'test note',
                                donation)
    TransferDonation.add_note(donation, note)

    assert donation.status == TransferDonationStatus.WAIL_FOR_APPROVE

    TransferDonation.set_to_cancelled(donation)
    assert donation.status == TransferDonationStatus.CANCELLED


def test_donation_set_to_failed(donor_individual, donee_project):
    donation = TransferDonation(donor_individual, donee_project, Money(100, "THB"))

    note = TransferDonationNote(Money(100, "THB"),
                                datetime.strptime('2021-01-01', '%Y-%m-%d'),
                                'test note.jpg',
                                'test note',
                                donation)
    TransferDonation.add_note(donation, note)

    assert donation.status == TransferDonationStatus.WAIL_FOR_APPROVE

    TransferDonation.set_to_failed(donation)

    assert donation.status == TransferDonationStatus.FAILED
