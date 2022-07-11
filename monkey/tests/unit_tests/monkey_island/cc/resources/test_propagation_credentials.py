import json

import pytest
from tests.common import StubDIContainer
from tests.monkey_island import (
    PROPAGATION_CREDENTIALS_1,
    PROPAGATION_CREDENTIALS_2,
    StubPropagationCredentialsRepository,
)
from tests.unit_tests.common.utils.test_code_utils import raise_error
from tests.unit_tests.monkey_island.conftest import get_url_for_resource

from monkey_island.cc.repository import ICredentialsRepository, RemovalError
from monkey_island.cc.resources.credentials.propagation_credentials import PropagationCredentials


@pytest.fixture
def flask_client(build_flask_client):
    container = StubDIContainer()

    container.register(ICredentialsRepository, StubPropagationCredentialsRepository)

    with build_flask_client(container) as flask_client:
        yield flask_client


def test_propagation_credentials_endpoint_get(flask_client):
    propagation_credentials_url = get_url_for_resource(PropagationCredentials)

    resp = flask_client.get(propagation_credentials_url)

    assert resp.status_code == 200
    actual_propagation_credentials = json.loads(resp.data)
    assert len(actual_propagation_credentials) == 2

    # TODO: delete the removal of monkey_guid key when the serialization of credentials
    del actual_propagation_credentials[0]["monkey_guid"]
    assert actual_propagation_credentials[0] == PROPAGATION_CREDENTIALS_1
    del actual_propagation_credentials[1]["monkey_guid"]
    assert actual_propagation_credentials[1] == PROPAGATION_CREDENTIALS_2


def test_propagation_credentials_endpoint_delete(flask_client):
    propagation_credentials_url = get_url_for_resource(PropagationCredentials)

    resp = flask_client.delete(propagation_credentials_url)

    assert resp.status_code == 200


def test_propagation_credentials_endpoint_delete_failed(monkeypatch, flask_client):
    propagation_credentials_url = get_url_for_resource(PropagationCredentials)
    monkeypatch.setattr(
        "tests.monkey_island.StubPropagationCredentialsRepository.remove_all_credentials",
        lambda: raise_error(RemovalError),
    )
    resp = flask_client.delete(propagation_credentials_url)

    assert resp.status_code == 500
