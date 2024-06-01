from tkinter import *
import matplotlib.pyplot as plt
from matplotlib import patches as patches
from pyomeca import Analogs
from pyomeca import Markers
import os
import sys
from cgas import prepare_references as ref
from cgas import prepare_graphs as prep

from cgas import filefunctions as ff
import mysql.connector
from mysql.connector import Error


class EMGContainer:
    def __init__(self, rows, columns, emggraphs):
        self.columns = columns
        self.rows = rows
        self.emggraphs = emggraphs

class EMGGraph:
    def __init__(self, channel, context,  grow, gcol, gtitle, refdata):
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



zoomed_axes = [None]

def on_click(event):
    ax = event.inaxes
    i = 0
    if ax is None:
        # occurs when a region not in an axis is clicked...
        return

    # we want to allow other navigation modes as well. Only act in case
    # shift was pressed and the correct mouse button was used
    if event.key != 'shift' or event.button != 1:
        return

    if zoomed_axes[0] is None:
        # not zoomed so far. Perform zoom

        # store the original position of the axes
        zoomed_axes[0] = (ax, ax.get_position())
        ax.set_position([0.1, 0.1, 0.85, 0.85])

        # hide all the other axes...
        for axis in event.canvas.figure.axes:
            if axis is not ax:
                axis.set_visible(False)

        plt.savefig("_GRAPH_DATA//_Current_EMG//_selected_" + ax.get_title())
        print ("save to:" + "_selected_" + ax.get_title())

    else:
        # restore the original state

        zoomed_axes[0][0].set_position(zoomed_axes[0][1])
        zoomed_axes[0] = None

        # make other axes visible again
        for axis in event.canvas.figure.axes:
            if axis.get_title(loc='center') > '':
                axis.set_visible(True)

    event.canvas.draw()



def on_plot_hover(event):
    # Iterating over each data member plotted
    for curve in plt.get_lines():
        # Searching which data member corresponds to current mouse position
        if curve.contains(event)[0]:
            print ("over %s" % curve.get_gid())


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
                gl.append(EMGGraph(int(fields[3].strip('"')) - 1, fields[4].strip('"'), int(fields[1].strip('"'))-1, int(fields[2].strip('"'))-1, fields[5].strip('"'), fields[6].strip("\n").strip('"')))
                grow.append(int(fields[1].strip('"')))
                gcol.append(int(fields[2].strip('"')))
    g = []
    g.append(EMGContainer(max(grow[:]), max(gcol[:]), gl))
    return g




#Register the calling App directory
if __name__ == "__main__":
    working_dir = sys.argv[1].replace("\\","//")
    if working_dir[-2] != "//":
        working_dir = working_dir + "//"

# Change current Directory to the calling App directory
os.chdir(working_dir)

# Register the python code Local Directory
localdir = os.path.dirname(os.path.realpath(__file__))

#Initialize c3d import
ref_file = "Ax.txt"
use_refs = "NO"
lab = ""

#Get Ax.txt import file data or Select a file manualy
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

if os.path.isfile("EMG_Template.ini"):
    f = open("EMG_Template.ini", "r")
    if f.mode == 'r':
        fl = f.readlines()
        preprow = []
        co = ''
        fields = fl[0].split(',')
        channel_offset = int(fields[1].strip('"'))
        frq_factor = int(fields[2].strip("\n").strip('"'))

else:
    channel_offset = 12 #uncomment for Vicon Analysis
    frq_factor = 10 #uncomment for Vicon Analysis
    #channel_offset = 0 #uncomment for GaitRite Analysis
    #frq_factor = 2 #uncomment for GaitRite Analysis


lstart = int(levent_list[0].ic_frame * frq_factor)
lswing = int(levent_list[0].ts_frame * frq_factor)
lend = int(levent_list[0].sc_frame * frq_factor)
ldswing = int(levent_list[0].ts_frame * frq_factor - lstart)

