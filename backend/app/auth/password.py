import logging

from passlib.context import CryptContext

# passlib 1.7.4 probes ``bcrypt.__about__``, which bcrypt 4.x removed. The
# probe failure is caught by passlib and is harmless, but it prints a
# misleading traceback on the first hash; silence that one logger.
logging.getLogger("passlib.handlers.bcrypt").setLevel(logging.ERROR)

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str
) -> bool:
    return pwd_context.verify(
        plain_password,
        hashed_password
    )