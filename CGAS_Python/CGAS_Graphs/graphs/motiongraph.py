from matplotlib import pyplot as plt
import filefunctions as ff


class GaitGraph:
    def __init__(self, graph_type, graph_name, all_graphs):
        self.graph_type = graph_type
        self.graph_name = graph_name
        self.all_graphs = all_graphs
        self.x_data = []
        self.y_data = []
        self.ref_data = []
        self.ref_lines = []
        self.refsd_data = []
        self.refsdminus_data = []
        self.refsdplus_data = []
        self.group_colours = []
        self.line_colours = []
        self.groupno = 0
        self.gno = 0
        self.graphs_space = 0.0
        self.samples = 0
        self.plane_names = []
        self.planes = 0
        self.plotlevels = 0
        self.graph_labels = []
        self.plot_labels = []
        self.plot_min = []
        self.plot_max = []
        self.division_lines = []




    def plotgraphs(self):

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

        global refno
        global global_graph_type
        refno = self.groupno
        fig, axs = plt.subplots(self.plotlevels, self.planes, figsize=(8, 9.5))
        fig.tight_layout(pad=self.graphs_space)


        plt.subplots_adjust(left=0.10,
                            bottom=0.05,
                            right=0.95,
                            top=0.95,
                            wspace=0.30,
                            hspace=0.30)

        fig.suptitle("Gait Graphs " + self.graph_type + " " + self.graph_name,  y=0.02, fontsize=8, color='gray')

        for g in range(self.groupno):
            for i in range(self.plotlevels):
                for j in range(self.planes):
                    if self.plotlevels > 1 and self.planes > 1:
                        ax = axs[i, j]
                    elif self.plotlevels > 1 and self.planes == 1:
                        ax = axs[i]
                    elif self.plotlevels == 1 and self.planes > 1:
                        ax = axs[j]

                    if self.plot_names[i][j] > '':

                        ax.set_title(self.plot_names[i][j], fontsize=8)
                        text = self.plot_axis_xyz[i][j].split("|")
                        if len(text) > 1:
                            ax.set_ylabel(text[1], labelpad=0.2, fontsize=6)
                        ax.tick_params(axis='x', labelsize=6)
                        ax.tick_params(axis='y', labelsize=6)
                        ax.plot(self.x_data[0][0], [0] * 101, c='black', linewidth=0.5)
                        ax.set_xlim(0, self.samples)
                        ax.set_ylim(self.plot_min[i][j], self.plot_max[i][j])
                        ax.linewidth = 0.50
                        try:
                            ax.fill_between(self.x_data[0][0], self.refsdminus_data[g][i][j], self.refsdplus_data[g][i][j], color=self.group_colours[g], alpha=0.2)

      # You may remove the hash symbol line below to show the average line between the +/-SD areas
                            if self.groupno > 1:
                                ax.plot(self.x_data[0][0], self.ref_data[g][i][j], color=self.group_colours[g], linewidth=1, alpha=0.80)

                            ax.axvline(x=self.ref_lines[g][0][0], color=self.group_colours[g], linewidth=2)
                            m = self.ref_lines[g][0][0] - self.ref_lines[g][1][0]
                            p = self.ref_lines[g][0][0] + self.ref_lines[g][1][0]
                            ax.axvline(x=m, color=self.group_colours[g], linewidth=0.4)
                            ax.axvline(x=p, color=self.group_colours[g], linewidth=0.4)
                        except:
                            print((g, i, j))
                    else:
                        ax.set_visible(False)


        for g in range(self.gno):
            for i in range(self.plotlevels):
                for j in range(self.planes):
                    if self.plotlevels > 1 and self.planes > 1:
                        ax = axs[i, j]
                    elif self.plotlevels > 1 and self.planes == 1:
                        ax = axs[i]
                    elif self.plotlevels == 1 and self.planes > 1:
                        ax = axs[j]
                    if self.plot_names[i][j] > '':
                        ax.set_title(self.plot_names[i][j], fontsize=8)
                        text = self.plot_axis_xyz[i][j].split("|")
                        if len(text) > 1:
                            ax.set_ylabel(text[1], labelpad=0.2, fontsize=6)
                        ax.tick_params(axis='x', labelsize=6)
                        ax.tick_params(axis='y', labelsize=6)
                    else:
                        ax.set_visible(False)
                    ax.set_xlim(0, self.samples)
                    if self.plot_min[i][j] == self.plot_max[i][j]:
                        ax.set_ylim(-10, 10)
                    else:
                        ax.set_ylim(self.plot_min[i][j], self.plot_max[i][j])
                    ax.linewidth = 0.50

                    if len(self.division_lines[g][0]) > 0:
                         ax.axvline(x=self.division_lines[g][0][0], c=self.line_colours[g][0], linewidth=0.5, picker=True)
                         try:
                             ax.plot(self.x_data[g][i], self.y_data[g][i][j], c=self.line_colours[g][0], linewidth=0.5,
                                     picker=True)
                         except IndexError:
                             print("Error: list index out of range. No graph for this level was plotted")
                         ax.xaxis.set_pickradius(5.)
                         ax.yaxis.set_pickradius(5.)
                    #print(g, i, j)

        global_graph_type = self.graph_type
        fig.canvas.mpl_connect('button_press_event', on_click)
        fig.canvas.mpl_connect('pick_event', on_pick)

        fig.canvas.manager.set_window_title(self.graph_type + "_Gait_Graphs")
        if self.groupno > 0  and self.gno == 0:
            plt.savefig(self.graph_type + "_Gait_Graphs_AVG" + ".png")
        else:
            plt.savefig(self.graph_type + "_Gait_Graphs" + ".png")
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
    if event.key != 'shift' and event.key != 'ctrl+shift' and event.button != 1:
        return

    if event.key == None:
        return

    if event.key == 'ctrl+shift':
        print(event.key)
        # hide all the other axes...
        for zoom_axis in event.canvas.figure.axes:
            i += 1
            zoomed_axes[0] = (zoom_axis, zoom_axis.get_position())
            zoom_axis.set_position([0.1, 0.1, 0.85, 0.85])
            for axis in event.canvas.figure.axes:
                if axis is not zoom_axis:
                    axis.set_visible(False)
            if zoom_axis.get_title() != '':
                plt.savefig("_" + global_graph_type + "_" +  "{:0>2}".format(i) + "_" + zoom_axis.get_title())
                print("save to:" + "_" + global_graph_type + "_" + "{:0>2}".format(i) + "_" + zoom_axis.get_title())
            zoom_axis.set_position(zoomed_axes[0][1])
            zoomed_axes[0] = None
            # make other axes visible again
            for axis in event.canvas.figure.axes:
                if axis.get_title( loc='center') > '':
                    axis.set_visible(True)
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
        print("save to:" + "_selected_" + ax.get_title())
        print(event.key)

    else:
        # restore the original state

        zoomed_axes[0][0].set_position(zoomed_axes[0][1])
        zoomed_axes[0] = None

        # make other axes visible again
        for axis in event.canvas.figure.axes:
            if axis.get_title( loc='center') > '':
                axis.set_visible(True)

    event.canvas.draw()

def on_pick(event):
    ax = event.artist.axes
    if (refno % 2) == 0:
        fixit = (int(refno / 2)) - 1
    else:
        fixit = (int(refno / 2))

    print_selected_line(int(ax.lines.index(event.artist) / 2)-((refno * 2) + fixit))

def print_selected_line(lineno):
    print("selected line: " + str(lineno))

