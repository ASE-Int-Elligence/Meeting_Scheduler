from backend.login import login_email, login_username, create_user
from backend.Models import db, User
# import main
import unittest

# class login_and_signup_unittest(unittest.TestCase):

#     def test_login_success(self):
#         res = login_page("user1", "password")
#         self.assertTrue(res)

#     def signup_success(self):
#         res = sign_up("user7","password7","G","chandana","email@gmail.com","125")
#         self.assertEqual(res,"The row has been inserted")

class LoginTest(unittest.TestCase):

    def test_login_email(self):
        self.assertTrue(login_email("example@gmail.com", "admin"))
        self.assertFalse(login_email("example@gmail.com", "a"))
        self.assertFalse(login_email("example@hotmail.com", "admin"))
        self.assertFalse(login_email("example", "a"))

    def test_login_username(self):
        self.assertTrue(login_username("admin", "admin"))
        self.assertFalse(login_username("admin", "a"))
        self.assertFalse(login_username("e1234", "admin"))
        self.assertFalse(login_username("example", "a"))

    def test_create_user(self):
        create_user(email="testuser@gmail.com", password="test", username="testuser", firstname="Eddie", lastname="Black")

        user = User.query.filter(email="testuser@gmail.com").first()

        self.assertEqual(user.password, 'test')
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.firstname, 'Eddie')
        self.assertEqual(user.lastname, 'Black')
        

if __name__ == '__main__':
    unittest.main()