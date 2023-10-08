from tkinter import *
import matplotlib.pyplot as plt
from matplotlib import patches as patches
from pyomeca import Analogs
from pyomeca import Markers
import os
import sys
from cgas import prepare_references as ref
from cgas import prepare_graphs as prep
from cgas import prepare_temporospatial as prept
from cgas import store_temporospatial as proct
import pandas as pd
import numpy as np
import tkinter.messagebox
import tkinter.filedialog
from cgas import store_graphs as proc

from cgas import filefunctions as ff
import mysql.connector
from mysql.connector import Error


class EMGContainer:
    def __init__(self, rows, columns, emggraphs):
        self.columns = columns
        self.rows = rows
        self.emggraphs = emggraphs


class EMGGraph:
    def __init__(self, channel, context, grow, gcol, gtitle, refdata):
        self.channel = channel
        self.context = context
        self.gcol = gcol
        self.grow = grow
        self.gtitle = gtitle
        self.refdata = refdata


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


def get_emg_filename(working_dir, c3did):
    try:
        mydb = connect_to_db(working_dir)
        mycursor = mydb.cursor()
        emgfilename = ""

        sql_select_query = "select C3DFileName from AxC3D where AxC3DID = '" + c3did + "'"
        mycursor.execute(sql_select_query)
        records = mycursor.fetchall()
        for row in records:
            emgfilename = row[0]

    except Error as e:
        print(("Error reading data from MySQL table", e))

    finally:
        if mydb.is_connected():
            mydb.close()
            mycursor.close()
            print("MySQL connection is closed")
            return emgfilename


def contextcolour(context, returntype):
    cc = ""
    if context == "Left":
        if returntype == "raw":
            cc = "gray"
        if returntype == "filtered":
            cc = "red"
        if returntype == "envelope":
            cc = "deeppink"
        if returntype == "reference":
            cc = "magenta"

    if context == "Right":
        if returntype == "raw":
            cc = "gray"
        if returntype == "filtered":
            cc = "blue"
        if returntype == "envelope":
            cc = "darkturquoise"
        if returntype == "reference":
            cc = "cyan"
    return cc


def normalise_motion_data(motiondata, tot_frames, sampling_frq, pcnt):
    i = 0
    j = 0

    norm = (sampling_frq / tot_frames)
    normalised_data = np.zeros(101)
    df = pd.DataFrame(motiondata)
    df = df.replace(np.nan, 0)
    # df.to_csv('graphdata.csv', index=False)
    frame_indexes = np.linspace(0, tot_frames, num=tot_frames, endpoint=True)
    df = pd.DataFrame(frame_indexes)
    # df.to_csv('frame_indexes.csv', index=False)
    normalized_indexes = frame_indexes * norm
    df = pd.DataFrame(normalized_indexes)
    # df.to_csv('normalized_indexes.csv', index=False)
    a = []
    a = np.interp(pcnt, normalized_indexes, motiondata, left=None, right=None, period=None)
    df = pd.DataFrame(a)
    # df.to_csv('a.csv', index=False)
    return df


zoomed_axes = [None]


def on_click(event):
    ax = event.inaxes
    i = 0
    if ax is None:
        for axis in event.canvas.figure.axes:
            axis.set_visible(True)
        # occurs when a region not in an axis is clicked...
        event.canvas.draw()
        return

    # we want to allow other navigation modes as well. Only act in case
    # shift was pressed and the correct mouse button was used
    if event.key != 'shift' or event.button != 1:
        for axis in event.canvas.figure.axes:
            axis.set_visible(True)
        event.canvas.draw()
        return

    print(ax.get_visible())

    if ax.get_visible() == True:

        print(ax.get_visible())
        ax.set_visible(False)

    else:

        ax.set_visible(True)

    event.canvas.draw()


def on_plot_hover(event):
    # Iterating over each data member plotted
    for curve in plt.get_lines():
        # Searching which data member corresponds to current mouse position
        if curve.contains(event)[0]:
            print("over %s" % curve.get_gid())


