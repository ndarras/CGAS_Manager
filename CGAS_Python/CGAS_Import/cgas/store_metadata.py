import mysql.connector
from cgas import filefunctions as ff


def connect_to_db(working_dir):
    database_name = ff.getfileparams(working_dir + "Connection.ini", 0)
    server_name = ff.getfileparams(working_dir + "Connection.ini", 1)
    user_name = ff.getfileparams(working_dir + "Connection.ini", 2)
    user_pwd = ff.getfileparams(working_dir + "Connection.ini", 3)

    return mysql.connector.connect(
        host=server_name,
        user=user_name,
        password=user_pwd,
        database=database_name
    )


def save_metadata(working_dir, userid, c3did, metadatalist):
    database_name = ff.getfileparams(working_dir + "Connection.ini", 0)
    mydb = connect_to_db(working_dir)
    axid = get_table_field_value(working_dir, "AxC3D", "AxID", "AxC3DID = '" + c3did + "'")
    mycursor = mydb.cursor()
    for i in range(0, len(metadatalist)):
        sql = 'Delete from AxData where AxID = "' + str(axid[0]) + '" and Parameter = "' + metadatalist[i][3] + '"'
        mycursor.execute(sql)
        if metadatalist[i][2] == "Numeric":
            sql = 'INSERT INTO AxData (SourceDatabase, UserID, AxID, Parameter, numVal) VALUES ("{}","{}", "{}", "{}", {})'.format(database_name, userid, axid[0], metadatalist[i][3], metadatalist[i][4])
        if metadatalist[i][2] == "Text":
            sql = 'INSERT INTO AxData (SourceDatabase, UserID, AxID, Parameter, strVal) VALUES ("{}","{}", "{}", "{}", "{}")'.format(database_name, userid, axid[0],  metadatalist[i][3], metadatalist[i][4])
        if metadatalist[i][2] == "Date":
            sql = 'INSERT INTO AxData (SourceDatabase, UserID, AxID, Parameter, DVal) VALUES ("{}","{}", "{}", "{}", #{}#)'.format(database_name, userid, axid[0],  metadatalist[i][3], metadatalist[i][4])
        mycursor.execute(sql)
    mydb.commit()
    mycursor.close()
    mydb.close()


def get_table_field_value(working_dir, table_name, fieldname, wheresql):
    try:
        mydb = connect_to_db(working_dir)
        mycursor = mydb.cursor()
        results = []
        sql_select_query = "select " + fieldname + " from " + table_name + " where " + wheresql
        mycursor.execute(sql_select_query)
        records = mycursor.fetchall()
        for row in records:
            if type(row[0]) == int or type(row[0]) == float:
                results.append(row[0])
            else:
                results.append(row[0])

    except Error as e:
        print(("Error reading data from MySQL table", e))
    finally:
        if mydb.is_connected():
            mydb.close()
            mycursor.close()
            # print("MySQL connection is closed")
            # print(results)
            return results