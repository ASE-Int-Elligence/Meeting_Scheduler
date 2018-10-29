import pymysql
import json

cnx = pymysql.connect(host='localhost', port=3306, user='dbuser', password='dbuser', db='ase_project_db', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)


def run_q(q, args, fetch=False):
    cursor = cnx.cursor()
    cursor.execute(q, args)
    if fetch:
        result = cursor.fetchall()
    else:
        result = None
    cnx.commit()
    return result

def template_to_where_clause(t):
    s = ""
    for (k, v) in t.items():
        if s != "":
            s += " AND "
        s = s + k
        s = s + " ='"
        if type(v) == list:
            s = s + v[0]
        else:
            s = s + v
        s = s + "'"

    if s != "":
        s = "WHERE " + s

    return s


def find_by_primary_key(table, username):

    q = "select password from " + table + " where username = '"+username+"'"
    #q = "select * from " + table
    result = run_q(q, None, True)
    #result = q
    return result

def create_user(table,template):
    try:
        columns = ""
        values = ""
        for columnName in template.keys():
            columns = columns + columnName + ", "
        columns = columns[:-2]
        for columnValue in template.values():
            values = values + "'" + columnValue + "'" + ", "
        values = values[:-2]
        sql = "INSERT INTO " + table + "(" + columns + ")" + "values" + "(" + values + ")"
        run_q(sql, None, True)
        result = "The row has been inserted"
    except Exception as e:
        result = str(e)
    return result