rstart = int(revent_list[0].ic_frame * frq_factor)
rswing = int(revent_list[0].ts_frame * frq_factor)
rend = int(revent_list[0].sc_frame * frq_factor)
rdswing = int(revent_list[0].ts_frame * frq_factor - rstart)


g = getemgparams()

i = 0
k = 0




ncols = g[0].columns
nrows = g[0].rows
channel_no = ncols * nrows
gcolor = []
gcolor.append("red")
gcolor.append("blue")

plt.rcParams.update({'font.size': 8})
if ncols > 1:
    fig, axes = plt.subplots(nrows=nrows, ncols=ncols, squeeze=False, figsize=(8, 8))
else:
    fig, axes = plt.subplots(nrows=nrows, ncols=ncols, squeeze=True, figsize=(8, 8))

fig.canvas.mpl_connect('button_press_event', on_click)
fig.subplots_adjust(top=0.958,
                    bottom=0.048,
                    left=0.079,
                    right=0.967,
                    hspace=0.571,
                    wspace=0.141)



data_path = filename

emg = Analogs.from_c3d(data_path, suffix_delimiter=".")

myfrq = 333
tr1 = 1
tr2 = 0.7

# ===================================================================================

emg_processed = (
    emg.meca.center()
    .meca.normalize()
)

for i in range(0, len(g[0].emggraphs)):
    if g[0].emggraphs[i].gtitle != "N/A":
        channel = g[0].emggraphs[i].channel + 1
        if ncols > 1:
            axes[g[0].emggraphs[i].grow][g[0].emggraphs[i].gcol].set_title(g[0].emggraphs[i].gtitle + " ch(" + str(channel) + ")")
            ax = axes[g[0].emggraphs[i].grow][g[0].emggraphs[i].gcol]
        else:
            axes[i].set_title(g[0].emggraphs[i].gtitle + " ch(" + str(channel) + ")")
            ax = axes[i]
        ax.set_ylim(-100, 100)
        if g[0].emggraphs[i].channel == -1:
            ax.set_visible(False)


for i in range(0, len(g[0].emggraphs)):
    if g[0].emggraphs[i].gtitle != "N/A":
        channel = g[0].emggraphs[i].channel
        a = emg_processed.data[channel + channel_offset][:]
        if ncols > 1:
            axes[g[0].emggraphs[i].grow][g[0].emggraphs[i].gcol].plot(a, alpha=tr1,  color=contextcolour(g[0].emggraphs[i].context, "raw"), linewidth=0.60)
            ax = axes[g[0].emggraphs[i].grow][g[0].emggraphs[i].gcol]
        else:
            axes[i].plot(a, alpha=tr1, color=contextcolour(g[0].emggraphs[i].context, "raw"), linewidth=0.60)
            ax = axes[i]
        ax.set_ylim(-100, 100)
        if g[0].emggraphs[i].channel == -1:
            ax.set_visible(False)

emg_processed = (
    emg.meca.band_stop(order=2, cutoff=[0.5, 15], freq=myfrq)
    .meca.high_pass(order=2, cutoff=16, freq=myfrq)
    .meca.normalize()
)


