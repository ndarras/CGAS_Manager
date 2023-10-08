from matplotlib import pyplot as plt
import filefunctions as ff
import numpy as np
import pickle
import logging
import os

class tsBarsData:
    def __init__(self, graph_type, graph_name, all_graphs):
        self.graph_type = graph_type
        self.graph_name = graph_name
        self.all_graphs = all_graphs
        self.ts_fields = ff.getdata("sysdata", "ts_fields.p")
        self.ts_data = ff.getdata("sysdata", "ts_data.p")
        self.ts_ref_fields = ff.getdata("sysdata", "ts_ref_fields.p")
        self.gno = ff.getdata("sysdata", "ts_ref_data.p")
        self.graph_LR_sets = ff.getdata("sysdata", "lr_sets.p")
        self.ts_avg_data = ff.getdata("sysdata", "ts_avg_data.p")
        self.ts_sd_data = ff.getdata("sysdata", "ts_sd_data.p")
        self.division_lines = ff.getdata("sysdata", "division_lines.p")
        self.ref_lines = ff.getdata("sysdata", "ref_lines.p")
        self.line_colours = ff.getdata("sysdata", "lineColours.p")

        self.cadence = []
        self.doublesupport = []
        self.singlesupport = []
        self.steplength = []
        self.stepwidth = []
        self.walkingvelocity = []
        self.stridelength = []
        self.stancepcnt = []

        self.cadencel = []
        self.doublesupportl = []
        self.singlesupportl = []
        self.steplengthl = []
        self.stepwidthl = []
        self.walkingvelocityl = []
        self.stridelengthl = []
        self.stancepcntl = []

        self.cadencer = []
        self.doublesupportr = []
        self.singlesupportr = []
        self.steplengthr = []
        self.stepwidthr = []
        self.walkingvelocityr = []
        self.stridelengthr = []
        self.stancepcntr = []

        self.cadence_stats = []
        self.doublesupport_stats = []
        self.singlesupport_stats = []
        self.steplength_stats = []
        self.stepwidth_stats = []
        self.walkingvelocity_stats = []
        self.stridelength_stats = []
        self.stancepcnt_stats = []

        self.barcolor = []
        self.leftcolor = "red"
        self.rightcolor = "blue"

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

    def tsrefval (self, vallist, rounddigits):
        retpcnt = []
        retlabel = []
        if rounddigits == 0:
            retlabel.append(str(int(vallist[0])) )
            retpcnt.append(str(100) + "%")
        else:
            retlabel.append(str(round(vallist[0], rounddigits)))
            retpcnt.append( str(100) + "%")
        for i in range(1, len(vallist)):
            pcnt = 0
            pcnt = (vallist[i] / vallist[0]) * 100
            retpcnt.append(str(int(pcnt))+"%")
            if rounddigits == 0:
                retlabel.append(str(int(vallist[i])))
            else:
                retlabel.append(str(round(vallist[i], rounddigits)))
        return retlabel, retpcnt

    def calc_graph_data(self):

        n = (4, 2)

        self.cadence_stats = np.zeros(n)
        self.doublesupport_stats = np.zeros(n)
        self.singlesupport_stats = np.zeros(n)
        self.steplength_stats = np.zeros(n)
        self.stepwidth_stats = np.zeros(n)
        self.walkingvelocity_stats = np.zeros(n)
        self.stridelength_stats = np.zeros(n)
        self.stancepcnt_stats = np.zeros(n)

        self.cadence.append(self.ts_avg_data[0:][0][0])
        self.doublesupport.append(self.ts_avg_data[0:][0][1])
        self.singlesupport.append(self.ts_avg_data[0:][0][2])
        self.steplength.append(self.ts_avg_data[0:][0][3])
        self.stepwidth.append(self.ts_avg_data[0:][0][4])
        self.walkingvelocity.append(self.ts_avg_data[0:][0][5])
        self.stridelength.append(self.ts_avg_data[0:][0][6])
        self.stancepcnt.append(self.ref_lines[0][0][0])
        self.barcolor.append("green")

        selectedC3Ds = []
        lineColours = []
        selectedC3Ds, lineColours = ff.getselectedc3ds()


        for i in range(len(self.ts_data)):
            self.cadence.append(self.ts_data[0:][i][0])
            self.doublesupport.append(self.ts_data[0:][i][1])
            self.singlesupport.append(self.ts_data[0:][i][2])
            self.steplength.append(self.ts_data[0:][i][3])
            self.stepwidth.append(self.ts_data[0:][i][4])
            self.walkingvelocity.append(self.ts_data[0:][i][5])
            self.stridelength.append(self.ts_data[0:][i][6])
            self.stancepcnt.append(self.division_lines[0:][i][0][0])

            if (selectedC3Ds[i][2] == "Left"):
                self.cadencel.append(self.ts_data[0:][i][0])
                self.doublesupportl.append(self.ts_data[0:][i][1])
                self.singlesupportl.append(self.ts_data[0:][i][2])
                self.steplengthl.append(self.ts_data[0:][i][3])
                self.stepwidthl.append(self.ts_data[0:][i][4])
                self.walkingvelocityl.append(self.ts_data[0:][i][5])
                self.stridelengthl.append(self.ts_data[0:][i][6])
                self.barcolor.append(self.line_colours[i][0])
                self.stancepcntl.append(self.division_lines[0:][i][0][0])

            if (selectedC3Ds[i][2] == "Right"):
                self.cadencer.append(self.ts_data[0:][i][0])
                self.doublesupportr.append(self.ts_data[0:][i][1])
                self.singlesupportr.append(self.ts_data[0:][i][2])
                self.steplengthr.append(self.ts_data[0:][i][3])
                self.stepwidthr.append(self.ts_data[0:][i][4])
                self.walkingvelocityr.append(self.ts_data[0:][i][5])
                self.stridelengthr.append(self.ts_data[0:][i][6])
                self.barcolor.append(self.line_colours[i][0])
                self.stancepcntr.append(self.division_lines[0:][i][0][0])


        self.cadence_stats[0, 0] = self.ts_avg_data[0:][0][0]
        self.cadence_stats[0, 1] = self.ts_sd_data[0:][0][0]
        self.cadence_stats[1, 0] = self.mean(self.cadence[1:])
        self.cadence_stats[1, 1] = self.stdev(self.cadence[1:])
        self.cadence_stats[2, 0] = self.mean(self.cadencel)
        self.cadence_stats[2, 1] = self.stdev(self.cadencel)
        self.cadence_stats[3, 0] = self.mean(self.cadencer)
        self.cadence_stats[3, 1] = self.stdev(self.cadencer)

        self.doublesupport_stats[0, 0] = self.ts_avg_data[0:][0][1]
        self.doublesupport_stats[0, 1] = self.ts_sd_data[0:][0][1]
        self.doublesupport_stats[1, 0] = self.mean(self.doublesupport[1:])
        self.doublesupport_stats[1, 1] = self.stdev(self.doublesupport[1:])
        self.doublesupport_stats[2, 0] = self.mean(self.doublesupportl)
        self.doublesupport_stats[2, 1] = self.stdev(self.doublesupportl)
        self.doublesupport_stats[3, 0] = self.mean(self.doublesupportr)
        self.doublesupport_stats[3, 1] = self.stdev(self.doublesupportr)

        self.singlesupport_stats[0, 0] = self.ts_avg_data[0:][0][2]
        self.singlesupport_stats[0, 1] = self.ts_sd_data[0:][0][2]
        self.singlesupport_stats[1, 0] = self.mean(self.singlesupport[1:])
        self.singlesupport_stats[1, 1] = self.stdev(self.singlesupport[1:])
        self.singlesupport_stats[2, 0] = self.mean(self.singlesupportl)
        self.singlesupport_stats[2, 1] = self.stdev(self.singlesupportl)
        self.singlesupport_stats[3, 0] = self.mean(self.singlesupportr)
        self.singlesupport_stats[3, 1] = self.stdev(self.singlesupportr)

        self.steplength_stats[0, 0] = self.ts_avg_data[0:][0][3]
        self.steplength_stats[0, 1] = self.ts_sd_data[0:][0][3]
        self.steplength_stats[1, 0] = self.mean(self.steplength[1:])
        self.steplength_stats[1, 1] = self.stdev(self.steplength[1:])
        self.steplength_stats[2, 0] = self.mean(self.steplengthl)
        self.steplength_stats[2, 1] = self.stdev(self.steplengthl)
        self.steplength_stats[3, 0] = self.mean(self.steplengthr)
        self.steplength_stats[3, 1] = self.stdev(self.steplengthr)

        self.stepwidth_stats[0, 0] = self.ts_avg_data[0:][0][4]
        self.stepwidth_stats[0, 1] = self.ts_sd_data[0:][0][4]
        self.stepwidth_stats[1, 0] = self.mean(self.stepwidth[1:])
        self.stepwidth_stats[1, 1] = self.stdev(self.stepwidth[1:])
        self.stepwidth_stats[2, 0] = self.mean(self.stepwidthl)
        self.stepwidth_stats[2, 1] = self.stdev(self.stepwidthl)
        self.stepwidth_stats[3, 0] = self.mean(self.stepwidthr)
        self.stepwidth_stats[3, 1] = self.stdev(self.stepwidthr)

        self.walkingvelocity_stats[0, 0] = self.ts_avg_data[0:][0][5]
        self.walkingvelocity_stats[0, 1] = self.ts_sd_data[0:][0][5]
        self.walkingvelocity_stats[1, 0] = self.mean(self.walkingvelocity[1:])
        self.walkingvelocity_stats[1, 1] = self.stdev(self.walkingvelocity[1:])
        self.walkingvelocity_stats[2, 0] = self.mean(self.walkingvelocityl)
        self.walkingvelocity_stats[2, 1] = self.stdev(self.walkingvelocityl)
        self.walkingvelocity_stats[3, 0] = self.mean(self.walkingvelocityr)
        self.walkingvelocity_stats[3, 1] = self.stdev(self.walkingvelocityr)

        self.stridelength_stats[0, 0] = self.ts_avg_data[0:][0][6]
        self.stridelength_stats[0, 1] = self.ts_sd_data[0:][0][6]
        self.stridelength_stats[1, 0] = self.mean(self.stridelength[1:])
        self.stridelength_stats[1, 1] = self.stdev(self.stridelength[1:])
        self.stridelength_stats[2, 0] = self.mean(self.stridelengthl)
        self.stridelength_stats[2, 1] = self.stdev(self.stridelengthl)
        self.stridelength_stats[3, 0] = self.mean(self.stridelengthr)
        self.stridelength_stats[3, 1] = self.stdev(self.stridelengthr)

        self.stancepcnt_stats[0, 0] = self.ref_lines[0][0][0]
        self.stancepcnt_stats[0, 1] = self.ref_lines[0][1][0]
        self.stancepcnt_stats[1, 0] = self.mean(self.stancepcnt[1:])
        self.stancepcnt_stats[1, 1] = self.stdev(self.stancepcnt[1:])
        self.stancepcnt_stats[2, 0] = self.mean(self.stancepcntl[1:])
        self.stancepcnt_stats[2, 1] = self.stdev(self.stancepcntl[1:])
        self.stancepcnt_stats[3, 0] = self.mean(self.stancepcntr[1:])
        self.stancepcnt_stats[3, 1] = self.stdev(self.stancepcntr[1:])

        outfile = open('sysdata//Reference_' + self.graph_type + '_TS_AVG.p', 'wb')
        pickle.dump(self.cadence_stats, outfile)
        pickle.dump(self.doublesupport_stats, outfile)
        pickle.dump(self.singlesupport_stats, outfile)
        pickle.dump(self.steplength_stats, outfile)
        pickle.dump(self.stepwidth_stats, outfile)
        pickle.dump(self.walkingvelocity_stats, outfile)
        pickle.dump(self.stridelength_stats, outfile)
        pickle.dump(self.stancepcnt_stats, outfile)
        outfile.close()
        logging.info("TS Stat Calculated")




    def plottsbars(self):

        self.calc_graph_data()

        graphprefs = ff.getgraphprefs("Temporospatial")
        if len(graphprefs) > 0:
            fig, axs = plt.subplots(4, 2, figsize=(graphprefs[0], graphprefs[1]))
        else:
            fig, axs = plt.subplots(4, 2, figsize=(8, 9.5))


        fig.canvas.mpl_connect('button_press_event', on_click)


        plt.subplots_adjust(left=0.05,
                            bottom=0.05,
                            right=0.95,
                            top=0.95,
                            wspace=0.4,
                            hspace=0.4)

        x = 0
        x = np.arange(len(self.ts_data)+1)
        barerror = np.zeros(len(self.ts_data)+1)

        barerror[0] = self.ts_sd_data[:][0][0]
        axs[0, 0].set_title(self.ts_fields[0], fontsize=8)
        axs[0, 0].bar(x, self.cadence, color=self.barcolor, yerr=barerror)

        barerror[0] = self.ts_sd_data[:][0][1]
        axs[0, 1].set_title(self.ts_fields[1], fontsize=8)
        axs[0, 1].bar(x, self.doublesupport, color=self.barcolor, yerr=barerror)

        barerror[0] = self.ts_sd_data[:][0][2]
        axs[1, 0].set_title(self.ts_fields[2], fontsize=8)
        axs[1, 0].bar(x, self.singlesupport, color=self.barcolor, yerr=barerror)

        barerror[0] = self.ts_sd_data[:][0][3]
        axs[1, 1].set_title(self.ts_fields[3], fontsize=8)
        axs[1, 1].bar(x, self.steplength, color=self.barcolor, yerr=barerror)

        barerror[0] = self.ts_sd_data[:][0][4]
        axs[2, 0].set_title(self.ts_fields[4], fontsize=8)
        axs[2, 0].bar(x, self.stepwidth, color=self.barcolor, yerr=barerror)

        barerror[0] = self.ts_sd_data[:][0][5]
        axs[2, 1].set_title(self.ts_fields[5], fontsize=8)
        axs[2, 1].bar(x, self.walkingvelocity, color=self.barcolor, yerr=barerror)

        barerror[0] = self.ts_sd_data[:][0][6]
        axs[3, 0].set_title(self.ts_fields[6], fontsize=8)
        axs[3, 0].bar(x, self.stridelength, color=self.barcolor, yerr=barerror)

        barerror[0] = self.ref_lines[0][1][0]
        axs[3, 1].set_title("Stance Phase as % Gait Cycle", fontsize=8)
        axs[3, 1].bar(x, self.stancepcnt, color=self.barcolor, yerr=barerror)

        fig.suptitle("Temporospatial " + self.graph_type + " " + self.graph_name,  y=0.02, fontsize=8, color='gray')

        plt.savefig(self.graph_type + "_Temporospatial_Avg.png")

        if self.all_graphs != 1:
            plt.show()
        else:
            plt.close

    def plotavgtsbars(self):

        self.calc_graph_data()
        ref_color = "gray"
        ref_alpha = 0.35
        ref_info = ""
        ref_path = ff.getfileparams("compare.ini", 0)
        ref_name = ff.getfileparams("compare.ini", 1)
        ref_comp_caption = ff.getfileparams("compare.ini", 2)

        ref_filename = ""
        if ref_name != '':
            for file in os.listdir(ref_path):
                if file.startswith("Reference_Kinematics_TS"):
                    ref_filename = file

            if ref_filename != "":
                ref_info = ref_filename.split("_")
                if os.path.isfile(ref_path + ref_filename):
                    infile = open(ref_path + ref_filename, 'rb')
                    ref_cadence_stats = pickle.load(infile)
                    ref_doublesupport_stats = pickle.load(infile)
                    ref_singlesupport_stats = pickle.load(infile)
                    ref_steplength_stats = pickle.load(infile)
                    ref_stepwidth_stats = pickle.load(infile)
                    ref_walkingvelocity_stats = pickle.load(infile)
                    ref_stridelength_stats = pickle.load(infile)
                    ref_stancepcnt_stats = pickle.load(infile)
                    infile.close()

        graphprefs = ff.getgraphprefs("AverageTemporospatial")
        if len(graphprefs) > 0:
            fig, axs = plt.subplots(4, 2, figsize=(graphprefs[0], graphprefs[1]))
        else:
            fig, axs = plt.subplots(4, 2, figsize=(8, 9.5))

        # fig, axs = plt.subplots(4, 2, figsize=(8, 9.5))
        fig.canvas.mpl_connect('button_press_event', on_click)

        if ref_name == "":
            fig.suptitle("TS Graphs Average(SD) " + self.graph_type + " " + self.graph_name, y=0.02, fontsize=8,
                         color='gray')
        else:
            fig.suptitle("TS Graphs Average(SD) " + self.graph_type + " " + self.graph_name + "_vs_" + ref_comp_caption,
                         y=0.02, fontsize=8,
                         color='gray')

        titlefsize = 10
        fsize = 7

        self.barcolor = []

        self.barcolor.append('green')
        self.barcolor.append('orange')
        self.barcolor.append(self.line_colours[0][0])
        self.barcolor.append(self.line_colours[1][0])

        plt.subplots_adjust(left=0.10,
                            bottom=0.05,
                            right=0.90,
                            top=0.95,
                            wspace=0.4,
                            hspace=0.4)
        i = 0
        x = []
        reflabel = []
        refpcnt = []
        # x = np.arange(len(self.cadence_stats[:, 0]))
        x = ["Normal", "L&R", "Left", "Right"]

        barerror = self.walkingvelocity_stats[:, 1]
        axs[0, 0].set_title("Walking Velocity", fontsize=titlefsize)
        axs[0, 0].tick_params(axis='x', labelsize=10)
        axs[0, 0].tick_params(axis='y', labelsize=8)
        axs[0, 0].set_ylabel('m/s', fontsize=8)
        axs[0, 0].bar(x, self.walkingvelocity_stats[:, 0], color=self.barcolor, yerr=barerror)
        if ref_name != '':
            barerror = ref_walkingvelocity_stats[:, 1]
            axs[0, 0].bar(x, ref_walkingvelocity_stats[:, 0], color=ref_color, yerr=barerror, alpha=ref_alpha)
            reflabel, refpcnt = self.tsrefval(ref_walkingvelocity_stats[:, 0], 2)
            xmin, xmax, ymin, ymax = axs[0, 0].axis()
            for i in range(len(ref_walkingvelocity_stats[:, 0])):
                axs[0, 0].text(i - 0.34, .1 * ymax, reflabel[i], fontsize=fsize, color="black", fontweight='bold')
                axs[0, 0].text(i - 0.38, 0, refpcnt[i], fontsize=fsize + 3, color="black", fontweight='bold')
        reflabel, refpcnt = self.tsrefval(self.walkingvelocity_stats[:, 0], 2)
        for i in range(len(self.walkingvelocity_stats[:, 0])):
            axs[0, 0].text(i - 0.38, self.walkingvelocity_stats[i, 0], reflabel[i], fontsize=fsize, color="gray",
                           fontweight='bold')
            axs[0, 0].text(i - 0.38, self.walkingvelocity_stats[i, 0] / 2, refpcnt[i], fontsize=fsize + 3, color="white",
                           fontweight='bold')

        barerror = self.cadence_stats[:, 1]
        axs[0, 1].set_title("Cadence", fontsize=titlefsize)
        axs[0, 1].tick_params(axis='x', labelsize=10)
        axs[0, 1].tick_params(axis='y', labelsize=8)
        axs[0, 1].set_ylabel('steps/min', fontsize=8)
        axs[0, 1].bar(x, self.cadence_stats[:, 0], color=self.barcolor, yerr=barerror)
        if ref_name != '':
            barerror = ref_cadence_stats[:, 1]
            axs[0, 1].bar(x, ref_cadence_stats[:, 0], color=ref_color, yerr=barerror, alpha=ref_alpha)
            reflabel, refpcnt = self.tsrefval(ref_cadence_stats[:, 0], 2)
            xmin, xmax, ymin, ymax = axs[0, 1].axis()
            for i in range(len(ref_cadence_stats[:, 0])):
                axs[0, 1].text(i - 0.34, .1 * ymax, reflabel[i], fontsize=fsize, color="black", fontweight='bold')
                axs[0, 1].text(i - 0.38, 0, refpcnt[i], fontsize=fsize + 3, color="black", fontweight='bold')
        reflabel, refpcnt = self.tsrefval(self.cadence_stats[:, 0], 0)
        for i in range(len(self.cadence_stats[:, 0])):
            axs[0, 1].text(i - 0.40, self.cadence_stats[i, 0], reflabel[i], fontsize=fsize, color="gray", fontweight='bold')
            axs[0, 1].text(i - 0.38, self.cadence_stats[i, 0] / 2, refpcnt[i], fontsize=fsize + 3, color="white",
                           fontweight='bold')

        barerror = self.steplength_stats[:, 1]
        axs[1, 0].set_title("Step Length", fontsize=titlefsize)
        axs[1, 0].tick_params(axis='x', labelsize=10)
        axs[1, 0].tick_params(axis='y', labelsize=8)
        axs[1, 0].set_ylabel('m', fontsize=8)
        axs[1, 0].bar(x, self.steplength_stats[:, 0], color=self.barcolor, yerr=barerror)
        reflabel, refpcnt = self.tsrefval(self.steplength_stats[:, 0], 2)
        if ref_name != '':
            barerror = ref_steplength_stats[:, 1]
            axs[1, 0].bar(x, ref_steplength_stats[:, 0], color=ref_color, yerr=barerror, alpha=ref_alpha)
            reflabel, refpcnt = self.tsrefval(ref_steplength_stats[:, 0], 2)
            xmin, xmax, ymin, ymax = axs[1, 0].axis()
            for i in range(len(ref_steplength_stats[:, 0])):
                axs[1, 0].text(i - 0.34, .1 * ymax, reflabel[i], fontsize=fsize, color="black", fontweight='bold')
                axs[1, 0].text(i - 0.38, 0, refpcnt[i], fontsize=fsize + 3, color="black", fontweight='bold')
        reflabel, refpcnt = self.tsrefval(self.steplength_stats[:, 0], 2)
        for i in range(len(self.steplength_stats[:, 0])):
            axs[1, 0].text(i - 0.40, self.steplength_stats[i, 0], reflabel[i], fontsize=fsize, color="gray",
                           fontweight='bold')
            axs[1, 0].text(i - 0.38, self.steplength_stats[i, 0] / 2, refpcnt[i], fontsize=fsize + 3, color="white",
                           fontweight='bold')

        barerror = self.stridelength_stats[:, 1]
        axs[1, 1].set_title("Stride Length", fontsize=titlefsize)
        axs[1, 1].tick_params(axis='x', labelsize=10)
        axs[1, 1].tick_params(axis='y', labelsize=8)
        axs[1, 1].set_ylabel('m', fontsize=8)
        axs[1, 1].bar(x, self.stridelength_stats[:, 0], color=self.barcolor, yerr=barerror)
        if ref_name != '':
            barerror = ref_stridelength_stats[:, 1]
            axs[1, 1].bar(x, ref_stridelength_stats[:, 0], color=ref_color, yerr=barerror, alpha=ref_alpha)
            reflabel, refpcnt = self.tsrefval(ref_stridelength_stats[:, 0], 2)
            xmin, xmax, ymin, ymax = axs[1, 1].axis()
            for i in range(len(ref_stridelength_stats[:, 0])):
                axs[1, 1].text(i - 0.34, .1 * ymax, reflabel[i], fontsize=fsize, color="black", fontweight='bold')
                axs[1, 1].text(i - 0.38, 0, refpcnt[i], fontsize=fsize + 3, color="black", fontweight='bold')
        reflabel, refpcnt = self.tsrefval(self.stridelength_stats[:, 0], 2)
        for i in range(len(self.stridelength_stats[:, 0])):
            axs[1, 1].text(i - 0.40, self.stridelength_stats[i, 0], reflabel[i], fontsize=fsize, color="gray",
                           fontweight='bold')
            axs[1, 1].text(i - 0.38, self.stridelength_stats[i, 0] / 2, refpcnt[i], fontsize=fsize + 3, color="white",
                           fontweight='bold')

        barerror = self.singlesupport_stats[:, 1]
        axs[2, 0].set_title("Single Support", fontsize=titlefsize)
        axs[2, 0].tick_params(axis='x', labelsize=10)
        axs[2, 0].tick_params(axis='y', labelsize=8)
        axs[2, 0].set_ylabel('s', fontsize=8)
        axs[2, 0].bar(x, self.singlesupport_stats[:, 0], color=self.barcolor, yerr=barerror)
        if ref_name != '':
            barerror = ref_singlesupport_stats[:, 1]
            axs[2, 0].bar(x, ref_singlesupport_stats[:, 0], color=ref_color, yerr=barerror, alpha=ref_alpha)
            reflabel, refpcnt = self.tsrefval(ref_singlesupport_stats[:, 0], 2)
            xmin, xmax, ymin, ymax = axs[2, 0].axis()
            for i in range(len(ref_singlesupport_stats[:, 0])):
                axs[2, 0].text(i - 0.34, .1 * ymax, reflabel[i], fontsize=fsize, color="black", fontweight='bold')
                axs[2, 0].text(i - 0.38, 0, refpcnt[i], fontsize=fsize + 3, color="black", fontweight='bold')
        reflabel, refpcnt = self.tsrefval(self.singlesupport_stats[:, 0], 2)
        for i in range(len(self.singlesupport_stats[:, 0])):
            axs[2, 0].text(i - 0.40, self.singlesupport_stats[i, 0], reflabel[i], fontsize=fsize, color="gray",
                           fontweight='bold')
            axs[2, 0].text(i - 0.38, self.singlesupport_stats[i, 0] / 2, refpcnt[i], fontsize=fsize + 3, color="white",
                           fontweight='bold')

        barerror = self.doublesupport_stats[:, 1]
        axs[2, 1].set_title("Double Support", fontsize=titlefsize)
        axs[2, 1].tick_params(axis='x', labelsize=10)
        axs[2, 1].tick_params(axis='y', labelsize=8)
        axs[2, 1].set_ylabel('s', fontsize=8)
        axs[2, 1].bar(x, self.doublesupport_stats[:, 0], color=self.barcolor, yerr=barerror)
        if ref_name != '':
            barerror = ref_doublesupport_stats[:, 1]
            axs[2, 1].bar(x, ref_doublesupport_stats[:, 0], color=ref_color, yerr=barerror, alpha=ref_alpha)
            reflabel, refpcnt = self.tsrefval(ref_doublesupport_stats[:, 0], 2)
            xmin, xmax, ymin, ymax = axs[2, 1].axis()
            for i in range(len(ref_doublesupport_stats[:, 0])):
                axs[2, 1].text(i - 0.34, .1 * ymax, reflabel[i], fontsize=fsize, color="black", fontweight='bold')
                axs[2, 1].text(i - 0.38, 0, refpcnt[i], fontsize=fsize + 3, color="black", fontweight='bold')
        reflabel, refpcnt = self.tsrefval(self.doublesupport_stats[:, 0], 2)
        for i in range(len(self.doublesupport_stats[:, 0])):
            axs[2, 1].text(i - 0.40, self.doublesupport_stats[i, 0], reflabel[i], fontsize=fsize, color="gray",
                           fontweight='bold')
            axs[2, 1].text(i - 0.38, self.doublesupport_stats[i, 0] / 2, refpcnt[i], fontsize=fsize + 3, color="white",
                           fontweight='bold')

        barerror = self.stepwidth_stats[:, 1]
        axs[3, 0].set_title("Step Width", fontsize=titlefsize)
        axs[3, 0].tick_params(axis='x', labelsize=10)
        axs[3, 0].tick_params(axis='y', labelsize=8)
        axs[3, 0].set_ylabel('m', fontsize=8)
        axs[3, 0].bar(x, self.stepwidth_stats[:, 0], color=self.barcolor, yerr=barerror)

        if ref_name != '':
            barerror = ref_stepwidth_stats[:, 1]
            axs[3, 0].bar(x, ref_stepwidth_stats[:, 0], color=ref_color, yerr=barerror, alpha=ref_alpha)
            reflabel, refpcnt = self.tsrefval(ref_stepwidth_stats[:, 0], 2)
            xmin, xmax, ymin, ymax = axs[3, 0].axis()
            for i in range(len(ref_stepwidth_stats[:, 0])):
                axs[3, 0].text(i - 0.34, .1 * ymax, reflabel[i], fontsize=fsize, color="black", fontweight='bold')
                axs[3, 0].text(i - 0.38, 0, refpcnt[i], fontsize=fsize + 3, color="black", fontweight='bold')
        reflabel, refpcnt = self.tsrefval(self.stepwidth_stats[:, 0], 2)
        for i in range(len(self.stepwidth_stats[:, 0])):
            axs[3, 0].text(i - 0.40, self.stepwidth_stats[i, 0], reflabel[i], fontsize=fsize, color="gray",
                           fontweight='bold')
            axs[3, 0].text(i - 0.38, self.stepwidth_stats[i, 0] / 2, refpcnt[i], fontsize=fsize + 3, color="white",
                           fontweight='bold')

        barerror = self.stancepcnt_stats[:, 1]
        axs[3, 1].set_title("Stance Phase ", fontsize=titlefsize)
        axs[3, 1].tick_params(axis='x', labelsize=10)
        axs[3, 1].tick_params(axis='y', labelsize=8)
        axs[3, 1].set_ylabel('% Gait Cycle', fontsize=8)
        axs[3, 1].bar(x, self.stancepcnt_stats[:, 0], color=self.barcolor, yerr=barerror)
        if ref_name != '':
            barerror = ref_stancepcnt_stats[:, 1]
            axs[3, 1].bar(x, ref_stancepcnt_stats[:, 0], color=ref_color, yerr=barerror, alpha=ref_alpha)
            reflabel, refpcnt = self.tsrefval(ref_stancepcnt_stats[:, 0], 2)
            xmin, xmax, ymin, ymax = axs[3, 1].axis()
            for i in range(len(ref_stancepcnt_stats[:, 0])):
                axs[3, 1].text(i - 0.34, .1 * ymax, reflabel[i], fontsize=fsize, color="black", fontweight='bold')
                axs[3, 1].text(i - 0.38, 0, refpcnt[i], fontsize=fsize + 3, color="black", fontweight='bold')
        reflabel, refpcnt = self.tsrefval(self.stancepcnt_stats[:, 0], 2)
        for i in range(len(self.stancepcnt_stats[:, 0])):
            axs[3, 1].text(i - 0.40, self.stancepcnt_stats[i, 0], reflabel[i], fontsize=fsize, color="gray",
                           fontweight='bold')
            axs[3, 1].text(i - 0.38, self.stancepcnt_stats[i, 0] / 2, refpcnt[i], fontsize=fsize + 3, color="white",
                           fontweight='bold')

        if ref_name == "":
            plt.savefig(self.graph_type + "_TemporospatialAvg.png")
        else:
            plt.savefig(self.graph_type + "_TemporospatialAvg" +  "_" + self.graph_name+ "_vs_" + ref_comp_caption + ".png")

        if self.all_graphs != 1:
            plt.show()
        else:
            plt.close

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
        logging.info("save to:" + "_selected_" + ax.get_title())

    else:
        # restore the original state

        zoomed_axes[0][0].set_position(zoomed_axes[0][1])
        zoomed_axes[0] = None

        # make other axes visible again
        for axis in event.canvas.figure.axes:
            if axis.get_title( loc='center') > '':
                axis.set_visible(True)

    event.canvas.draw()



def on_plot_hover(event):
    # Iterating over each data member plotted
    for curve in plt.get_lines():
        # Searching which data member corresponds to current mouse position
        if curve.contains(event)[0]:
            print ("over %s" % curve.get_gid())

