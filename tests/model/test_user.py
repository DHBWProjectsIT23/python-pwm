# pylint: disable=C

import unittest

from src.model.user import User
from src.model.password import Password
from src.crypto.hashing import hash_sha256


class TestUser(unittest.TestCase):
    def test_init_user(self):
        user_password = Password("test")
        username = hash_sha256(b"test")
        user = User(username, user_password)
        self.assertTrue(isinstance(user, User))
        self.assertEqual(user.username, hash_sha256(b"test"))
        self.assertEqual(user.password(), hash_sha256(b"test"))

    def test_init_static_user(self):
        user = User.new("test", "test")
        self.assertTrue(isinstance(user, User))
        self.assertEqual(user.username, hash_sha256(b"test"))
        self.assertEqual(user.password(), hash_sha256(b"test"))
