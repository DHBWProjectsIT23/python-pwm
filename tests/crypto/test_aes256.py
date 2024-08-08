# pylint: disable=C
import unittest

import src.crypto.aes256 as aes


class TestCryptoAES(unittest.TestCase):
    def test_aes_256_encrypt(self):
        """
        Test AES-256 encrypting.
        """
        


    def test_aes_256_decrypt(self):
        """
        Test AES-256 decrypting.
        """
        ciphertext = b'\xce:\x9f\x07\xd89\xb1p \xfc\xc3\xe0KbKx\xe1{.\xb5\x08\xa9\x06\x8b=\x91f\x96v\x8a43\xebf\xf5\x0by\xd5\x1b\x025\xaaW\xebW\x83\xdb*\xcc\xff>I\xc4\x8a\x9a\xd8\x83\x15\xa6Hh\x8b;g'
        key = b'3)\x0e\xb7QX\x94R\x84\x1a\xa4K\xef\xd4\xc6>\x99v\x0ez~+\xd9+:\xaa*\x04G\xa3M\xd7'
        expected = b'Dies ist ein geheimer Text mit AES.'
        dec = aes.decrypt_aes(ciphertext, key)
        self.assertEqual(dec, expected)

