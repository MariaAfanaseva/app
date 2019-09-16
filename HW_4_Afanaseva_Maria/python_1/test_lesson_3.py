import unittest
from lesson_3 import about_user, max_function, long_str


class TestHW(unittest.TestCase):
    def test_about_user(self):
        self.assertEqual(about_user('Mark', 23, 'London'), 'Mark, 23 год(а), проживает в городе London')

    def test_about_user_isinstance(self):
        self.assertIsInstance(about_user('Mark', 23, 'London'), str)

    def test_about_user_in(self):
        self.assertIn('London', about_user('Mark', 23, 'London'))

    def test_max_function_not(self):
        self.assertNotEqual(max_function(4, 8, 6), 6)

    def test_max_function_true(self):
        self.assertTrue(max_function(4, 8, 6))

    def test_max_function_false(self):
        self.assertFalse(max_function(0, 0, 0))

    def test_long_str(self):
        self.assertIsNotNone(long_str('aa', 'bbb', 'cccc'))


if __name__ == '__main__':
    unittest.main()
