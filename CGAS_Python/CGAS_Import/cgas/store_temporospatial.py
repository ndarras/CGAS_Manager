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


def save_temporospatial_data(working_dir, userid, c3did, context, gc,  tmps_data):
    database_name = ff.getfileparams(working_dir + "Connection.ini", 0)
    mydb = connect_to_db(working_dir)
    mycursor = mydb.cursor()
    sql = 'Delete from C3DTSData where AxC3DID = "{}"  and GaitCycle = {} and Context = "{}"'.format(c3did, gc, context) # type: str
    mycursor.execute(sql)
    print(sql)
    if context == "Left":
        c = 0
    else:
        c = 1
    if len(tmps_data[gc]) == 1:
        c = 0
    sql = 'INSERT INTO C3DTSData (C3DTSData.SourceDatabase, UserID, AxC3DID, GaitCycle, Context, Cadence, DoubleSupport, SingleSupport, StepLength, StepWidth, WalkingVelocity, StrideLength, StepTime, StrideTime) VALUES ("{}","{}", "{}", {}, "{}", {}, {}, {}, {}, {}, {}, {}, {}, {})'.format(database_name, userid, c3did, gc, tmps_data[gc][c].context, tmps_data[gc][c].cadence, tmps_data[gc][c].dbl_support, tmps_data[gc][c].single_support, tmps_data[gc][c].step_length, tmps_data[gc][c].step_width, tmps_data[gc][c].walking_velocity, tmps_data[gc][c].stride_length, tmps_data[gc][c].step_time, tmps_data[gc][c].stride_time )  # type: strv
    mycursor.execute(sql)
    print(sql)
    mydb.commit()
    mycursor.close()
    mydb.close()

