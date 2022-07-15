from http import HTTPStatus

from flask import request

from common.credentials import Credentials
from monkey_island.cc.repository import ICredentialsRepository
from monkey_island.cc.resources.AbstractResource import AbstractResource

_configured_collection = "configured-credentials"
_stolen_collection = "stolen-credentials"


class PropagationCredentials(AbstractResource):
    urls = ["/api/propagation-credentials/", "/api/propagation-credentials/<string:collection>"]

    def __init__(self, credentials_repository: ICredentialsRepository):
        self._credentials_repository = credentials_repository

    def get(self, collection=None):
        if collection == _configured_collection:
            propagation_credentials = self._credentials_repository.get_configured_credentials()
        elif collection == _stolen_collection:
            propagation_credentials = self._credentials_repository.get_stolen_credentials()
        elif collection is None:
            propagation_credentials = self._credentials_repository.get_all_credentials()
        else:
            return {}, HTTPStatus.NOT_FOUND

        return propagation_credentials, HTTPStatus.OK

    def post(self, collection=None):
        credentials = [Credentials.from_mapping(c) for c in request.json]

        if collection == _configured_collection:
            self._credentials_repository.save_configured_credentials(credentials)
        elif collection == _stolen_collection:
            self._credentials_repository.save_stolen_credentials(credentials)
        elif collection is None:
            return {}, HTTPStatus.METHOD_NOT_ALLOWED
        else:
            return {}, HTTPStatus.NOT_FOUND

        return {}, HTTPStatus.NO_CONTENT

    def patch(self, collection=None):
        if collection != _configured_collection:
            return {}, HTTPStatus.METHOD_NOT_ALLOWED

        credentials = [Credentials.from_mapping(c) for c in request.json]
        self._credentials_repository.remove_configured_credentials()
        self._credentials_repository.save_configured_credentials(credentials)
        return {}, HTTPStatus.NO_CONTENT

    def delete(self, collection=None):
        if collection == _configured_collection:
            self._credentials_repository.remove_configured_credentials()
        elif collection == _stolen_collection:
            self._credentials_repository.remove_stolen_credentials()
        elif collection is None:
            self._credentials_repository.remove_all_credentials()
        else:
            return {}, HTTPStatus.NOT_FOUND

        return {}, HTTPStatus.NO_CONTENT
