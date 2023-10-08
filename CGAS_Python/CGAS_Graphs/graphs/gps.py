from matplotlib import pyplot as plt
import filefunctions as ff
import math
import numpy as np
import copy
import csv
import sys
import dbfunctions as dbf
import pickle
import logging
import os

class GPSData:
    def __init__(self, graph_type, graph_name, all_graphs):
        self.graph_type = graph_type
        self.graph_name = graph_name
        self.all_graphs = all_graphs
        self.gpsgraphs = []
        self.gpsgraphlabels = []
        self.lr_sets = []
        self.x_data = []
        self.y_data = []
        self.ref_data = []
        self.ref_lines = []
        self.refsd_data = []
        self.refsdminus_data = []
        self.refsdplus_data = []
        self.dev_data = []
        self.gvs_idx = []
        self.gps_idx = []
        self.lgps_idx = []
        self.rgps_idx = []
        self.map_graph_names = []
        self.graph_gvs = []
        self.gvs_avg = []
        self.gvs_sd = []
        self.lgvs_avg = []
        self.lgvs_sd = []
        self.rgvs_avg = []
        self.rgvs_sd = []
        self.gps_avg = []
        self.gps_sd = []
        self.lgps_avg = []
        self.lgps_sd = []
        self.rgps_avg = []
        self.rgps_sd = []


    def getgpslabel(self, graphname):
        label = ""
        gpslabel = ""
        workingdir = sys.argv[1].replace("\\","//")
        if workingdir[-2:] != "//":
            workingdir = workingdir + "\\"
        label = dbf.get_table_field_value(workingdir, "UserGraphParams", "PlotName", "GraphName = '" + graphname + "'")[0]
        gpslabel = str(label).replace("'", "")
        gpslabel = gpslabel[1:]
        return gpslabel

    def mean(self, data):
        n = len(data)
        mean = sum(data) / n
        return mean

    def variance(self, data):
        n = len(data)
        mean = sum(data) / n
        deviations = [(x - mean) ** 2 for x in data]
        variance = sum(deviations) / n
        return variance

    def stdev(self, data):
        import math
        var = self.variance(data)
        std_dev = math.sqrt(var)
        return std_dev

    def sumsqr(self, data):
        n = len(data)
        ndata = np.array(data)
        sumsqr = sum(ndata ** 2)
        return sumsqr

    def calc_gpsdata(self):

        w = float(0)
        w = float(1) / float(len(self.x_data[0][0]))
        #calc GVS
        for g in range(self.gno):
            for i in range(self.plotlevels):
                for j in range(self.planes):
                    for n in range(len(self.x_data[g][i])):
                        if self.plot_names[i][j] in self.gpsgraphlabels:
                            self.dev_data[g][i][j][n] = (self.y_data[g][i][j][n] - self.ref_data[0][i][j][n]) ** 2
                        else:
                            self.dev_data[g][i][j][n] = 0
                    self.gvs_idx[g][i][j] = math.sqrt(sum(self.dev_data[g][i][j][:]) * w)
                    # print(self.gvs_idx[g][i][j])
        # L&R MAP
        tmpavggps = []
        ltmpavggps = []
        rtmpavggps = []
        for g in range(len(self.lr_sets)):
            tmpsumsqr = []
            ltmpsumsqr = []
            rtmpsumsqr = []
            for i in range(self.plotlevels):
                for j in range(self.planes):
                    if self.plot_names[i][j] in self.gpsgraphlabels:
                        tmpsumsqr.append(self.gvs_idx[(self.lr_sets[g][0])][i][j])
                        tmpsumsqr.append(self.gvs_idx[(self.lr_sets[g][1])][i][j])
                        ltmpsumsqr.append(self.gvs_idx[(self.lr_sets[g][0])][i][j])
                        rtmpsumsqr.append(self.gvs_idx[(self.lr_sets[g][1])][i][j])
            if len(tmpsumsqr) > 0:
                self.gps_idx[g] = math.sqrt(self.sumsqr(tmpsumsqr) * (float(1) / len(tmpsumsqr)))
                self.lgps_idx[g] = math.sqrt(self.sumsqr(ltmpsumsqr) * (float(1) / len(ltmpsumsqr)))
                self.rgps_idx[g] = math.sqrt(self.sumsqr(rtmpsumsqr) * (float(1) / len(rtmpsumsqr)))
            else:
                self.gps_idx[g] = 0
                self.lgps_idx[g] = 0
                self.rgps_idx[g] = 0
            tmpavggps.append(self.gps_idx[g])
            ltmpavggps.append(self.lgps_idx[g])
            rtmpavggps.append(self.rgps_idx[g])

        self.gps_avg.append(self.mean(tmpavggps))
        self.gps_sd.append(self.stdev(tmpavggps))
        self.lgps_avg.append(self.mean(ltmpavggps))
        self.lgps_sd.append(self.stdev(ltmpavggps))
        self.rgps_avg.append(self.mean(rtmpavggps))
        self.rgps_sd.append(self.stdev(rtmpavggps))

        for s in range(len(self.gpsgraphs)):
            gi = []
            gj = []
            tmpgvslist = []
            for i in range(self.plotlevels):
                if len(gi) > 0:
                    break
                for j in range(self.planes):
                    if len(gj) > 0:
                        break
                    if self.plot_names[i][j] != '':
                        if self.plot_names[i][j] == self.gpsgraphlabels[s]:
                            gi.append(i)
                            gj.append(j)
                            j = self.planes
                            i = self.plotlevels
                        else:
                            print('-')
            for g in range(self.gno):
                # print(self.gpsgraphlabels[s])
                tmpgvslist.append(self.gvs_idx[g][gi[0]][gj[0]])
                # self.graph_gvs[s][g] = self.mean(tmpgvslist)
            for z in range(len(tmpgvslist)):
                self.graph_gvs[s][z] = tmpgvslist[z]
            self.gvs_avg[s] = self.mean(tmpgvslist)
            self.gvs_sd[s] = self.stdev(tmpgvslist)

        self.gvs_avg[s + 1] = 0
        self.gvs_sd[s + 1] = 0
        self.gvs_avg[s + 2] = self.gps_avg[0]
        self.gvs_sd[s + 2] = self.gps_sd[0]


        for s in range(len(self.gpsgraphs)):
            tmplavg = []
            tmpravg = []
            for g in range(len(self.lr_sets)):
                k = self.lr_sets[g][0]
                l = self.lr_sets[g][1]
                tmplavg.append(self.graph_gvs[s][k])
                tmpravg.append(self.graph_gvs[s][l])
            self.lgvs_avg[s] = self.mean(tmplavg)
            self.lgvs_sd[s] = self.stdev(tmplavg)
            self.rgvs_avg[s] = self.mean(tmpravg)
            self.rgvs_sd[s] = self.stdev(tmpravg)

        self.lgvs_avg[s + 1] = 0
        self.lgvs_sd[s + 1] = 0
        self.lgvs_avg[s + 2] = self.lgps_avg[0]
        self.lgvs_sd[s + 2] = self.lgps_sd[0]

        self.rgvs_avg[s + 1] = 0
        self.rgvs_sd[s + 1] = 0
        self.rgvs_avg[s + 2] = self.rgps_avg[0]
        self.rgvs_sd[s + 2] = self.rgps_sd[0]

        print("GPS Values Calculated")
        # print(self.gps_idx)

        with open(self.graph_name + '_GPS.csv', 'w') as f:
            # using csv.writer method from CSV package
            write = csv.writer(f)
            write.writerow(['GPS Avg'])
            write.writerow(self.gvs_avg[:])
            write.writerow(['GPS SD'])
            write.writerow(self.gvs_avg[:])
            write.writerow(['L GPS Avg'])
            write.writerow(self.lgvs_avg[:])
            write.writerow(['L GPS SD'])
            write.writerow(self.lgvs_avg[:])
            write.writerow(['R GPS Avg'])
            write.writerow(self.rgvs_avg[:])
            write.writerow(['R GPS SD'])
            write.writerow(self.rgvs_avg[:])
            write.writerow(['GPSvalues'])
            write.writerow(self.gps_idx[:])
            write.writerow(['Left GPSvalues'])
            write.writerow(self.lgps_idx[:])
            write.writerow(['Right GPSvalues'])
            write.writerow(self.rgps_idx[:])



        self.gvs_sd[s + 1] = 0


        with open(self.graph_name + '_GVS.csv', 'w') as f:
            # using csv.writer method from CSV package
            write = csv.writer(f)
            write.writerow(['GVSvalues'])
            write.writerow(self.gpsgraphs[:])
            write.writerow(['LeftRight Avg GVSvalues'])
            write.writerow(self.gvs_avg[:])
            write.writerow(self.gvs_sd[:])
            write.writerow(['Left GVSvalues'])
            write.writerow(self.lgvs_avg[:])
            write.writerow(['Left GVSvalues SD'])
            write.writerow(self.lgvs_sd[:])
            write.writerow(['Right GVSvalues'])
            write.writerow(self.rgvs_avg[:])
            write.writerow(['Right GVSvalues SD'])
            write.writerow(self.rgvs_sd[:])

        outfile = open('sysdata//Reference_' + self.graph_type + '_GPS.p', 'wb')
        pickle.dump(self.gpsgraphs, outfile)
        pickle.dump(self.lgvs_avg, outfile)
        pickle.dump(self.lgvs_sd, outfile)
        pickle.dump(self.rgvs_avg, outfile)
        pickle.dump(self.rgvs_sd, outfile)
        pickle.dump(self.gvs_avg, outfile)
        pickle.dump(self.gvs_sd, outfile)
        # pickle.dump(self.gps_avg, outfile)
        # pickle.dump(self.gps_sd, outfile)
        # pickle.dump(self.lgps_avg, outfile)
        # pickle.dump(self.lgps_sd, outfile)
        # pickle.dump(self.rgps_avg, outfile)
        # pickle.dump(self.rgps_sd, outfile)
        outfile.close()
        logging.info("Reference GPS/GVS Vals stored")

        print("GPS Calculated")

    def prep_gpsdata(self):
        self.group_colours = ff.getdata("sysdata", "groupColours.p")
        self.line_colours = ff.getdata("sysdata", "lineColours.p")
        self.groupno = ff.getdata("sysdata", "groupno.p")
        self.gno = ff.getdata("sysdata", "gno.p")

        self.graphs_space = ff.getdata("sysdata", "graphs_space.p")
        self.samples = ff.getdata("sysdata", "samples.p")
        self.planes = ff.getdata("sysdata", "planes.p")
        self.plane_names = ff.getdata("sysdata", "plane_names.p")
        self.plotlevels = ff.getdata("sysdata", "plotlevels.p")

        self.graph_names = ff.getdata("sysdata", "graph_names.p")
        self.plot_names = ff.getdata("sysdata", "plot_names.p")
        self.plot_axis_xyz = ff.getdata("sysdata", "plot_axis_xyz.p")
        self.plot_units_xyz = ff.getdata("sysdata", "plot_units_xyz.p")
        self.plot_min = ff.getdata("sysdata", "plot_min.p")
        self.plot_max = ff.getdata("sysdata", "plot_max.p")

        self.x_data= ff.getdata("sysdata", "x_data.p")
        self.y_data = ff.getdata("sysdata", "y_data.p", )
        self.division_lines = ff.getdata("sysdata", "division_lines.p")

        self.x_data = ff.getdata("sysdata", "x_data.p")
        self.ref_data = ff.getdata("sysdata", "ref_data.p")
        self.refsd_data = ff.getdata("sysdata", "refsd_data.p")
        self.refsdminus_data = ff.getdata("sysdata", "refsdminus_data.p")
        self.refsdplus_data = ff.getdata("sysdata", "refsdplus_data.p")
        self.ref_lines = ff.getdata("sysdata", "ref_lines.p")
        self.lr_sets = ff.getdata("sysdata", "lr_sets.p")

        self.gpsgraphs.append("Pelvic Tilt")
        self.gpsgraphs.append("Hip Flex-Ext")
        self.gpsgraphs.append("Knee Flex-Ext")
        self.gpsgraphs.append("Ankle Flex-Ext")
        self.gpsgraphs.append("Pelvic Obliquity")
        self.gpsgraphs.append("Hip Add-Abd")
        self.gpsgraphs.append("Pelvic Rotation")
        self.gpsgraphs.append("Hip Rotation")
        self.gpsgraphs.append("Foot Progression Int-Ext")

        gpslabel = self.getgpslabel("Pelvic Tilt")
        self.gpsgraphlabels.append(gpslabel)
        gpslabel = self.getgpslabel("Hip Flex-Ext")
        self.gpsgraphlabels.append(gpslabel)
        gpslabel = self.getgpslabel("Knee Flex-Ext")
        self.gpsgraphlabels.append(gpslabel)
        gpslabel = self.getgpslabel("Ankle Flex-Ext")
        self.gpsgraphlabels.append(gpslabel)
        gpslabel = self.getgpslabel("Pelvic Obliquity")
        self.gpsgraphlabels.append(gpslabel)
        gpslabel = self.getgpslabel("Hip Add-Abd")
        self.gpsgraphlabels.append(gpslabel)
        gpslabel = self.getgpslabel("Pelvic Rotation")
        self.gpsgraphlabels.append(gpslabel)
        gpslabel = self.getgpslabel("Hip Rotation")
        self.gpsgraphlabels.append(gpslabel)
        gpslabel = self.getgpslabel("Foot Progression Int-Ext")
        self.gpsgraphlabels.append(gpslabel)


        azero = np.zeros((self.gno, self.plotlevels, self.planes, 101))
        bzero = np.zeros((self.gno, self.plotlevels, self.planes))
        czero = np.zeros((len(self.lr_sets)))
        dzero = np.zeros((len(self.gpsgraphlabels), self.gno))
        ezero = np.zeros((len(self.gpsgraphlabels)) + 2)


        self.dev_data = copy.deepcopy(azero)
        self.gvs_idx = copy.deepcopy(bzero)
        self.gps_idx = copy.deepcopy(czero)
        self.lgps_idx = copy.deepcopy(czero)
        self.rgps_idx = copy.deepcopy(czero)
        self.graph_gvs = copy.deepcopy(dzero)
        self.gvs_avg = copy.deepcopy(ezero)
        self.gvs_sd = copy.deepcopy(ezero)
        self.lgvs_avg = copy.deepcopy(ezero)
        self.lgvs_sd = copy.deepcopy(ezero)
        self.rgvs_avg = copy.deepcopy(ezero)
        self.rgvs_sd = copy.deepcopy(ezero)





    def map_bars(self):

        self.prep_gpsdata()
        self.calc_gpsdata()

        ref_info = ""
        ref_path = ff.getfileparams("compare.ini", 0)
        ref_name = ff.getfileparams("compare.ini", 1)
        ref_comp_caption = ff.getfileparams("compare.ini", 2)

        ref_filename = ""
        if ref_name != '':
            for file in os.listdir(ref_path):
                if file.startswith('Reference_' + self.graph_type + '_GPS'):
                    ref_filename = file

            if ref_filename != "":
                ref_info = ref_filename.split("_")
                if os.path.isfile(ref_path + ref_filename):
                    infile = open(ref_path + ref_filename, 'rb')
                    ref_gpsgraphs = pickle.load(infile)
                    ref_lgvs_avg = pickle.load(infile)
                    ref_lgvs_sd = pickle.load(infile)
                    ref_rgvs_avg = pickle.load(infile)
                    ref_rgvs_sd = pickle.load(infile)
                    ref_gvs_avg = pickle.load(infile)
                    ref_gvs_sd = pickle.load(infile)
                    # ref_gps_avg = pickle.load(infile)
                    # ref_gps_sd = pickle.load(infile)
                    # ref_lgps_avg = pickle.load(infile)
                    # ref_lgps_sd = pickle.load(infile)
                    # ref_rgps_avg = pickle.load(infile)
                    # ref_rgps_sd = pickle.load(infile)
                    infile.close()


        graphprefs = ff.getgraphprefs("MAP and GVS")
        if len(graphprefs) > 0:
            fig, ax = plt.subplots(1, figsize=(graphprefs[0], graphprefs[1]))
        else:
            fig, ax = plt.subplots(1, figsize=(8, 9.5))

        fig.tight_layout(pad=self.graphs_space)

        fig.canvas.mpl_connect('button_press_event', on_click)

        plt.subplots_adjust(left=0.05,
                            bottom=0.40,
                            right=0.95,
                            top=0.95,
                            wspace=0.4,
                            hspace=0.15)
        ax.title.set_text('GPS per Ax')
        y = 1  # the label locations
        width = 0.30  # the width of the bars

        # rects1 = ax[0].bar(x - 2 * (width / 3), self.lgps_idx, width, label=' L GPS', color='red')
        # rects2 = ax[0].bar(x + (width / 3), self.rgps_idx, width, label=' R GPS', color='blue')
        # rects3 = ax[0].bar(x + 4 * (width / 3), self.gps_idx, width, label='LR GPS', color='orange')

        # rects1 = ax[0].bar(x - 2 * (width / 3), self.lgps_avg, width,  yerr=self.lgps_sd, label=' L GPS', color='red')
        # rects2 = ax[0].bar(x + (width / 3), self.rgps_avg, width, yerr=self.rgps_sd, label=' R GPS', color='blue')
        # rects3 = ax[0].bar(x + 4 * (width / 3), self.gps_avg, width, yerr=self.gps_sd, label='LR GPS', color='orange')

        # ax[0].set_xticks(np.arange(len(self.lr_sets)))
        ax.legend()

        ax.title.set_text('GVS & GPS')
        x = np.arange(len(self.gpsgraphs) + 2)  # the label locations
        width = 0.27
        rects1 = ax.bar(x, self.lgvs_avg, width, yerr=self.lgvs_sd, label=' L GVS', color='red', alpha=0.90)
        rects2 = ax.bar(x + width, self.rgvs_avg, width, yerr=self.rgvs_sd, label=' R GVS', color='blue', alpha=0.90)
        rects3 = ax.bar(x + 2 * width, self.gvs_avg, width, yerr=self.gvs_sd, label='LR GVS', color='orange', alpha=0.90)
        self.gpsgraphlabels.append("")
        self.gpsgraphlabels.append("GPS")
        x_pos = np.arange(len(self.gpsgraphlabels))
        ax.set_xticks(x_pos)
        ax.set_xticklabels(self.gpsgraphlabels, rotation=70)
        ax.grid(axis="y")

        if ref_info != "":
            rects4 = ax.bar(x, ref_lgvs_avg, width, yerr=ref_lgvs_sd, label=' L GVS', color='gray', alpha=0.40)
            rects5 = ax.bar(x + width, ref_rgvs_avg, width, yerr=ref_rgvs_sd, label=' R GVS', color='gray',
                            alpha=0.40)
            rects6 = ax.bar(x + 2 * width, ref_gvs_avg, width, yerr=ref_gvs_sd, label='LR GVS', color='gray',
                            alpha=0.40)

            rects4 = ax.bar(x, ref_lgvs_avg, width, label=' L GVS', color='gray', alpha=0.40)
            rects5 = ax.bar(x + width, ref_rgvs_avg, width, label=' R GVS', color='gray',
                            alpha=0.40)
            rects6 = ax.bar(x + 2 * width, ref_gvs_avg, width, label='LR GVS', color='gray',
                            alpha=0.40)


        fig.suptitle("GVS_MAP_" + self.graph_type + ".png", y=0.02, fontsize=8, color='gray')

        if ref_comp_caption == "" or ref_comp_caption == "PlugInGait":
            plt.savefig(self.graph_type + "_GVS_MAP" + ".png")
        else:
            plt.savefig(self.graph_type + "_GVS_MAP_" + self.graph_name + "_vs_" + ref_comp_caption + ".png")
        if self.all_graphs != 1:
            plt.show()
        else:
            plt.close
        return "Done"




    def plotrom(self):
        rom = []
        for g in range(self.gno):
            preprom = []
            for i in range(self.plotlevels):
                for j in range(self.planes):
                    if self.plot_labels[i][j] > '':
                        preprom.append(self.calc_rom(self.y_data[g][i][j]))
                    else:
                        preprom.append([0, 0, 0])
            rom.append(preprom)

        fig, axs = plt.subplots(self.plotlevels, self.planes, figsize=(8, 9.5))
        fig.tight_layout(pad=self.graphs_space)
        plt.subplots_adjust(left=0.05,
                            bottom=0.05,
                            right=0.95,
                            top=0.95,
                            wspace=0.4,
                            hspace=0.4)

        for g in range(len(self.refsdminus_data)):
            for i in range(self.plotlevels):
                for j in range(self.planes):
                    if self.plot_labels[i][j] > '':
                        axs[i, j].set_title(self.graph_labels[i][j], fontsize=9)
                        axs[i, j].set_ylim(0, 80)
                        for x in range(self.gno):
                           # rects0 = axs[i, j].bar(x, max(self.ref_data[g][i][j])[0] - min(self.ref_data[g][i][j])[0], yerr=(max(self.refsdminus_data[g][i][j])), color='gray', alpha=0.3)
                            rects0 = axs[i, j].bar(x, max(self.ref_data[g][i][j]) - min(self.ref_data[g][i][j]), color='gray', alpha=0.3)
                            autolabel(axs[i, j], rects0, 'left')
                           # axs[i, j].errorbar(x, max(self.ref_data[g][i][j])[0] - min(self.ref_data[g][i][j])[0], yerr=(self.refsdminus_data[g][i][j])[0], lolims=True, color='gray', linestyle='none', dash_capstyle='butt')

        for g in range(self.gno):
            for i in range(self.plotlevels):
                x = 0
                for j in range(self.planes):
                    if self.graph_labels[i][j] > '':
                        axs[i, j].set_title(self.plot_labels[i][j], fontsize=9)
                        # axs[i, j].set_ylim(0, 80)
                        if self.division_lines[g][1] == 'Left':
                           rects1 = axs[i, j].bar(g, rom[g][i][2], color='red', label = self.division_lines[g][1], alpha=0.3)
                        else:
                           rects1 = axs[i, j].bar(g, rom[g][i][2], color='blue', label = self.division_lines[g][1], alpha=0.3)
                        # print(g, i, j)
                    else:
                        axs[i, j].set_visible(False)
                    autolabel(axs[i, j], rects1, 'right')
                    # axs[i, j].text(80, 1, "MGDI: 1.0 NSDs", fontsize=6)
        plt.savefig("RomGraph.png")

        if self.all_graphs != 1:
            plt.show()
        else:
            plt.close
        return "Done"


    def plotromB(self):
        rom = []
        for g in range(self.gno):
            preprom = []
            for i in range(self.plotlevels):
                for j in range(self.planes):
                    if self.plot_labels[i][j] > '':
                        preprom.append(self.calc_rom(self.y_data[g][i][j]))
                    else:
                        preprom.append([0, 0, 0])
            rom.append(preprom)

        fig, axs = plt.subplots(self.plotlevels, self.planes, figsize=(8, 9.5))
        fig.tight_layout(pad=self.graphs_space)
        plt.subplots_adjust(left=0.05,
                            bottom=0.05,
                            right=0.95,
                            top=0.95,
                            wspace=0.4,
                            hspace=0.4)

        for g in range(len(self.refsdminus_data)):
            for i in range(self.plotlevels):
                for j in range(self.planes):
                    if self.plot_labels[i][j] > '':
                        axs[i, j].set_title(self.graph_labels[i][j], fontsize=9)
                        axs[i, j].set_ylim(0, 80)
                        for x in range(self.gno):
                            rects0 = axs[i, j].bar(x, max(self.ref_data[g][i][j]), yerr=(max(self.refsdplus_data[g][i][j])), color='gray', alpha=0.3)
                            rects0 = axs[i, j].bar(x, min(self.ref_data[g][i][j]), yerr=(max(self.refsdplus_data[g][i][j])), color='gray', alpha=1)
                            autolabel(axs[i, j], rects0, 'left')
                           # axs[i, j].errorbar(x, max(self.ref_data[g][i][j])[0] - min(self.ref_data[g][i][j])[0], yerr=(self.refsdminus_data[g][i][j])[0], lolims=True, color='gray', linestyle='none', dash_capstyle='butt')

        # for g in range(self.gno):
        #     for i in range(self.plotlevels):
        #         x = 0
        #         for j in range(self.planes):
        #             if self.graph_labels[i][j] > '':
        #                 axs[i, j].set_title(self.plot_labels[i][j], fontsize=9)
        #                 # axs[i, j].set_ylim(0, 80)
        #                 if self.division_lines[g][1] == 'Left':
        #                    rects1 = axs[i, j].bar(g, rom[g][i][2], color='red', label = self.division_lines[g][1], alpha=0.3)
        #                 else:
        #                    rects1 = axs[i, j].bar(g, rom[g][i][2], color='blue', label = self.division_lines[g][1], alpha=0.3)
        #                 print g, i, j
        #             else:
        #                 axs[i, j].set_visible(False)
        #             autolabel(axs[i, j], rects1, 'right')
        #             # axs[i, j].text(80, 1, "MGDI: 1.0 NSDs", fontsize=6)
        plt.savefig("RomBGraph.png")
        if self.all_graphs != 1:
            plt.show()
        else:
            plt.close
        return "Done"


def autolabel(axs, rects, xpos='center'):
    """
    Attach a text label above each bar in *rects*, displaying its height.

    *xpos* indicates which side to place the text w.r.t. the center of
    the bar. It can be one of the following {'center', 'right', 'left'}.
    """

    ha = {'center': 'center', 'right': 'left', 'left': 'right'}
    offset = {'center': 0, 'right': 1, 'left': -1}

    for rect in rects:
        height = rect.get_height()
        axs.annotate('{}'.format(int(height)),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(offset[xpos]*3, 0),  # use 3 points offset
                    textcoords="offset points",  # in both directions
                    ha=ha[xpos], va='bottom', fontsize=7)



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
        plt.savefig("_selected_" + ax.get_title())
        print ("save to:" + "_selected_" + ax.get_title())

    else:
        # restore the original state

        zoomed_axes[0][0].set_position(zoomed_axes[0][1])
        zoomed_axes[0] = None

        # make other axes visible again
        for axis in event.canvas.figure.axes:
            if axis.get_title( loc='center') > '':
                axis.set_visible(True)

    event.canvas.draw()
