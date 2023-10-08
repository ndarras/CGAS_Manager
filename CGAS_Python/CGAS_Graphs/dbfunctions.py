import mysql.connector
from mysql.connector import Error
import numpy as np
import filefunctions as ff
import logging

def connect_to_db(working_dir):

    database_name = ff.getfileparams(working_dir + "Connection.ini", 0)
    server_name = ff.getfileparams(working_dir + "Connection.ini", 1)
    user_name = ff.getfileparams(working_dir + "Connection.ini", 2)
    user_pwd = ff.getfileparams(working_dir + "Connection.ini", 3)

    # logging.info(database_name)
    # logging.info(server_name)
    # logging.info(user_name)
    # logging.info(user_pwd)
    return mysql.connector.connect(
        host=server_name,
        user=user_name,
        password=user_pwd,
        database=database_name
    )


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
                results.append(row[0].encode('utf-8'))

    except Error as e:
        logging.info(("Error reading data from MySQL table", e))
    finally:
        if mydb.is_connected():
            mycursor.close()
            mydb.close()
            #logging.info("MySQL connection is closed")
            logging.info(wheresql + " :" + str(results))
            return results


def get_graph_types(working_dir, Lab, Import_Type):
    try:
        mydb = connect_to_db(working_dir)
        mycursor = mydb.cursor()
        results = []
        sql_select_query = "SELECT GraphType FROM LabImportGraphNames WHERE Lab = '" + Lab + "' And  ImportType = '" + Import_Type + "' Group by Import_Type;"
        mycursor.execute(sql_select_query)
        records = mycursor.fetchall()
        for row in records:
            rdata = []
            rdata.append(row[0].encode('utf-8'))
            results.append(rdata)
    except Error as e:
        logging.info(("Error reading data from MySQL table", e))
    return results


def get_trial_selection(working_dir):
    try:
        mydb = connect_to_db(working_dir)
        mycursor = mydb.cursor()
        results = []
        sql_select_query = "SELECT AxC3DID, GaitCycle, GraphContext FROM PlotSelectionList WHERE Plot = -1;"
        mycursor.execute(sql_select_query)
        records = mycursor.fetchall()
        for row in records:
            rdata = []
            rdata.append(row[0])
            rdata.append(row[1])
            rdata.append(row[2].encode('utf-8'))
            results.append(rdata)
    except Error as e:
        logging.info(("Error reading data from MySQL table", e))
    return results


def get_graph_data(working_dir, table_name, c3dgraphid):
    try:
        i = 0
        mydb = connect_to_db(working_dir)
        mycursor = mydb.cursor()
        graphdata = []
        sql_select_query = "select YVal from " + table_name + " where C3DGraphID = '" + str(c3dgraphid,
                                                                                            'UTF-8') + "' order by Pcnt;"
        mycursor.execute(sql_select_query)
        records = mycursor.fetchall()
        # graphdata = list(records)
        for i in range(len(records)):
            graphdata.append(float(records[i][0]))
    except Error as e:
        logging.info(("Error reading data from MySQL table", e))
    finally:
        if mydb.is_connected():
            mycursor.close()
            mydb.close()
            # logging.info("MySQL connection is closed")
            # logging.info(graphdata)

            return graphdata


def get_ts_data(working_dir, selectedC3Ds):
    ts_fields = []
    ts_fields.append("Cadence")
    ts_fields.append("DoubleSupport")
    ts_fields.append("SingleSupport")
    ts_fields.append("StepLength")
    ts_fields.append("StepWidth")
    ts_fields.append("WalkingVelocity")
    ts_fields.append("StrideLength")

    try:
        i = 0
        j = 0
        sql_select_query = ""
        fieldsinline = ""
        mydb = connect_to_db(working_dir)
        mycursor = mydb.cursor()
        tsdata = []
        fieldsinline = ", ".join(ts_fields)
        for i in range(len(selectedC3Ds)):
            logging.info("Reading Trial No " + str(i) )
            row_data = np.zeros(len(ts_fields))
            j = 0
            d = 0
            sql_select_query = "select " + fieldsinline + "  from C3DTSData where AxC3DID = '" + str(selectedC3Ds[i][0]) + "' and GaitCycle = " + selectedC3Ds[i][1] + " and Context = '" + selectedC3Ds[i][2] + "';"
            mycursor.execute(sql_select_query)
            records = mycursor.fetchall()
            for record in records:
                for field in range(len(ts_fields)):
                    row_data[j] = (float(record[field]))
                    j += 1
            tsdata.append(row_data)
    except Error as e:
        logging.info(("Error reading ts data from MySQL table", e))
    finally:
        if mydb.is_connected():
            mycursor.close()
            mydb.close()
            # logging.info("MySQL connection is closed")
            # logging.info(graphdata)
            return tsdata, ts_fields


