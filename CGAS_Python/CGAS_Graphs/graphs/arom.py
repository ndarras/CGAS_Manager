from matplotlib import pyplot as plt
from matplotlib import patches as patches
import filefunctions as ff
import numpy as np
import copy
import csv


class AROMData:
    def __init__(self, graph_type, graph_name, all_graphs):
        self.graph_type = graph_type
        self.graph_name = graph_name
        self.all_graphs = all_graphs
        self.lr_sets = []
        self.x_data = []
        self.y_data = []
        self.ref_data = []
        self.ref_lines = []
        self.refsd_data = []
        self.refsdminus_data = []
        self.refsdplus_data = []
        self.dev_data = []
        self.norm_dev_data = []
        self.asy_data = []
        self.norm_asy_data = []
        self.dev_idx = []
        self.asy_idx = []
        self.mgdi_idx = []
        self.lmgdi_idx = []
        self.rmgdi_idx = []
        self.mgai_idx = []
        self.gpsgraphs = []
        self.rom =[]
        self.avgrom =[]
        self.sdrom =[]

    def calcromdata(self):
        self.group_colours = ff.getdata("sysdata", "groupColours.p")
        self.line_colours = ff.getdata("sysdata", "lineColours.p")
        self.groupno = ff.getdata("sysdata", "groupno.p")
        self.gno = ff.getdata("sysdata", "gno.p")

        self.graphs_space = ff.getdata("sysdata", "graphs_space.p")
        self.samples = ff.getdata("sysdata", "samples.p")
        self.planes =ff.getdata("sysdata", "planes.p")
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

        azero = np.zeros((self.gno, self.plotlevels, self.planes, 3))
        self.rom = copy.deepcopy(azero)
        for g in range(self.gno):
            for i in range(self.plotlevels):
                for j in range(self.planes):
                    preprom = []
                    if self.plot_names[i][j] > '':
                        preprom.append(self.calc_rom(self.y_data[g][i][j]))
                    else:
                        preprom.append([0, 0, 0])
                    self.rom[g][i][j][0] = preprom[0][0]
                    self.rom[g][i][j][1] = preprom[0][1]
                    self.rom[g][i][j][2] = preprom[0][2]

        azero = np.zeros((self.plotlevels, self.planes, 3, 3))
        self.avgrom = copy.deepcopy(azero)
        self.sdrom = copy.deepcopy(azero)

        for i in range(self.plotlevels):
            for j in range(self.planes):
                lrommin = []
                lrommax = []
                lrom = []
                rrommin = []
                rrommax = []
                rrom = []
                for g in range(len(self.lr_sets)):
                    lrommin.append(self.rom[self.lr_sets[g][0]][i][j][0])
                    lrommax.append(self.rom[self.lr_sets[g][0]][i][j][1])
                    lrom.append(self.rom[self.lr_sets[g][0]][i][j][2])
                    rrommin.append(self.rom[self.lr_sets[g][1]][i][j][0])
                    rrommax.append(self.rom[self.lr_sets[g][1]][i][j][1])
                    rrom.append(self.rom[self.lr_sets[g][1]][i][j][2])
                self.avgrom[i][j][0][0] = self.mean(lrommin)
                self.avgrom[i][j][0][1] = self.mean(lrommax)
                self.avgrom[i][j][0][2] = self.mean(lrom)
                self.avgrom[i][j][1][0] = self.mean(rrommin)
                self.avgrom[i][j][1][1] = self.mean(rrommax)
                self.avgrom[i][j][1][2] = self.mean(rrom)
                self.avgrom[i][j][2][0] = (self.avgrom[i][j][0][0] + self.avgrom[i][j][1][0]) /2
                self.avgrom[i][j][2][1] = (self.avgrom[i][j][0][1] + self.avgrom[i][j][1][1]) /2
                self.avgrom[i][j][2][2] = (self.avgrom[i][j][0][2] + self.avgrom[i][j][1][2]) /2
                self.sdrom[i][j][0][0] = self.stdev(lrommin)
                self.sdrom[i][j][0][1] = self.stdev(lrommax)
                self.sdrom[i][j][0][2] = self.stdev(lrom)
                self.sdrom[i][j][1][0] = self.stdev(rrommin)
                self.sdrom[i][j][1][1] = self.stdev(rrommax)
                self.sdrom[i][j][1][2] = self.stdev(rrom)
                self.sdrom[i][j][2][0] = (self.sdrom[i][j][0][0] + self.sdrom[i][j][1][0]) /2
                self.sdrom[i][j][2][1] = (self.sdrom[i][j][0][1] + self.sdrom[i][j][1][1]) /2
                self.sdrom[i][j][2][2] = (self.sdrom[i][j][0][2] + self.sdrom[i][j][1][2]) /2



    def calc_rom(self, gval):
        rom = []
        minval = float(15)
        maxval = float(15)
        romval = float(15)
        minval = min(gval)
        maxval = max(gval)
        rom.append(minval)
        rom.append(maxval)
        romval = maxval - minval
        rom.append(romval)
        return rom

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

    def plotrom(self):

        graphprefs = ff.getgraphprefs("Range Of Motion")
        if len(graphprefs) > 0:
            fig, axs = plt.subplots(self.plotlevels, self.planes, figsize=(graphprefs[0], graphprefs[1]))
        else:
            fig, axs = plt.subplots(self.plotlevels, self.planes, figsize=(8, 9.5))

        fig.tight_layout(pad=self.graphs_space)
        fig.canvas.mpl_connect('button_press_event', on_click)
        plt.subplots_adjust(left=0.05,
                            bottom=0.05,
                            right=0.95,
                            top=0.95,
                            wspace=0.4,
                            hspace=0.4)

        fig.suptitle("Dynamic Range of Motion Graphs " + self.graph_type + " " + self.graph_name,  y=0.02, fontsize=8, color='gray')
