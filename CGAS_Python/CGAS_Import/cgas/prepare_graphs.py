import tkinter
import numpy as np
import pandas as pd
from ezc3d import c3d


class EventSequence:
    def __init__(self, event_context, seq_no, c3d_seq_no, event_frame, c3d_event_frame, event_name):
        self.event_context = event_context
        self.seq_no = seq_no
        self.event_frame = c3d_seq_no
        self.event_frame = event_frame
        self.c3d_event_frame = c3d_event_frame
        self.event_name = event_name

class GaitEvent:
    def __init__(self, event_context, ic_frame, ic_label, ts_frame, ts_label, sc_frame, sc_label, tot_frames, ts_pcnt, ts_opposite_frame, ts_opposite_pcnt, fs_opposite_frame, fs_opposite_pcnt):
        self.event_context = event_context
        self.ic_frame = ic_frame
        self.ic_label = ic_label
        self.ts_frame = ts_frame
        self.ts_label = ts_label
        self.sc_frame = sc_frame
        self.sc_label = sc_label
        self.tot_frames = tot_frames
        self.ts_pcnt = ts_pcnt
        self.ts_opposite_frame = ts_opposite_frame
        self.ts_opposite_pcnt = ts_opposite_pcnt
        self.fs_opposite_frame = fs_opposite_frame
        self.fs_opposite_pcnt = fs_opposite_pcnt

# def read_c3d_file(filename):
#     reader = mybtk.btkAcquisitionFileReader()
#     reader.SetFilename(str(filename))
#     reader.Update()
#     return reader.GetOutput()  # type: reader

def read_c3d_file(filename):
    reader = c3d(filename, extract_forceplat_data=True)
    return reader

# def get_available_graphs(acq):
#     graph_list = []
#     for i in range(1, acq.GetPointNumber()):
#         graph = acq.GetPoint(i)
#         graph_list.append(graph.GetLabel())
#     return graph_list

def get_available_graphs(acq):
    graph_list = []
    graph_listA= []
    graph_listA = acq['parameters']['POINT']['LABELS']['value']
    graph_listB = []
    try:
        graph_listB = acq['parameters']['POINT']['LABELS2']['value']
    except:
        graph_listB = graph_listB
    graph_list = graph_listA + graph_listB
    return graph_list

def GetFirstFrame(acq):
    first_frame = 0
    first_frame = acq["header"]["points"]["first_frame"]
    return first_frame

def GetPointRate(acq):
    point_rate = 0
    point_rate = acq['parameters']['POINT']['RATE']['value'][0]
    return  point_rate

def GetEventLabel(acq):
    event_label = []
    event_label = acq["parameters"]["EVENT"]["LABELS"]["value"][:]
    return event_label

def GetEventNumber(acq):
    event_number = 0
    event_number = acq["parameters"]["EVENT"]["LABELS"]["value"][:]
    return len(event_number)

def GetEventContext(acq):
    event_context = []
    event_context = acq["parameters"]["EVENT"]["CONTEXTS"]["value"][:]
    return event_context

def GetEventTime(acq):
    event_time = []
    event_time = acq["parameters"]["EVENT"]["TIMES"]["value"][:]*GetPointRate(acq)
    event_time_int = [int(x) for x in event_time[1]]
    return event_time_int

def GetEventTerminalStance(acq):
    firstframe = GetFirstFrame(acq)
    eventnumber = GetEventNumber(acq)
    eventcontexts = GetEventContext(acq)
    eventlabels = GetEventLabel(acq)
    eventtimes = GetEventTime(acq)
    i = 0
    s = 0
    s = +  1
    event_dict = {}
    for i in range(0, eventnumber):
        if eventlabels[i] == "Foot Off":
            event_dict[int(eventtimes[i]) - firstframe] = eventcontexts[i]
    EventTerminalStance = list(event_dict.items())
    EventTerminalStance.sort()
    return EventTerminalStance

