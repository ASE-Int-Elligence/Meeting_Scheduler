
import Database_op
import copy

def login_page(username,password):

    result = Database_op.find_by_primary_key("user_credentials", username)
    if password == result[0]['password']:
        return True
    else:
        return False

def sign_up(username,password, nameLast,nameFirst,email,DOB):
    template={}
    template['username']=username
    template['nameFirst'] = nameFirst
    template['nameLast'] = nameLast
    template['email'] = email
    template['DOB'] = DOB
    template['password'] = password
    result = Database_op.create_user("user_credentials",template)
    return result

if __name__ == '__main__':
    result = sign_up("user4","password3","priya","chandana","email@gmail.com","125")
    print(result)