def get_ts_ref_data(working_dir, selectedGroups):
    ts_avg_fields = []
    ts_sd_fields = []
    ts_avg_fields.append("AvgCadence")
    ts_avg_fields.append("AvgDoubleSupport")
    ts_avg_fields.append("AvgSingleSupport")
    ts_avg_fields.append("AvgStepLength")
    ts_avg_fields.append("AvgStepWidth")
    ts_avg_fields.append("AvgWalkingVelocity")
    ts_avg_fields.append("AvgStrideLength")

    ts_sd_fields.append("SDCadence")
    ts_sd_fields.append("SDDoubleSupport")
    ts_sd_fields.append("SDSingleSupport")
    ts_sd_fields.append("SDStepLength")
    ts_sd_fields.append("SDStepWidth")
    ts_sd_fields.append("SDWalkingVelocity")
    ts_sd_fields.append("SDStrideLength")

    try:
        i = 0
        j = 0
        sql_select_query = ""
        fieldsinline = ""
        row_data = []
        mydb = connect_to_db(working_dir)
        mycursor = mydb.cursor()
        ts_avg_data = []
        ts_sd_data = []

        fieldsinline = ", ".join(ts_avg_fields)
        for i in range(len(selectedGroups)):
            row_data = []
            sql_select_query = "select " + fieldsinline + "  from GroupTSData where GroupID = " + selectedGroups[
                i] + ";"
            mycursor.execute(sql_select_query)
            records = mycursor.fetchall()
            for record in records:
                for field in range(len(ts_avg_fields)):
                    row_data.append(float(record[field]))
            ts_avg_data.append(row_data)

        fieldsinline = ", ".join(ts_sd_fields)
        for i in range(len(selectedGroups)):
            row_data = []
            sql_select_query = "select " + fieldsinline + "  from GroupTSData where GroupID = " + selectedGroups[
                i] + ";"
            mycursor.execute(sql_select_query)
            records = mycursor.fetchall()
            for record in records:
                for field in range(len(ts_sd_fields)):
                    row_data.append(float(record[field]))
            ts_sd_data.append(row_data)

    except Error as e:
        logging.info(("Error reading ts data from MySQL table", e))
    finally:
        if mydb.is_connected():
            mycursor.close()
            mydb.close()
            # logging.info("MySQL connection is closed")
            # logging.info(graphdata)
            return ts_avg_data, ts_sd_data


def get_ref_data(working_dir, table_name, tblfield, GroupGraphID):
    try:
        mydb = connect_to_db(working_dir)
        mycursor = mydb.cursor()
        refdata = []
        sql_select_query = "select " + tblfield + " from " + table_name + " where GroupGraphID = '" + str(GroupGraphID,
                                                                                                          'UTF-8') + "' order by Pcnt;"
        mycursor.execute(sql_select_query)
        records = mycursor.fetchall()
        if len(records) > 0:
            for i in range(len(records)):
                refdata.append(float(records[i][0]))
        else:
            refdata = [0] * 101
    except Error as e:
        logging.info(("Error reading data from MySQL table", e))
    finally:
        if mydb.is_connected():
            mycursor.close()
            mydb.close()
            # logging.info("MySQL connection is closed")
            # logging.info(refdata)
            return refdata


def get_plot_graph_params(working_dir, lab, graphtype, plotlevels, planes):
    try:
        sql_select_query = ''
        mydb = connect_to_db(working_dir)
        mycursor = mydb.cursor()
        graph_names = []
        level_plot_names = []
        level_plot_min = []
        level_plot_max = []
        level_graph_names = []
        plot_names = []
        plot_axis_xyz = []
        plot_units_xyz = []
        plot_min = []
        plot_max = []
        adplot = []
        gname = ''
        sgraph = ''
        cgraph = ''
        tgraph = ''
        userplotname = ''

        for l in range(plotlevels - 1, -1, -1):
            x = 0
            level_names = []
            level_plot_names = []
            level_plot_axis_xyz = []
            level_plot_units_xyz = []
            level_plot_min = []
            level_plot_max = []
            level_adplot = []
            for i in range(planes):
                sql_select_query = "SELECT GraphName, PlotName, PlotAxisXYZ, PlotUnitsXYZ, PlotMin, PlotMax, ADplot FROM UserGraphParams where Lab = '" + lab + "' and GraphType = '" + graphtype + "' and PlotRow = " + str(
                    l) + " and PlotPlane = " + str(i)
                mycursor.execute(sql_select_query)
                records = mycursor.fetchall()
                if mycursor.rowcount == 0:
                    level_names.append("")
                    level_plot_names.append("")
                    level_plot_min.append(0)
                    level_plot_max.append(0)
                    level_plot_axis_xyz.append("")
                    level_plot_units_xyz.append("")
                    level_adplot.append("")
                else:
                    for row in records:
                        gname = row[0]
                        level_names.append(gname)
                        userplotname = row[1]
                        level_plot_names.append(userplotname)
                        level_plot_axis_xyz.append(row[0o2])
                        level_plot_units_xyz.append(row[0o3])
                        level_plot_min.append(row[0o4])
                        level_plot_max.append(row[0o5])
                        level_adplot.append(row[0o6])
            graph_names.append(level_names)
            plot_names.append(level_plot_names)
            plot_axis_xyz.append(level_plot_axis_xyz)
            plot_units_xyz.append(level_plot_units_xyz)
            plot_min.append(level_plot_min)
            plot_max.append(level_plot_max)
            adplot.append(level_adplot)
    except Error as e:
        logging.info(("Error reading data from MySQL table", e))
    finally:
        if mydb.is_connected():
            mycursor.close()
            mydb.close()

            # logging.info("MySQL connection is closed")
            # logging.info(graph_names)
            return graph_names, plot_names, plot_axis_xyz, plot_units_xyz, plot_min, plot_max, adplot
