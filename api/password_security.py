"""Password hashing policy, independent of database and web framework.

Stored scrypt parameters are strictly validated before running a costly KDF.
Only the application's currently issued format is accepted; changes require
an explicit, tested migration strategy.
"""
import hashlib
import hmac
import os

_SCRYPT_N = 16384
_SCRYPT_R = 8
_SCRYPT_P = 1
_SALT_BYTES = 16
_DIGEST_BYTES = 64
_MAX_PASSWORD_BYTES = 1024


def hash_password(password: str) -> str:
    """Create a salted scrypt hash in the existing database-compatible format."""
    encoded = password.encode("utf-8")
    if len(encoded) > _MAX_PASSWORD_BYTES:
        raise ValueError("Password exceeds hashing limit")
    salt = os.urandom(_SALT_BYTES)
    digest = hashlib.scrypt(encoded, salt=salt, n=_SCRYPT_N, r=_SCRYPT_R, p=_SCRYPT_P)
    return f"scrypt${_SCRYPT_N}${_SCRYPT_R}${_SCRYPT_P}${salt.hex()}${digest.hex()}"


def verify_password(password: str, stored: str) -> bool:
    """Reject malformed or resource-intensive hash parameters without executing scrypt."""
    if not isinstance(password, str) or not isinstance(stored, str):
        return False
    encoded = password.encode("utf-8")
    if len(encoded) > _MAX_PASSWORD_BYTES or len(stored) > 256:
        return False
    try:
        algorithm, n, r, p, salt_hex, digest_hex = stored.split("$")
        if (algorithm, n, r, p) != ("scrypt", "16384", "8", "1"):
            return False
        if len(salt_hex) != _SALT_BYTES * 2 or len(digest_hex) != _DIGEST_BYTES * 2:
            return False
        salt = bytes.fromhex(salt_hex)
        expected = bytes.fromhex(digest_hex)
        actual = hashlib.scrypt(encoded, salt=salt, n=_SCRYPT_N, r=_SCRYPT_R, p=_SCRYPT_P)
        return hmac.compare_digest(actual, expected)
    except (ValueError, TypeError, OverflowError):
        return False
