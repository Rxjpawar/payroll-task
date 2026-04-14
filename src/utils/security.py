import hashlib
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    # pre-hash with SHA-256 to handle long passwords safely,
    # then truncate to 72 bytes to respect bcrypt's limit
    sha256_hash = hashlib.sha256(password.encode()).hexdigest()  # 64-char hex string
    return pwd_context.hash(sha256_hash[:72])

def verify_password(plain_password: str, hashed_password: str) -> bool:
    sha256_hash = hashlib.sha256(plain_password.encode()).hexdigest()
    return pwd_context.verify(sha256_hash[:72], hashed_password)