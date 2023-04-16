from passlib.hash import pbkdf2_sha256


def encrypt_passwd(passwd: str) -> str:
    return pbkdf2_sha256.hash(passwd)


def verify_passwd(passwd: str, hash: str) -> bool:
    return pbkdf2_sha256.verify(passwd, hash)
