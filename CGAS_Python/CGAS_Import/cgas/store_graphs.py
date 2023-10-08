import uuid
import mysql.connector
from mysql.connector import Error
from cgas import filefunctions as ff
import numpy as np


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


def get_import_graph_names(working_dir, lab, importtype, graph_list, context, returntype):
    try:
        lgname = ""
        mydb = connect_to_db(working_dir)
        mycursor = mydb.cursor()
        selected_graphs = []
        sql_select_query = "select * from LabImportGraphNames where Lab = '" + lab + "' and ImportType = '" + importtype + "' and Context = '" + context + "' order by OrderNo asc"
        mycursor.execute(sql_select_query)
        records = mycursor.fetchall()
        # print("Total number of graphs to be imported: ", mycursor.rowcount)
        # print("\nPrinting each Graph record")
        for row in records:
            # gname = str(row[6].encode('utf-8'), 'utf-8')
            gname = row[6]
            for lgname in graph_list:
                #if gname in lgname:
                if gname == lgname:
                    if returntype == "GraphName":
                        selected_graphs.append(lgname)
                    else:
                        selected_graphs.append(gname)

    except Error as e:
        print(("Error reading data from MySQL table", e))

    finally:
        if mydb.is_connected():
            mydb.close()
            mycursor.close()
            print("MySQL connection is closed")
            return selected_graphs


def save_event_data(working_dir, userid, c3did, xevents_list):
    mydb = connect_to_db(working_dir)
    database_name = ff.getfileparams(working_dir + "Connection.ini", 0)
    mycursor = mydb.cursor()
    mycontext = xevents_list[0].event_context
    sql = 'Delete from C3DGraphEvents where AxC3DID = "{}" and Context = "{}"'.format(c3did, mycontext)  # type: str
    print(('Saving Event List AxC3DID = {} and Context = "{}"'.format(c3did, mycontext)))
    mycursor.execute(sql)
    for i in range(0, len(xevents_list)):
        sql = 'INSERT INTO C3DGraphEvents (C3DGraphEvents.SourceDatabase, UserId, AxC3DID, Context, GaitCycle, IC_Frame, IC_Label, TS_Frame, TS_Label, SC_Frame, SC_Label, Total_Frames, TS_Pcnt, TS_Opposite_Frame, TS_Opposite_Pcnt, FS_Opposite_Frame, FS_Opposite_Pcnt) VALUES ("{}","{}", "{}", "{}", {}, {}, "{}",{}, "{}",{}, "{}", {}, {}, {}, {}, {}, {})'.format(
            database_name, userid, c3did, xevents_list[i].event_context, i, xevents_list[i].ic_frame, xevents_list[i].ic_label,
            xevents_list[i].ts_frame, xevents_list[i].ts_label, xevents_list[i].sc_frame, xevents_list[i].sc_label,
            xevents_list[i].tot_frames, xevents_list[i].ts_pcnt, xevents_list[i].ts_opposite_frame, xevents_list[i].ts_opposite_pcnt, xevents_list[i].fs_opposite_frame , xevents_list[i].fs_opposite_pcnt)  # type: str
        mycursor.execute(sql)
        mydb.commit()
    mycursor.close()
    mydb.close()


