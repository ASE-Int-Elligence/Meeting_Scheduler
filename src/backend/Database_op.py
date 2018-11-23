import pymysql
import json

cnx = pymysql.connect(host='localhost',
                              user='dbuser',
                              password='dbuser',
                              db='ase_project',
                              charset='utf8mb4',
                              cursorclass=pymysql.cursors.DictCursor)

group_id = 0
meeting_id = 0

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

def find_partial(table, row):
    #print (pk)
    row["username"] = "'" + row["username"] + "%'"
    q = "select username from user_credentials where username like " + row["username"]
    print (q)
    result = run_q(q, None, True)
    return result

def insert_group(table, rows):
    i = 0
    row = {}
    row["groupName"]=rows["groupName"]
    row["groupType"]=rows["groupType"]
    global group_id
    group_id += 1
    for user in rows["users"]:

        row['username'] = user
        row["groupID"] = str(group_id)
        col_name = ""
        val_name = ""
        for name,val in row.items():
            col_name = col_name + name + ","
            val_name = val_name + "'" + val + "'" + ","
        col_name = col_name[:-1]
        val_name = val_name[:-1]
        query = "INSERT INTO " + table + " (" + col_name + ") VALUES (" + val_name + ")"
        result = run_q(query, None, True)
        res = "Group Creation Successful"

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

def remove_group(table, groupID ):
    
    sql = "delete from " + table + "where groupID = "+"'"+groupID+"'"
    print(sql)
    result = run_q(sql, None, True)
    return "Deleted Group"


def find_groups(table, row):
    #print (pk)
    q = "select groupName,groupType from usergroups where username = '" + row["username"] + "'"
    print (q)
    result = run_q(q, None, True)
    return result

def print_indmeeting(table, row):
    #print (pk)
    q = "select meeting.meetingID, meeting.username, meeting.meetingLoc from meeting inner join groups on groups.meetingID = meeting.meetingID where username = '" + row["username"] + "' and groupName = '" + row["groupName"] + "'"
    print (q)
    result = run_q(q, None, True)
    return result

def print_indgroups(table, row):
    #print (pk)
    q = "select groups.username, user_credentials.nameFirst, user_credentials.nameLast from groups inner join user_credentials on groups.username = user_credentials.username where groupName = '" + row["groupName"] + "'"
    print (q)
    result = run_q(q, None, True)
    return result

def create_meeting(table,row):
    
    global meeting_id
    meeting_id += 1

    row["meetingID"] = str(meeting_id)
    col_name = ""
    val_name = ""
    for name,val in row.items():
        col_name = col_name + name + ","
        val_name = val_name + "'" + val + "'" + ","
    col_name = col_name[:-1]
    val_name = val_name[:-1]
    query = "INSERT INTO " + table + " (" + col_name + ") VALUES (" + val_name + ")"
    result = run_q(query, None, True)
    res = "Meeting Creation Successful"

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

def remove_meeting(table, meetingID ):
    
    sql = "delete from " + table + " where meetingID = "+"'"+meetingID+"'"
    print(sql)
    result = run_q(sql, None, True)
    return "Deleted Meeting"

