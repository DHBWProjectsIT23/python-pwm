# pylint: disable=C
import unittest

import src.crypto.hashing as crypto


class TestCrypto(unittest.TestCase):
    def test_sha_256(self):
        """
        Test SHA-256 hashing with a basic string input.
        """
        string = "test"
        expected_hash = (
            "9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08"
        )
        has = crypto.hash_sha256(string.encode())
        self.assertEqual(has.hex(), expected_hash)
