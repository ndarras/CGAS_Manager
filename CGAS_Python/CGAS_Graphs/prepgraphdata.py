import dbfunctions as dbf
import numpy as np


def get_group_graph_data(working_dir, groupno, selectedGroups, plotlevels , planes, graph_names):
    # Get Group Graph Data
    Ref_Lines = []
    x_data = []
    ref_data = []
    refsd_data = []
    refsdminus_data = []
    refsdplus_data = []

    for c in range(groupno):
        xgraphs = list()
        gpgraphs = []
        gpgraphsd = []
        gpgraphsm = []
        gpgraphsp = []

        xvals = []
        xvals = np.arange(0, 101, 1).tolist()

        # Register Ref Events
        dl = []
        dl.append(dbf.get_table_field_value(working_dir, "GroupEventsData", "AvgPcnt", "GroupID = " + selectedGroups[c]))
        dl.append(dbf.get_table_field_value(working_dir, "GroupEventsData", "SD", "GroupID = " + selectedGroups[c]))
        Ref_Lines.append(dl)

        for g in range(plotlevels):
            gpvals = []
            gpvalsd = []
            gpvalsm = []
            gpvalsp = []
            for i in range(planes):
                gp = []
                if str(graph_names[g][i]) == '':
                    gpvals.append([0] * 101)
                    gpvalsd.append([0] * 101)
                    gpvalsm.append([0] * 101)
                    gpvalsp.append([0] * 101)
                else:
                    gp = dbf.get_table_field_value(working_dir, "GroupGraphs", "GroupGraphID", "GroupID = " + selectedGroups[c] + " and GraphName = '" + graph_names[g][i] + "'")
                    if len(gp) > 0:
                        print("Group Graph ID:" + str(gp[0]))
                        gpvals.append(dbf.get_ref_data(working_dir, "GroupGraphData", "MeanVal", gp[0]))
                        gpvalsd.append(dbf.get_ref_data(working_dir, "GroupGraphData", "SD", gp[0]))
                        gpvalsm.append(dbf.get_ref_data(working_dir, "GroupGraphData", "(MeanVal - SD)", gp[0]))
                        gpvalsp.append(dbf.get_ref_data(working_dir, "GroupGraphData", "(MeanVal + SD)", gp[0]))
                    else:
                        gpvals.append([0] * 101)
                        gpvalsd.append([0] * 101)
                        gpvalsm.append([0] * 101)
                        gpvalsp.append([0] * 101)

            xgraphs.append(xvals)
            gpgraphs.append(gpvals)
            gpgraphsd.append(gpvalsd)
            gpgraphsm.append(gpvalsm)
            gpgraphsp.append(gpvalsp)

        x_data.append(xgraphs)
        ref_data.append(gpgraphs)
        refsd_data.append(gpgraphsd)
        refsdminus_data.append(gpgraphsm)
        refsdplus_data.append(gpgraphsp)
    return x_data, ref_data, refsd_data, refsdminus_data, refsdplus_data,  Ref_Lines



def get_graph_data(working_dir, gno, selectedC3Ds, plotlevels , planes, graph_names):
    Division_Lines = list()
    x_data = list()
    y_data = list()
    for c in range(gno):

        xgraphs = list()
        ygraphs = list()

        gpgraphs = list()
        gpgraphsm = list()
        gpgraphsp = list()

        axC3Did = str(selectedC3Ds[c][0])

        axC3Did_gait_cycle = str(selectedC3Ds[c][1])

        axC3Did_context = str(selectedC3Ds[c][2])

        # Graph Events
        dl = []
        dl.append(dbf.get_table_field_value(working_dir, "C3DGraphEvents", "TS_Pcnt", "AxC3DID = '" + axC3Did + "' and GaitCycle = " + axC3Did_gait_cycle + " and Context = '" + axC3Did_context + "'"))
        dl.append(axC3Did_context)
        Division_Lines.append(dl)

        xvals = []
        xvals = np.arange(0, 101, 1).tolist()

        for g in range(plotlevels):

            yvals = []
            for i in range(planes):
                y = []
                if str(graph_names[g][i]) == '':
                    yvals.append(xvals)
                else:
                    y = dbf.get_table_field_value(working_dir, "C3DGraphs", "C3DGraphID", "AxC3DID = '" + axC3Did + "' and GaitCycle = " + axC3Did_gait_cycle + " and GraphContext = '" + axC3Did_context + "' and GraphName ='" + str(graph_names[g][i]) + "'")
                    if len(y) > 0:
                        yvals.append(dbf.get_graph_data(working_dir, "C3DGraphData", y[0]))

            xgraphs.append(xvals)
            ygraphs.append(yvals)

        x_data.append(xgraphs)
        y_data.append(ygraphs)
    return x_data, y_data, Division_Lines



def get_graph_sets(selectedC3Ds, graph_LR_sets):
    for i in range(0, len(selectedC3Ds), 2):
        LR_set = []
        j = i + 1
        if j <= len(selectedC3Ds) - 1:
            if (selectedC3Ds[i][0] == selectedC3Ds[j][0]) and (selectedC3Ds[i][1] == selectedC3Ds[j][1]):
                    if (selectedC3Ds[i][2] == "Left" and selectedC3Ds[j][2] == "Right") or (selectedC3Ds[i][2] == "Right" and selectedC3Ds[j][2] == "Left"):
                        LR_set.append(i)
                        LR_set.append(i+1)
                        graph_LR_sets.append(LR_set)
        else:
            return