def GetEventFootStrike(acq):
    firstframe = GetFirstFrame(acq)
    eventnumber = GetEventNumber(acq)
    eventcontexts = GetEventContext(acq)
    eventlabels = GetEventLabel(acq)
    eventtimes = GetEventTime(acq)
    i = 0
    s = 0
    s = +  1
    event_dict = {}
    for i in range(0, eventnumber):
        if eventlabels[i] == "Foot Strike":
            event_dict[int(eventtimes[i]) - firstframe] = eventcontexts[i]
    EventFootStrike = list(event_dict.items())
    EventFootStrike.sort()
    return EventFootStrike


def get_selected_graphs(graph_list):
    selected_graphs = []
    master = tkinter.Tk()
    master.title('Graphs Selection')
    master.geometry("200x800")
    # for scrolling vertically
    yscrollbar = tkinter.Scrollbar(master)
    yscrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)

    def curselect(event):
        widget = event.widget
        selection = widget.curselection()
        selected_graphs.append(widget.get(selection[0]))
        print(selected_graphs)

    listbox = tkinter.Listbox(master, selectmode="extended", yscrollcommand=yscrollbar.set)
    listbox.pack(expand=tkinter.YES, fill="both")
    for i in range(0, len(graph_list)):
        listbox.insert(i, graph_list[i])
    listbox.bind('<<ListboxSelect>>', curselect)
    yscrollbar.config(command=listbox.yview)
    print(selected_graphs)
    master.mainloop()
    return selected_graphs


def get_event_sequence (acq, my_context):
    return_event_sequence = []
    event_context = GetEventContext(acq)
    event_time = GetEventTime(acq)
    event_label = GetEventLabel(acq)
    event_dict = {}
    firstframe = GetFirstFrame(acq)
    i = 0
    original_order = {}
    for i in range(0, GetEventNumber(acq)):
        if event_context[i] == my_context:
            event_dict[event_time[i] - firstframe] = str(event_label[i])
            original_order[event_time[i] - firstframe] = i
    keylist = list(event_dict.keys())
    keylist.sort()
    k = 0
    for key in keylist:
            return_event_sequence.append(EventSequence(my_context, k, original_order[key], key, key+firstframe,  event_dict[key]))
            k += 1
    return return_event_sequence


def get_gait_cycles(acq, my_context, ts_event_list, fs_event_list):
    event_sequence = []
    return_events = []
    event_sequence = get_event_sequence(acq, my_context)
    s = len(event_sequence) - 1
    j = 1
    i = 0
    while i < s-1:
        if event_sequence[i].event_name == "Foot Strike" and event_sequence[i+1].event_name == "Foot Off" and event_sequence[i+2].event_name == "Foot Strike":
            a = event_sequence[i].event_frame
            b = event_sequence[i].event_name
            c = event_sequence[i + 1].event_frame
            d = event_sequence[i + 1].event_name
            e = event_sequence[i + 2].event_frame
            f = event_sequence[i + 2].event_name
            g = event_sequence[i + 2].event_frame - event_sequence[i].event_frame
            h = (float(event_sequence[i + 1].event_frame - event_sequence[i].event_frame) / float(g)) * 100
            if my_context == "Left":
                for w in range(0, len(ts_event_list)):
                    if ts_event_list[w][1] == "Right" and c > ts_event_list[w][0] and a < ts_event_list[w][0]:
                        ts_value = ts_event_list[w][0]
                for w in range(0, len(ts_event_list)):
                    if fs_event_list[w][1] == "Right" and c > fs_event_list[w][0] and a < fs_event_list[w][0]:
                        fs_value = fs_event_list[w][0]
            else:
                for w in range(0, len(ts_event_list)):
                    if ts_event_list[w][1] == "Left" and c > ts_event_list[w][0] and a < ts_event_list[w][0]:
                        ts_value = ts_event_list[w][0]
                for w in range(0, len(fs_event_list)):
                    if fs_event_list[w][1] == "Left" and c > fs_event_list[w][0] and a < fs_event_list[w][0]:
                        fs_value = fs_event_list[w][0]

            k = ts_value
            l = (float(ts_value - event_sequence[i].event_frame) / float(g)) * 100
            m = fs_value
            n = (float(fs_value - event_sequence[i].event_frame) / float(g)) * 100
            return_events.append(GaitEvent(my_context, a, b, c, d, e, f, g, h, k, l, m, n))
            i += 2
        else:
            i += 1
    return return_events

