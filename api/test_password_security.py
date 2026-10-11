"""Database-independent regression tests for password verification policy."""
import pytest

from password_security import hash_password, verify_password


def test_password_round_trip_and_wrong_password():
    stored = hash_password("a valid test password")
    assert stored.startswith("scrypt$16384$8$1$")
    assert verify_password("a valid test password", stored)
    assert not verify_password("wrong password", stored)


@pytest.mark.parametrize("stored", [
    "", "plaintext", "argon2$16384$8$1$bad$bad",
    "scrypt$999999999$8$1$" + "00" * 16 + "$" + "00" * 64,
    "scrypt$16384$999999$1$" + "00" * 16 + "$" + "00" * 64,
    "scrypt$16384$8$999999$" + "00" * 16 + "$" + "00" * 64,
    "scrypt$16384$8$1$zz" + "00" * 15 + "$" + "00" * 64,
    "scrypt$16384$8$1$" + "00" * 16 + "$" + "gg" * 64,
    "scrypt$16384$8$1$" + "00" * 16 + "$" + "00" * 63,
])
def test_malformed_hashes_are_rejected(stored):
    assert not verify_password("a valid test password", stored)


def test_password_input_size_is_bounded():
    huge = "x" * 1025
    with pytest.raises(ValueError):
        hash_password(huge)
    assert not verify_password(huge, hash_password("normal password"))


def test_scrypt_is_not_called_for_untrusted_work_factors(monkeypatch):
    import password_security

    def fail_if_called(*args, **kwargs):
        raise AssertionError("scrypt must not execute on untrusted work factors")

    monkeypatch.setattr(password_security.hashlib, "scrypt", fail_if_called)
    malicious = "scrypt$1073741824$8$1$" + "00" * 16 + "$" + "00" * 64
    assert not verify_password("password", malicious)
