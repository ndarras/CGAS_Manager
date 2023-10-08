import os
import sys
import logging
import filefunctions as ff
import dbfunctions as dbf
import prepgraphdata as pgd
import motiongraph as mg


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    working_dir = sys.argv[1].replace("\\","//")

# Change to Local Directory
os.chdir(working_dir)

# os.remove("errors.log")
logging.basicConfig(filename='main.log', level=logging.INFO)
logging.info("Setting Working Directory to: " + working_dir)

# Register the Local Directory
localdir = os.path.dirname(os.path.realpath(__file__))
logging.info("Local Directory is: " + localdir)

#Initialize Lists and Variables
selectedGroups = []
groupColours = []
selectedC3Ds = []
graph_LR_sets = []
lineColours = []
planes = 0
gno = 0
groupno = 0
division_lines = list()
Ref_Lines = list()
axC3Did = ""
axC3Did_gait_cycle = ""
axC3Did_context = ""
C3D_AxID = ""
Lab = ""
Import_Type =""
Graph_Type = ""
Graph_Name = ""
plotlevels = 0
graph_labels = []
plot_names = []
plot_axis_xyz = []
plot_units_xyz = []
plot_min = []
plot_max = []
adplot = []
x_data = []
y_data = []
devision_lines = []
ref_data = []
refsd_data = []
refsdminus_data = []
refsdplus_data = []
ref_lines = []
ts_data = []
ts_fields = []
ts_ref_data = []


#Get GroupIDs and Selected Group Colours
selectedGroups, groupColours = ff.getselectedgroups()
#Get C3D IDs and Selected Line Colours
selectedC3Ds, lineColours = ff.getselectedc3ds()
#Get Current Lab
Lab = ff.getgraphparams(1)
#Get Graph Type
Graph_Type = ff.getgraphparams(2)
Graph_Name = ff.getgraphparams(3)

#Calc the number of Groups
groupno = len(selectedGroups)
#Calc the number of C3D files
gno = len(selectedC3Ds)


if gno == 0 and groupno == 0:
    logging.warning("No Data to plot")
    quit()



planes = dbf.get_table_field_value(working_dir, "UserGraphParams", "max(PlotPlane)", "Lab = '" + Lab + "' and GraphType = '" + Graph_Type + "'")[0] + 1
plotlevels = dbf.get_table_field_value(working_dir, "UserGraphParams", "max(PlotRow)", "Lab = '" + Lab + "' and GraphType = '" + Graph_Type + "'")[0] + 1
graph_names, plot_names, plot_axis_xyz, plot_units_xyz, plot_min, plot_max, adplot = dbf.get_plot_graph_params(working_dir, Lab, Graph_Type, plotlevels, planes)

ts_data, ts_fields = dbf.get_ts_data(working_dir, selectedC3Ds)
ts_avg_data, ts_sd_data = dbf.get_ts_ref_data(working_dir, selectedGroups)

if groupno > 0:
    x_data, ref_data, refsd_data, refsdminus_data, refsdplus_data, ref_lines = pgd.get_group_graph_data(working_dir, groupno, selectedGroups, plotlevels, planes, graph_names)
if gno > 0:
    x_data, y_data, division_lines = pgd.get_graph_data(working_dir, gno, selectedC3Ds, plotlevels, planes, graph_names)

pgd.get_graph_sets(selectedC3Ds, graph_LR_sets)

ff.savedata("sysdata",  "groupColours.p", groupColours)
ff.savedata("sysdata",  "lineColours.p", lineColours)
ff.savedata("sysdata",  "groupno.p", groupno)
ff.savedata("sysdata",  "gno.p", gno)
ff.savedata("sysdata",  "graphs_space.p", 1.2)
ff.savedata("sysdata",  "samples.p", 100)
ff.savedata("sysdata",  "plotlevels.p", plotlevels)
ff.savedata("sysdata",  "planes.p", planes)
ff.savedata("sysdata",  "plane_names.p", ["Sagittal", "Coronal", "Transverse"])
ff.savedata("sysdata",  "graph_names.p", graph_names)
ff.savedata("sysdata",  "plot_names.p", plot_names)
ff.savedata("sysdata",  "plot_axis_xyz.p", plot_axis_xyz)
ff.savedata("sysdata",  "plot_units_xyz.p", plot_units_xyz)
ff.savedata("sysdata",  "plot_min.p", plot_min)
ff.savedata("sysdata",  "plot_max.p", plot_max)
ff.savedata("sysdata",  "adplot.p", adplot)
ff.savedata("sysdata",  "x_data.p", x_data)
ff.savedata("sysdata",  "y_data.p", y_data)
ff.savedata("sysdata",  "division_lines.p", division_lines)
ff.savedata("sysdata",  "x_data.p", x_data)
ff.savedata("sysdata",  "ref_data.p", ref_data)
ff.savedata("sysdata",  "refsd_data.p", refsd_data)
ff.savedata("sysdata",  "refsdminus_data.p", refsdminus_data)
ff.savedata("sysdata",  "refsdplus_data.p", refsdplus_data)
ff.savedata("sysdata",  "ref_lines.p", ref_lines)
ff.savedata("sysdata",  "lr_sets.p", graph_LR_sets)
ff.savedata("sysdata",  "ts_fields.p", ts_fields)
ff.savedata("sysdata",  "ts_data.p", ts_data)
ff.savedata("sysdata",  "ts_avg_data.p", ts_avg_data)
ff.savedata("sysdata",  "ts_sd_data.p", ts_sd_data)

a = mg.GaitGraph(Graph_Type, Graph_Name)
a.plotgraphs()

    # d.plotromB(
