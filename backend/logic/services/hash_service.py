import bcrypt
from backend.config import PEPPER


class HashService():
    def password_hasher(self, raw_password: str, salt: bytes) -> str:
        password = bytes(PEPPER + raw_password, encoding="utf-8")
        hashed = bcrypt.hashpw(password, salt)
        return hashed.decode()
    
    def generate_salt(self) -> bytes:
        salt = bcrypt.gensalt()
        return salt