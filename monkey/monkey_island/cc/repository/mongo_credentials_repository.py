from typing import Any, Dict, Mapping, Sequence

from pymongo import MongoClient

from common.credentials import Credentials
from monkey_island.cc.repository import RemovalError, RetrievalError, StorageError
from monkey_island.cc.repository.i_credentials_repository import ICredentialsRepository
from monkey_island.cc.server_utils.encryption import ILockableEncryptor


class MongoCredentialsRepository(ICredentialsRepository):
    """
    Store credentials in a mongo database that can be used to propagate around the network.
    """

    def __init__(self, mongo: MongoClient, repository_encryptor: ILockableEncryptor):
        self._mongo = mongo
        self._repository_encryptor = repository_encryptor

    def get_configured_credentials(self) -> Sequence[Credentials]:
        return self._get_credentials_from_collection(self._mongo.db.configured_credentials)

    def get_stolen_credentials(self) -> Sequence[Credentials]:
        return self._get_credentials_from_collection(self._mongo.db.stolen_credentials)

    def get_all_credentials(self) -> Sequence[Credentials]:
        configured_credentials = self.get_configured_credentials()
        stolen_credentials = self.get_stolen_credentials()

        return [*configured_credentials, *stolen_credentials]

    def save_configured_credentials(self, credentials: Sequence[Credentials]):
        # TODO: Fix deduplication of Credentials in mongo
        self._save_credentials_to_collection(credentials, self._mongo.db.configured_credentials)

    def save_stolen_credentials(self, credentials: Sequence[Credentials]):
        self._save_credentials_to_collection(credentials, self._mongo.db.stolen_credentials)

    def remove_configured_credentials(self):
        MongoCredentialsRepository._remove_credentials_fom_collection(
            self._mongo.db.configured_credentials
        )

    def remove_stolen_credentials(self):
        MongoCredentialsRepository._remove_credentials_fom_collection(
            self._mongo.db.stolen_credentials
        )

    def remove_all_credentials(self):
        self.remove_configured_credentials()
        self.remove_stolen_credentials()

    def _get_credentials_from_collection(self, collection) -> Sequence[Credentials]:
        try:
            collection_result = []
            list_collection_result = list(collection.find({}))
            for encrypted_credentials in list_collection_result:
                del encrypted_credentials["_id"]
                plaintext_credentials = self._decrypt_credentials_mapping(encrypted_credentials)
                collection_result.append(Credentials.from_mapping(plaintext_credentials))

            return collection_result
        except Exception as err:
            raise RetrievalError(err)

    def _save_credentials_to_collection(self, credentials: Sequence[Credentials], collection):
        try:
            for c in credentials:
                encrypted_credentials = self._encrypt_credentials_mapping(Credentials.to_mapping(c))
                collection.insert_one(encrypted_credentials)
        except Exception as err:
            raise StorageError(err)

    # NOTE: The encryption/decryption is complicated and also full of mostly duplicated code. Rather
    #       than spend the effort to improve them now, we can revisit them when we resolve #2072.
    #       Resolving #2072 will make it easier to simplify these methods and remove duplication.
    #
    #       If possible, implement the encryption/decryption as a decorator so it can be reused with
    #       different ICredentialsRepository implementations
    def _encrypt_credentials_mapping(self, mapping: Mapping[str, Any]) -> Mapping[str, Any]:
        encrypted_mapping: Dict[str, Any] = {}

        for secret_or_identity, credentials_components in mapping.items():
            encrypted_mapping[secret_or_identity] = []
            for component in credentials_components:
                encrypted_component = {}
                for key, value in component.items():
                    encrypted_component[key] = self._repository_encryptor.encrypt(value.encode())

                encrypted_mapping[secret_or_identity].append(encrypted_component)

        return encrypted_mapping

    def _decrypt_credentials_mapping(self, mapping: Mapping[str, Any]) -> Mapping[str, Any]:
        encrypted_mapping: Dict[str, Any] = {}

        for secret_or_identity, credentials_components in mapping.items():
            encrypted_mapping[secret_or_identity] = []
            for component in credentials_components:
                encrypted_component = {}
                for key, value in component.items():
                    encrypted_component[key] = self._repository_encryptor.decrypt(value).decode()

                encrypted_mapping[secret_or_identity].append(encrypted_component)

        return encrypted_mapping

    @staticmethod
    def _remove_credentials_fom_collection(collection):
        try:
            collection.delete_many({})
        except RemovalError as err:
            raise err
