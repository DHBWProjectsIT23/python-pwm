import unittest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

import src.crypto.hashing as crypto


class TestCrypto(unittest.TestCase):
    def test_sha_256(self):
        string = "test"
        expected_hash = (
            "9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08"
        )
        has = crypto.hash_sha256(string.encode())
        self.assertEqual(has.hex(), expected_hash)