# def save_graph_data(working_dir, userid, c3did, lab, importtype, selected_graphs, reference_graphs, planes, normalised_data,
#                     context, gait_cycle):
#     graph_no = len(selected_graphs)
#     database_name = ff.getfileparams(working_dir + "Connection.ini", 0)
#     mydb = connect_to_db(working_dir)
#     mycursor = mydb.cursor()
#     pcent = np.linspace(0, 100, num=101, endpoint=True)
#
#     sql = 'SELECT GraphType from LabImportGraphNames where ImportType = "{}" group by GraphType'.format(importtype)
#     mycursor.execute(sql)
#     record = mycursor.fetchall()
#     gt = ""
#     graph_types = ""
#     for row in record:
#         gt = row[0]
#         graph_types = graph_types + "'" + str(gt) + "', "
#     graph_types = graph_types[0: len(graph_types) - 2]
#
#     sql = 'SELECT C3DGraphID from C3DGraphs where AxC3DID = "{}" and GraphContext = "{}" and GraphType IN ({}) and GaitCycle = {}'.format(
#         c3did, context, graph_types, gait_cycle)
#     mycursor.execute(sql)
#     record = mycursor.fetchall()
#     graph_ids = ""
#     gid = 0
#     graph_ids_list = ""
#     for row in record:
#         gid = row[0]
#         sql = 'Delete from C3DGraphData where C3DGraphID = "{}" '.format(gid)
#         mycursor.execute(sql)
#         sql = 'Delete from C3DGraphs where C3DGraphID = "{}"'.format(gid)
#         mycursor.execute(sql)
#     mydb.commit()
#
#     for i in range(0, graph_no):
#         j = 0
#         for j in range(0, planes):
#             # Get Data From LabImportGraphNames
#             # Create C3DGraphs record
#             GraphLabel = reference_graphs[i]
#             sql = 'SELECT GraphType, OrderNo, ActivePlanes, Context, SagitalGraphName, CoronalGraphName, TransverseGraphName, GraphUnits from LabImportGraphNames where Lab = "{}" and ImportType = "{}"  and C3DLabel = "{}" and Context = "{}"'.format(
#                 lab, importtype, GraphLabel, context)
#             mycursor.execute(sql)
#             record = mycursor.fetchall()
#             for row in record:
#                 GraphType = row[0]
#                 GraphSequenceID = row[1]
#                 ActivePlanes = row[2]
#                 Context = row[3]
#                 if j == 0:
#                     if row[4] is not None:
#                         GraphName = row[4]
#                 elif j == 1:
#                     if row[5] is not None:
#                         GraphName = row[5]
#                 elif j == 2:
#                     if row[6] is not None:
#                         GraphName = row[6]
#                 GraphUnits = row[7]
#             C3DGraphID = str(uuid.uuid4())
#             if ActivePlanes[j] != "-":
#                 sql = 'Insert into C3DGraphs (C3DGraphs.SourceDatabase, UserID, C3DGraphID, AxC3DID, GraphType, GraphLabel, GraphSequenceID,  GraphContext, GraphPlane, GaitCycle, GraphName,  GraphUnits) values ("{}","{}", "{}", "{}", "{}", "{}", {}, "{}", {}, {}, "{}", "{}")'.format(
#                     database_name, userid, C3DGraphID, c3did, GraphType, GraphLabel, GraphSequenceID, Context, j, gait_cycle,
#                     GraphName, GraphUnits)
#                 mycursor.execute(sql)
#                 mydb.commit()
#                 # sql = 'SELECT max(C3DGraphID) from C3DGraphs'
#                 # mycursor.execute(sql)
#                 # record = mycursor.fetchall()
#                 # for row in record:
#                 #     C3DGraphID = row[0]
#                 # x = 0
#                 for x in range(0, 101):
#                     sql = 'Insert into C3DGraphData (C3DGraphData.SourceDatabase, UserID, AxC3DID, C3DGraphID, GaitCycle, Plane,  Pcnt, yVal) VALUES ("{}","{}", "{}",  "{}",  {}, {}, {}, {})'.format(
#                         database_name, userid, c3did, C3DGraphID, gait_cycle, j, pcent[x],
#                         float("{:.4f}".format(normalised_data[i][j][x])))
#                     mycursor.execute(sql)
#                     # mydb.commit()
#         # print("Saving Graph: % 3d, Plane : % 2d" % (i, j))
#     mydb.commit()
#     mycursor.close()
#     mydb.close()


