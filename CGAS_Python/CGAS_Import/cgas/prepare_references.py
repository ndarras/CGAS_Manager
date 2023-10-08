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


def get_references_data(ref_file):
    f = open(ref_file, "r")
    if f.mode == 'r':
        fl = f.readlines()
        c3did = fl[0].rstrip("\n")
        filename = fl[1].rstrip("\n")
        lab = fl[2].rstrip("\n")
        importtype = fl[3].rstrip("\n")
        lts_graphname = fl[4].rstrip("\n")
        rts_graphname = fl[5].rstrip("\n")
        # print(filename)
        get_references_data = "OK"
        return get_references_data, c3did, lab, importtype, lts_graphname, rts_graphname, filename



def get_emgreferences_data(working_dir, reference_name, muscle):
        try:
            refdata = []
            factor = -100
            scaledval = 0
            mydb = mysql.connector.connection
            mydb = connect_to_db(working_dir)
            mycursor = mydb.cursor()
            #sql_select_query = "select * from MuscleReferences where Reference = '" + reference_name + "' and Muscle = '" + muscle + "' order by Pcnt asc"
            sql_select_query = "select * from MuscleReferences where Muscle = '" + muscle + "' order by Pcnt asc"
            mycursor.execute(sql_select_query)
            records = mycursor.fetchall()
            for row in records:
                scaledval = factor + row[3] * 30
                refdata.append(scaledval)
        except Error as e:
            print(("Error reading data from MySQL table", e))

        finally:
            if mydb.is_connected():
                mydb.close()
                mycursor.close()
                print("MySQL connection is closed")
                return refdata


def get_import_filter(importtype, c3did):
    reimport = False
    import_filter = []
    if importtype == 'ALL':
        import_filter = ff.getfilterdata()
        if import_filter[0][0] == c3did:
            reimport = True
    import_graph_types = []
    graph_types = [i[1] for i in import_filter]
    gait_cycles = [i[2] for i in import_filter]
    cycle_context = [i[3] for i in import_filter]
    reimport_flags = []
    for i in range(0, len(import_filter)):
        flag = ""
        if graph_types[i] == "EMG":
            flag = "E" + cycle_context[i][0] + str(gait_cycles[i])
        else:
            flag = graph_types[i][4] + cycle_context[i][0] + str(gait_cycles[i])
        reimport_flags.append(flag.upper())
    for x in graph_types:
        if x not in import_graph_types:
            import_graph_types.append(x)
    return reimport, import_graph_types, reimport_flags

