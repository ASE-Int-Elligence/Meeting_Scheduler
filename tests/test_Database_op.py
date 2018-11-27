import unittest
import os
import sys
sys.path.append("../")
from src.backend import Database_op as db_op

class TestAdd(unittest.TestCase):
    """
    Test the add function from the mymath library
    """

    def cleanup(self,table,template):
        db_op.remove_account('user_credentials',template)
 
    def test_add_groups(self):
        """
        Test that the addition of two integers returns the correct total
        """
        template = {}
        template['username']='testuser'
        template['password']='pass'
        template['nameFirst']='testfirstname'
        template['nameLast']='testLastname'
        template['email']='testemail'
        template['dob']='testdob'
        self.cleanup('user_credentials',template)
        result = db_op.insert('user_credentials',template)
        self.assertEqual(result, "Insert Successful")
 
    # def test_add_floats(self):
    #     """
    #     Test that the addition of two floats returns the correct result
    #     """
    #     result = mymath.add(10.5, 2)
    #     self.assertEqual(result, 12.5)
 
    # def test_add_strings(self):
    #     """
    #     Test the addition of two strings returns the two string as one
    #     concatenated string
    #     """
    #     result = mymath.add('abc', 'def')
    #     self.assertEqual(result, 'abcdef')
 
 
if __name__ == '__main__':
    unittest.main()