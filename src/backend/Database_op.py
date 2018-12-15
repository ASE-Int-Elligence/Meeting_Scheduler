import pymysql
import json

cnx = pymysql.connect(host='localhost',
                              user='dbuser',
                              password='dbuser',
                              db='ase_project',
                              charset='utf8mb4',
                              cursorclass=pymysql.cursors.DictCursor)

#group_id = 0
#meeting_id = 0
#item_id = 0

def run_q(q, args, fetch=False):
    cursor = cnx.cursor()
    cursor.execute(q, args)
    if fetch:
        result = cursor.fetchall()
    else:
        result = None
    cnx.commit()
    return result

def templateToWhereClause_old(t):
    s = ""
    for (k,v) in t.items():
        if s != "":
            s += " AND "
        s += k + "='" + v + "'"

    if s != "":
        s = "WHERE " + s;
    #print (s)
    return s

def find_by_pk(table, pk, fields = None):
    #print (pk)
    q = "SELECT `COLUMN_NAME` FROM `information_schema`.`COLUMNS` WHERE (`TABLE_SCHEMA` = 'ase_project') AND (`TABLE_NAME` = '" + table + "' ) AND (`COLUMN_KEY` = 'PRI');"
    primarykeys = run_q(q, None, True)
    print (primarykeys)
    template = {}
    template[primarykeys[0]['COLUMN_NAME']] = pk
    wc = templateToWhereClause_old(template)
    if fields == None:
        q = "select * from "+ table + " " + wc
    else:
        q = "select " + fields + " from " + table + " " + wc
    print (q)
    result = run_q(q, None, True)
    return result

def insert(table, row):
    col_name = ""
    val_name = ""
    for name,val in row.items():
        col_name = col_name + name + ","
        val_name = val_name + "'" + val + "'" + ","
    col_name = col_name[:-1]
    val_name = val_name[:-1]
    query = "INSERT INTO " + table + " (" + col_name + ") VALUES (" + val_name + ");"
    result = run_q(query, None, True)
    res = "Insert Successful"
    return res


def insert_more_users(table, row):
    set_existing_users = []
    final_users = []
    print("WE ARE HEREEE")
    q = "select username from usergroups where groupID = '" + row["groupID"] + "'"
    ans = run_q(q, None, True)
    for i in range(len(ans)):
        set_existing_users.append(i["username"])
    for j in range(len(row["username"])):
        if row["username"][j] not in set_existing_users:
            final_users.append(row["username"][j])
    if len(final_users) == 0:
        return []
    else:
        row["username"] = final_users
    col_name = ""
    val_name = ""
    for i in range(len(row["users"])):
        col_name = ""
        val_name = ""
        for name,val in row.items():
            if name == "users":
                col_name = col_name + "username" + ","
                val_name = val_name + "'" + val[i] + "'" + ","
            else:
                col_name = col_name + name + ","
                val_name = val_name + "'" + str(val) + "'" + ","
        col_name = col_name[:-1]
        val_name = val_name[:-1]
        query = "INSERT INTO " + table + " (" + col_name + ") VALUES (" + val_name + ")"
        print ("THE QUERY IS",query)
        result = run_q(query, None, True)
    res = "Insert Successful"
    return res


def delete_user_from_group(table,template):
    for username in template['users']:
        sql = "delete from " + table + " where groupID = "+"'"+str(template['groupID'])+"'"+" and username = "+"'"+str(username)+"'"
        print(sql)
        result = run_q(sql, None, True)
    return "Deleted Users"

def find_partial(table, row):
    #print (pk)
    row["username"] = "'" + row["username"] + "%'"
    q = "select username from user_credentials where username like " + row["username"]
    print (q)
    result = run_q(q, None, True)
    return result

def insert_group(table, row):
    print ("BRUUUUUH", row)
    # global group_id
    # group_id += 1
    q = "select MAX(groupID) from usergroups"
    result = run_q(q, None, True)
    print("BHOSADIWALEEEE", result)
    row["groupID"] = result[0]["MAX(groupID)"] + 1
    col_name = ""
    val_name = ""
    for i in range(len(row["users"])):
        col_name = ""
        val_name = ""
        for name,val in row.items():
            if name == "users":
                col_name = col_name + "username" + ","
                val_name = val_name + "'" + val[i] + "'" + ","
            else:
                col_name = col_name + name + ","
                val_name = val_name + "'" + str(val) + "'" + ","
        col_name = col_name[:-1]
        val_name = val_name[:-1]
        query = "INSERT INTO " + table + " (" + col_name + ") VALUES (" + val_name + ")"
        print ("THE QUERY IS",query)
        result = run_q(query, None, True)
    res = "Insert Successful"
    return res

def update_group_info(table, data_template):

    set_values = ""
    for column,value in data_template.items():
        set_values += ""+column+"="+"'"+value+"'" + ", "
    set_values = set_values[:-2]
    update_string = "SET "+set_values
    sql = "update " + table + "  " + update_string + " " + "where groupID = "+"'"+data_template["groupID"]+"'"
    print(sql)
    result = run_q(sql, None, True)
    return "Updated Group"