for i in range(0, len(g[0].emggraphs)):
    if g[0].emggraphs[i].gtitle != "N/A":
        channel = g[0].emggraphs[i].channel
        a = emg_processed.data[channel + channel_offset][:]
        if ncols > 1:
            axes[g[0].emggraphs[i].grow][g[0].emggraphs[i].gcol].plot(a, alpha=tr2, color=contextcolour(g[0].emggraphs[i].context, "filtered"), linewidth=0.60)
            ax=axes[g[0].emggraphs[i].grow][g[0].emggraphs[i].gcol]
        else:
            axes[i].plot(a, alpha=tr2, color=contextcolour(g[0].emggraphs[i].context, "filtered"), linewidth=0.60)
            ax = axes[i]
        ax.set_ylim(-100, 100)
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
        channel = g[0].emggraphs[i].channel
        a = emg_processed.data[channel + channel_offset][:]
        if ncols > 1:
                axes[g[0].emggraphs[i].grow][g[0].emggraphs[i].gcol].plot(a, alpha=tr1, color=contextcolour(g[0].emggraphs[i].context, "envelope"))
                ax = axes[g[0].emggraphs[i].grow][g[0].emggraphs[i].gcol]
        else:
            axes[i].plot(a, alpha=tr2, color=contextcolour(g[0].emggraphs[i].context, "envelope"))
            ax = axes[i]
        ax.set_ylim(-100, 100)
        channel = g[0].emggraphs[i].channel
        ax.set_xlim(0, len(emg_processed.data[channel + channel_offset][:]))
        if g[0].emggraphs[i].channel == -1:
            ax.set_visible(False)


for i in range(0, len(g[0].emggraphs)):
    for k in range(0, l_gait_cycles):
        if g[0].emggraphs[i].context == "Left":
            lstart = levent_list[k].ic_frame * frq_factor
            lswing = levent_list[k].ts_frame * frq_factor
            lend = levent_list[k].sc_frame * frq_factor
            ldswing = levent_list[k].ts_frame * frq_factor - lstart
            if ncols > 1:
                axes[g[0].emggraphs[i].grow][g[0].emggraphs[i].gcol].add_patch(
                    patches.Rectangle((lstart, -100), ldswing, 200, edgecolor='black', facecolor='pink', fill=True,
                                      alpha=0.25, zorder=5))
                axes[g[0].emggraphs[i].grow][g[0].emggraphs[i].gcol].add_patch(
                    patches.Rectangle((lswing, -100), (lend - lswing), 200, edgecolor='black', facecolor='gray', fill=True,
                                      alpha=0.25, zorder=5))

            else:
                axes[g[0].emggraphs[i].grow].add_patch(
                    patches.Rectangle((lstart, -100), ldswing, 200, edgecolor='black', facecolor='pink',
                                      fill=True, alpha=0.25, zorder=5))
                axes[g[0].emggraphs[i].grow].add_patch(
                    patches.Rectangle((lswing, -100), (lend - lswing), 200, edgecolor='black', facecolor='gray',
                                      fill=True, alpha=0.25, zorder=5))


    for k in range(0, r_gait_cycles):
        if g[0].emggraphs[i].context == "Right":
            rstart = revent_list[k].ic_frame * frq_factor
            rswing = revent_list[k].ts_frame * frq_factor
            rend = revent_list[k].sc_frame * frq_factor
            rdswing = revent_list[k].ts_frame * frq_factor - rstart
            if ncols > 1:
                axes[g[0].emggraphs[i].grow][g[0].emggraphs[i].gcol].add_patch(
                    patches.Rectangle((rstart, -100), rdswing, 200, edgecolor='black', facecolor='cyan', fill=True,
                                      alpha=0.25, zorder=5))
                axes[g[0].emggraphs[i].grow][g[0].emggraphs[i].gcol].add_patch(
                    patches.Rectangle((rswing, -100), (rend - rswing), 200, edgecolor='black', facecolor='gray', fill=True,
                                      alpha=0.25, zorder=5))
            else:
                axes[g[0].emggraphs[i].grow].add_patch(
                    patches.Rectangle((rstart, -100), rdswing, 200, edgecolor='black', facecolor='cyan', fill=True,
                                      alpha=0.25, zorder=5))
                axes[g[0].emggraphs[i].grow].add_patch(
                    patches.Rectangle((rswing, -100), (rend - rswing), 200, edgecolor='black', facecolor='gray', fill=True,
                                      alpha=0.25, zorder=5))



fig.canvas.set_window_title('EMG_All_Gait_Cycles')
fig.suptitle(emgfilename + '_All_Gait_Cycles', y=0.02, fontsize=8, color='gray')
plt.savefig( working_dir + "_GRAPH_DATA//_Current_EMG//_EMG_All_Gait_Cycles.png")
plt.figure
# ===========================================================
k = 0
events = 0

