from ezc3d import c3d

class TmpsData:
    def __init__(self, gc, context, cadence, dbl_support, single_support, step_length, step_width, walking_velocity, stride_length, step_time, stride_time):
        self.gc = gc
        self.context = context
        self.cadence = cadence
        self.dbl_support = dbl_support
        self.single_support = single_support
        self.step_length = step_length
        self.step_width = step_width
        self.walking_velocity = walking_velocity
        self.stride_length = stride_length
        self.step_time = step_time
        self.stride_time = stride_time

# def get_raw_data(gc, acq, selected_graph, event_list, planes):
#     graphdata = []
#     for i in range(0, planes):
#         graphdata.append(acq.GetPoint(selected_graph).GetValues()[event_list[gc].ic_frame:event_list[gc].sc_frame, i])
#     return graphdata


def get_available_graphs(acq):
    graph_list = []
    graph_list = acq['parameters']['POINT']['LABELS']['value']
    return graph_list

def get_raw_data(gc, acq, selected_graph, event_list, planes):
    graphdata = []
    graph_list = get_available_graphs(acq)
    for j in range(len(graph_list)):
        if graph_list[j] == selected_graph:
            for i in range(0, planes):
                graphdata.append(acq['data']['points'][i, j, event_list[gc].ic_frame:event_list[gc].sc_frame])
            break
    return graphdata


