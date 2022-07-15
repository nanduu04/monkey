from pathlib import Path

from cryptography.fernet import Fernet

from monkey_island.cc.server_utils.file_utils import open_new_securely_permissioned_file

from . import ILockableEncryptor, LockedKeyError, ResetKeyError, UnlockError
from .key_based_encryptor import KeyBasedEncryptor
from .password_based_bytes_encryptor import PasswordBasedBytesEncryptor


class RepositoryEncryptor(ILockableEncryptor):
    _KEY_LENGTH_BYTES = 32

    def __init__(self, key_file: Path):
        self._key_file = key_file
        self._password_based_encryptor = None
        self._key_based_encryptor = None

    def unlock(self, secret: bytes):
        try:
            self._password_based_encryptor = PasswordBasedBytesEncryptor(secret.decode())
            self._key_based_encryptor = self._initialize_key_based_encryptor()
        except Exception as err:
            raise UnlockError(err)

    def _initialize_key_based_encryptor(self):
        if self._key_file.is_file():
            return self._load_key()

        return self._create_key()

    def _load_key(self) -> KeyBasedEncryptor:
        with open(self._key_file, "rb") as f:
            encrypted_key = f.read()

        plaintext_key = self._password_based_encryptor.decrypt(encrypted_key)
        return KeyBasedEncryptor(plaintext_key)

    def _create_key(self) -> KeyBasedEncryptor:
        plaintext_key = Fernet.generate_key()

        encrypted_key = self._password_based_encryptor.encrypt(plaintext_key)
        with open_new_securely_permissioned_file(str(self._key_file), "wb") as f:
            f.write(encrypted_key)

        return KeyBasedEncryptor(plaintext_key)

    def lock(self):
        self._key_based_encryptor = None

    def reset_key(self):
        try:
            if self._key_file.is_file():
                self._key_file.unlink()
        except Exception as err:
            raise ResetKeyError(err)

        self._password_based_encryptor = None
        self._key_based_encryptor = None

    def encrypt(self, plaintext: bytes) -> bytes:
        if self._key_based_encryptor is None:
            raise LockedKeyError("Cannot encrypt while the encryptor is locked")

        return self._key_based_encryptor.encrypt(plaintext)

    def decrypt(self, ciphertext: bytes) -> bytes:
        if self._key_based_encryptor is None:
            raise LockedKeyError("Cannot decrypt while the encryptor is locked")

        return self._key_based_encryptor.decrypt(ciphertext)
