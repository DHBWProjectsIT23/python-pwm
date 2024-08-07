import pickle
import unittest

from src.crypto.placeholder import dummy_decrypt_fernet
from src.model.metadata import EncryptedMetadata
from src.model.metadata import Metadata
from src.model.password import Password
from src.model.password_information import PasswordInformation
from src.model.password_information import adapt_password_information
from src.model.password_information import convert_password_information
from src.model.user import User


class TestPasswordInformation(unittest.TestCase):
    def test_init(self):
        info, pw, user = create_test_info()

    def test_note(self):
        info, pw, user = create_test_info()
        note = "This password is a test"
        info.set_note(note)
        self.assertEqual(info.note, note)

    def test_category_maximum(self):
        info, pw, user = create_test_info()
        categories = ["Test", "Old", "Password"]
        info.add_categories(categories)
        more_categories = ["AnotherTest"], ["Safe"], ["Uncool"]
        self.assertRaises(ValueError, info.add_categories, more_categories)
        info.add_category("AnotherTest")
        info.add_category("Safe")
        self.assertRaises(ValueError, info.add_category, "Uncool")

    def test_duplicate_category(self):
        info, pw, user = create_test_info()
        info.add_category("Test")
        self.assertRaises(ValueError, info.add_category, "Test")

    def test_encrypt(self):
        info, pw, user = create_test_info()
        info.add_password(Password("test2"))
        for password in info.passwords:
            self.assertFalse(password.is_encrypted)
            self.assertTrue(isinstance(password.metadata, Metadata))

        info.encrypt("FakeKey")
        for password in info.passwords:
            self.assertTrue(password.is_encrypted)
            self.assertTrue(isinstance(password.metadata, EncryptedMetadata))

    def test_decrypt(self):
        info, pw, user = create_test_info()

        info.add_password(Password("test2"))
        info.encrypt("FakeKey")
        for password in info.passwords:
            self.assertTrue(password.is_encrypted)
            self.assertTrue(isinstance(password.metadata, EncryptedMetadata))

        info.decrypt("FakeKey")
        for password in info.passwords:
            self.assertFalse(password.is_encrypted)
            self.assertTrue(isinstance(password.metadata, Metadata))

    def test_adapter(self):
        info, pw, user = create_test_info()
        self.assertRaises(ValueError, adapt_password_information, info)
        info.encrypt("FakeKey")
        adapted = adapt_password_information(info)
        decrypted = dummy_decrypt_fernet(adapted)
        returned_info = pickle.loads(decrypted)
        self.assertTrue(isinstance(returned_info, PasswordInformation))
        self.assertEqual(pickle.dumps(info), pickle.dumps(returned_info))

    def test_converter(self):
        info, pw, user = create_test_info()
        self.assertRaises(ValueError, adapt_password_information, info)
        info.encrypt("FakeKey")
        adapted = adapt_password_information(info)
        decrypted = dummy_decrypt_fernet(adapted)
        returned_info = pickle.loads(decrypted)
        converted_info = convert_password_information(adapted)
        self.assertTrue(isinstance(converted_info, PasswordInformation))
        self.assertEqual(pickle.dumps(converted_info), pickle.dumps(returned_info))
        self.assertEqual(pickle.dumps(converted_info), pickle.dumps(info))


def create_test_info() -> tuple[PasswordInformation, Password, User]:
    test_password = Password("test")
    test_user = User.new("test_user", "test_user_pw")
    test_info = PasswordInformation(test_user, test_password, "Test Password")
    return test_info, test_password, test_user