def calculate_tmps(lgc, rgc, levent, revent, lts_source, rts_source, ts_event_list):

    return_tmps_data = []

    # Calc Step Time
    lstep_time = (float(levent.ic_frame) - float(revent.ic_frame)) / 100
    rstep_time = (float(levent.sc_frame) - float(revent.sc_frame)) / 100

    # Calc Stride Time
    lstride_time = (float(levent.sc_frame) - float(levent.ic_frame)) / 100
    rstride_time = (float(revent.sc_frame) - float(revent.ic_frame)) / 100

    if len(lts_source) > 0:
        #Calc Left Stride Length
        a = float(lts_source[0][0])
        b = int(levent.tot_frames) - 1
        c = float(lts_source[0][b])
        aa = (a - c) / 1000
        lstridelenght = abs(aa)

        #Calc Left Walking Velocity
        d = float((float(b) / float(100)))
        lwalkingvelocity = abs(aa / d)

        #Calc Right Stride Length
        a = float(rts_source[0][0])
        b = int(revent.tot_frames) - 1
        c = float(rts_source[0][b])
        aa = (a - c) / 1000
        rstridelenght = abs(aa)

        #Calc Right Walking Velocity
        d = float((float(b) / float(100)))
        rwalkingvelocity = abs(aa / d)
    else:
        lstridelenght = 0
        lwalkingvelocity = 0
        rstridelenght = 0
        rwalkingvelocity = 0


    if levent.ic_frame > revent.ic_frame:

        # Calc Step Time
        lstep_time = abs(float(levent.ic_frame) - float(revent.ic_frame)) / 100
        rstep_time = abs(float(levent.sc_frame) - float(revent.sc_frame)) / 100

        # Calc Stride Time
        lstride_time = abs(float(levent.sc_frame) - float(levent.ic_frame)) / 100
        rstride_time = abs(float(revent.sc_frame) - float(revent.ic_frame)) / 100

        #Calc Cadence
        # Decided to change the calculation usign the Stride time to be compatible with Nexus calculation
        # lcadence = 60 /(abs(float(levent.ic_frame) - float(revent.ic_frame)) / 100)
        # rcadence = 60 /(abs(float(revent.sc_frame) - float(levent.ic_frame)) / 100)
        lcadence = 60 / (lstride_time / 2)
        rcadence = 60 / (rstride_time / 2)

        # Calc Double Support
        for h in range(0, len(ts_event_list)):
            if ts_event_list[h][1] == "Left" and levent.ic_frame > ts_event_list[h][0] and revent.ic_frame < ts_event_list[h][0]:
                ts_value = ts_event_list[h][0]
        rdblsupport = (ts_value - float(revent.ic_frame)) / 100
        rdblsupport = rdblsupport + ((float(revent.ts_frame) - float(levent.ic_frame))) / 100

        ldblsupport = ((float(revent.ts_frame) - float(levent.ic_frame))) / 100
        ldblsupport = ldblsupport + ((float(levent.ts_frame) - float(revent.sc_frame))) / 100

        # Calc Single Support
        rsinglesupport = rstride_time - (rdblsupport + ((revent.sc_frame - revent.ts_frame) / 100))
        lsinglesupport = lstride_time - (ldblsupport + ((levent.sc_frame - levent.ts_frame) / 100))

        if len(rts_source) > 0:
            # Calc Step Length
            a = float(rts_source[0][0]) - float(lts_source[0][0])
            lsteplength = abs(a / 1000)
            b = int(revent.tot_frames) - 1
            c = float(rts_source[0][b])
            a = float(lts_source[0][0]) - c

            rsteplength = abs(a / 1000)
            # Calc Step Width

            a = float(float(rts_source[1][0]) - float(lts_source[1][0]))
            lstepwidth = abs(a / 1000)
            b = int(revent.tot_frames) - 1
            c = float(rts_source[1][b])
            a = c - float(lts_source[1][0])
            rstepwidth = abs(a / 1000)
        else:
            lsteplength  = 0
            rsteplength = 0
            lstepwidth = 0
            rstepwidth = 0

    else:

        # Calc Step Time
        lstep_time = abs(float(levent.ic_frame) - float(revent.ic_frame)) / 100
        rstep_time = abs(float(levent.sc_frame) - float(revent.sc_frame)) / 100

        # Calc Stride Time
        lstride_time = abs(float(levent.sc_frame) - float(levent.ic_frame)) / 100
        rstride_time = abs(float(revent.sc_frame) - float(revent.ic_frame)) / 100

        #Calc Cadence
        # Decided to change the calculation usign the Stride time to be compatible with Nexus calculation
        # lcadence = 60 / (abs(float(revent.ic_frame) - float(levent.ic_frame)) / 100)
        # rcadence = 60 / (abs(float(levent.sc_frame) - float(revent.sc_frame)) / 100)
        lcadence = 60 / (lstride_time / 2)
        rcadence = 60 / (rstride_time / 2)

        # Calc Double Support
        rdblsupport = ((float(levent.ts_frame) - float(revent.ic_frame))) / 100
        rdblsupport = rdblsupport + ((float(revent.ts_frame) - float(levent.sc_frame))) / 100
        for h in range(0, len(ts_event_list)):
            if ts_event_list[h][1] == "Right" and revent.ic_frame > ts_event_list[h][0] and levent.ic_frame < ts_event_list[h][0]:
                ts_value = ts_event_list[h][0]

        ldblsupport = ((float(levent.ts_frame) - float(revent.ic_frame))) / 100
        ldblsupport = ldblsupport + (ts_value - float(levent.ic_frame)) / 100

        # Calc Single Support
        rsinglesupport = rstride_time - (rdblsupport + ((revent.sc_frame - revent.ts_frame) / 100))
        lsinglesupport = lstride_time - (ldblsupport + ((levent.sc_frame - levent.ts_frame) / 100))

        if len(lts_source) > 0:
            # Calc Step Length
            a = float(lts_source[0][0]) - float(rts_source[0][0])
            lsteplength = abs(a / 1000)
            b = int(levent.tot_frames) - 1
            c = float(lts_source[0][b])
            a = float(rts_source[0][0]) - c
            rsteplength = abs(a / 1000)

            # Calc Step Width
            a = float(float(lts_source[1][0]) - float(rts_source[1][0]))
            rstepwidth = abs(a / 1000)
            b = int(levent.tot_frames) - 1
            c = float(lts_source[1][b])
            a = c - float(rts_source[1][0])
            lstepwidth = abs(a / 1000)
        else:
            lsteplength  = 0
            rsteplength = 0
            rstepwidth= 0
            lstepwidth = 0


    if lgc == rgc:
        return_tmps_data.append(TmpsData(lgc, "Left", lcadence, ldblsupport, lsinglesupport, lsteplength, lstepwidth, lwalkingvelocity, lstridelenght, lstep_time, lstride_time))
        return_tmps_data.append(TmpsData(rgc, "Right", rcadence, rdblsupport, rsinglesupport, rsteplength, rstepwidth, rwalkingvelocity, rstridelenght, rstep_time, rstride_time))
    elif lgc > rgc:
        return_tmps_data.append(TmpsData(lgc, "Left", lcadence, ldblsupport, lsinglesupport, lsteplength, lstepwidth, lwalkingvelocity, lstridelenght, lstep_time, lstride_time))
    else:
        return_tmps_data.append(TmpsData(rgc, "Right", rcadence, rdblsupport, rsinglesupport, rsteplength, rstepwidth, rwalkingvelocity, rstridelenght, rstep_time, rstride_time))
    return return_tmps_data



