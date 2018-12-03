import json

# Include Flask packages
from flask import Flask
from flask import request
import copy
import Database_op
import requests
import urllib.request

# The main program that executes. This call creates an instance of a
# class and the constructor starts the runtime.
app = Flask(__name__)

def parse_and_print_args():
    fields = None
    in_args = None
    if request.args is not None:
        in_args = dict(copy.copy(request.args))
        fields = copy.copy(in_args.get('fields', None))
    if fields:
        del(in_args['fields'])
    try:
        print (request)
        if request.data:
            body = json.loads(request.data)
        else:
            body = None
    except Exception as e:
        print ("Got exception = ", e)
        body = None
    print("Request.args : ",json.dumps(in_args))
    return in_args, fields, body


@app.route('/login', methods = ['POST'])
def login_page():
    in_args, fields, body = parse_and_print_args()
    print(body)
    res= Database_op.find_by_pk("user_credentials",body["username"])
    if res[0]['password'] == body["password"]:
        return json.dumps("Login Successful"), 200, {"content-type": "application/json; charset: utf-8"}
    else:
        return json.dumps("Login Failed"), 400, {"content-type": "application/json; charset: utf-8"}

@app.route('/signup', methods = ['POST'])
def signup_page():
    in_args, fields, body = parse_and_print_args()
    res= Database_op.insert("user_credentials",body)
    return "Signup successful"

'''
input for create groups
{
            "users": ["G.priya","G.chandu"],
            "groupName": "Sample group",
            "groupType":"Personal"
}
'''

@app.route('/create_group', methods = ['POST'])   ## Get default meeting-id in body
def create_group():
    in_args, fields, body = parse_and_print_args()
    res= Database_op.insert_group("usergroups",body)
    return "Group Creation successful"

@app.route('/add_users_to_group', methods = ['POST'])   ## Get default meeting-id in bodydef create_group(groupID,groupName,groupTypes):
def add_users_to_group():
    in_args, fields, body = parse_and_print_args()
    res= Database_op.insert_group("usergroups",body)
    return "User added to Group successfully"

@app.route('/search_user', methods = ['POST'])
def search_user():
    in_args, fields, body = parse_and_print_args()
    res= Database_op.find_partial("user_credentials",body)
    return json.dumps(res), 200, {"content-type": "application/json; charset: utf-8"}

@app.route('/display_members', methods = ['POST'])      #username
def display_members():
    in_args, fields, body = parse_and_print_args()
    res= Database_op.find_partial("user_credentials",body)
    return json.dumps(res), 200, {"content-type": "application/json; charset: utf-8"}

@app.route('/display_groups', methods = ['POST'])      #print all groups that user belongs to
def display_groups():
    in_args, fields, body = parse_and_print_args()
    res= Database_op.find_groups("user_credentials",body)
    ans = {}
    i = 0
    for r in res:
        ans[str(i)] = r
        i = i + 1
    print (ans)
    return json.dumps(ans), 200, {"content-type": "application/json; charset: utf-8"}

'''
input for upated_group: updated values corresponding to each value
{
    "groupName": "Sample group",
    "groupType":"Personal"
}
'''
'''
we query with where clause on body["groupID"]
'''
@app.route('/update_group', methods = ['PUT']) 
def update_group():
    in_args, fields, body = parse_and_print_args()
    res= Database_op.update_group_info("usergroups",body)
    return "Group Updation successful"

'''
we query with where clause on body["groupID"]
'''

@app.route('/remove_group/groupID', methods = ['POST']) 
def remove_group(groupID):
    in_args, fields, body = parse_and_print_args()
    res= Database_op.remove_group("usergroups",groupID)
    return "Group deletion successful"


@app.route('/individual_groups', methods = ['POST'])      #print all user_details where users belong to that group
def ind_groups():
    in_args, fields, body = parse_and_print_args()
    res= Database_op.print_indgroups("user_credentials",body)
    ans = {}
    i = 0
    for r in res:
        ans[str(i)] = r
        i = i + 1
    return json.dumps(ans), 200, {"content-type": "application/json; charset: utf-8"}

@app.route('/create_meeting', methods = ['POST'])   ## Get default meeting-id in body
def create_meeting():
    in_args, fields, body = parse_and_print_args()
    res= Database_op.create_meeting("meeting",body)
    return "Meeting Creation successful"

'''
sample input (body)
{
            "meetingID":"1",
            "username": "priya",
            "meetingLoc":"location string",
            "groupID":"1",
            "meetingname":"ASE project discussion"
}
'''

@app.route('/update_meeting', methods = ['PUT']) 
def update_meeting():
    in_args, fields, body = parse_and_print_args()
    res= Database_op.update_meeting_info("meeting",body)
    return "Group Updation successful"

@app.route('/get_meetings/<username>', methods = ['POST']) 
def get_meeting(username):
    in_args, fields, body = parse_and_print_args()
    res= Database_op.get_meeting_list(username)
    return res

@app.route('/remove_meeting/<meetingID>', methods = ['POST']) 
def remove_meeting(meetingID):
    in_args, fields, body = parse_and_print_args()
    res= Database_op.remove_meeting("meeting",meetingID)
    return res

@app.route('/handle_mapdata',methods = ['POST'])
def mapdata():
    in_args, fields, body = parse_and_print_args()
    print("latitude",request.form['latitude'])
    print("longitutde",request.form['longitude'])
    #result = {'latitude':request.form['latitude'],'longitutde':request.form['longitude']}
    url = "https://maps.googleapis.com/maps/api/geocode/json?latlng="+request.form['latitude']+','+request.form['longitude']+"&sensor=true_or_false&key=AIzaSyCyADWR91wYDIC3PiVhO3t6l_EQRslBl_s"
    result = urllib.request.urlopen(url).read()
    #print("result:",result)
    #return result
    return result, 200, {"content-type": "application/json; charset: utf-8"}

if __name__ == '__main__':
    app.run()
