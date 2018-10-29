import main
import unittest

class login_and_signup_unittest(unittest.TestCase):

    def test_login_success(self):
        res = main.login_page("user1", "password")
        self.assertTrue(res)

    def signup_success(self):
        res = main.sign_up("user7","password7","G","chandana","email@gmail.com","125")
        self.assertEqual(res,"The row has been inserted")

if __name__ == '__main__':
    unittest.main()