# pylint: disable=C
import unittest

import src.crypto.fernet as fernet


def test_encrypt_fernet(self):
    """
    Test fernet encryption.
    """
    test_data = b"password"
    key = b"\x02\xd5LGK?\t\x82WOH/\xcc\xbb\xdd\xde\x10\x91\xf2|\xd2Q\x08\xb0b\x95\xc80\x8b\x92\xe5i"
    enc = fernet.encrypt_fernet(test_data, key)
    expected = b"gAAAAABmtM5-uYgymge8bM_BBpQvEGudcbq4bMrS3BlNf6IBS_WCdiS_BFGeWxwQv1PeR6DGjaVb2xvf05jRojU3goZRrOJ85A=="
    self.assertEqual(enc, expected)


def test_encrypt_fernet(self):
    """
    Test fernet decryption.
    """
    test_ciphertext = b"gAAAAABmtM5-uYgymge8bM_BBpQvEGudcbq4bMrS3BlNf6IBS_WCdiS_BFGeWxwQv1PeR6DGjaVb2xvf05jRojU3goZRrOJ85A=="
    key = b"\x02\xd5LGK?\t\x82WOH/\xcc\xbb\xdd\xde\x10\x91\xf2|\xd2Q\x08\xb0b\x95\xc80\x8b\x92\xe5i"
    dec = fernet.decrypt_fernetcrypt_fernet(test_ciphertext, key)
    expected = b"password"
    self.assertEqual(dec, expected)
