from passlib.hash import pbkdf2_sha256


class PasswordManager:
    @staticmethod
    def gen_hash(password: str) -> str:
        return pbkdf2_sha256.hash(password)

    @staticmethod
    def verify(password: str, hash_: str) -> bool:
        return pbkdf2_sha256.verify(password, hash_)