if len(revent_list) > len(levent_list):
    events = len(revent_list)
else:
    events = len(levent_list)

for k in range(events):
    if k <= len(levent_list) - 1:
        lstart = int(levent_list[k].ic_frame * frq_factor)
        lswing = int(levent_list[k].ts_frame * frq_factor)
        lend = int(levent_list[k].sc_frame * frq_factor)
        ldswing = int(levent_list[k].ts_frame * frq_factor - lstart)
    if k <= len(revent_list) - 1:
        rstart = int(revent_list[k].ic_frame * frq_factor)
        rswing = int(revent_list[k].ts_frame * frq_factor)
        rend = int(revent_list[k].sc_frame * frq_factor)
        rdswing = int(revent_list[k].ts_frame * frq_factor - rstart)

    if ncols > 1:
        fig, axes = plt.subplots(nrows=nrows, ncols=ncols, squeeze=False, figsize=(8, 8))
    else:
        fig, axes = plt.subplots(nrows=nrows, ncols=ncols, squeeze=True, figsize=(8, 8))
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
        channel = g[0].emggraphs[i].channel + 1
        if ncols > 1:
            axes[g[0].emggraphs[i].grow][g[0].emggraphs[i].gcol].set_title(g[0].emggraphs[i].gtitle + " ch(" + str(channel) + ")")
            axes[g[0].emggraphs[i].grow][g[0].emggraphs[i].gcol].set_ylim(-100, 100)
        else:
            axes[i].set_title(g[0].emggraphs[i].gtitle + " ch(" + str(channel) + ")")
            axes[i].set_ylim(-100, 100)

    for i in range(0, len(g[0].emggraphs)):
        channel = g[0].emggraphs[i].channel
        if g[0].emggraphs[i].context == "Left":
            a = emg_processed.data[channel + channel_offset][lstart:lend]
        else:
            a = emg_processed.data[channel + channel_offset][rstart:rend]
        if ncols > 1:
            axes[g[0].emggraphs[i].grow][g[0].emggraphs[i].gcol].plot(a, alpha=tr1,  color=contextcolour(g[0].emggraphs[i].context, "raw"), linewidth=0.85)
            axes[g[0].emggraphs[i].grow][g[0].emggraphs[i].gcol].set_ylim(-100, 100)
        else:
            axes[i].plot(a, alpha=tr1,  color=contextcolour(g[0].emggraphs[i].context, "raw"), linewidth=0.85)
            axes[i].set_ylim(-100, 100)

    emg_processed = (
        emg.meca.normalize()
        .meca.band_stop(order=2, cutoff=[0.5, 15], freq=myfrq)
        .meca.high_pass(order=2, cutoff=16, freq=myfrq)

    )


    for i in range(0, len(g[0].emggraphs)):
        channel = g[0].emggraphs[i].channel
        if g[0].emggraphs[i].context == "Left":
            a = emg_processed.data[channel + channel_offset][lstart:lend]
        else:
            a = emg_processed.data[channel + channel_offset][rstart:rend]
        if ncols > 1:
            axes[g[0].emggraphs[i].grow][g[0].emggraphs[i].gcol].plot(a, alpha=tr2, color=contextcolour(g[0].emggraphs[i].context, "filtered"), linewidth=0.85)
            ax = axes[g[0].emggraphs[i].grow][g[0].emggraphs[i].gcol]
        else:
            axes[i].plot(a, alpha=tr2, color=contextcolour(g[0].emggraphs[i].context, "filtered"), linewidth=0.85)
            ax = axes[i]
        ax.set_ylim(-100, 100)
        ax.set_xlim(0, lend - lstart)
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
                        patches.Rectangle((0, -100), ldswing, 200, edgecolor='black', facecolor='pink', fill=True,
                                          alpha=0.25, zorder=5))
                    axes[g[0].emggraphs[i].grow][g[0].emggraphs[i].gcol].set_ylim(-100, 100)
                else:
                    axes[i].add_patch(
                        patches.Rectangle((0, -100), ldswing, 200, edgecolor='black', facecolor='pink', fill=True,
                                          alpha=0.25, zorder=5))
                channel = g[0].emggraphs[i].channel
                a = emg_processed.data[channel + channel_offset][lstart:lend]
                arange = lend - lstart
                afactor = arange / 101
                gref_data = []
                x_data = []
                gref_data = ref.get_emgreferences_data(working_dir, ReferenceName, g[0].emggraphs[i].refdata)
                for x in range(0, 101):
                    x_data.append(x * afactor)
                if ncols > 1:
                    axes[g[0].emggraphs[i].grow][g[0].emggraphs[i].gcol].plot(x_data, gref_data, alpha=tr1, color=contextcolour(g[0].emggraphs[i].context, "reference"),  linewidth=5.0)
                    axes[g[0].emggraphs[i].grow][g[0].emggraphs[i].gcol].set_xlim(0, arange)
                else:
                    axes[i].plot(x_data, gref_data, alpha=tr1, color=contextcolour(g[0].emggraphs[i].context, "reference"), linewidth=5.0)
                    ax.set_xlim(0, arange)

            else:
                if ncols > 1:
                    axes[g[0].emggraphs[i].grow][g[0].emggraphs[i].gcol].add_patch(
                        patches.Rectangle((0, -100), rdswing, 200, edgecolor='black', facecolor='cyan', fill=True,
                                          alpha=0.25, zorder=5))
                else:
                    axes[i].add_patch(
                        patches.Rectangle((0, -100), rdswing, 200, edgecolor='black', facecolor='cyan', fill=True,
                                          alpha=0.25, zorder=5))
                channel = g[0].emggraphs[i].channel
                a = emg_processed.data[channel + channel_offset][rstart:rend]
                arange = rend - rstart
                afactor = arange / 101
                gref_data = []
                x_data = []
                gref_data = ref.get_emgreferences_data(working_dir, ReferenceName, g[0].emggraphs[i].refdata)
                for x in range(0, 101):
                    x_data.append(x * afactor)
                if ncols > 1:
                    axes[g[0].emggraphs[i].grow][g[0].emggraphs[i].gcol].plot(x_data, gref_data, alpha=tr1, color=contextcolour(g[0].emggraphs[i].context, "reference"),  linewidth=5.0)
                    axes[g[0].emggraphs[i].grow][g[0].emggraphs[i].gcol].set_xlim(0, arange)
                else:
                    axes[i].plot(x_data, gref_data, alpha=tr1, color=contextcolour(g[0].emggraphs[i].context, "reference"), linewidth=5.0)
                    axes[i].set_xlim(0, arange)

            if ncols > 1:
                axes[g[0].emggraphs[i].grow][g[0].emggraphs[i].gcol].plot(a, alpha=tr1, color=contextcolour(g[0].emggraphs[i].context, "envelope"))
                axes[g[0].emggraphs[i].grow][g[0].emggraphs[i].gcol].set_ylim(-100, 100)
            else:
                axes[i].plot(a, alpha=tr1, color=contextcolour(g[0].emggraphs[i].context, "envelope"))
                axes[i].set_ylim(-100, 100)

    fig.canvas.manager.set_window_title('EMG_Gait_Cycle_' + str(k+1))
    fig.suptitle(emgfilename  +'EMG_Gait_Cycle_nN_' + str(k+1), y=0.02, fontsize=8, color='gray')
    plt.savefig(working_dir + "_GRAPH_DATA//_Current_EMG//_EMG_Gait_Cycle_nN_" + str(k+1) + ".png")
    plt.figure

plt.show()
#os.remove(filename)