def get_events(acq, my_context):
    return_events = []
    tmplist = []
    firstframe = acq.GetFirstFrame()
    i = 0
    s = 0
    s = +  1
    event_dict = {}
    for i in range(0, acq.GetEventNumber()):
        if acq.GetEvent(i).GetContext() == my_context:
            event_dict[acq.GetEvent(i).GetFrame() - firstframe] = str(acq.GetEvent(i).GetLabel())
    keylist = list(event_dict.keys())
    keylist.sort()
    i = 0
    for key in keylist:
        print((my_context, key, event_dict[key]))
        if event_dict[key] == "Foot Strike" and s == 1:
            relativeframe = key
            tmplist.append(relativeframe)
            tmplist.append("Foot Strike")
            s = 2
        elif event_dict[key] == "Foot Off" and s == 2:
            relativeframe = key
            tmplist.append(relativeframe)
            tmplist.append("Foot Off")
            s = 3
        elif event_dict[key] == "Foot Strike" and s == 3:
            relativeframe = key
            tmplist.append(relativeframe)
            tmplist.append("Foot Strike")
            tmplist.append(tmplist[4] - tmplist[0])
            ts_pcnt = int(float((int(tmplist[2]) - int(tmplist[0]))) / float(tmplist[6]) * 100)
            tmplist.append(ts_pcnt)
            tmplist.append(ts_opposit)
            return_events.append(GaitEvent(my_context, tmplist[0], tmplist[1], tmplist[2], tmplist[3], tmplist[4], tmplist[5],tmplist[6], tmplist[7]))
            s = 4
    else:
        pass
        return return_events


def get_normalised_data(acq, selected_graphs, event_list, pcent):
    gno = len(selected_graphs)
    planes = 3
    graph_list = get_available_graphs(acq)
    i = 0
    j = 0
    norm = (GetPointRate(acq) / event_list[0].tot_frames)
    temp_normalised_data = np.zeros((gno, planes, 101))
    for i in range(0, len(selected_graphs)):
        for j in range(0, planes):
            graphdata = []
            # graphdata = acq.GetPoint(selected_graphs[i]).GetValues()[event_list[0].ic_frame:event_list[0].sc_frame, j]
            for k in range(len(graph_list)):
                if graph_list[k] == selected_graphs[i]:
                    graphdata = acq['data']['points'][j, k, event_list[0].ic_frame:event_list[0].sc_frame]
                    break
            df = pd.DataFrame(graphdata)
            df = df.replace(np.nan, 0)
            df.to_csv('graphdata.csv', index=False)
            frame_indexes = np.linspace(0, event_list[0].tot_frames, num=event_list[0].tot_frames, endpoint=True)
            df = pd.DataFrame(frame_indexes )
            df.to_csv('frame_indexes.csv', index=False)
            normalized_indexes = frame_indexes * norm
            df = pd.DataFrame(normalized_indexes )
            df.to_csv('normalized_indexes.csv', index=False)
            a = []
            a = np.interp(pcent, normalized_indexes, graphdata, left=None, right=None, period=None)
            temp_normalised_data[i][j][:] = a
            df = pd.DataFrame(a)
            df.to_csv('a.csv', index=False)
    return temp_normalised_data

def get_reimport_gc_validation(reimport_flags, gc, context):
    current_gc = context[0] + str(gc)
    valid_gc = []
    for x in reimport_flags:
        valid_gc.append(x[1:])
    if current_gc in valid_gc:
        return True
    else:
        return False