def remove_group(table, group ):

    sql = "delete from " + table + " where groupID = "+"'"+str(group['groupID'])+"'"
    print(sql)
    result = run_q(sql, None, True)
    return "Deleted Group"


def find_groups(table, row):
    #print (pk)
    q = "select * from usergroups where username = '" + row["username"] + "'"
    print (q)
    result = run_q(q, None, True)
    return result

def print_indmeeting(table, row):
    #print (pk)
    q = "select meeting.meetingID, meeting.username, meeting.meetingLoc from meeting inner join usergroups on meeting.meetingID = meeting.meetingID where meeting.username = '" + row["username"] + "' and usergroups.groupName = '" + row["groupName"] + "'"
    print (q)
    result = run_q(q, None, True)
    return result

def print_indgroups(table, row):
    #print (pk)
    q = "select usergroups.username, user_credentials.nameFirst, user_credentials.nameLast from usergroups inner join user_credentials on usergroups.username = user_credentials.username where groupID = '" + str(row["groupID"]) + "'"
    print (q)
    result = run_q(q, None, True)
    return result

def get_single_meeting(table,row):
    q = "select * from meeting where meetingID = '" + row["meetingID"] + "'"
    print ("get single meeting=",q)
    result = run_q(q, None, True)
    return result

def create_meeting(table,row):

    q = "select MAX(meetingID) from meeting"
    result = run_q(q, None, True)
    print("BHOSADIWALEEEE", result)
    if result[0]["MAX(meetingID)"] == None:
        row["meetingID"] = 0
    else:
        row["meetingID"] = result[0]["MAX(meetingID)"] + 1
    col_name = ""
    val_name = ""
    for name,val in row.items():
        col_name = col_name + name + ","
        print("val:",val)
        val_name = val_name + "'" + str(val) + "'" + ","
    col_name = col_name[:-1]
    val_name = val_name[:-1]
    query = "INSERT INTO " + table + " (" + col_name + ") VALUES (" + val_name + ")"
    print (query)
    result = run_q(query, None, True)
    res = "Meeting Creation Successful"

    return res

def create_todoitem(table, row):
    #print ("BRUUUUUH", row)
    # global group_id
    # group_id += 1
    q = "select MAX(itemid) from todolist"
    result = run_q(q, None, True)
    print("BHOSADIWALEEEE", result)
    if result[0]["MAX(itemid)"] == None:
        row["itemid"] = 0
    else:
        row["itemid"] = result[0]["MAX(itemid)"] + 1
    col_name = ""
    val_name = ""
    for name,val in row.items():
        col_name = col_name + name + ","
        val_name = val_name + "'" + str(val) + "'" + ","
    col_name = col_name[:-1]
    val_name = val_name[:-1]
    query = "INSERT INTO " + table + " (" + col_name + ") VALUES (" + val_name + ")"
    print ("THE QUERY IS",query)
    print("THIS IS MY LIFEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE")
    result = run_q(query, None, True)
    return row["itemid"]

def get_todoitem(table, row):
    #print (pk)
    q = "select iteminfo,checked from todolist where meeting_id = '" + str(row["meeting_id"]) + "'"
    print (q)
    result = run_q(q, None, True)
    return result

def save_todoitem(table, row):
    col_name = ""
    val_name = ""
    for k,v in row.items():
        for name,val in v.items():
            col_name = col_name + name + ","
            val_name = val_name + "'" + str(val) + "'" + ","
        col_name = col_name[:-1]
        val_name = val_name[:-1]
        if v["checked"] == 0:
            v["checked"] = "NO"
        else:
            v["checked"] = "YES"
        query = "UPDATE " + table + " SET checked=" + "'"+v["checked"]+"'" + " where meeting_id=" + str(v["meeting_id"]) + " and itemid=" + str(k)
        print ("THE QUERY IS",query)
        result = run_q(query, None, True)
        res = "Insert Successful"
    return res

def update_meeting_info(table, data_template):

    set_values = ""
    for column,value in data_template.items():
        set_values += ""+column+"="+"'"+value+"'" + ", "
    set_values = set_values[:-2]
    update_string = "SET "+set_values
    sql = "update " + table + "  " + update_string + " " + "where meetingID = "+"'"+data_template["meetingID"]+"'"
    print(sql)
    result = run_q(sql, None, True)
    return "Updated Meeting"

def show_meeting(table, row):
    #print (pk)
    q = "select * from meeting inner join usergroups on meeting.groupID = usergroups.groupID where usergroups.username = '" + row["username"] + "'"
    print (q)
    result = run_q(q, None, True)
    return result



def remove_meeting(table, meetingID ):

    sql = "delete from " + table + " where meetingID = "+"'"+str(meetingID)+"'"
    print(sql)
    result = run_q(sql, None, True)
    return "Deleted Meeting"

def remove_account(table,template):
    sql = "delete from " + table + " where username= "+"'"+template['username']+"'"
    result = run_q(sql, None, True)
    return "Deleted Account"
