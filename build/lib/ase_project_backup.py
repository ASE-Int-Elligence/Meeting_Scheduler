import json
import webbrowser
# Include Flask packages
from flask import Flask
from flask import request
import copy
import Database_op
import requests
import urllib
import ast
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
    print ("Jamba lakadi")
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
    return json.dumps("Signup Successful"), 200, {"content-type": "application/json; charset: utf-8"}

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
    return json.dumps("Group Creation Successful"), 200, {"content-type": "application/json; charset: utf-8"}

@app.route('/add_users_to_group', methods = ['POST'])   ## Get default meeting-id in bodydef create_group(groupID,groupName,groupTypes):
def add_users_to_group():
    in_args, fields, body = parse_and_print_args()
    res= Database_op.insert_group("usergroups",body)
    return json.dumps("User added successfully"), 200, {"content-type": "application/json; charset: utf-8"}

@app.route('/add_more_users', methods = ['POST'])   ## Get default meeting-id in bodydef create_group(groupID,groupName,groupTypes):
def add_more_users():
    in_args, fields, body = parse_and_print_args()
    res= Database_op.insert_more_users("usergroups",body)
    return json.dumps("User added successfully"), 200, {"content-type": "application/json; charset: utf-8"}

@app.route('/delete_users_in_group',methods = ['POST'])
def delete_users_from_group():
    in_args, fields, body = parse_and_print_args()
    res = Database_op.delete_user_from_group('usergroups',body)
    return json.dumps("User added successfully"), 200, {"content-type": "application/json; charset: utf-8"}

@app.route('/handle_mapdata',methods = ['POST'])
def mapdata():
    in_args, fields, body = parse_and_print_args()
    print("latitude",request.form['latitude'])
    print("longitutde",request.form['longitude'])
    global lat
    lat = request.form['latitude']
    global lng
    lng = request.form['longitude']
    #result = {'latitude':request.form['latitude'],'longitutde':request.form['longitude']}
    url = "https://maps.googleapis.com/maps/api/geocode/json?latlng="+request.form['latitude']+','+request.form['longitude']+"&sensor=true_or_false&key=AIzaSyCyADWR91wYDIC3PiVhO3t6l_EQRslBl_s"
    result = urllib.request.urlopen(url).read()
    result =  result.decode("utf-8")
    result = ast.literal_eval(result)
    global mapaddress
    mapaddress = str(result["results"][0]["formatted_address"])
    print("mapaddress = ",mapaddress)
    #print("result:",result)
    #return result
    #return mapaddress, 200, {"content-type": "application/json; charset: utf-8"}
    return json.dumps(result,indent=2), 200, {"content-type": "application/json; charset: utf-8"}

@app.route('/get_address',methods = ['POST'])
def get_address():
    global mapaddress
    global lat
    global lng
    result = {'mapaddress':mapaddress,'lat':lat,'lng':lng}
    return json.dumps(result), 200, {"content-type": "application/json; charset: utf-8"}

@app.route('/search_user', methods = ['POST'])
def search_user():
    in_args, fields, body = parse_and_print_args()
    res= Database_op.find_partial("user_credentials",body)
    ans = {}
    x = 0
    for i in res:
        ans[x] = i["username"]
        x += 1
    return json.dumps(ans), 200, {"content-type": "application/json; charset: utf-8"}

@app.route('/display_members', methods = ['POST'])      #username
def display_members():
    in_args, fields, body = parse_and_print_args()
    res= Database_op.find_partial("user_credentials",body)
    return json.dumps(res), 200, {"content-type": "application/json; charset: utf-8"}

@app.route('/display_groups', methods = ['POST'])      #print all groups that user belongs to
def display_groups():
    print ("Calling MEEEEE")
    in_args, fields, body = parse_and_print_args()
    res= Database_op.find_groups("user_credentials",body)
    print ("Answer is", res)
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
    print ("Cometh the hour,cometh the man")
    in_args, fields, body = parse_and_print_args()
    res= Database_op.create_meeting("meeting",body)
    return json.dumps("Yes"), 200, {"content-type": "application/json; charset: utf-8"}

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
    return json.dumps("OK"), 200, {"content-type": "application/json; charset: utf-8"}

@app.route('/remove_meeting/<meetingID>', methods = ['POST'])
def remove_meeting(meetingID):
    in_args, fields, body = parse_and_print_args()
    res= Database_op.remove_meeting("meeting",meetingID)
    return json.dumps("OK"), 200, {"content-type": "application/json; charset: utf-8"}

@app.route('/display_meetings', methods = ['POST'])
def display_meetings():
    in_args, fields, body = parse_and_print_args()
    res= Database_op.show_meeting("meeting",body)
    ans = {}
    i = 0
    for r in res:
        ans[str(i)] = r
        i = i + 1
    return json.dumps(ans), 200, {"content-type": "application/json; charset: utf-8"}

@app.route('/create_todoitem', methods = ['POST'])   ## Get default meeting-id in body
def create_todoitem():
    print ("SRUJANNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN")
    in_args, fields, body = parse_and_print_args()
    res= Database_op.create_todoitem("todolist",body)
    return json.dumps(res), 200, {"content-type": "application/json; charset: utf-8"}

@app.route('/get_todoitem', methods = ['POST'])   ## Get default meeting-id in body
def get_todoitem():
    print ("Cometh the hour,cometh the man")
    in_args, fields, body = parse_and_print_args()
    res= Database_op.get_todoitem("todolist",body)
    return json.dumps(res), 200, {"content-type": "application/json; charset: utf-8"}

@app.route('/save_todoitem', methods = ['POST'])   ## Get default meeting-id in body
def save_todoitem():
    print ("Cometh the hour,cometh the man")
    in_args, fields, body = parse_and_print_args()
    print ("THE SEXY BODY ISSSSS", body)
    res= Database_op.save_todoitem("todolist",body)
    return json.dumps(res), 200, {"content-type": "application/json; charset: utf-8"}

@app.route('/choose_location', methods = ['POST'])
def choose_location(meetingID):
    webbrowser.open_new("ase_maps.html")
    return
@app.route('/current_location',methods = ['POST'])
def current_location():
    in_args, fields, body = parse_and_print_args()
    print("current_location : ",body)
    return "success"
    #return json.dumps(body,indent=2), 200, {"content-type": "application/json; charset: utf-8"}

@app.route('/render_location',methods = ['GET','POST'])
def render_location():
    print("in render")
    return render_template("loc.html",var ="parameter passed")

@app.route('/checkin',methods = ['GET','POST'])
def checkin():
    in_args, fields, body = parse_and_print_args()
    # R = 6373.0
    # lat1 = float(body['lat1'])
    # long1 = float(body['long1'])
    # lat2 = float(body['lat2'])
    # long2 = float(body['long2'])

    # dlon = float(long2) - float(long1)
    # dlat = float(lat2) - float(lat1)

    # a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    # c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    # distance = R * c
    # coords_1 = (52.2296756, 21.0122287)
    # coords_2 = (52.406374, 16.9251681)

    coords_1 = (float(body['lat1']),float(body['long1']))
    coords_2 = (float(body['lat2']),float(body['long2']))

    distance = geopy.distance.vincenty(coords_1, coords_2).km

    if distance <=2:
        status = True
    else:
        status = False
    print("distance:",distance)
    return json.dumps({'status':status},indent=2), 200, {"content-type": "application/json; charset: utf-8"}
@app.route('/')

if __name__ == '__main__':
    app.run()
