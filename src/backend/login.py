
# from backend.Database_op import *
# # import Database_op
# import copy

# def login_page(username,password):

#     result = find_by_primary_key("user_credentials", username)
#     if password == result[0]['password']:
#         return True
#     else:
#         return False

# def sign_up(username,password, nameLast,nameFirst,email,DOB):
#     template={}
#     template['username']=username
#     template['nameFirst'] = nameFirst
#     template['nameLast'] = nameLast
#     template['email'] = email
#     template['DOB'] = DOB
#     template['password'] = password
#     result = create_user("user_credentials",template)
#     return result

# if __name__ == '__main__':
#     result = sign_up("user4","password3","priya","chandana","email@gmail.com","125")
#     print(result)

from backend.Models import db, User

def login_username(username, password):
    user = User.query.filter_by(username=username).first()
    if not user:
        return False
    else:
        if password == user.password:
            return True
        else:
            return False

def login_email(email, password):
    user = User.query.filter_by(email=email).first()
    if not user:
        return False
    else:
        if password == user.password:
            return True
        else:
            return False

def create_user(email, password, username, firstname, lastname):
    user = User(email=email, password=password, username=username, firstname=firstname, lastname=lastname)
    db.session.add(user)
    db.session.commit()

if __name__ == "__main__":
    print(login_username("test", "alsotest"))
    print(login_username("admin", "admin"))