def save_graph_data(working_dir, userid, c3did, lab, importtype, selected_graphs, reference_graphs, planes, normalised_data,
                    context, gait_cycle, reimport_flags = []):
    graph_no = len(selected_graphs)
    database_name = ff.getfileparams(working_dir + "Connection.ini", 0)
    mydb = connect_to_db(working_dir)
    mycursor = mydb.cursor()
    pcent = np.linspace(0, 100, num=101, endpoint=True)

    sql = 'SELECT GraphType from LabImportGraphNames where ImportType = "{}" group by GraphType'.format(importtype)
    mycursor.execute(sql)
    record = mycursor.fetchall()
    gt = ""
    graph_types = ""
    for row in record:
        gt = row[0]
        graph_types = graph_types + "'" + str(gt) + "', "
    graph_types = graph_types[0: len(graph_types) - 2]

    sql = 'SELECT C3DGraphID from C3DGraphs where AxC3DID = "{}" and GraphContext = "{}" and GraphType IN ({}) and GaitCycle = {}'.format(
        c3did, context, graph_types, gait_cycle)
    mycursor.execute(sql)
    record = mycursor.fetchall()
    graph_ids = ""
    gid = 0
    graph_ids_list = ""
    for row in record:
        gid = row[0]
        sql = 'Delete from C3DGraphData where C3DGraphID = "{}" '.format(gid)
        mycursor.execute(sql)
        sql = 'Delete from C3DGraphs where C3DGraphID = "{}"'.format(gid)
        mycursor.execute(sql)
    mydb.commit()

    for i in range(0, graph_no):
        j = 0
        for j in range(0, planes):
            # Get Data From LabImportGraphNames
            # Create C3DGraphs record
            GraphLabel = reference_graphs[i]
            sql = 'SELECT GraphType, OrderNo, ActivePlanes, Context, SagitalGraphName, CoronalGraphName, TransverseGraphName, GraphUnits from LabImportGraphNames where Lab = "{}" and ImportType = "{}"  and C3DLabel = "{}" and Context = "{}"'.format(
                lab, importtype, GraphLabel, context)
            mycursor.execute(sql)
            record = mycursor.fetchall()
            for row in record:
                GraphType = row[0]
                GraphSequenceID = row[1]
                ActivePlanes = row[2]
                Context = row[3]
                if j == 0:
                    if row[4] is not None:
                        GraphName = row[4]
                elif j == 1:
                    if row[5] is not None:
                        GraphName = row[5]
                elif j == 2:
                    if row[6] is not None:
                        GraphName = row[6]
                GraphUnits = row[7]

            skip_save = False
            if len(reimport_flags) > 0:
                flag = GraphType[4] + Context[0] + str(gait_cycle)
                if flag.upper() in reimport_flags:
                    skip_save = False
                else:
                    skip_save = True
            if skip_save == False:
                C3DGraphID = str(uuid.uuid4())
                if ActivePlanes[j] != "-":
                    sql = 'Insert into C3DGraphs (C3DGraphs.SourceDatabase, userid, C3DGraphID, AxC3DID, GraphType, GraphLabel, GraphSequenceID,  GraphContext, GraphPlane, GaitCycle, GraphName,  GraphUnits) values ("{}","{}", "{}", "{}", "{}", "{}", {}, "{}", {}, {}, "{}", "{}")'.format(
                        database_name, userid, C3DGraphID, c3did, GraphType, GraphLabel, GraphSequenceID, Context, j, gait_cycle,
                        GraphName, GraphUnits)
                    mycursor.execute(sql)
                    mydb.commit()
                    # sql = 'SELECT max(C3DGraphID) from C3DGraphs'
                    # mycursor.execute(sql)
                    # record = mycursor.fetchall()
                    # for row in record:
                    #     C3DGraphID = row[0]
                    # x = 0
                    for x in range(0, 101):
                        if isNaN(normalised_data[i][j][x]):
                            sql = 'Insert into C3DGraphData (C3DGraphData.SourceDatabase, userid, AxC3DID, C3DGraphID, GaitCycle, Plane,  Pcnt, yVal) VALUES ("{}","{}", "{}",  "{}",  {}, {}, {}, {})'.format(
                                database_name, userid, c3did, C3DGraphID, gait_cycle, j, pcent[x], 0)
                        else:
                            sql = 'Insert into C3DGraphData (C3DGraphData.SourceDatabase, userid, AxC3DID, C3DGraphID, GaitCycle, Plane,  Pcnt, yVal) VALUES ("{}","{}", "{}",  "{}",  {}, {}, {}, {})'.format(
                                database_name, userid, c3did, C3DGraphID, gait_cycle, j, pcent[x],
                                float("{:.4f}".format(normalised_data[i][j][x])))
                        mycursor.execute(sql)

                    # mydb.commit()
        # print("Saving Graph: % 3d, Plane : % 2d" % (i, j))
    mydb.commit()
    mycursor.close()
    mydb.close()


