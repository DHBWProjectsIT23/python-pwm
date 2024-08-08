# pylint: disable=C
import unittest

import src.crypto.key_derivation as kdf


def test_scrypt_derive(self):
    """
    Test password derivation.
    """
    test_pw = b"password"
    salt = b"\x88w\xa2\x81\xdc\xc43QVI\xcfe0\xc1\x93\xab"
    key = kdf.scrypt_derive(test_pw, salt)
    expected_key = b"\x13\xe1\xd4\xf7\xbaKf\x9f\xc81\x86\xc5\xba\xb1\x0e;\xd0\x8d\x9c\x1c\x03w\xa5}\x8a\xf7\x10h\xb4\xd7\x92\x1f"
    self.assertEqual(key, expected_key)


def test_scrypt_derive(self):
    """
    Test password verification.
    """
    test_pw = b"password"
    derived_key = b"\x13\xe1\xd4\xf7\xbaKf\x9f\xc81\x86\xc5\xba\xb1\x0e;\xd0\x8d\x9c\x1c\x03w\xa5}\x8a\xf7\x10h\xb4\xd7\x92\x1f"
    salt = b"\x88w\xa2\x81\xdc\xc43QVI\xcfe0\xc1\x93\xab"
    is_same = kdf.scrypt_verify(test_pw, derived_key, salt)
    self.assertTrue(is_same)