def get_all_gait_data(acq, tmps_data, lts_graphname, rts_graphname,  l_gait_cycles, r_gait_cycles, levent_list, revent_list, lts_source, rts_source, levent, revent, ts_event_list):

    planes = 3

    if l_gait_cycles == r_gait_cycles:
        for gc in range(0, l_gait_cycles):
            lts_source = get_raw_data(gc, acq, lts_graphname, levent_list, planes)
            rts_source = get_raw_data(gc, acq, rts_graphname, revent_list, planes)
            levent = levent_list[gc]
            revent = revent_list[gc]
            tmps_data.append(calculate_tmps(gc, gc, levent, revent, lts_source, rts_source, ts_event_list))
        get_gait_data = "OK"
        return get_gait_data
    else:
        if l_gait_cycles - r_gait_cycles == 1:
            for gc in range(0, r_gait_cycles):

                lts_source = get_raw_data(gc, acq, lts_graphname, levent_list, planes)
                rts_source = get_raw_data(gc, acq, rts_graphname, revent_list, planes)

                levent = levent_list[gc]
                revent = revent_list[gc]
                tmps_data.append(calculate_tmps(gc, gc, levent, revent, lts_source, rts_source, ts_event_list))

            lts_source = get_raw_data(gc+1, acq, lts_graphname, levent_list, planes)
            rts_source = get_raw_data(gc, acq, rts_graphname, revent_list, planes)
            levent = levent_list[gc + 1]
            revent = revent_list[gc]
            tmps_data.append(calculate_tmps(gc + 1, gc, levent, revent, lts_source, rts_source, ts_event_list))
            get_gait_data = "OK"
            return get_gait_data
        else:
            if r_gait_cycles - l_gait_cycles == 1:
                for gc in range(0, l_gait_cycles):

                    lts_source = get_raw_data(gc, acq, lts_graphname, levent_list, planes)
                    rts_source = get_raw_data(gc, acq, rts_graphname, revent_list, planes)

                    levent = levent_list[gc]
                    revent = revent_list[gc]
                    tmps_data.append(calculate_tmps(gc, gc, levent, revent, lts_source, rts_source, ts_event_list))

                lts_source = get_raw_data(gc, acq, lts_graphname, levent_list, planes)
                rts_source = get_raw_data(gc+1, acq, rts_graphname, revent_list, planes)
                levent = levent_list[gc]
                revent = revent_list[gc + 1]
                tmps_data.append(calculate_tmps(gc, gc+1, levent, revent, lts_source, rts_source, ts_event_list ))
                get_gait_data = "OK"
                return get_gait_data
            else:
                get_gait_data = "ERROR"
                return get_gait_data
                exit()

