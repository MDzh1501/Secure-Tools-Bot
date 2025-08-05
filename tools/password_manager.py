import os
from dotenv import load_dotenv
from cryptography.fernet import Fernet
from .password_config import CryptoConfig
from .config_loader import load_crypto_config

load_dotenv()

def encrypt_pwd(msg: str) -> dict:
    pwd = os.getenv("KEY_PWD")
    if not pwd:
        raise ValueError("Missing KEY_PWD in environment")

    config = load_crypto_config()
    
    cfg = CryptoConfig(
        password=pwd.encode(),
        algorithm=config["algorithm"],
        iterations=config["iterations"],
        length=config["length"]
    )

    key = cfg.get_key()
    f = Fernet(key)
    token = f.encrypt(msg.encode())

    return {
        "encrypted": token.decode(),
        "salt": cfg.salt_b64()
    }


def decrypt_pwd(encrypted_pwd: str, salt_b64: str) -> str:
    pwd = os.getenv("KEY_PWD")
    if not pwd:
        raise ValueError("Missing KEY_PWD in environment")

    config = load_crypto_config()
    salt = CryptoConfig.salt_from_b64(salt_b64)

    cfg = CryptoConfig(
        password=pwd.encode(),
        algorithm=config["algorithm"],
        iterations=config["iterations"],
        length=config["length"],
        salt=salt
    )

    key = cfg.get_key()
    f = Fernet(key)

    return f.decrypt(encrypted_pwd.encode()).decode()