def save_EMG_data(working_dir, userid, c3did, lab, selected_graphs, reference_graphs, planes, normalised_data, context, gait_cycle):
    graph_no = len(selected_graphs)
    database_name = ff.getfileparams(working_dir + "Connection.ini", 0)
    mydb = connect_to_db(working_dir)
    mycursor = mydb.cursor()
    pcent = np.linspace(0, 100, num=101, endpoint=True)
    GraphType = "EMG"

    sql = 'SELECT C3DGraphID from C3DGraphs where AxC3DID = "{}" and GraphContext = "{}" and GraphType = "EMG" and GaitCycle = {}'.format(
        c3did, context, gait_cycle)
    mycursor.execute(sql)
    record = mycursor.fetchall()
    graph_ids = ""
    gid = 0
    graph_ids_list = ""
    for row in record:
        gid = row[0]
        sql = 'Delete from C3DGraphData where C3DGraphID = "{}" '.format(gid)
        mycursor.execute(sql)
        sql = 'Delete from C3DGraphs where C3DGraphID = "{}"'.format(gid)
        mycursor.execute(sql)
    mydb.commit()

    for i in range(0, graph_no):
        j = 0
        for j in range(0, planes):
            GraphLabel = context[i][0] + reference_graphs[i]
            sql = 'SELECT OrderNo, GraphUnits from Muscles where MuscleID = "{}"'.format(GraphLabel)
            mycursor.execute(sql)
            record = mycursor.fetchall()
            for row in record:
                GraphSequenceID = row[0]
                GraphUnits = row[1]
            C3DGraphID = str(uuid.uuid4())
            sql = 'Insert into C3DGraphs (C3DGraphs.SourceDatabase, userid, C3DGraphID, AxC3DID, GraphType, GraphLabel, GraphSequenceID,  GraphContext, GraphPlane, GaitCycle, GraphName,  GraphUnits) values ("{}","{}", "{}", "{}", "{}", "{}", {}, "{}", {}, {}, "{}", "{}")'.format(
                   database_name, userid, C3DGraphID, c3did, GraphType, GraphLabel, GraphSequenceID, context[i], j, gait_cycle,
                   selected_graphs[i], GraphUnits)
            mycursor.execute(sql)
            mydb.commit()
            for x in range(0, 101):
                if isNaN(normalised_data[i][j][x]):
                    sql = 'Insert into C3DGraphData (C3DGraphData.SourceDatabase, userid, AxC3DID, C3DGraphID, GaitCycle, Plane,  Pcnt, yVal) VALUES ("{}","{}", "{}",  "{}",  {}, {}, {}, {})'.format(
                        database_name, userid, c3did, C3DGraphID, gait_cycle, j, pcent[x], 0)
                else:
                    sql = 'Insert into C3DGraphData (C3DGraphData.SourceDatabase, userid, AxC3DID, C3DGraphID, GaitCycle, Plane,  Pcnt, yVal) VALUES ("{}","{}", "{}",  "{}",  {}, {}, {}, {})'.format(
                        database_name, userid, c3did, C3DGraphID, gait_cycle, j, pcent[x],
                        float("{:.4f}".format(normalised_data[i][j][x])))
                mycursor.execute(sql)
                    # mydb.commit()
        # print("Saving Graph: % 3d, Plane : % 2d" % (i, j))
    mydb.commit()
    mycursor.close()
    mydb.close()


def isNaN(num):
    return num != num
