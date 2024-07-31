# pylint: disable=C
import unittest
import main


class TestMain(unittest.TestCase):
    def test_sanity_check(self):
        sanity_var = True
        true_var = True
        false_var = False
        self.assertEqual(true_var, sanity_var)
        self.assertNotEqual(false_var, sanity_var)
