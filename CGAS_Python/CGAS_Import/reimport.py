from tkinter import *
import sys
import tkinter.messagebox
import tkinter.filedialog
import os
import numpy as np
import pandas

from matplotlib import pyplot as plt

from cgas import prepare_graphs as prep
from cgas import prepare_temporospatial as prept
from cgas import store_graphs as proc
from cgas import store_temporospatial as proct
from cgas import plot_motion_graph as pmg
from cgas import prepare_references as ref
from cgas import prepare_metadata as pmd
from cgas import store_metadata as smd


# Register the calling App directory
if __name__ == "__main__":
    working_dir = sys.argv[1].replace("\\", "//")
    if working_dir[-2] != "//":
        working_dir = working_dir + "//"

# Change current Directory to the calling App directory
os.chdir(working_dir)

# Register the python code Local Directory
localdir = os.path.dirname(os.path.realpath(__file__))

userid = os.getlogin()

# Initialize c3d import
ref_file = "Ax.txt"
use_refs = "NO"
lab = ""

ref_data = ref.get_references_data(ref_file)
use_refs = ref_data[0]
c3did = ref_data[1]
lab = ref_data[2]
importtype = ref_data[3]
lts_graphname = ref_data[4]
rts_graphname = ref_data[5]
filename = ref_data[6]

# # If Reference File Exists read Reference Name
# if os.path.isfile("Reference.ini"):
#     f = open("Reference.ini", "r")
#     if f.mode == 'r':
#         fl = f.readlines()
#         ReferenceName = fl[0].rstrip("\n")
#         print(ReferenceName)

# Read C3D File
acq = prep.read_c3d_file(filename)
# os.remove(filename)

reimport, import_graph_types, reimport_flags = ref.get_import_filter(importtype, c3did)

if importtype == 'MetaData':
    metadatalist = []
    metadatalist = pmd.get_meta_data_params(working_dir, acq)
    smd.save_metadata(working_dir, userid, c3did, metadatalist)
    quit


# List C3D available graphs
graph_list = []
graph_list = prep.get_available_graphs(acq)

# Register Foot Strike events
fs_event_list = []
fs_event_list = prep.GetEventFootStrike(acq)
print(fs_event_list)

# Register TerminalStance events
ts_event_list = []
ts_event_list = prep.GetEventTerminalStance(acq)
print(ts_event_list)

# Separate Left from Right Selected Graphs
if use_refs == "OK":
    if lab != "":
        l_selected_graphs = proc.get_import_graph_names(working_dir, lab, importtype, graph_list, "Left", "GraphName")
        l_selected_refgraphs = proc.get_import_graph_names(working_dir, lab, importtype, graph_list, "Left", "RefName")

        r_selected_graphs = proc.get_import_graph_names(working_dir, lab, importtype, graph_list, "Right", "GraphName")
        r_selected_refgraphs = proc.get_import_graph_names(working_dir, lab, importtype, graph_list, "Right", "RefName")
    else:
        quit
else:
    # Get a selection of Graphs to be processed
    l_selected_graphs = prep.get_selected_graphs(graph_list)
    l_selected_refgraphs = l_selected_graphs
    r_selected_graphs = prep.get_selected_graphs(graph_list)
    r_selected_refgraphs = r_selected_graphs

# Read the Left and Right events and count Gait_Cycles to be processed
levent_list = []
l_gait_cycles = 0
revent_list = []
r_gait_cycles = 0

# Read Gait_Cycles Data to be processed
levent_list = prep.get_gait_cycles(acq, "Left", ts_event_list, fs_event_list)
l_gait_cycles = len(levent_list)
revent_list = prep.get_gait_cycles(acq, "Right", ts_event_list, fs_event_list)
r_gait_cycles = len(revent_list)

tmps_data = []
lts_source = []
rts_source = []
levent = []
revent = []
g_status = ""

# Check if event detection graph exists for left and right sides
sub = lts_graphname
lts_graphname = (next((s for s in graph_list if sub in s), None))
sub = rts_graphname
rts_graphname = (next((s for s in graph_list if sub in s), None))

# Read all Graph Data
if use_refs == "OK":
    g_status = prept.get_all_gait_data(acq, tmps_data, lts_graphname, rts_graphname, l_gait_cycles, r_gait_cycles,
                                       levent_list, revent_list, lts_source, rts_source, levent, revent, ts_event_list)

# # Read the Reference Graph Data
# if use_refs == "OK":
#     ref_names_df = pandas.read_csv('_REFERENCES/' + ReferenceName + '/ReferenceNames.ini', sep=',', quotechar='"',
#                                    engine='python')
#     excel_data_df = pandas.read_excel('_REFERENCES/' + ReferenceName + '/' + ReferenceName + '.xlsx',
#                                       sheet_name=ReferenceName)

# Start Graphing Data
planes = 3

# Set the sampling frequency that the graphs should be normalised
pcent = np.linspace(0, 100, num=101, endpoint=True)

# Set plane names
plane_name = ["Sagittal", "Coronal", "Transverse"]

# Plot graphs for all gait cycles
for gc in range(0, l_gait_cycles):
    if prep.get_reimport_gc_validation(reimport_flags, gc, "Left"):
        event_list = []
        event_list.append(levent_list[gc])
        normalised_data = []
        # Return the Normalised Graph data
        normalised_data = prep.get_normalised_data(acq, l_selected_graphs, event_list, pcent)
        if c3did != "":
            proc.save_event_data(working_dir, userid, c3did, levent_list)
            proct.save_temporospatial_data(working_dir, userid, c3did, "Left", gc, tmps_data)
            #proc.save_graph_data(working_dir, userid, c3did, lab, importtype, l_selected_graphs,
            #                     l_selected_refgraphs, planes, normalised_data, "Left", gc, reimport_flags)

for gc in range(0, r_gait_cycles):
    if prep.get_reimport_gc_validation(reimport_flags, gc, "Right"):
        event_list = []
        event_list.append(revent_list[gc])
        normalised_data = []
        # Return the Normalised Graph data
        normalised_data = prep.get_normalised_data(acq, r_selected_graphs, event_list, pcent)

        if c3did != "":
            proc.save_event_data(working_dir, userid, c3did, revent_list)
            proct.save_temporospatial_data(working_dir, userid, c3did, "Right", gc, tmps_data)
            #proc.save_graph_data(working_dir, userid, c3did, lab, importtype, r_selected_graphs,
            #                     r_selected_refgraphs, planes, normalised_data, "Right", gc, reimport_flags)