def getemgparams():
    gl = []
    grow = []
    gcol = []
    if os.path.isfile("EMG.ini"):
        f = open("EMG.ini", "r")
        if f.mode == 'r':
            fl = f.readlines()

            for x in fl:
                preprow = []
                co = ''
                fields = x.split(',')
                gl.append(EMGGraph(int(fields[3].strip('"')) - 1, fields[4].strip('"'), int(fields[1].strip('"')) - 1,
                                   int(fields[2].strip('"')) - 1, fields[5].strip('"'),
                                   fields[6].strip("\n").strip('"')))
                grow.append(int(fields[1].strip('"')))
                gcol.append(int(fields[2].strip('"')))
    g = []
    g.append(EMGContainer(max(grow[:]), max(gcol[:]), gl))
    return g


# Register the calling App directory
if __name__ == "__main__":
    working_dir = sys.argv[1].replace("\\", "//")
    if working_dir[-2] != "//":
        working_dir = working_dir + "//"

# Change current Directory to the calling App directory
os.chdir(working_dir)

# Register the python code Local Directory
localdir = os.path.dirname(os.path.realpath(__file__))

# Initialize c3d import
ref_file = "Ax.txt"
use_refs = "NO"
lab = ""

userid = os.getlogin()

# Get Ax.txt import file data or Select a file manualy
if os.path.isfile(ref_file):
    ref_data = ref.get_references_data(ref_file)
    use_refs = ref_data[0]
    c3did = ref_data[1]
    lab = ref_data[2]
    importtype = ref_data[3]
    lts_graphname = ref_data[4]
    rts_graphname = ref_data[5]
    filename = ref_data[6]
else:
    # Get 3CD Filename to be processed
    root = Tk()
    root.withdraw()
    # Get C3D Filename
    filename = tkinter.filedialog.askopenfilename(parent=root)
    root.destroy()

emgfilename = get_emg_filename(working_dir, c3did)

# If Reference File Exists read Reference Name
if os.path.isfile("Reference.ini"):
    f = open("Reference.ini", "r")
    if f.mode == 'r':
        fl = f.readlines()
        ReferenceName = fl[0].rstrip("\n")
        print(ReferenceName)

acq = prep.read_c3d_file(filename)

# Register Foot Strike events
fs_event_list = []
fs_event_list = prep.GetEventFootStrike(acq)
print(fs_event_list)

# Register TerminalStance events
ts_event_list = []
ts_event_list = prep.GetEventTerminalStance(acq)
print(ts_event_list)

# Read the Left and Right events and count Gait_Cycles to be processed
levent_list = []
l_gait_cycles = 0
revent_list = []
r_gait_cycles = 0

# Read Gait_Cycles Data to be processed
levent_list = prep.get_gait_cycles(acq, "Left", ts_event_list, fs_event_list)
l_gait_cycles=len(levent_list)
revent_list = prep.get_gait_cycles(acq, "Right", ts_event_list, fs_event_list)
r_gait_cycles=len(revent_list)

graph_list = []
graph_list = prep.get_available_graphs(acq)


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
g_status = prept.get_all_gait_data(acq, tmps_data, lts_graphname, rts_graphname,  l_gait_cycles, r_gait_cycles, levent_list, revent_list, lts_source, rts_source, levent, revent, ts_event_list)

g = getemgparams()

i = 0
k = 0

channel_offset = 12
ncols = g[0].columns
nrows = g[0].rows
channel_no = ncols * nrows
gcolor = []
gcolor.append("red")
gcolor.append("blue")

plt.rcParams.update({'font.size': 8})

data_path = filename

emg = Analogs.from_c3d(data_path, suffix_delimiter=".")

myfrq = 333
tr1 = 1
tr2 = 0.7

# =======================


k = 0
events = 0

if len(revent_list) > len(levent_list):
    events = len(revent_list)
else:
    events = len(levent_list)

