# pylint: disable=C
import unittest

import src.crypto.password_util as util


def test_validate_password_safety(self):
    """
    Test password validation.
    """
    test_password = "0rz06mRNTKDkkZ9cE"
    score = util.validate_password_safety(test_password)
    expected_score = 4
    self.assertEqual(score, expected_score)
