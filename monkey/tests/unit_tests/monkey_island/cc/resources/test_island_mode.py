import json
from unittest.mock import MagicMock

import pytest
from tests.common import StubDIContainer
from tests.monkey_island import InMemorySimulationRepository

from monkey_island.cc.models import IslandMode
from monkey_island.cc.repository import RetrievalError
from monkey_island.cc.resources.island_mode import IslandMode as IslandModeResource
from monkey_island.cc.services import IslandModeService


class MockIslandModeService(IslandModeService):
    def __init__(self):
        self._simulation_repository = InMemorySimulationRepository()

    def get_mode(self) -> IslandMode:
        return self._simulation_repository.get_mode()

    def set_mode(self, mode: IslandMode):
        self._simulation_repository.set_mode(mode)


@pytest.fixture
def flask_client(build_flask_client):
    container = StubDIContainer()
    container.register_instance(IslandModeService, MockIslandModeService())

    with build_flask_client(container) as flask_client:
        yield flask_client


@pytest.mark.parametrize(
    "mode",
    [IslandMode.RANSOMWARE.value, IslandMode.ADVANCED.value, IslandMode.UNSET.value],
)
def test_island_mode_post(flask_client, mode):
    resp = flask_client.post(
        IslandModeResource.urls[0], data=json.dumps({"mode": mode}), follow_redirects=True
    )
    assert resp.status_code == 200


def test_island_mode_post__invalid_mode(flask_client):
    resp = flask_client.post(
        IslandModeResource.urls[0], data=json.dumps({"mode": "bogus mode"}), follow_redirects=True
    )
    assert resp.status_code == 422


@pytest.mark.parametrize("invalid_json", ["42", "{test"])
def test_island_mode_post__invalid_json(flask_client, invalid_json):
    resp = flask_client.post(IslandModeResource.urls[0], data="{test", follow_redirects=True)
    assert resp.status_code == 400


def test_island_mode_post__internal_server_error(build_flask_client):
    mock_island_mode_service = MagicMock(spec=IslandModeService)
    mock_island_mode_service.set_mode = MagicMock(side_effect=RetrievalError)

    container = StubDIContainer()
    container.register_instance(IslandModeService, mock_island_mode_service)

    with build_flask_client(container) as flask_client:
        resp = flask_client.post(
            IslandModeResource.urls[0],
            data=json.dumps({"mode": IslandMode.RANSOMWARE.value}),
            follow_redirects=True,
        )

    assert resp.status_code == 500


@pytest.mark.parametrize("mode", [IslandMode.RANSOMWARE.value, IslandMode.ADVANCED.value])
def test_island_mode_endpoint(flask_client, mode):
    flask_client.post(
        IslandModeResource.urls[0], data=json.dumps({"mode": mode}), follow_redirects=True
    )
    resp = flask_client.get(IslandModeResource.urls[0], follow_redirects=True)
    assert resp.status_code == 200
    assert json.loads(resp.data)["mode"] == mode


def test_island_mode_endpoint__invalid_mode(flask_client):
    resp_post = flask_client.post(
        IslandModeResource.urls[0], data=json.dumps({"mode": "bogus_mode"}), follow_redirects=True
    )
    resp_get = flask_client.get(IslandModeResource.urls[0], follow_redirects=True)
    assert resp_post.status_code == 422
    assert json.loads(resp_get.data)["mode"] == IslandMode.UNSET.value
