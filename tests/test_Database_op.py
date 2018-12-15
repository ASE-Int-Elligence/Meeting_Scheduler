import unittest
import os
import sys
sys.path.append("../")
from src.backend import Database_op as db_op

def cleanup_account(template):

    print("cleanup")
    cleanup_meeting({'username':template['username']})
    cleanup_groups({'username':template['username']})
    db_op.remove_account('user_credentials',template)

def cleanup_groups(template):
    groups = db_op.find_groups('usergroups',template)
    for group in groups:
        res = db_op.remove_group('usergroups',group)

def cleanup_meeting(template):
    meeting = db_op.print_indmeeting('meeting',{'username':template['username'],'groupName':"testgroupname"})
    print("meeting:",meeting)
    if(len(meeting)>0):
        db_op.remove_meeting('meeting',meeting[0]['meetingID'])
    else:
        meeting = db_op.print_indmeeting('meeting',{'username':template['username'],'groupName':"updated groupname"})
        if(len(meeting)>0):
            db_op.remove_meeting('meeting',meeting[0]['meetingID'])


class Unit_testing(unittest.TestCase):
    """
    """
    # @unittest.skip()
    # def cleanup(self):
    #     template = {}
    #     template['username']='testuser'
    #     template['password']='pass'
    #     template['nameFirst']='testfirstname'
    #     template['nameLast']='testLastname'
    #     template['email']='testemail'
    #     template['dob']='testdob'
    #     template['users']=['testuser']
    #     template['groupID']='100'
    #     template['groupName']='testgroupname'
    #     template['groupType']='testgrouptype'
    #     template['meetingname']='testmeetingname'
    #     template['meetingLoc']='testmeetingloc'
    #     for user in template['users']:
    #         self.cleanup_groups({'username':user})
    #     self.cleanup_account(template)
 
    def test_add_account(self):
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
        cleanup_account(template)
        result = db_op.insert('user_credentials',template)
        self.assertEqual(result, "Insert Successful")

    def test_add_groups(self):
        print("hello")
        template = {}
        template['users']=['testuser']
        template['groupID']='100'
        template['groupName']='testgroupname'
        template['groupType']='testgrouptype'
        #template['username']='testusername'
        for user in template['users']:
            cleanup_groups({'username':user})
      
        result = db_op.insert_group('usergroups',template)
        self.assertEqual(result, "Group Creation Successful")

    def test_add_meeting(self):
        template = {}
        template['username']='testuser'
        template['groupID']='1'
        template['meetingname']='testmeetingname'
        template['meetingLoc']='testmeetingloc'

        #template['meetingID']='100'
        #template['username']='testusername'
        # for user in template['users']:
        #     self.cleanup_groups({'username':user})

        cleanup_meeting(template)
        result = db_op.create_meeting('meeting',template)
        self.assertEqual(result, "Meeting Creation Successful")

    def test_update_meeting(self):
        template = {}
        meeting = db_op.show_meeting('meeting',{'username':'testuser'})
        #meeting = db_op.print_indmeeting('meeting',{'username':"testuser",'groupName':"testgroupname"})
        print("meeting = ",meeting)
        no_meeting = True
        if(len(meeting)>0):
            no_meeting = False
            template['meetingname']='updated meeting name'
            template['meetingID'] = meeting[0]['meetingID']
            result = db_op.update_meeting_info('meeting',template)
            self.assertEqual(result, "Updated Meeting")
        else:
            self.assertTrue(no_meeting)

    def test_update_group(self):
        template = {}
        group = db_op.find_groups('usergroups',{'username':"testuser",'groupName':"testgroupname"})
        no_group = True
        if(len(group)>0):
            no_group = False
            template['groupName']='updated groupname'
            template['groupID'] = group[0]['groupID']
            result = db_op.update_group_info('usergroups',template)
            self.assertEqual(result, "Updated Group")
        else:
            self.assertTrue(no_group)

    def test_print_indgroups(self):
        template = {}
        group = db_op.print_indgroups('meeting',{'username':"testuser",'groupName':"testgroupname",'groupID':'1'})
        no_group = True
        if(len(group)>0):
            no_group = False
            self.assertFalse(no_group)
        else:
            self.assertTrue(no_group)

    def test_find_partial(self):
        user = db_op.find_partial('user_credentials',{'username':'test'})
        no_user = True
        if(len(user)>0):
            no_user = False
            self.assertEqual(user[0]['username'],'testuser')
        else:
            self.assertTrue(no_group)

    def test_find_by_pk(self):
        user = db_op.find_by_pk('user_credentials','username',fields = None)
        no_user = True
        if(len(user)>0):
            no_group = False
            self.assertFalse(no_user)
        else:
            self.assertTrue(no_user)

    def test_find_by_pk_fields(self):
        user = db_op.find_by_pk('user_credentials','username',fields = 'username')
        no_user = True
        if(len(user)>0):
            no_group = False
            self.assertFalse(no_user)
        else:
            self.assertTrue(no_user)

    def test_templateToWhereClause_old_s(self):
        template = db_op.templateToWhereClause_old({'username':'testuser','nameFirst':'testfirstname'})
        no_template = True
        if(len(template)>0):
            no_template = False
            self.assertFalse(no_template)
        else:
            self.assertTrue(no_template)

    def test_templateToWhereClause_old_for_empty_s(self):
        template = db_op.templateToWhereClause_old({})
        no_template = True
        if(len(template)>0):
            no_template = False
            self.assertFalse(no_template)
        else:
            self.assertTrue(no_template)

    def test_run_q_fetch(self):
        template = db_op.run_q("select 8 from usergroups",None,fetch = True)
        no_template = True
        if(len(template)>0):
            no_template = False
            self.assertFalse(no_template)
        else:
            self.assertTrue(no_template)

    def test_run_q_no_fetch(self):
        template = db_op.run_q("select 8 from usergroups",None,fetch = False)
        no_template = True
        if(template is None):
            no_template = False
            self.assertFalse(no_template)
        else:
            self.assertTrue(no_template)

    # def test_delete_account(self):
    #     template = {}
    #     template['username']='testuser'
    #     template['password']='pass'
    #     template['nameFirst']='testfirstname'
    #     template['nameLast']='testLastname'
    #     template['email']='testemail'
    #     template['dob']='testdob'
    #     cleanup_account({'username':template['username']})
    #     result = db_op.remove_account('user_credentials',template)
    #     self.assertEqual(result, "Deleted Account")


if __name__ == '__main__':
    unittest.main()
    #run_tests()