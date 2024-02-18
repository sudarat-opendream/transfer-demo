import uuid

import pytest

from transfer.values_objects import Donor, Donee


@pytest.fixture
def donor_individual():
    return Donor(uuid.uuid4(), 'John Doe', 'john.doe@mail.com', 'individual')


@pytest.fixture
def donor_company():
    return Donor(uuid.uuid4(), 'John Co.', 'john.comp@mail.com', 'company')


@pytest.fixture
def project_donee():
    return Donee(uuid.uuid4(), "Project", "PROJ")


@pytest.fixture
def donee_fundraiser():
    return Donee(uuid.uuid4(), "Fundraiser", "FUND")


def test_donor(donor_individual, donor_company):
    assert donor_individual.name == 'John Doe'
    assert donor_individual.email == 'john.doe@mail.com'
    assert donor_individual.donor_type == 'individual'

    assert donor_company.name == 'John Co.'
    assert donor_company.email == 'john.comp@mail.com'
    assert donor_company.donor_type == 'company'


def test_donor_change_information(donor_individual, donor_company):
    assert donor_individual.name == 'John Doe'
    assert donor_individual.email == 'john.doe@mail.com'
    assert donor_individual.donor_type == 'individual'

    with pytest.raises(AttributeError):
        donor_individual.name = 'John Smith'

    assert donor_company.name == 'John Co.'
    assert donor_company.email == 'john.comp@mail.com'
    assert donor_company.donor_type == 'company'

    with pytest.raises(AttributeError):
        donor_company.name = 'John Comp.'


def test_donee(project_donee, donee_fundraiser):
    assert project_donee.name == 'Project'
    assert project_donee.donee_type == 'PROJ'

    assert donee_fundraiser.name == 'Fundraiser'
    assert donee_fundraiser.donee_type == 'FUND'
