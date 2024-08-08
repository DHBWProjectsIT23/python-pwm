import pickle
import unittest
from src.model.password import Password, adapt_password, convert_password
from src.exceptions.encryption_exception import EncryptionException


class TestPassword(unittest.TestCase):
    def setUp(self):
        self.password = Password("test_password")
        self.user_password = "FakePassword"

    def test_encrypt_decrypt(self):
        self.password.encrypt(self.user_password)
        self.assertTrue(self.password.is_encrypted)
        encrypted_password = self.password()
        self.password.decrypt(self.user_password)
        self.assertFalse(self.password.is_encrypted)
        self.assertNotEqual(encrypted_password, self.password())

    def test_make_master(self):
        self.password.make_master()
        self.assertTrue(self.password.is_master)
        with self.assertRaises(ValueError):
            self.password.make_master()

    def test_encrypt_master_password(self):
        self.password.make_master()
        with self.assertRaises(EncryptionException):
            self.password.encrypt(self.user_password)

    def test_decrypt_master_password(self):
        self.password.make_master()
        with self.assertRaises(EncryptionException):
            self.password.decrypt(self.user_password)

    def test_adapt_password(self):
        self.password.encrypt(self.user_password)
        serialized_password = adapt_password(self.password)
        self.assertIsInstance(serialized_password, bytes)

    def test_convert_password(self):
        self.password.encrypt(self.user_password)
        serialized_password = adapt_password(self.password)
        deserialized_password = convert_password(serialized_password)
        self.assertIsInstance(deserialized_password, Password)
        self.assertTrue(deserialized_password.is_encrypted)

    def test_adapt_password_not_encrypted(self):
        with self.assertRaises(TypeError):
            adapt_password(self.password)

    def test_convert_password_invalid_type(self):
        invalid_type = pickle.dumps("not_a_password")
        with self.assertRaises(TypeError):
            convert_password(invalid_type)