for k in range(events):
    if k <= len(levent_list) - 1:
        lstart = levent_list[k].ic_frame * 10
        lswing = levent_list[k].ts_frame * 10
        lend = levent_list[k].sc_frame * 10
        ldswing = levent_list[k].ts_frame * 10 - lstart
    if k <= len(revent_list) - 1:
        rstart = revent_list[k].ic_frame * 10
        rswing = revent_list[k].ts_frame * 10
        rend = revent_list[k].sc_frame * 10
        rdswing = revent_list[k].ts_frame * 10 - rstart

    fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=(8, 8))
    fig.canvas.mpl_connect('button_press_event', on_click)
    fig.subplots_adjust(top=0.958,
                        bottom=0.048,
                        left=0.079,
                        right=0.967,
                        hspace=0.571,
                        wspace=0.141)

    emg_processed = (
        emg.meca.center()
            .meca.normalize()
    )

    for i in range(0, len(g[0].emggraphs)):
        if g[0].emggraphs[i].gtitle != "N/A":
            channel = g[0].emggraphs[i].channel + 1
            if ncols > 1:
                axes[g[0].emggraphs[i].grow][g[0].emggraphs[i].gcol].set_title(
                    g[0].emggraphs[i].gtitle + " ch(" + str(channel) + ")")
                axes[g[0].emggraphs[i].grow][g[0].emggraphs[i].gcol].set_ylim(-100, 100)
            else:
                axes[i].set_title(g[0].emggraphs[i].gtitle + " ch(" + str(channel) + ")")
                axes[i].set_ylim(-100, 100)
        else:
            if ncols > 1:
                if g[0].emggraphs[i].channel == -1:
                    axes[g[0].emggraphs[i].grow][g[0].emggraphs[i].gcol].set_visible(False)
            else:
                if g[0].emggraphs[i].channel == -1:
                    axes[i].set_visible(False)

    for i in range(0, len(g[0].emggraphs)):
        if g[0].emggraphs[i].gtitle != "N/A":
            channel = g[0].emggraphs[i].channel
            if g[0].emggraphs[i].context == "Left":
                a = emg_processed.data[channel + channel_offset][lstart:lend]
                arange = lend - lstart
            else:
                a = emg_processed.data[channel + channel_offset][rstart:rend]
                arange = rend - rstart
        else:
            arange = 101
            a = [0] * 101

        afactor = 101 / arange
        gref_data = []
        x_data = []

        gref_data = ref.get_emgreferences_data(working_dir, ReferenceName, g[0].emggraphs[i].refdata)
        for x in range(0, arange):
            x_data.append(x * afactor)

        if ncols > 1:
            axes[g[0].emggraphs[i].grow][g[0].emggraphs[i].gcol].plot(x_data, a, alpha=tr1,
                                                                      color=contextcolour(g[0].emggraphs[i].context,
                                                                                          "raw"), linewidth=0.85)
            axes[g[0].emggraphs[i].grow][g[0].emggraphs[i].gcol].set_ylim(-100, 100)
            axes[g[0].emggraphs[i].grow][g[0].emggraphs[i].gcol].set_xlim(0, 100)
        else:
            axes[i].plot(x_data, a, alpha=tr1, color=contextcolour(g[0].emggraphs[i].context, "raw"), linewidth=0.85)
            axes[i].set_ylim(-100, 100)
            axes[i].set_xlim(0, 100)

    emg_processed = (
        emg.meca.normalize()
            .meca.band_stop(order=2, cutoff=[0.5, 15], freq=myfrq)
            .meca.high_pass(order=2, cutoff=16, freq=myfrq)

    )

    for i in range(0, len(g[0].emggraphs)):
        if g[0].emggraphs[i].gtitle != "N/A":
            channel = g[0].emggraphs[i].channel
            if g[0].emggraphs[i].context == "Left":
                a = emg_processed.data[channel + channel_offset][lstart:lend]
                arange = lend - lstart
            else:
                a = emg_processed.data[channel + channel_offset][rstart:rend]
                arange = rend - rstart

            afactor = 101 / arange
            gref_data = []
            x_data = []

            for x in range(0, arange):
                x_data.append(x * afactor)

            if ncols > 1:
                axes[g[0].emggraphs[i].grow][g[0].emggraphs[i].gcol].plot(x_data, a, alpha=tr2,
                                                                          color=contextcolour(g[0].emggraphs[i].context,
                                                                                              "filtered"), linewidth=0.85)
                ax = axes[g[0].emggraphs[i].grow][g[0].emggraphs[i].gcol]
            else:
                axes[i].plot(x_data, a, alpha=tr2, color=contextcolour(g[0].emggraphs[i].context, "filtered"),
                             linewidth=0.85)
                ax = axes[i]
            ax.set_ylim(-100, 100)
            ax.set_xlim(0, 100)
            if g[0].emggraphs[i].channel == -1:
                ax.set_visible(False)

    emg_processed = (
        emg.meca.center()
            .meca.band_stop(order=2, cutoff=[0.5, 15], freq=myfrq)
            .meca.high_pass(order=2, cutoff=16, freq=myfrq)
            .meca.abs()
            .meca.low_pass(order=10, cutoff=2.8, freq=myfrq)
            .meca.normalize()
    )

    for i in range(0, len(g[0].emggraphs)):
        if g[0].emggraphs[i].gtitle != "N/A":
            if g[0].emggraphs[i].context == "Left":
                if ncols > 1:
                    axes[g[0].emggraphs[i].grow][g[0].emggraphs[i].gcol].add_patch(
                        patches.Rectangle((0, -100), (ldswing / (lend - lstart)) * 100, 200, edgecolor='black',
                                          facecolor='pink', fill=True,
                                          alpha=0.25, zorder=5))
                    axes[g[0].emggraphs[i].grow][g[0].emggraphs[i].gcol].set_ylim(-100, 100)
                else:
                    axes[i].add_patch(
                        patches.Rectangle((0, -100), (ldswing / (lend - lstart)) * 100, 200, edgecolor='black',
                                          facecolor='pink', fill=True,
                                          alpha=0.25, zorder=5))
                channel = g[0].emggraphs[i].channel
                a = emg_processed.data[channel + channel_offset][lstart:lend]
                arange = lend - lstart

                pcent = np.linspace(0, 100, num=101, endpoint=True)
                normalised = normalise_motion_data(a, arange, 100, pcent)

                arange = 100
                afactor = 1
                gref_data = []
                x_data = []

                gref_data = ref.get_emgreferences_data(working_dir, ReferenceName, g[0].emggraphs[i].refdata)
                for x in range(0, 101):
                    x_data.append(x * afactor)
                if ncols > 1:
                    axes[g[0].emggraphs[i].grow][g[0].emggraphs[i].gcol].plot(x_data, gref_data, alpha=tr1,
                                                                              color=contextcolour(g[0].emggraphs[i].context,
                                                                                                  "reference"),
                                                                              linewidth=5.0)
                    axes[g[0].emggraphs[i].grow][g[0].emggraphs[i].gcol].set_xlim(0, arange)
                else:
                    axes[i].plot(x_data, gref_data, alpha=tr1, color=contextcolour(g[0].emggraphs[i].context, "reference"),
                                 linewidth=5.0)
                    ax.set_xlim(0, arange)

            else:
                if ncols > 1:
                    axes[g[0].emggraphs[i].grow][g[0].emggraphs[i].gcol].add_patch(
                        patches.Rectangle((0, -100), (rdswing / (rend - rstart)) * 100, 200, edgecolor='black',
                                          facecolor='cyan', fill=True,
                                          alpha=0.20, zorder=5))
                else:
                    axes[i].add_patch(
                        patches.Rectangle((0, -100), (rdswing / (rend - rstart)) * 100, 200, edgecolor='black',
                                          facecolor='cyan', fill=True,
                                          alpha=0.20, zorder=5))
                channel = g[0].emggraphs[i].channel
                a = emg_processed.data[channel + channel_offset][rstart:rend]
                arange = rend - rstart

                pcent = np.linspace(0, 100, num=101, endpoint=True)
                normalised = normalise_motion_data(a, arange, 100, pcent)

                arange = 100
                afactor = 1
                gref_data = []
                x_data = []
                gref_data = ref.get_emgreferences_data(working_dir, ReferenceName, g[0].emggraphs[i].refdata)
                for x in range(0, 101):
                    x_data.append(x)
                if ncols > 1:
                    axes[g[0].emggraphs[i].grow][g[0].emggraphs[i].gcol].plot(x_data, gref_data, alpha=tr1,
                                                                              color=contextcolour(g[0].emggraphs[i].context,
                                                                                                  "reference"),
                                                                              linewidth=5.0)
                    axes[g[0].emggraphs[i].grow][g[0].emggraphs[i].gcol].set_xlim(0, arange)
                else:
                    axes[i].plot(x_data, gref_data, alpha=tr1, color=contextcolour(g[0].emggraphs[i].context, "reference"),
                                 linewidth=5.0)
                    axes[i].set_xlim(0, arange)

    emg_processed = (
        emg.meca.center()
            .meca.band_stop(order=2, cutoff=[0.5, 15], freq=myfrq)
            .meca.high_pass(order=2, cutoff=16, freq=myfrq)
            .meca.abs()
            .meca.low_pass(order=10, cutoff=2.8, freq=myfrq)
            .meca.normalize()
    )

    all_graphs = []
    all_reference_graphs = []
    all_normalised_data = []
    all_context = []

    for i in range(0, len(g[0].emggraphs)):
        if g[0].emggraphs[i].gtitle != "N/A":
            if g[0].emggraphs[i].context == "Left":
                channel = g[0].emggraphs[i].channel
                a = emg_processed.data[channel + channel_offset][lstart:lend]
                arange = lend - lstart

            else:
                channel = g[0].emggraphs[i].channel
                a = emg_processed.data[channel + channel_offset][rstart:rend]
                arange = rend - rstart

            pcent = np.linspace(0, 100, num=101, endpoint=True)
            normalised = normalise_motion_data(a, arange, 100, pcent)

            if ncols > 1:
                axes[g[0].emggraphs[i].grow][g[0].emggraphs[i].gcol].plot(normalised, alpha=tr1,
                                                                          color=contextcolour(g[0].emggraphs[i].context,
                                                                                              "envelope"))
                axes[g[0].emggraphs[i].grow][g[0].emggraphs[i].gcol].set_ylim(-100, 100)
            else:
                axes[i].plot(normalised, alpha=tr1, color=contextcolour(g[0].emggraphs[i].context, "envelope"))
                axes[i].set_ylim(-100, 100)

        all_graphs.append(g[0].emggraphs[i].gtitle)
        all_reference_graphs.append(g[0].emggraphs[i].refdata)
        all_normalised_data.append(normalised)
        all_context.append(g[0].emggraphs[i].context)

    fig.canvas.set_window_title('EMG_Gait_Cycle_' + str(k + 1))
    fig.suptitle(emgfilename + 'EMG_Gait_Cycle_' + str(k + 1), y=0.02, fontsize=8, color='gray')
    plt.savefig(working_dir + "_GRAPH_DATA//_Current_EMG//_EMG_Gait_Cycle_" + str(k + 1) + ".png")
    plt.figure

    plt.show()
    root = Tk()
    root.iconify()
    form1 = Canvas(root, width=300, height=300)
    form1.pack()
    if use_refs == "OK":
        answer = tkinter.messagebox.askyesno("Graphs Storage", "Do you want to save this Gait Cycle?")
        if (answer == True):
            selected_graphs = []
            reference_graphs = []
            planes = 1
            normalised_data = []
            context = []
            if c3did != "":
                for i in range(0, len(g[0].emggraphs)):
                    if ncols > 1:
                        if axes[g[0].emggraphs[i].grow][g[0].emggraphs[i].gcol].get_visible() == True:
                            selected_graphs.append(all_graphs[i])
                            reference_graphs.append(all_reference_graphs[i])
                            normalised_data.append(all_normalised_data[i])
                            context.append(all_context[i])
                    else:
                        if axes[i].get_visible() == True:
                            selected_graphs.append(all_graphs[i])
                            reference_graphs.append(all_reference_graphs[i])
                            normalised_data.append(all_normalised_data[i])
                            context.append(all_context[i])

                gait_cycle = k
                proc.save_EMG_data(working_dir, userid, c3did, lab, selected_graphs, reference_graphs, planes,
                                   normalised_data, context, gait_cycle)
                proc.save_event_data(working_dir, userid, c3did, levent_list)
                proc.save_event_data(working_dir, userid, c3did, revent_list)
                proct.save_temporospatial_data(working_dir, userid, c3did, "Left", gait_cycle, tmps_data)
                proct.save_temporospatial_data(working_dir, userid, c3did, "Right", gait_cycle, tmps_data)
                root.destroy()

            else:
                root.destroy()
#os.remove(filename)