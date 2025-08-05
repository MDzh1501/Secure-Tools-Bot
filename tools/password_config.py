from dataclasses import dataclass
import os
import base64
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes

@dataclass
class CryptoConfig:
    password: bytes
    algorithm: str
    iterations: int
    length: int
    salt: bytes = None

    def __post_init__(self):
        if self.salt is None:
            self.salt = os.urandom(16)

    def get_key(self) -> bytes:
        algo_class = getattr(hashes, self.algorithm)
        kdf = PBKDF2HMAC(
            algorithm=algo_class(),
            length=self.length,
            salt=self.salt,
            iterations=self.iterations,
        )
        return base64.urlsafe_b64encode(kdf.derive(self.password))

    def salt_b64(self) -> str:
        return base64.urlsafe_b64encode(self.salt).decode()

    @staticmethod
    def salt_from_b64(s: str) -> bytes:
        return base64.urlsafe_b64decode(s)