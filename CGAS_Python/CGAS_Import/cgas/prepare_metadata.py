import uuid
import mysql.connector
from mysql.connector import Error
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


def get_meta_data_params(working_dir, acq):
    try:
        mydb = connect_to_db(working_dir)
        mycursor = mydb.cursor()
        metadatalist = []

        sql_select_query = "select * from MetaDataParams where Active = -1;"
        mycursor.execute(sql_select_query)
        records = mycursor.fetchall()
        for row in records:
            mditem = []
            mditem.append(row[0])
            mditem.append(row[1])
            mditem.append(row[2])
            mditem.append(row[3])
            mditem.append(acq["parameters"][mditem[0]][mditem[1]]['value'][0])
            metadatalist.append(mditem)

    except Error as e:
        print(("Error reading data from MySQL table", e))

    finally:
        if mydb.is_connected():
            mydb.close()
            mycursor.close()
            print("MySQL connection is closed")
            return metadatalist