# ''        for g in range(self.gno):
        for i in range(self.plotlevels):
            for j in range(self.planes):
                if self.plot_names[i][j] > '':
                    axs[i, j].set_title(self.plot_names[i][j], fontsize=8)
                    text = self.plot_axis_xyz[i][j].split("|")
                    if len(text) > 1:
                        axs[i, j].set_ylabel(text[1], labelpad=0.2, fontsize=6)
                    axs[i, j].tick_params(axis='x', labelsize=6)
                    axs[i, j].tick_params(axis='y', labelsize=6)
                    axs[i, j].set_ylim(self.plot_min[i][j], self.plot_max[i][j])
                    axs[i, j].set_title(self.plot_names[i][j], fontsize=9)
                    axs[i, j].add_patch(patches.Rectangle((0, min(self.ref_data[0][i][j])), self.gno +1, max(self.ref_data[0][i][j]) - min(self.ref_data[0][i][j]), alpha=0.20, color='gray'))
                    axs[i, j].text(self.gno * 0.25, self.plot_min[i][j] + 0.9 * (self.plot_max[i][j] - self.plot_min[i][j]), 'Normal ROM = ' + str(int(max(self.ref_data[0][i][j]) - min(self.ref_data[0][i][j]))) + ' (deg)', fontsize=6)

        for g in range(self.gno):
            x = g
            for i in range(self.plotlevels):
                for j in range(self.planes):
                    if self.plot_names[i][j] > '':
                        axs[i, j].set_title(self.plot_names[i][j], fontsize=8)
                        text = self.plot_axis_xyz[i][j].split("|")
                        if len(text) > 1:
                            axs[i, j].set_ylabel(text[1], labelpad=0.2, fontsize=6)
                        # axs[i, j].set_ylim(0, 80)
                        axs[i, j].set_xlim(0, self.gno + 1)
                        if self.division_lines[g][1] == 'Left':
                           axs[i, j].add_patch(patches.Rectangle((g + 1 - 0.4, self.rom[g][i][j][0]), 0.4, self.rom[g][i][j][2], alpha=0.20, color=self.line_colours[g][0]))
                           axs[i, j].text(g+1-0.40, self.rom[g][i][j][0] + (self.rom[g][i][j][2]/2), int(self.rom[g][i][j][2]), fontsize=6)
                        else:
                           axs[i, j].add_patch(patches.Rectangle((g + 1 - 0.4, self.rom[g][i][j][0]), 0.4, self.rom[g][i][j][2], alpha=0.20, color=self.line_colours[g][0]))
                           axs[i, j].text(g+1-0.40, self.rom[g][i][j][0] + (self.rom[g][i][j][2]/2), int(self.rom[g][i][j][2]), fontsize=6)
                        print(g, i, j)
                    else:
                        axs[i, j].set_visible(False)
                    # autolabel(axs[i, j], rects1, 'right')

        plt.savefig(self.graph_type + "_RomGraph.png")
        if self.all_graphs != 1:
            plt.show()
        else:
            plt.close
        return "Done"


    def plotavgrom(self):

        graphprefs = ff.getgraphprefs("Average Range Of Motion")
        if len(graphprefs) > 0:
            fig, axs = plt.subplots(self.plotlevels, self.planes, figsize=(graphprefs[0], graphprefs[1]))
        else:
            fig, axs = plt.subplots(self.plotlevels, self.planes, figsize=(8, 9.5))

        fig.tight_layout(pad=self.graphs_space)
        fig.canvas.mpl_connect('button_press_event', on_click)
        plt.subplots_adjust(left=0.05,
                            bottom=0.05,
                            right=0.95,
                            top=0.95,
                            wspace=0.4,
                            hspace=0.4)
        x = [ 0.5 , 1.5]
        labels = ["", "Left", "",  "Right"]
        degree_sign = u"\N{DEGREE SIGN}"

        fig.suptitle("Dynamic Range of Motion Graphs " + self.graph_type + " " + self.graph_name,  y=0.02, fontsize=8, color='gray')
        for i in range(self.plotlevels):
            for j in range(self.planes):
                if self.plot_names[i][j] > '':
                    axs[i, j].set_title(self.plot_names[i][j], fontsize=8)
                    text = self.plot_axis_xyz[i][j].split("|")
                    if len(text) > 1:
                        axs[i, j].set_ylabel(text[1], labelpad=0.2, fontsize=6)
                    axs[i, j].tick_params(axis='x', labelsize=6)
                    axs[i, j].tick_params(axis='y', labelsize=6)
                    axs[i, j].set_ylim(self.plot_min[i][j], self.plot_max[i][j])
                    axs[i, j].set_title(self.plot_names[i][j], fontsize=9)
                    axs[i, j].add_patch(patches.Rectangle((0, min(self.ref_data[0][i][j])), 3, max(self.ref_data[0][i][j]) - min(self.ref_data[0][i][j]), alpha=0.20, color='gray'))
                    axs[i, j].text(0.5, self.plot_min[i][j] + 0.9 * (self.plot_max[i][j] - self.plot_min[i][j]), 'Normal ROM = ' + str(int(max(self.ref_data[0][i][j]) - min(self.ref_data[0][i][j]))) + degree_sign, fontsize=6)
                    # axs[i, j].text(0.5, self.plot_min[i][j] + 0.9 * (self.plot_max[i][j] - self.plot_min[i][j]), 'Normal ROM = ' + str(int(max(self.ref_data[0][i][j]) - min(self.ref_data[0][i][j]))) + degree_sign, fontsize=6, ha='center', va='top')

        for i in range(self.plotlevels):
            for j in range(self.planes):
                if self.plot_names[i][j] > '':
                    axs[i, j].set_title(self.plot_names[i][j], fontsize=8)
                    text = self.plot_axis_xyz[i][j].split("|")
                    if len(text) > 1:
                        axs[i, j].set_ylabel(text[1], labelpad=0.2, fontsize=6)
                    # axs[i, j].set_ylim(0, 80)
                    axs[i, j].set_xlim(0, 2)
                    g = 0
                    axs[i, j].add_patch(patches.Rectangle((0.1, self.avgrom[i][j][0][0]-self.sdrom[i][j][1][2]), 0.8, self.sdrom[i][j][2][2], alpha=0.20, color='green'))
                    axs[i, j].add_patch(patches.Rectangle((0.1, self.avgrom[i][j][0][1]), 0.8, self.sdrom[i][j][1][2], alpha=0.20, color='green'))

                    axs[i, j].add_patch(patches.Rectangle((0.1, self.avgrom[i][j][0][0]), 0.8, self.avgrom[i][j][0][2], alpha=0.20, color='red'))
                    axs[i, j].text(0.2, self.avgrom[i][j][0][0] + (self.avgrom[i][j][0][2]/2), str(int(self.avgrom[i][j][0][2])) + degree_sign, fontsize=6)

                    nrom = int(max(self.ref_data[0][i][j]) - min(self.ref_data[0][i][j]))
                    if self.avgrom[i][j][0][2] == 0 or nrom ==0:
                        pcnt = 0
                        axs[i, j].text(0.6, 0, str(int(pcnt))+"%", fontsize=6)
                    else:
                        pcnt = (self.avgrom[i][j][0][2] / nrom) * 100
                        axs[i, j].text(0.6, self.avgrom[i][j][0][0] + (self.avgrom[i][j][0][2]/2), str(int(pcnt))+"%", fontsize=6)

                    g = 1
                    axs[i, j].add_patch(patches.Rectangle((1.1, self.avgrom[i][j][1][0]-self.sdrom[i][j][2][2]), 0.8, self.sdrom[i][j][2][2], alpha=0.20, color='green'))
                    axs[i, j].add_patch(patches.Rectangle((1.1, self.avgrom[i][j][1][1]), 0.8, self.sdrom[i][j][2][2], alpha=0.20, color='green'))

                    axs[i, j].add_patch(patches.Rectangle((1.1, self.avgrom[i][j][1][0]), 0.8, self.avgrom[i][j][1][2], alpha=0.20, color='blue'))
                    axs[i, j].text(1.2, self.avgrom[i][j][1][0] + (self.avgrom[i][j][1][2]/2), str(int(self.avgrom[i][j][1][2])) + degree_sign, fontsize=6)

                    nrom = int(max(self.ref_data[0][i][j]) - min(self.ref_data[0][i][j]))
                    if self.avgrom[i][j][1][2] == 0 or nrom ==0:
                        pcnt = 0
                        axs[i, j].text(0.6, 0, str(int(pcnt))+"%", fontsize=6)
                    else:
                        pcnt = (self.avgrom[i][j][1][2] / nrom) * 100
                        axs[i, j].text(1.6, self.avgrom[i][j][1][0] + (self.avgrom[i][j][1][2]/2), str(int(pcnt))+"%", fontsize=6)
                    # axs[i, j].get_xaxis().set_ticks([])
                    axs[i, j].set_xticklabels(labels)
                else:
                    axs[i, j].set_visible(False)


        plt.savefig(self.graph_type + "_AvgRomGraph.png")
        if self.all_graphs != 1:
            plt.show()
        else:
            plt.close
        return "Done"


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



def on_plot_hover(event):
    # Iterating over each data member plotted
    for curve in plt.get_lines():
        # Searching which data member corresponds to current mouse position
        if curve.contains(event)[0]:
            print ("over %s" % curve.get_gid())



