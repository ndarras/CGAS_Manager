from matplotlib import pyplot as plt
from matplotlib import patches as patches
import filefunctions as ff
from operator import sub
import numpy as np
import copy
import csv
import pickle
import os
import logging


class ADplotData:
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
        self.mgai_idx = []
        self.lmgdi_idx = []
        self.rmgdi_idx = []

        self.global_mgdi_idx = []
        self.global_mgai_idx = []
        self.global_lmgdi_idx = []
        self.global_rmgdi_idx = []

        self.triplane_mgdi_idx = []
        self.triplane_mgai_idx = []
        self.triplane_lmgdi_idx = []
        self.triplane_rmgdi_idx = []

        self.perplane_mgdi_idx = []
        self.perplane_mgai_idx = []
        self.perplane_lmgdi_idx = []
        self.perplane_rmgdi_idx = []

        self.plane_mgdi_idx = []
        self.plane_mgai_idx = []
        self.plane_lmgdi_idx = []
        self.plane_rmgdi_idx = []

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
        self.adplot = ff.getdata("sysdata", "adplot.p")

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

        self.calcdeviationdata()




    def mean(self, data):
        k = int(0)
        n = len(data)
        for i in range(n):
            if data[i] != 0:
                k += 1
        mean = sum(data) / k
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



    def calcdeviationdata(self):
        azero = np.zeros((self.gno, self.plotlevels, self.planes, 101))
        bzero = np.zeros((self.gno, self.plotlevels, self.planes, 3))
        czero = np.zeros((1, self.plotlevels, self.planes, 6))
        dzero = np.zeros((self.plotlevels, 2))
        ezero = np.zeros((self.planes, 2))
        fzero = np.zeros((2))
        self.dev_data = copy.deepcopy(azero)
        self.norm_dev_data = copy.deepcopy(azero)
        self.asy_data = copy.deepcopy(azero)
        self.norm_asy_data = copy.deepcopy(azero)
        self.dev_idx = copy.deepcopy(bzero)
        self.asy_idx = copy.deepcopy(bzero)
        self.mgdi_idx = copy.deepcopy(czero)
        self.lmgdi_idx = copy.deepcopy(czero)
        self.rmgdi_idx = copy.deepcopy(czero)
        self.mgai_idx = copy.deepcopy(czero)
        self.global_mgdi_idx = copy.deepcopy(fzero)
        self.global_mgai_idx = copy.deepcopy(fzero)
        self.global_lmgdi_idx = copy.deepcopy(fzero)
        self.global_rmgdi_idx = copy.deepcopy(fzero)
        self.triplane_mgdi_idx = copy.deepcopy(dzero)
        self.triplane_mgai_idx = copy.deepcopy(dzero)
        self.triplane_lmgdi_idx = copy.deepcopy(dzero)
        self.triplane_rmgdi_idx = copy.deepcopy(dzero)
        self.perplane_mgdi_idx = copy.deepcopy(ezero)
        self.perplane_mgai_idx = copy.deepcopy(ezero)
        self.perplane_lmgdi_idx = copy.deepcopy(ezero)
        self.perplane_rmgdi_idx = copy.deepcopy(ezero)


        global refno
        refno = self.groupno

        w = float(0)
        w = float(1) / float(len(self.x_data[0][0]))

        for g in range(len(self.lr_sets)):
            k = self.lr_sets[g][0]
            l = self.lr_sets[g][1]
            for i in range(self.plotlevels):
                for j in range(self.planes):

                    for n in range(len(self.x_data[g][i])):
                        # cal dif = normal mean - subject y val
                        self.dev_data[k][i][j][n] = (self.y_data[k][i][j][n] - self.ref_data[0][i][j][n])
                        self.dev_data[l][i][j][n] = (self.y_data[l][i][j][n] - self.ref_data[0][i][j][n])

                        # normalise dif to normal sds
                        if self.refsd_data[0][i][j][n] != 0 and self.dev_data[k][i][j][n] != 0:
                            self.norm_dev_data[k][i][j][n] = (self.dev_data[k][i][j][n] / self.refsd_data[0][i][j][n])
                        else:
                            self.norm_dev_data[k][i][j][n] = 0

                        if self.refsd_data[0][i][j][n] != 0 and self.dev_data[l][i][j][n] != 0:
                            self.norm_dev_data[l][i][j][n] = (self.dev_data[l][i][j][n] / self.refsd_data[0][i][j][n])
                        else:
                            self.norm_dev_data[l][i][j][n] = 0

                        # Apply weight (1/100 1/sapling) to normalised dif value
                        if self.norm_dev_data[k][i][j][n] <= 0:
                            self.dev_idx[k][i][j][1] = self.dev_idx[k][i][j][1] + (self.norm_dev_data[k][i][j][n] * w)
                        else:
                            self.dev_idx[k][i][j][2] = self.dev_idx[k][i][j][2] + (self.norm_dev_data[k][i][j][n] * w)

                        if self.norm_dev_data[l][i][j][n] <= 0:
                            self.dev_idx[l][i][j][1] = self.dev_idx[l][i][j][1] + (self.norm_dev_data[l][i][j][n] * w)
                        else:
                            self.dev_idx[l][i][j][2] = self.dev_idx[l][i][j][2] + (self.norm_dev_data[l][i][j][n] * w)

                    # Left and Right Deviations to calculate the LR value
                    self.dev_idx[k][i][j][0] = abs(self.dev_idx[k][i][j][1]) + abs(self.dev_idx[k][i][j][2])
                    self.dev_idx[l][i][j][0] = abs(self.dev_idx[l][i][j][1]) + abs(self.dev_idx[l][i][j][2])


        logging.info("Deviation Indexes Calculated")
        for g in range(len(self.lr_sets)):
            k = self.lr_sets[g][0]
            l = self.lr_sets[g][1]
            for i in range(self.plotlevels):
                for j in range(self.planes):
                    for n in range(len(self.x_data[g][i])):
                        self.asy_data[k][i][j][n] = (self.y_data[k][i][j][n] - self.y_data[l][i][j][n])
                        self.asy_data[l][i][j][n] = self.asy_data[k][i][j][n]
                        if self.refsd_data[0][i][j][n] != 0 or self.asy_data[k][i][j][n] != 0:
                            self.norm_asy_data[k][i][j][n] = (self.asy_data[k][i][j][n] / self.refsd_data[0][i][j][n])
                            self.norm_asy_data[l][i][j][n] = self.norm_asy_data[k][i][j][n]
                        else:
                            self.norm_asy_data[k][i][j][n] = 0
                            self.norm_asy_data[l][i][j][n] = 0
                        if self.norm_asy_data[k][i][j][n] <= 0:
                            self.asy_idx[k][i][j][1] = self.asy_idx[k][i][j][1] + (self.norm_asy_data[k][i][j][n] * w)
                            self.asy_idx[l][i][j][1] = self.asy_idx[k][i][j][1]
                        else:
                            self.asy_idx[k][i][j][2] = self.asy_idx[k][i][j][2] + (self.norm_asy_data[k][i][j][n] * w)
                            self.asy_idx[l][i][j][2] = self.asy_idx[k][i][j][2]

                    if self.adplot[i][j] == 'Scale=2':
                        self.asy_idx[k][i][j][0] = (abs(self.asy_idx[k][i][j][1]) + abs(self.asy_idx[k][i][j][2])) / 2
                        self.asy_idx[l][i][j][0] = (abs(self.asy_idx[l][i][j][1]) + abs(self.asy_idx[l][i][j][2])) / 2
                    else:
                        self.asy_idx[k][i][j][0] = (abs(self.asy_idx[k][i][j][1]) + abs(self.asy_idx[k][i][j][2]))
                        self.asy_idx[l][i][j][0] = (abs(self.asy_idx[l][i][j][1]) + abs(self.asy_idx[l][i][j][2]))


        logging.info( "Asymmetry Indexes Calculated")

        # Calculation of MGDI(sd), MGDI-(SD), MGDI+(SD) AND MGAI(sd), MGAI-(SD), MGAI+(SD) per graph
        for i in range(self.plotlevels):
            for j in range(self.planes):
                a = []
                b = []
                c = []
                d = []
                e = []
                la = []
                lb = []
                lc = []
                ra = []
                rb = []
                rc = []

                for g in range(len(self.lr_sets)):

                    k = self.lr_sets[g][0]
                    l = self.lr_sets[g][1]

                    a.append(self.dev_idx[k][i][j][0])
                    a.append(self.dev_idx[l][i][j][0])

                    b.append(self.dev_idx[k][i][j][1])
                    b.append(self.dev_idx[l][i][j][1])

                    c.append(self.dev_idx[k][i][j][2])
                    c.append(self.dev_idx[l][i][j][2])

                    la.append(self.dev_idx[k][i][j][0])
                    lb.append(self.dev_idx[k][i][j][1])
                    lc.append(self.dev_idx[k][i][j][2])


                    ra.append(self.dev_idx[l][i][j][0])
                    rb.append(self.dev_idx[l][i][j][1])
                    rc.append(self.dev_idx[l][i][j][2])

                #Calc MGDI and SD
                d = np.array(a)
                self.mgdi_idx[0][i][j][0] = self.mean(d)
                self.mgdi_idx[0][i][j][1] = self.stdev(d)
                # Calc MGDI(-) and SD
                d = np.array(b)
                self.mgdi_idx[0][i][j][2] = self.mean(d)
                self.mgdi_idx[0][i][j][3] = self.stdev(d)
                # Calc MGDI(+) and SD
                d = np.array(c)
                self.mgdi_idx[0][i][j][4] = self.mean(d)
                self.mgdi_idx[0][i][j][5] = self.stdev(d)
                # Calc LMGDI and SD
                d = np.array(la)
                self.lmgdi_idx[0][i][j][0] = self.mean(d)
                self.lmgdi_idx[0][i][j][1] = self.stdev(d)
                # Calc LMGDI(-) and SD
                d = np.array(lb)
                self.lmgdi_idx[0][i][j][2] = self.mean(d)
                self.lmgdi_idx[0][i][j][3] = self.stdev(d)
                # Calc LMGDI(+) and SD
                d = np.array(lc)
                self.lmgdi_idx[0][i][j][4] = self.mean(d)
                self.lmgdi_idx[0][i][j][5] = self.stdev(d)
                # Calc RMGDI and SD
                d = np.array(ra)
                self.rmgdi_idx[0][i][j][0] = self.mean(d)
                self.rmgdi_idx[0][i][j][1] = self.stdev(d)
                # Calc MGDI(-) and SD
                d = np.array(rb)
                self.rmgdi_idx[0][i][j][2] = self.mean(d)
                self.rmgdi_idx[0][i][j][3] = self.stdev(d)
                # Calc MGDI(+) and SD
                d = np.array(rc)
                self.rmgdi_idx[0][i][j][4] = self.mean(d)
                self.rmgdi_idx[0][i][j][5] = self.stdev(d)
                a = []
                b = []
                c = []
                d = []

                for g in range(len(self.lr_sets)):

                    k = self.lr_sets[g][0]
                    l = self.lr_sets[g][1]

                    a.append(self.asy_idx[k][i][j][0])
                    a.append(self.asy_idx[l][i][j][0])

                    b.append(self.asy_idx[k][i][j][1])
                    b.append(self.asy_idx[l][i][j][1])

                    c.append(self.asy_idx[k][i][j][2])
                    c.append(self.asy_idx[l][i][j][2])

                d = np.array(a)
                self.mgai_idx[0][i][j][0] = self.mean(d)
                self.mgai_idx[0][i][j][1] = self.stdev(d)
                d = np.array(b)
                self.mgai_idx[0][i][j][2] = self.mean(d)
                self.mgai_idx[0][i][j][3] = self.stdev(d)
                d = np.array(c)
                self.mgai_idx[0][i][j][4] = self.mean(d)
                self.mgai_idx[0][i][j][5] = self.stdev(d)


        # Global Calculations
        globd = []
        globa = []
        globl = []
        globr = []

        for i in range(self.plotlevels):
            for j in range(self.planes):

                for g in range(len(self.lr_sets)):
                    k = self.lr_sets[g][0]
                    l = self.lr_sets[g][1]

                    globd.append(self.dev_idx[k][i][j][0])
                    globd.append(self.dev_idx[l][i][j][0])
                    globl.append(self.dev_idx[k][i][j][0])
                    globr.append(self.dev_idx[l][i][j][0])

                for g in range(len(self.lr_sets)):
                    k = self.lr_sets[g][0]
                    l = self.lr_sets[g][1]

                    globa.append(self.asy_idx[k][i][j][0])
                    globa.append(self.asy_idx[l][i][j][0])

        d = []
        d = np.array(globd)
        self.global_mgdi_idx[0] = self.mean(d)
        self.global_mgdi_idx[1] = self.stdev(d)
        d = np.array(globa)
        self.global_mgai_idx[0] = self.mean(d)
        self.global_mgai_idx[1] = self.stdev(d)
        d = np.array(globl)
        self.global_lmgdi_idx[0] = self.mean(d)
        self.global_lmgdi_idx[1] = self.stdev(d)
        d = np.array(globr)
        self.global_rmgdi_idx[0] = self.mean(d)
        self.global_rmgdi_idx[1] = self.stdev(d)



        # Triplane Calculations
        for i in range(self.plotlevels):
            trid = []
            tria = []
            ltri = []
            rtri = []
            d = []
            for j in range(self.planes):

                for g in range(len(self.lr_sets)):
                    k = self.lr_sets[g][0]
                    l = self.lr_sets[g][1]

                    trid.append(self.dev_idx[k][i][j][0])
                    trid.append(self.dev_idx[l][i][j][0])
                    ltri.append(self.dev_idx[k][i][j][0])
                    rtri.append(self.dev_idx[l][i][j][0])

                for g in range(len(self.lr_sets)):
                    k = self.lr_sets[g][0]
                    l = self.lr_sets[g][1]

                    tria.append(self.asy_idx[k][i][j][0])
                    tria.append(self.asy_idx[l][i][j][0])

            d = np.array(trid)
            self.triplane_mgdi_idx[i][0] = self.mean(d)
            self.triplane_mgdi_idx[i][1] = self.stdev(d)
            d = np.array(tria)
            self.triplane_mgai_idx[i][0] = self.mean(d)
            self.triplane_mgai_idx[i][1] = self.stdev(d)
            d = np.array(ltri)
            self.triplane_lmgdi_idx[i][0] = self.mean(d)
            self.triplane_lmgdi_idx[i][1] = self.stdev(d)
            d = np.array(rtri)
            self.triplane_rmgdi_idx[i][0] = self.mean(d)
            self.triplane_rmgdi_idx[i][1] = self.stdev(d)


        # PerPlane Calculations
        for j in range(self.planes):
            perd = []
            pera = []
            lper = []
            rper = []
            d = []
            for i in range(self.plotlevels):

                for g in range(len(self.lr_sets)):

                    k = self.lr_sets[g][0]
                    l = self.lr_sets[g][1]

                    perd.append(self.dev_idx[k][i][j][0])
                    perd.append(self.dev_idx[l][i][j][0])
                    lper.append(self.dev_idx[k][i][j][0])
                    rper.append(self.dev_idx[l][i][j][0])

                for g in range(len(self.lr_sets)):

                    k = self.lr_sets[g][0]
                    l = self.lr_sets[g][1]

                    pera.append(self.asy_idx[k][i][j][0])
                    pera.append(self.asy_idx[l][i][j][0])

            d = np.array(perd)
            self.perplane_mgdi_idx[j][0] = self.mean(d)
            self.perplane_mgdi_idx[j][1] = self.stdev(d)
            d = np.array(pera)
            self.perplane_mgai_idx[j][0] = self.mean(d)
            self.perplane_mgai_idx[j][1] = self.stdev(d)
            d = np.array(lper)
            self.perplane_lmgdi_idx[j][0] = self.mean(d)
            self.perplane_lmgdi_idx[j][1] = self.stdev(d)
            d = np.array(rper)
            self.perplane_rmgdi_idx[j][0] = self.mean(d)
            self.perplane_rmgdi_idx[j][1] = self.stdev(d)



        with open(self.graph_type + '_MGDI_MGDI.csv', 'w', newline ='') as f:

            # using csv.writer method from CSV package
            write = csv.writer(f)
            for i in range(self.plotlevels):
                for j in range(self.planes):
                    out_txt = []
                    out_txt.append('Left Deviation Indexes')
                    out_txt.append( self.plot_names[i][j])
                    out_txt.append(str(self.lmgdi_idx[0][i][j][0]))
                    out_txt.append(str(self.lmgdi_idx[0][i][j][1]))
                    out_txt.append(str(self.lmgdi_idx[0][i][j][2]))
                    out_txt.append(str(self.lmgdi_idx[0][i][j][3]))
                    out_txt.append(str(self.lmgdi_idx[0][i][j][4]))
                    out_txt.append(str(self.lmgdi_idx[0][i][j][5]))
                    write.writerow(out_txt)


            for i in range(self.plotlevels):
                for j in range(self.planes):
                    out_txt = []
                    out_txt.append('Right Deviation Indexes')
                    out_txt.append( self.plot_names[i][j])
                    out_txt.append(str(self.rmgdi_idx[0][i][j][0]))
                    out_txt.append(str(self.rmgdi_idx[0][i][j][1]))
                    out_txt.append(str(self.rmgdi_idx[0][i][j][2]))
                    out_txt.append(str(self.rmgdi_idx[0][i][j][3]))
                    out_txt.append(str(self.rmgdi_idx[0][i][j][4]))
                    out_txt.append(str(self.rmgdi_idx[0][i][j][5]))
                    write.writerow(out_txt)

            for i in range(self.plotlevels):
                for j in range(self.planes):
                    out_txt = []
                    out_txt.append('Motion Graph Deviation Indexes')
                    out_txt.append( self.plot_names[i][j])
                    out_txt.append(str(self.mgdi_idx[0][i][j][0]))
                    out_txt.append(str(self.mgdi_idx[0][i][j][1]))
                    out_txt.append(str(self.mgdi_idx[0][i][j][2]))
                    out_txt.append(str(self.mgdi_idx[0][i][j][3]))
                    out_txt.append(str(self.mgdi_idx[0][i][j][4]))
                    out_txt.append(str(self.mgdi_idx[0][i][j][5]))
                    write.writerow(out_txt)

            for i in range(self.plotlevels):
                for j in range(self.planes):
                    out_txt = []
                    out_txt.append('Motion Graph Asymmetry Indexes')
                    out_txt.append( self.plot_names[i][j])
                    out_txt.append(str(self.mgai_idx[0][i][j][0]))
                    out_txt.append(str(self.mgai_idx[0][i][j][1]))
                    out_txt.append(str(self.mgai_idx[0][i][j][2]))
                    out_txt.append(str(self.mgai_idx[0][i][j][3]))
                    out_txt.append(str(self.mgai_idx[0][i][j][4]))
                    out_txt.append(str(self.mgai_idx[0][i][j][5]))
                    write.writerow(out_txt)

        outfile = open('sysdata//Reference_' + self.graph_type + '_MGDI_MGAI_AllGraphs.p', 'wb')
        pickle.dump(self.lmgdi_idx, outfile)
        pickle.dump(self.rmgdi_idx, outfile)
        pickle.dump(self.mgdi_idx, outfile)
        pickle.dump(self.mgai_idx, outfile)
        outfile.close()
        logging.info("Reference AD Plot Vals stored")

        outfile = open('sysdata//Reference_' + self.graph_type + '_MGDI_MGAI_Global.p', 'wb')
        pickle.dump(self.global_lmgdi_idx, outfile)
        pickle.dump(self.global_rmgdi_idx, outfile)
        pickle.dump(self.global_mgdi_idx, outfile)
        pickle.dump(self.global_mgai_idx, outfile)
        outfile.close()
        logging.info("Reference AD Plot Vals stored")


        outfile = open('sysdata//Reference_' + self.graph_type + '_MGDI_MGAI_Triplane.p', 'wb')
        pickle.dump(self.triplane_rmgdi_idx, outfile)
        pickle.dump(self.triplane_lmgdi_idx, outfile)
        pickle.dump(self.triplane_mgdi_idx, outfile)
        pickle.dump(self.triplane_mgai_idx, outfile)
        outfile.close()
        logging.info("Reference AD Plot Triplane Vals stored")

        outfile = open('sysdata//Reference_' + self.graph_type + '_MGDI_MGAI_Perplane.p', 'wb')
        pickle.dump(self.perplane_rmgdi_idx, outfile)
        pickle.dump(self.perplane_lmgdi_idx, outfile)
        pickle.dump(self.perplane_mgdi_idx, outfile)
        pickle.dump(self.perplane_mgai_idx, outfile)
        outfile.close()
        logging.info("Reference AD Plot Perplane Vals stored")

    def plotzscoredeviationgraphs(self):

        graphprefs = ff.getgraphprefs("Z Score Deviation Graphs")
        if len(graphprefs) > 0:
            fig, axs = plt.subplots(self.plotlevels, self.planes, figsize=(graphprefs[0], graphprefs[1]))
        else:
            fig, axs = plt.subplots(self.plotlevels, self.planes, figsize=(8, 9.5))

        fig.tight_layout(pad=self.graphs_space)

        fig.canvas.mpl_connect('button_press_event', on_click)
        #fig.canvas.mpl_connect('motion_notify_event', on_plot_hover)

        plt.subplots_adjust(left=0.05,
                            bottom=0.05,
                            right=0.95,
                            top=0.95,
                            wspace=0.4,
                            hspace=0.4)

        fig.suptitle("Deviation Graphs",  y=0.99)
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
                        ax.set_ylim(-7, 7)
                        ax.linewidth = 0.50
                        t = "   L MGDI: " + str(round(self.lmgdi_idx[0][i][j][0], 1)) + " NSDs ±(" + str(
                            round(self.lmgdi_idx[0][i][j][1], 2)) + ")"
                        axs[i, j].text(0.5, 0.9,  t, fontdict=None,  color='red', fontsize=7, zorder=40, alpha=0.50, horizontalalignment='center', verticalalignment='center', transform = ax.transAxes)
                        t = "   R MGDI: " + str(round(self.rmgdi_idx[0][i][j][0], 2)) + " NSDs ±(" + str(
                            round(self.lmgdi_idx[0][i][j][1], 2)) + ")"
                        axs[i, j].text(0.5, 0.8,  t, fontdict=None,   color='blue', fontsize=7, zorder=40, alpha=0.50, horizontalalignment='center', verticalalignment='center', transform = ax.transAxes)

                        a = list()
                        b = list()
                        c = list()
                        d = list()
                        e = list()

                        a = self.x_data[0][0]
                        b = self.refsd_data[0][i][j]
                        c = np.repeat(1,101)
                        d = np.zeros(101)
                        e = d-c
                        ax.fill_between(a, 3 * e, 3 * c, color='pink', alpha=1)
                        ax.fill_between(a, 2 * e, 2 * c, color='peachpuff', alpha=1)
                        ax.fill_between(a, e, c, color='silver', alpha=1)

                        ax.plot(a, d, color=self.group_colours[g], linewidth=1, alpha=0.80)
                        ax.axvline(x=self.ref_lines[g][0], color=self.group_colours[g], linewidth=2)
                        m = self.ref_lines[g][0][0] - self.ref_lines[g][1][0]
                        p = self.ref_lines[g][0][0] + self.ref_lines[g][1][0]
                        ax.axvline(x=m, color=self.group_colours[g], linewidth=0.4)
                        ax.axvline(x=p, color=self.group_colours[g], linewidth=0.4)

                    else:
                        ax.set_visible(False)

        for k in range(len(self.lr_sets)):
            for l in range(2):
                g = self.lr_sets[k][l]
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
                        ax.set_ylim(-7, 7)
                        ax.linewidth = 0.50
                        if self.plot_names[i][j] > '':
                            a = list()
                            b = list()
                            c = list()
                            d = list()
                            for n in range(len(self.x_data[g][i])):
                                a.append(self.x_data[g][i][n])
                            for n in range(len(self.y_data[g][i][j])):
                                b.append(float(self.y_data[g][i][j][n]))
                            for n in range(len(self.ref_data[0][i][j])):
                                c.append(self.ref_data[0][i][j][n])
                            d = list(map(sub, b, c))
                            if self.division_lines[g][1] == 'Left':
                                if len(self.division_lines[g][0]) > 0:
                                    ax.axvline(x=self.division_lines[g][0][0], c=self.line_colours[g][0], linewidth=0.5)
                                    ax.plot(a, self.dev_data[g][i][j] / self.refsd_data[0][i][j], c=self.line_colours[g][0], linewidth=0.5)
                            else:
                                if len(self.division_lines[g][0]) > 0:
                                    ax.axvline(x=self.division_lines[g][0][0], c=self.line_colours[g][0], linewidth=0.5)
                                    ax.plot(a, self.dev_data[g][i][j] / self.refsd_data[0][i][j], c=self.line_colours[g][0], linewidth=0.5)
                            logging.info(str(g) + "," + str(i) + "," + str(j))

        fig.canvas.mpl_connect('button_press_event', on_click)
        fig.canvas.mpl_connect('pick_event', on_pick)

        fig.canvas.manager.set_window_title("Gait Graphs " + self.graph_type)
        plt.savefig(self.graph_type + "_Deviation_nsd_Graph.png")

        if self.all_graphs != 1:
            plt.show()
        else:
            plt.close
        return "Done"



    def plotdeviationgraphs(self):

        graphprefs = ff.getgraphprefs("Deviation Graphs")
        if len(graphprefs) > 0:
            fig, axs = plt.subplots(self.plotlevels, self.planes, figsize=(graphprefs[0], graphprefs[1]))
        else:
            fig, axs = plt.subplots(self.plotlevels, self.planes, figsize=(8, 9.5))

        fig.tight_layout(pad=self.graphs_space)

        fig.canvas.mpl_connect('button_press_event', on_click)
        #fig.canvas.mpl_connect('motion_notify_event', on_plot_hover)

        plt.subplots_adjust(left=0.05,
                            bottom=0.05,
                            right=0.95,
                            top=0.95,
                            wspace=0.4,
                            hspace=0.4)

        fig.suptitle("Deviation Graphs",  y=0.99)
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
                        t = "   L MGDI: " + str(round(self.lmgdi_idx[0][i][j][0], 1)) + " NSDs ±(" + str(
                            round(self.lmgdi_idx[0][i][j][1], 2)) + ")"
                        axs[i, j].text(0.5, 0.9,  t, fontdict=None,  color='red', fontsize=7, zorder=40, alpha=0.50, horizontalalignment='center', verticalalignment='center', transform = ax.transAxes)
                        t = "   R MGDI: " + str(round(self.rmgdi_idx[0][i][j][0], 2)) + " NSDs ±(" + str(
                            round(self.lmgdi_idx[0][i][j][1], 2)) + ")"
                        axs[i, j].text(0.5, 0.8,  t, fontdict=None,   color='blue', fontsize=7, zorder=40, alpha=0.50, horizontalalignment='center', verticalalignment='center', transform = ax.transAxes)

                        a = list()
                        b = list()
                        c = list()
                        d = list()
                        e = list()

                        a = self.x_data[0][0]
                        b = self.refsd_data[0][i][j]
                        c = self.refsd_data[0][i][j]
                        d = np.zeros(101)
                        e = d-c
                        ax.fill_between(a, e, b, color=self.group_colours[g], alpha=0.2)
                        ax.plot(a, d, color=self.group_colours[g], linewidth=1, alpha=0.80)
                        ax.axvline(x=self.ref_lines[g][0], color=self.group_colours[g], linewidth=2)
                        m = self.ref_lines[g][0][0] - self.ref_lines[g][1][0]
                        p = self.ref_lines[g][0][0] + self.ref_lines[g][1][0]
                        ax.axvline(x=m, color=self.group_colours[g], linewidth=0.4)
                        ax.axvline(x=p, color=self.group_colours[g], linewidth=0.4)

                    else:
                        ax.set_visible(False)

        for k in range(len(self.lr_sets)):
            for l in range(2):
                g = self.lr_sets[k][l]
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
                        ax.set_ylim(self.plot_min[i][j], self.plot_max[i][j])
                        ax.linewidth = 0.50
                        if self.plot_names[i][j] > '':
                            a = list()
                            b = list()
                            c = list()
                            d = list()
                            for n in range(len(self.x_data[g][i])):
                                a.append(self.x_data[g][i][n])
                            for n in range(len(self.y_data[g][i][j])):
                                b.append(float(self.y_data[g][i][j][n]))
                            for n in range(len(self.ref_data[0][i][j])):
                                c.append(self.ref_data[0][i][j][n])
                            d = list(map(sub, b, c))
                            if self.division_lines[g][1] == 'Left':
                                if len(self.division_lines[g][0]) > 0:
                                    ax.axvline(x=self.division_lines[g][0][0], c=self.line_colours[g][0], linewidth=0.5)
                                    ax.plot(a, self.dev_data[g][i][j], c=self.line_colours[g][0], linewidth=0.5)
                            else:
                                if len(self.division_lines[g][0]) > 0:
                                    ax.axvline(x=self.division_lines[g][0][0], c=self.line_colours[g][0], linewidth=0.5)
                                    ax.plot(a, self.dev_data[g][i][j], c=self.line_colours[g][0], linewidth=0.5)
                            logging.info(str(g) + "," + str(i) + "," + str(j))

        fig.canvas.mpl_connect('button_press_event', on_click)
        fig.canvas.mpl_connect('pick_event', on_pick)

        fig.canvas.manager.set_window_title("Gait Graphs " + self.graph_type)
        plt.savefig(self.graph_type + "_DeviationGraph.png")

        if self.all_graphs != 1:
            plt.show()
        else:
            plt.close
        return "Done"


    def plotzscoreasymmetrygraphs(self):

        self.group_colours = ff.getdata("sysdata", "groupColours.p")
        self.line_colours = ff.getdata("sysdata", "lineColours.p")
        self.groupno = ff.getdata("sysdata", "groupno.p")
        self.gno = ff.getdata("sysdata", "gno.p")

        self.graphs_space = ff.getdata("sysdata", "graphs_space.p")
        self.samples = ff.getdata("sysdata", "samples.p")
        self.planes =ff.getdata("sysdata", "planes.p")
        self.plane_names = ff.getdata("sysdata", "plane_names.p")
        self.plotlevels = ff.getdata("sysdata", "plotlevels.p")

        self.graph_labels = ff.getdata("sysdata", "graph_labels.p")
        self.plot_labels = ff.getdata("sysdata", "plot_labels.p")
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

        self.calcdeviationdata()

        graphprefs = ff.getgraphprefs("Z Score Asymmetry Graphs")
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

        fig.suptitle("Asymmetry Graphs " + self.graph_type + " " + self.graph_name,  y=0.02, fontsize=8, color='gray')
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
                        # ax.grid(axis="y")
                        ax.set_title(self.plot_names[i][j], fontsize=8)
                        ax.tick_params(axis='x', labelsize=6)
                        ax.tick_params(axis='y', labelsize=6)
                        ax.plot(self.x_data[0][0], [0] * 101, c='black', linewidth=0.5)
                        ax.set_xlim(0, self.samples)
                        ax.set_ylim(-7, 7)
                        ax.linewidth = 0.50
                        t = "   MGAI: " + str(round(self.mgai_idx[0][i][j][0], 2)) + " NSDs ±(" + str(round(self.mgai_idx[0][i][j][1], 2)) + ")"
                        axs[i, j].text(0.5, 0.9,  t, fontdict=None,  color='green', fontsize=7, zorder=40, alpha=0.50, horizontalalignment='center', verticalalignment='center', transform = ax.transAxes)
                        a = list()
                        b = list()
                        c = list()
                        d = list()
                        e = list()

                        a = self.x_data[0][0]
                        b = self.refsd_data[0][i][j]
                        c = np.repeat(1,101)
                        d = np.zeros(101)
                        e = d-c
                        ax.fill_between(a, 3 * e, 3 * c, color='pink', alpha=1)
                        ax.fill_between(a, 2 * e, 2 * c, color='peachpuff', alpha=1)
                        ax.fill_between(a, e, c, color='silver', alpha=1)

                        ax.plot(a, d, color=self.group_colours[g], linewidth=1, alpha=0.80)
                        ax.axvline(x=self.ref_lines[g][0], color=self.group_colours[g], linewidth=2)
                        m = self.ref_lines[g][0][0] - self.ref_lines[g][1][0]
                        p = self.ref_lines[g][0][0] + self.ref_lines[g][1][0]
                        ax.axvline(x=m, color=self.group_colours[g], linewidth=0.4)
                        ax.axvline(x=p, color=self.group_colours[g], linewidth=0.4)

                    else:
                        ax.set_visible(False)


        for k in range(len(self.lr_sets)):
            for l in range(2):
                g = self.lr_sets[k][l]
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
                        ax.set_ylim(-7, 7)
                        ax.linewidth = 0.50
                        if self.plot_names[i][j] > '':
                            a = list()
                            b = list()
                            c = list()
                            d = list()
                            for n in range(len(self.x_data[g][i])):
                                a.append(self.x_data[g][i][n])
                            for n in range(len(self.y_data[g][i][j])):
                                b.append(float(self.y_data[g][i][j][n]))
                            for n in range(len(self.ref_data[0][i][j])):
                                c.append(self.ref_data[0][i][j][n])
                            d = list(map(sub, b, c))
                            ax.axvline(x=self.division_lines[g][0][0], c=self.line_colours[g][0], linewidth=0.5)
                            ax.plot(a, self.asy_data[g][i][j] / self.refsd_data[0][i][j], c='green', linewidth=0.5)
                            logging.info(str(g) + "," + str(i) + "," + str(j))

        plt.savefig(self.graph_type + "_ZScore_AsymmetryGraph.png")

        if self.all_graphs != 1:
            plt.show()
        else:
            plt.close
        return "Done"


    def plotasymmetrygraphs(self):

        self.group_colours = ff.getdata("sysdata", "groupColours.p")
        self.line_colours = ff.getdata("sysdata", "lineColours.p")
        self.groupno = ff.getdata("sysdata", "groupno.p")
        self.gno = ff.getdata("sysdata", "gno.p")

        self.graphs_space = ff.getdata("sysdata", "graphs_space.p")
        self.samples = ff.getdata("sysdata", "samples.p")
        self.planes =ff.getdata("sysdata", "planes.p")
        self.plane_names = ff.getdata("sysdata", "plane_names.p")
        self.plotlevels = ff.getdata("sysdata", "plotlevels.p")

        self.graph_labels = ff.getdata("sysdata", "graph_labels.p")
        self.plot_labels = ff.getdata("sysdata", "plot_labels.p")
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

        self.calcdeviationdata()

        graphprefs = ff.getgraphprefs("Asymmetry Graphs")
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

        fig.suptitle("Asymmetry Graphs " + self.graph_type + " " + self.graph_name,  y=0.02, fontsize=8, color='gray')
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
                        # ax.grid(axis="y")
                        ax.set_title(self.plot_names[i][j], fontsize=8)
                        ax.tick_params(axis='x', labelsize=6)
                        ax.tick_params(axis='y', labelsize=6)
                        ax.plot(self.x_data[0][0], [0] * 101, c='black', linewidth=0.5)
                        ax.set_xlim(0, self.samples)
                        ax.set_ylim(self.plot_min[i][j], self.plot_max[i][j])
                        ax.linewidth = 0.50
                        t = "   MGAI: " + str(round(self.mgai_idx[0][i][j][0], 2)) + " NSDs ±(" + str(round(self.mgai_idx[0][i][j][1], 2)) + ")"
                        axs[i, j].text(0.5, 0.9,  t, fontdict=None,  color='green', fontsize=7, zorder=40, alpha=0.50, horizontalalignment='center', verticalalignment='center', transform = ax.transAxes)
                        a = list()
                        b = list()
                        c = list()
                        d = list()
                        e = list()

                        a = self.x_data[0][0]
                        b = self.refsd_data[0][i][j]
                        c = self.refsd_data[0][i][j]
                        d = np.zeros(101)
                        e = d-c
                        ax.fill_between(a, e, b, color=self.group_colours[g], alpha=0.2)
                        ax.plot(a, d, color=self.group_colours[g], linewidth=1, alpha=0.80)
                        ax.axvline(x=self.ref_lines[g][0], color=self.group_colours[g], linewidth=2)
                        m = self.ref_lines[g][0][0] - self.ref_lines[g][1][0]
                        p = self.ref_lines[g][0][0] + self.ref_lines[g][1][0]
                        ax.axvline(x=m, color=self.group_colours[g], linewidth=0.4)
                        ax.axvline(x=p, color=self.group_colours[g], linewidth=0.4)

                    else:
                        ax.set_visible(False)


        for k in range(len(self.lr_sets)):
            for l in range(2):
                g = self.lr_sets[k][l]
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
                        ax.set_ylim(self.plot_min[i][j], self.plot_max[i][j])
                        ax.linewidth = 0.50
                        if self.plot_names[i][j] > '':
                            a = list()
                            b = list()
                            c = list()
                            d = list()
                            for n in range(len(self.x_data[g][i])):
                                a.append(self.x_data[g][i][n])
                            for n in range(len(self.y_data[g][i][j])):
                                b.append(float(self.y_data[g][i][j][n]))
                            for n in range(len(self.ref_data[0][i][j])):
                                c.append(self.ref_data[0][i][j][n])
                            d = list(map(sub, b, c))
                            ax.axvline(x=self.division_lines[g][0][0], c=self.line_colours[g][0], linewidth=0.5)
                            ax.plot(a, self.asy_data[g][i][j], c='green', linewidth=0.5)
                            logging.info(str(g) + "," + str(i) + "," + str(j))

        plt.savefig(self.graph_type + "_AsymmetryGraph.png")

        if self.all_graphs != 1:
            plt.show()
        else:
            plt.close
        return "Done"



    def plotgraphsplusindexes(self):

        graphprefs = ff.getgraphprefs("Motion Graphs plus Indexes")
        if len(graphprefs) > 0:
            fig, axs = plt.subplots(self.plotlevels, self.planes, figsize=(graphprefs[0], graphprefs[1]))
        else:
            fig, axs = plt.subplots(self.plotlevels, self.planes, figsize=(8, 9.5))

        fig.tight_layout(pad=self.graphs_space)

        fig.canvas.mpl_connect('button_press_event', on_click)
        #fig.canvas.mpl_connect('motion_notify_event', on_plot_hover)

        plt.subplots_adjust(left=0.05,
                            bottom=0.05,
                            right=0.95,
                            top=0.95,
                            wspace=0.4,
                            hspace=0.4)

        fig.suptitle("Motion Graphs plus Indexes " + self.graph_type + " " + self.graph_name,  y=0.02, fontsize=8, color='gray')
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
                        t = "   L MGDI: " + str(round(self.lmgdi_idx[0][i][j][0], 2)) + " NSDs ±(" + str(
                            round(self.lmgdi_idx[0][i][j][1], 1)) + ")"
                        axs[i, j].text(0.5, 0.9,  t, fontdict=None,  color='red', fontsize=7, zorder=40, alpha=0.50, horizontalalignment='center', verticalalignment='center', transform = ax.transAxes)
                        t = "   R MGDI: " + str(round(self.rmgdi_idx[0][i][j][0], 2)) + " NSDs ±(" + str(
                            round(self.lmgdi_idx[0][i][j][1], 2)) + ")"
                        axs[i, j].text(0.5, 0.8,  t, fontdict=None,   color='blue', fontsize=7, zorder=40, alpha=0.50, horizontalalignment='center', verticalalignment='center', transform = ax.transAxes)

                        t = "   MGAI: " + str(round(self.mgai_idx[0][i][j][0], 2)) + " NSDs ±(" + str(round(self.mgai_idx[0][i][j][1], 2)) + ")"
                        axs[i, j].text(0.5, 0.1,  t, fontdict=None,  color='green', fontsize=7, zorder=40, alpha=0.50, horizontalalignment='center', verticalalignment='center', transform = ax.transAxes)


                        try:
                            ax.fill_between(self.x_data[0][0], self.refsdminus_data[g][i][j], self.refsdplus_data[g][i][j], color=self.group_colours[g], alpha=0.2)
                            ax.plot(self.x_data[0][0], self.ref_data[g][i][j], color=self.group_colours[g], linewidth=1, alpha=0.80)
                            ax.axvline(x=self.ref_lines[g][0][0], color=self.group_colours[g], linewidth=2)
                            m = self.ref_lines[g][0][0] - self.ref_lines[g][1][0]
                            p = self.ref_lines[g][0][0] + self.ref_lines[g][1][0]
                            ax.axvline(x=m, color=self.group_colours[g], linewidth=0.4)
                            ax.axvline(x=p, color=self.group_colours[g], linewidth=0.4)
                        except:
                            logging.info(str(g) + "," + str(i) + "," + str(j))


                    else:
                        ax.set_visible(False)


        if self.gno > 0:
            for k in range(len(self.lr_sets)):
                for l in range(2):
                    g = self.lr_sets[k][l]
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
                            ax.set_ylim(self.plot_min[i][j], self.plot_max[i][j])
                            ax.linewidth = 0.50

                            if len(self.division_lines[g][0]) > 0:
                                 ax.axvline(x=self.division_lines[g][0][0], c=self.line_colours[g][0], linewidth=0.5)
                                 try:
                                    ax.plot(self.x_data[g][i], self.y_data[g][i][j], c=self.line_colours[g][0], linewidth=0.5)
                                 except IndexError:
                                    print("Error: list index out of range. No graph for this level was plotted")
                            logging.info(str(g) + "," + str(i) + "," + str(j))

        plt.savefig(self.graph_type + "_GraphsPlusIndexes.png")

        if self.all_graphs != 1:
            plt.show()
        else:
            plt.close
        return "Done"



    def adplot_global_graph(self):

        ref_info = ""
        ref_path = ff.getfileparams("compare.ini", 0)
        ref_name = ff.getfileparams("compare.ini", 1)
        ref_comp_caption = ff.getfileparams("compare.ini", 2)
        ref_filename = ""
        if ref_name != '':
            for file in os.listdir(ref_path):
                if file.startswith("Reference_Kinematics_MGDI_MGAI_Global"):
                    ref_filename = file

            if ref_filename != "":
                ref_info = ref_filename.split("_")
                if os.path.isfile(ref_path + ref_filename):
                    infile = open(ref_path + ref_filename, 'rb')
                    ref_lmgdi_idx = pickle.load(infile)
                    ref_rmgdi_idx = pickle.load(infile)
                    ref_mgdi_idx = pickle.load(infile)
                    ref_mgai_idx = pickle.load(infile)
                    infile.close()

        graphprefs = ff.getgraphprefs("ADPlot Global Graph")

        GraphLabel = ["Global Indexes"]

        if len(graphprefs) > 0:
            fig, axs = plt.subplots(1, figsize=(graphprefs[0], graphprefs[1]), facecolor = 'yellow')
        else:
            fig, axs = plt(figsize=(3, 9.5))

        fig.tight_layout(pad=self.graphs_space)

        fig.canvas.mpl_connect('button_press_event', on_click)

        plt.subplots_adjust(left=0.16,
                            bottom=0.15,
                            right=0.95,
                            top=0.95,
                            wspace=0.4,
                            hspace=0.4)

        if ref_name == "":
            fig.suptitle("AD plot Global Graph " + self.graph_type + " " + self.graph_name, y=0.05, fontsize=8,
                         color='gray')
        else:
            fig.suptitle("AD plot Global Graph " + self.graph_type + " " + self.graph_name + "_vs_" + ref_comp_caption, y=0.02, fontsize=8,
                         color='gray')

        for i in range(1):
                axs.tick_params(axis='x', labelsize=6)
                axs.tick_params(axis='y', labelsize=6)
                axs.plot(self.x_data[0][0], [0] * 101, color='black', linewidth=0.5)
                axs.set_xlim(0, 7)
                axs.set_ylim(0, 7)
                axs.set_ylabel('Deviation (SD)', fontsize=6)
                axs.set_xlabel('Asymmetry (SD)', fontsize=6)
                axs.linewidth = 0.50
                axs.spines['right'].set_visible(False)
                axs.spines['left'].set_visible(False)
                axs.spines['top'].set_visible(False)
                axs.spines['bottom'].set_visible(False)
                axs.tick_params(axis='x', colors='gray')
                axs.tick_params(axis='y', colors='gray')
                axs.add_patch(patches.Rectangle((0, 0), 1, 1, edgecolor='lightgreen', facecolor='lightgreen', fill=True, alpha=0.30, zorder=5))
                axs.add_patch(patches.Rectangle((1, 0), 7, 1, edgecolor='lightgray', facecolor='lightgray', fill=True, alpha=0.30, zorder=10))
                axs.plot([0, 7], [0, 7], color='lightgray', linewidth=0.5)
                t = "   L MGDI: " + str(round(self.global_lmgdi_idx[0], 2)) + " NSDs ±(" + str(round(self.global_lmgdi_idx[1], 2)) + ")"
                axs.text(1.2, 6.3, t, fontdict=None, color='red', fontsize=7, zorder=40, alpha=0.50)
                t = "   R MGDI: " + str(round(self.global_rmgdi_idx[0], 2)) + " NSDs ±(" + str(round(self.global_rmgdi_idx[1], 2)) + ")"
                axs.text(1.2, 5.7, t, fontdict=None, color='blue', fontsize=7, zorder=40, alpha=0.50)
                t = "Mean MGDI: " + str(round(self.global_mgdi_idx[0], 2)) + " NSDs ±(" + str(round(self.global_mgdi_idx[1], 2)) + ")"
                axs.text(1.2, 5.0, t, fontdict=None, color='gray', fontsize=7, zorder=40, alpha=0.30)
                t = "Mean MGAI: " + str(round(self.global_mgai_idx[0], 2)) + " NSDs ±(" + str(round(self.global_mgai_idx[1], 2)) + ")"
                axs.text(1.2, 0.3, t, fontdict=None, color='green', fontsize=7, zorder=40, alpha=0.30)
                axs.add_patch(patches.Rectangle((self.global_mgai_idx[0] - self.global_mgai_idx[1], self.global_lmgdi_idx[0] - self.global_lmgdi_idx[1]), 2 * self.global_mgai_idx[1], 2 * self.global_lmgdi_idx[1], color='red', zorder=0, alpha=0.10))
                axs.add_patch(patches.Rectangle((self.global_mgai_idx[0] - self.global_mgai_idx[1], self.global_rmgdi_idx[0] - self.global_rmgdi_idx[1]), 2 * self.global_mgai_idx[1], 2 * self.global_rmgdi_idx[1], color='blue', zorder=0, alpha=0.10))

                axs.scatter(self.global_mgai_idx[0], self.global_mgdi_idx[0], color='black',
                               marker='*', alpha=0.50, zorder=30)

                a = list()
                b = list()
                c = list()
                d = list()


        if ref_info != "":
            # axs[i, j].add_patch(patches.Rectangle((ref_mgai_idx[0][i][j][0] - ref_mgai_idx[0][i][j][1], ref_lmgdi_idx[0][i][j][0] - ref_lmgdi_idx[0][i][j][1]), 2 * ref_mgai_idx[0][i][j][1], 2 * ref_lmgdi_idx[0][i][j][1], color='magenta', zorder=0, alpha=0.10))
            # axs[i, j].add_patch(patches.Rectangle((ref_mgai_idx[0][i][j][0] - ref_mgai_idx[0][i][j][1], ref_rmgdi_idx[0][i][j][0] - ref_rmgdi_idx[0][i][j][1]), 2 * ref_mgai_idx[0][i][j][1], 2 * ref_rmgdi_idx[0][i][j][1], color='cyan', zorder=0, alpha=0.10))
            axs.add_patch(patches.Rectangle((ref_mgai_idx[0] - ref_mgai_idx[1],
                                                   ref_mgdi_idx[0] - ref_mgdi_idx[1]),
                                                  2 * ref_mgai_idx[1], 2 * ref_mgdi_idx[1],
                                                  color='yellow', zorder=10, alpha=0.40))
            axs.plot([ref_mgai_idx[0] - ref_mgai_idx[1],
                         ref_mgai_idx[0] + ref_mgai_idx[1]],
                        [ref_mgdi_idx[0], ref_mgdi_idx[0]], color='green', zorder=15,
                        alpha=0.80, linewidth=0.5)
            axs.plot([ref_mgai_idx[0], ref_mgai_idx[0]],
                        [ref_mgdi_idx[0] - ref_mgdi_idx[1],
                         ref_mgdi_idx[0] + ref_mgdi_idx[1]], color='orange', zorder=15,
                        alpha=0.80, linewidth=0.5)
            # axs[i, j].scatter(ref_mgai_idx[0][i][j][0], ref_mgdi_idx[0][i][j][0], color='black', marker='+', alpha=0.60, zorder=50)
            ref_caption = "   " + ref_info[3][0:len(ref_info[3])] + ", " + ref_info[2][0:len(ref_info[2])]
            axs.text(ref_mgai_idx[0], ref_mgdi_idx[0],
                           ref_caption + " (" + str(round(ref_mgai_idx[0], 2)) + ", " + str(
                               round(ref_mgdi_idx[0], 2)) + ")", fontdict=None, color='black', fontsize=7,
                           zorder=50, alpha=0.50)

            if ref_mgai_idx[0] > 1 and ref_mgdi_idx[0] > 1:
                axs.arrow(0, 0,
                                ref_mgai_idx[0],
                                ref_mgdi_idx[0], width=0.075, zorder=60,
                                alpha=0.99, edgecolor='red', facecolor='red')
            elif ref_mgai_idx[0] < 1 and ref_mgdi_idx[0] < 1:
                axs.arrow(0, 0,
                                ref_mgai_idx[0],
                                ref_mgdi_idx[0], width=0.075, zorder=60,
                                alpha=0.99,
                                edgecolor='green', facecolor='green')
            else:
                axs.arrow(0, 0,
                                ref_mgai_idx[0],
                                ref_mgdi_idx[0], width=0.075, zorder=60,
                                alpha=0.99,
                                edgecolor='orange', facecolor='orange')

            if self.global_mgai_idx[0] - ref_mgai_idx[0] > 0 and self.global_mgdi_idx[0] - \
                    ref_mgdi_idx[0] > 0:
                axs.arrow(ref_mgai_idx[0], ref_mgdi_idx[0],
                                self.global_mgai_idx[0] - ref_mgai_idx[0],
                                self.global_mgdi_idx[0] - ref_mgdi_idx[0], width=0.075, zorder=60,
                                alpha=0.99, edgecolor='red', facecolor='red')
            elif self.global_mgai_idx[0] - ref_mgai_idx[0] < 0 and self.global_mgdi_idx[
                0] - ref_mgdi_idx[0] < 0:
                axs.arrow(ref_mgai_idx[0], ref_mgdi_idx[0],
                                self.global_mgai_idx[0] - ref_mgai_idx[0],
                                self.global_mgdi_idx[0] - ref_mgdi_idx[0], width=0.075, zorder=60,
                                alpha=0.99,
                                edgecolor='green', facecolor='green')
            else:
                axs.arrow(ref_mgai_idx[0], ref_mgdi_idx[0],
                                self.global_mgai_idx[0] - ref_mgai_idx[0],
                                self.global_mgdi_idx[0] - ref_mgdi_idx[0], width=0.075, zorder=60,
                                alpha=0.99,
                                edgecolor='gray', facecolor='gray')

            a = list()
            b = list()
            c = list()
            d = list()

        else:
            if self.global_mgai_idx[0] > 1 and self.global_mgdi_idx[0] > 1:
                axs.arrow(0, 0,
                                self.global_mgai_idx[0],
                                self.global_mgdi_idx[0], width=0.075, zorder=60,
                                alpha=0.99, edgecolor='red', facecolor='red')
            elif self.global_mgai_idx[0] < 1 and self.global_mgdi_idx[0] < 1:
                axs.arrow(0, 0,
                                self.global_mgai_idx[0],
                                self.global_mgdi_idx[0], width=0.075, zorder=60,
                                alpha=0.99,
                                edgecolor='green', facecolor='green')
            else:
                axs.arrow(0, 0,
                                self.global_mgai_idx[0],
                                self.global_mgdi_idx[0], width=0.075, zorder=60,
                                alpha=0.99,
                                edgecolor='orange', facecolor='orange')


        if ref_comp_caption == "":
            plt.savefig(self.graph_type + "_Global_ADPlotGraph.png")
        else:
            plt.savefig(self.graph_type + "_Global_ADPlotGraph" + "_" + self.graph_name+ "_vs_" + ref_comp_caption + ".png")

        if self.all_graphs != 1:
            plt.show()
        else:
            plt.close
        return "Done"



    def adplot_triplane_graphs(self):

        ref_info = ""
        ref_path = ff.getfileparams("compare.ini", 0)
        ref_name = ff.getfileparams("compare.ini", 1)
        ref_comp_caption = ff.getfileparams("compare.ini", 2)
        ref_filename = ""
        if ref_name != '':
            for file in os.listdir(ref_path):
                if file.startswith("Reference_Kinematics_MGDI_MGAI_Triplane"):
                    ref_filename = file

            if ref_filename != "":
                ref_info = ref_filename.split("_")
                if os.path.isfile(ref_path + ref_filename):
                    infile = open(ref_path + ref_filename, 'rb')
                    ref_lmgdi_idx = pickle.load(infile)
                    ref_rmgdi_idx = pickle.load(infile)
                    ref_mgdi_idx = pickle.load(infile)
                    ref_mgai_idx = pickle.load(infile)
                    infile.close()

        graphprefs = ff.getgraphprefs("ADPlot Triplane Graphs")

        LevelLabels = ["Pelvic Level", "Hip Level", "Knee Level", "Ankle Level"]
        PlaneLabels = ["S", "F", "T"]

        if len(graphprefs) > 0:
            fig, axs = plt.subplots(self.plotlevels, figsize=(graphprefs[0], graphprefs[1]))
        else:
            fig, axs = plt.subplots(self.plotlevels,  figsize=(3, 9.5))

        fig.tight_layout(pad=self.graphs_space)

        fig.canvas.mpl_connect('button_press_event', on_click)

        plt.subplots_adjust(left=0.16,
                            bottom=0.075,
                            right=0.95,
                            top=0.95,
                            wspace=0.4,
                            hspace=0.4)

        if ref_name == "":
            fig.suptitle("AD plot Triplane Graphs " + self.graph_type + " " + self.graph_name, y=0.035, fontsize=8,
                         color='gray')
        else:
            fig.suptitle("AD plot Triplane Graphs " + self.graph_type + " " + self.graph_name + "_vs_" + ref_comp_caption, y=0.02, fontsize=8,
                         color='gray')

        for i in range(self.plotlevels):
            for j in range(self.planes):
                if self.plotlevels > 1 and self.planes > 1:
                    if self.plot_names[i][j] > '':
                        axs[i].set_title(LevelLabels[i], fontsize=8)
                        text = self.plot_axis_xyz[i][j].split("|")
                        if len(text) > 1:
                            axs[i].set_ylabel(text[1], labelpad=0.2, fontsize=6)
                    axs[i].tick_params(axis='x', labelsize=6)
                    axs[i].tick_params(axis='y', labelsize=6)
                    axs[i].plot(self.x_data[0][0], [0] * 101, color='black', linewidth=0.5)
                    axs[i].set_xlim(0, 7)
                    axs[i].set_ylim(0, 7)
                    axs[i].set_ylabel('Deviation (SD)', fontsize=6)
                    axs[i].set_xlabel('Asymmetry (SD)', fontsize=6)
                    axs[i].linewidth = 0.50
                    axs[i].spines['right'].set_visible(False)
                    axs[i].spines['left'].set_visible(False)
                    axs[i].spines['top'].set_visible(False)
                    axs[i].spines['bottom'].set_visible(False)
                    axs[i].tick_params(axis='x', colors='gray')
                    axs[i].tick_params(axis='y', colors='gray')
                    axs[i].add_patch(patches.Rectangle((0, 0), 1, 1, edgecolor='lightgreen', facecolor='lightgreen', fill=True, alpha=0.30, zorder=5))
                    axs[i].add_patch(patches.Rectangle((1, 0), 7, 1, edgecolor='lightgray', facecolor='lightgray', fill=True, alpha=0.30, zorder=10))
                    axs[i].plot([0, 7], [0, 7], color='lightgray', linewidth=0.5)
                    t = "   L MGDI: " + str(round(self.triplane_lmgdi_idx[i][0], 2)) + " NSDs ±(" + str(round(self.triplane_lmgdi_idx[i][1], 2)) + ")"
                    axs[i].text(1.2, 6.3, t, fontdict=None, color='red', fontsize=7, zorder=40, alpha=0.50)
                    t = "   R MGDI: " + str(round(self.triplane_rmgdi_idx[i][0], 2)) + " NSDs ±(" + str(round(self.triplane_rmgdi_idx[i][1], 2)) + ")"
                    axs[i].text(1.2, 5.7, t, fontdict=None, color='blue', fontsize=7, zorder=40, alpha=0.50)
                    t = "Mean MGDI: " + str(round(self.triplane_mgdi_idx[i][0], 2)) + " NSDs ±(" + str(round(self.triplane_mgdi_idx[i][1], 2)) + ")"
                    axs[i].text(1.2, 5.0, t, fontdict=None, color='gray', fontsize=7, zorder=40, alpha=0.30)
                    t = "Mean MGAI: " + str(round(self.triplane_mgai_idx[i][0], 2)) + " NSDs ±(" + str(round(self.triplane_mgai_idx[i][1], 2)) + ")"
                    axs[i].text(1.2, 0.3, t, fontdict=None, color='green', fontsize=7, zorder=40, alpha=0.30)
                    # axs[i].add_patch(patches.Rectangle((self.mgai_idx[0][i][j][0] - self.mgai_idx[0][i][j][1], self.lmgdi_idx[0][i][j][0] - self.lmgdi_idx[0][i][j][1]), 2 * self.mgai_idx[0][i][j][1], 2 * self.lmgdi_idx[0][i][j][1], color='red', zorder=0, alpha=0.10))
                    # axs[i].add_patch(patches.Rectangle((self.mgai_idx[0][i][j][0] - self.mgai_idx[0][i][j][1], self.rmgdi_idx[0][i][j][0] - self.rmgdi_idx[0][i][j][1]), 2 * self.mgai_idx[0][i][j][1], 2 * self.rmgdi_idx[0][i][j][1], color='blue', zorder=0, alpha=0.10))

                    axs[i].scatter(self.triplane_mgai_idx[i][0], self.triplane_mgdi_idx[i][0], color='black',
                                   marker='*', alpha=0.50, zorder=30)

                    a = list()
                    b = list()
                    c = list()
                    d = list()
                else:
                    axs[i].set_visible(False)

            if ref_info != "":
                # axs[i, j].add_patch(patches.Rectangle((ref_mgai_idx[0][i][j][0] - ref_mgai_idx[0][i][j][1], ref_lmgdi_idx[0][i][j][0] - ref_lmgdi_idx[0][i][j][1]), 2 * ref_mgai_idx[0][i][j][1], 2 * ref_lmgdi_idx[0][i][j][1], color='magenta', zorder=0, alpha=0.10))
                # axs[i, j].add_patch(patches.Rectangle((ref_mgai_idx[0][i][j][0] - ref_mgai_idx[0][i][j][1], ref_rmgdi_idx[0][i][j][0] - ref_rmgdi_idx[0][i][j][1]), 2 * ref_mgai_idx[0][i][j][1], 2 * ref_rmgdi_idx[0][i][j][1], color='cyan', zorder=0, alpha=0.10))
                axs[i].add_patch(patches.Rectangle((ref_mgai_idx[i][0] - ref_mgai_idx[i][1],
                                                       ref_mgdi_idx[i][0] - ref_mgdi_idx[i][1]),
                                                      2 * ref_mgai_idx[i][1], 2 * ref_mgdi_idx[i][1],
                                                      color='yellow', zorder=30, alpha=0.40))
                axs[i].plot([ref_mgai_idx[i][0] - ref_mgai_idx[i][1],
                             ref_mgai_idx[i][0] + ref_mgai_idx[i][1]],
                            [ref_mgdi_idx[i][0], ref_mgdi_idx[i][0]], color='green', zorder=15,
                            alpha=0.80, linewidth=0.5)
                axs[i].plot([ref_mgai_idx[i][0], ref_mgai_idx[i][0]],
                            [ref_mgdi_idx[i][0] - ref_mgdi_idx[i][1],
                             ref_mgdi_idx[i][0] + ref_mgdi_idx[i][1]], color='orange', zorder=15,
                            alpha=0.80, linewidth=0.5)
                # axs[i, j].scatter(ref_mgai_idx[0][i][j][0], ref_mgdi_idx[0][i][j][0], color='black', marker='+', alpha=0.60, zorder=50)
                ref_caption = "   " + ref_info[3][0:len(ref_info[3])] + ", " + ref_info[2][0:len(ref_info[2])]
                axs[i].text(ref_mgai_idx[i][0], ref_mgdi_idx[i][0],
                               ref_caption + " (" + str(round(ref_mgai_idx[i][0], 2)) + ", " + str(
                                   round(ref_mgdi_idx[i][0], 2)) + ")", fontdict=None, color='black', fontsize=7,
                               zorder=50, alpha=0.50)

                if ref_mgai_idx[i][0] > 1 and ref_mgdi_idx[i][0] > 1:
                    axs[i].arrow(0, 0,
                                    ref_mgai_idx[i][0],
                                    ref_mgdi_idx[i][0], width=0.075, zorder=60,
                                    alpha=0.99, edgecolor='red', facecolor='red')
                elif ref_mgai_idx[i][0] < 1 and ref_mgdi_idx[i][0] < 1:
                    axs[i].arrow(0, 0,
                                    ref_mgai_idx[i][0],
                                    ref_mgdi_idx[i][0], width=0.075, zorder=60,
                                    alpha=0.99,
                                    edgecolor='green', facecolor='green')
                else:
                    axs[i].arrow(0, 0,
                                    ref_mgai_idx[i][0],
                                    ref_mgdi_idx[i][0], width=0.075, zorder=60,
                                    alpha=0.99,
                                    edgecolor='orange', facecolor='orange')

                if self.triplane_mgai_idx[i][0] - ref_mgai_idx[i][0] > 0 and self.triplane_mgdi_idx[i][0] - \
                        ref_mgdi_idx[i][0] > 0:
                    axs[i].arrow(ref_mgai_idx[i][0], ref_mgdi_idx[i][0],
                                    self.triplane_mgai_idx[i][0] - ref_mgai_idx[i][0],
                                    self.triplane_mgdi_idx[i][0] - ref_mgdi_idx[i][0], width=0.075, zorder=60,
                                    alpha=0.99, edgecolor='red', facecolor='red')
                elif self.triplane_mgai_idx[i][0] - ref_mgai_idx[i][0] < 0 and self.triplane_mgdi_idx[j][
                    0] - ref_mgdi_idx[i][0] < 0:
                    axs[i].arrow(ref_mgai_idx[i][0], ref_mgdi_idx[i][0],
                                    self.triplane_mgai_idx[i][0] - ref_mgai_idx[i][0],
                                    self.triplane_mgdi_idx[i][0] - ref_mgdi_idx[i][0], width=0.075, zorder=60,
                                    alpha=0.99,
                                    edgecolor='green', facecolor='green')
                else:
                    axs[i].arrow(ref_mgai_idx[i][0], ref_mgdi_idx[i][0],
                                    self.triplane_mgai_idx[i][0] - ref_mgai_idx[i][0],
                                    self.triplane_mgdi_idx[i][0] - ref_mgdi_idx[i][0], width=0.075, zorder=60,
                                    alpha=0.99,
                                    edgecolor='gray', facecolor='gray')

                a = list()
                b = list()
                c = list()
                d = list()

            else:
                if self.triplane_mgai_idx[i][0] > 1 and self.triplane_mgdi_idx[i][0] > 1:
                    axs[i].arrow(0, 0,
                                    self.triplane_mgai_idx[i][0],
                                    self.triplane_mgdi_idx[i][0], width=0.075, zorder=60,
                                    alpha=0.99, edgecolor='red', facecolor='red')
                elif self.triplane_mgai_idx[i][0] < 1 and self.triplane_mgdi_idx[i][0] < 1:
                    axs[i].arrow(0, 0,
                                    self.triplane_mgai_idx[i][0],
                                    self.triplane_mgdi_idx[i][0], width=0.075, zorder=60,
                                    alpha=0.99,
                                    edgecolor='green', facecolor='green')
                else:
                    axs[i].arrow(0, 0,
                                    self.triplane_mgai_idx[i][0],
                                    self.triplane_mgdi_idx[i][0], width=0.075, zorder=60,
                                    alpha=0.99,
                                    edgecolor='orange', facecolor='orange')


        for i in range(self.plotlevels):
            for j in range(self.planes):
                if self.plotlevels > 1 and self.planes > 1:
                    if self.mgai_idx[0][i][j][0] > 0 and self.lmgdi_idx[0][i][j][0] > 0:
                        axs[i].scatter(self.mgai_idx[0][i][j][0], self.lmgdi_idx[0][i][j][0], color='red',
                                          marker='x', alpha=0.50, zorder=55)
                        axs[i].text(self.mgai_idx[0][i][j][0] + 0.10, self.lmgdi_idx[0][i][j][0], PlaneLabels[j], fontdict=None,
                                    color='red', fontsize=7, zorder=55)
                    if self.mgai_idx[0][i][j][0] > 0 and self.rmgdi_idx[0][i][j][0] > 0:
                        axs[i].scatter(self.mgai_idx[0][i][j][0], self.rmgdi_idx[0][i][j][0], color='blue', marker='o',
                                          alpha=0.50, zorder=55, facecolors='none', edgecolors='blue')
                        axs[i].text(self.mgai_idx[0][i][j][0] + 0.10, self.rmgdi_idx[0][i][j][0], PlaneLabels[j], fontdict=None,
                                    color='blue', fontsize=7, zorder=55)

        if ref_comp_caption == "":
            plt.savefig(self.graph_type + "_Triplane_ADPlotGraph.png")
        else:
            plt.savefig(self.graph_type + "_Triplane_ADPlotGraph" + "_" + self.graph_name+ "_vs_" + ref_comp_caption + ".png")

        if self.all_graphs != 1:
            plt.show()
        else:
            plt.close
        return "Done"


    def adplot_perplane_graphs(self):

        ref_info = ""
        ref_path = ff.getfileparams("compare.ini", 0)
        ref_name = ff.getfileparams("compare.ini", 1)
        ref_comp_caption = ff.getfileparams("compare.ini", 2)
        ref_filename = ""
        if ref_name != '':
            for file in os.listdir(ref_path):
                if file.startswith("Reference_Kinematics_MGDI_MGAI_Perplane"):
                    ref_filename = file

            if ref_filename != "":
                ref_info = ref_filename.split("_")
                if os.path.isfile(ref_path + ref_filename):
                    infile = open(ref_path + ref_filename, 'rb')
                    ref_lmgdi_idx = pickle.load(infile)
                    ref_rmgdi_idx = pickle.load(infile)
                    ref_mgdi_idx = pickle.load(infile)
                    ref_mgai_idx = pickle.load(infile)
                    infile.close()

        graphprefs = ff.getgraphprefs("ADPlot Perplane Graphs")

        PlaneLabels = ["Sagittal Plane", "Coronal Plane", "Transverse Plane"]
        PlotLevelLabels = ["P", "H", "K", "A"]

        if len(graphprefs) > 0:
            fig, axs = plt.subplots(1, self.planes, figsize=(graphprefs[0], graphprefs[1]))
        else:
            fig, axs = plt.subplots(1, self.planes, figsize=(9.5, 3.5))

        fig.tight_layout(pad=self.graphs_space)

        fig.canvas.mpl_connect('button_press_event', on_click)

        plt.subplots_adjust(left=0.05,
                            bottom=0.17,
                            right=0.95,
                            top=0.90,
                            wspace=0.2,
                            hspace=0.2)

        if ref_name == "":
            fig.suptitle("AD plot Perplane Graphs " + self.graph_type + " " + self.graph_name, y=0.035, fontsize=8,
                         color='gray')
        else:
            fig.suptitle("AD plot Perplane Graphs " + self.graph_type + " " + self.graph_name + "_vs_" + ref_comp_caption, y=0.02, fontsize=8,
                         color='gray')

        for j in range(self.planes):
                axs[j].set_title(PlaneLabels[j], fontsize=8)
                axs[j].tick_params(axis='x', labelsize=6)
                axs[j].tick_params(axis='y', labelsize=6)
                axs[j].plot(self.x_data[0][0], [0] * 101, color='black', linewidth=0.5)
                axs[j].set_xlim(0, 7)
                axs[j].set_ylim(0, 7)
                axs[j].set_ylabel('Deviation (SD)', fontsize=6)
                axs[j].set_xlabel('Asymmetry (SD)', fontsize=6)
                axs[j].linewidth = 0.50
                axs[j].spines['right'].set_visible(False)
                axs[j].spines['left'].set_visible(False)
                axs[j].spines['top'].set_visible(False)
                axs[j].spines['bottom'].set_visible(False)
                axs[j].tick_params(axis='x', colors='gray')
                axs[j].tick_params(axis='y', colors='gray')
                axs[j].add_patch(
                    patches.Rectangle((0, 0), 1, 1, edgecolor='lightgreen', facecolor='lightgreen', fill=True,
                                      alpha=0.30, zorder=5))
                axs[j].add_patch(
                    patches.Rectangle((1, 0), 7, 1, edgecolor='lightgray', facecolor='lightgray', fill=True,
                                      alpha=0.30, zorder=10))
                axs[j].plot([0, 7], [0, 7], color='lightgray', linewidth=0.5)
                t = "   L MGDI: " + str(round(self.perplane_lmgdi_idx[j][0], 2)) + " NSDs ±(" + str(
                    round(self.perplane_lmgdi_idx[j][1], 2)) + ")"
                axs[j].text(1.2, 6.3, t, fontdict=None, color='red', fontsize=7, zorder=40, alpha=0.50)
                t = "   R MGDI: " + str(round(self.perplane_rmgdi_idx[j][0], 2)) + " NSDs ±(" + str(
                    round(self.perplane_rmgdi_idx[j][1], 2)) + ")"
                axs[j].text(1.2, 5.7, t, fontdict=None, color='blue', fontsize=7, zorder=40, alpha=0.50)
                t = "Mean MGDI: " + str(round(self.perplane_mgdi_idx[j][0], 2)) + " NSDs ±(" + str(
                    round(self.perplane_mgdi_idx[j][1], 2)) + ")"
                axs[j].text(1.2, 5.0, t, fontdict=None, color='gray', fontsize=7, zorder=40, alpha=0.30)
                t = "Mean MGAI: " + str(round(self.perplane_mgai_idx[j][0], 2)) + " NSDs ±(" + str(
                    round(self.perplane_mgai_idx[j][1], 2)) + ")"
                axs[j].text(1.2, 0.3, t, fontdict=None, color='green', fontsize=7, zorder=40, alpha=0.30)

                # axs[j].add_patch(patches.Rectangle((self.mgai_idx[0][i][j][0] - self.mgai_idx[0][i][j][1],
                #                                     self.lmgdi_idx[0][i][j][0] - self.lmgdi_idx[0][i][j][1]),
                #                                    2 * self.mgai_idx[0][i][j][1], 2 * self.lmgdi_idx[0][i][j][1],
                #                                    color='red', zorder=0, alpha=0.10))
                # axs[j].add_patch(patches.Rectangle((self.mgai_idx[0][i][j][0] - self.mgai_idx[0][i][j][1],
                #                                     self.rmgdi_idx[0][i][j][0] - self.rmgdi_idx[0][i][j][1]),
                #                                    2 * self.mgai_idx[0][i][j][1], 2 * self.rmgdi_idx[0][i][j][1],
                #                                    color='blue', zorder=0, alpha=0.10))

                axs[j].scatter(self.perplane_mgai_idx[j][0], self.perplane_mgdi_idx[j][0], color='black',
                               marker='*', alpha=0.50, zorder=30)

                # if self.perplane_mgai_idx[j][0] > 1 and self.perplane_mgdi_idx[j][0] > 1:
                #     axs[j].arrow(0, 0,
                #                     self.perplane_mgai_idx[j][0],
                #                     self.perplane_mgdi_idx[j][0], width=0.075,
                #                     alpha=0.99, edgecolor='red', facecolor='red')
                # elif self.perplane_mgai_idx[j][0] < 1 and self.perplane_mgdi_idx[j][0] < 1:
                #     axs[j].arrow(0, 0,
                #                     self.perplane_mgai_idx[j][0],
                #                     self.perplane_mgdi_idx[j][0], width=0.075,
                #                     alpha=0.99,
                #                     edgecolor='green', facecolor='green')
                # else:
                #     axs[j].arrow(0, 0,
                #                     self.perplane_mgai_idx[j][0],
                #                     self.perplane_mgdi_idx[j][0], width=0.075,
                #                     alpha=0.99,
                #                     edgecolor='orange', facecolor='orange')
                # a = list()
                # b = list()
                # c = list()
                # d = list()

                if ref_info != "":
                    # axs[i, j].add_patch(patches.Rectangle((ref_mgai_idx[0][i][j][0] - ref_mgai_idx[0][i][j][1], ref_lmgdi_idx[0][i][j][0] - ref_lmgdi_idx[0][i][j][1]), 2 * ref_mgai_idx[0][i][j][1], 2 * ref_lmgdi_idx[0][i][j][1], color='magenta', zorder=0, alpha=0.10))
                    # axs[i, j].add_patch(patches.Rectangle((ref_mgai_idx[0][i][j][0] - ref_mgai_idx[0][i][j][1], ref_rmgdi_idx[0][i][j][0] - ref_rmgdi_idx[0][i][j][1]), 2 * ref_mgai_idx[0][i][j][1], 2 * ref_rmgdi_idx[0][i][j][1], color='cyan', zorder=0, alpha=0.10))
                    axs[j].add_patch(patches.Rectangle((ref_mgai_idx[j][0] - ref_mgai_idx[j][1],
                                                           ref_mgdi_idx[j][0] - ref_mgdi_idx[j][1]),
                                                          2 * ref_mgai_idx[j][1], 2 * ref_mgdi_idx[j][1],
                                                          color='yellow', zorder=30, alpha=0.40))
                    axs[j].plot([ref_mgai_idx[j][0] - ref_mgai_idx[j][1],
                                    ref_mgai_idx[j][0] + ref_mgai_idx[j][1]],
                                   [ref_mgdi_idx[j][0], ref_mgdi_idx[j][0]], color='green', zorder=15,
                                   alpha=0.80, linewidth=0.5)
                    axs[j].plot([ref_mgai_idx[j][0], ref_mgai_idx[j][0]],
                                   [ref_mgdi_idx[j][0] - ref_mgdi_idx[j][1],
                                    ref_mgdi_idx[j][0] + ref_mgdi_idx[j][1]], color='orange', zorder=15,
                                   alpha=0.80, linewidth=0.5)

                    # axs[i, j].scatter(ref_mgai_idx[0][i][j][0], ref_mgdi_idx[0][i][j][0], color='black', marker='+', alpha=0.60, zorder=50)
                    ref_caption = "   " + ref_info[3][0:len(ref_info[3])] + ", " + ref_info[2][0:len(ref_info[2])]
                    axs[j].text(ref_mgai_idx[j][0], ref_mgdi_idx[j][0],
                                   ref_caption + " (" + str(round(ref_mgai_idx[j][0], 2)) + ", " + str(
                                       round(ref_mgdi_idx[j][0], 2)) + ")", fontdict=None, color='black', fontsize=7,
                                   zorder=50, alpha=0.50)

                    if ref_mgai_idx[j][0] > 1 and ref_mgdi_idx[j][0] > 1:
                        axs[j].arrow(0, 0,
                                        ref_mgai_idx[j][0],
                                        ref_mgdi_idx[j][0], width=0.075, zorder=60,
                                        alpha=0.99, edgecolor='red', facecolor='red')
                    elif ref_mgai_idx[j][0] < 1 and ref_mgdi_idx[j][0] < 1:
                        axs[j].arrow(0, 0,
                                        ref_mgai_idx[j][0],
                                        ref_mgdi_idx[j][0], width=0.075, zorder=60,
                                        alpha=0.99,
                                        edgecolor='green', facecolor='green')
                    else:
                        axs[j].arrow(0, 0,
                                        ref_mgai_idx[j][0],
                                        ref_mgdi_idx[j][0], width=0.075, zorder=60,
                                        alpha=0.99,
                                        edgecolor='orange', facecolor='orange')

                    if self.perplane_mgai_idx[j][0] - ref_mgai_idx[j][0] > 0 and self.perplane_mgdi_idx[j][0] - \
                            ref_mgdi_idx[j][0] > 0:
                        axs[j].arrow(ref_mgai_idx[j][0], ref_mgdi_idx[j][0],
                                        self.perplane_mgai_idx[j][0] - ref_mgai_idx[j][0],
                                        self.perplane_mgdi_idx[j][0] - ref_mgdi_idx[j][0], width=0.075, zorder=60,
                                        alpha=0.99, edgecolor='red', facecolor='red')
                    elif self.perplane_mgai_idx[j][0] - ref_mgai_idx[j][0] < 0 and self.perplane_mgdi_idx[j][
                        0] - ref_mgdi_idx[j][0] < 0:
                        axs[j].arrow(ref_mgai_idx[j][0], ref_mgdi_idx[j][0],
                                        self.perplane_mgai_idx[j][0] - ref_mgai_idx[j][0],
                                        self.perplane_mgdi_idx[j][0] - ref_mgdi_idx[j][0], width=0.075, zorder=60,
                                        alpha=0.99,
                                        edgecolor='green', facecolor='green')
                    else:
                        axs[j].arrow(ref_mgai_idx[j][0], ref_mgdi_idx[j][0],
                                        self.perplane_mgai_idx[j][0] - ref_mgai_idx[j][0],
                                        self.perplane_mgdi_idx[j][0] - ref_mgdi_idx[j][0], width=0.075, zorder=60,
                                        alpha=0.99,
                                        edgecolor='gray', facecolor='gray')

                    a = list()
                    b = list()
                    c = list()
                    d = list()

                else:
                    if self.perplane_mgai_idx[j][0] > 1 and self.perplane_mgdi_idx[j][0] > 1:
                        axs[j].arrow(0, 0,
                                        self.perplane_mgai_idx[j][0],
                                        self.perplane_mgdi_idx[j][0], width=0.075, zorder=60,
                                        alpha=0.99, edgecolor='red', facecolor='red')
                    elif self.perplane_mgai_idx[j][0] < 1 and self.perplane_mgdi_idx[j][0] < 1:
                        axs[j].arrow(0, 0,
                                        self.perplane_mgai_idx[j][0],
                                        self.perplane_mgdi_idx[j][0], width=0.075, zorder=60,
                                        alpha=0.99,
                                        edgecolor='green', facecolor='green')
                    else:
                        axs[j].arrow(0, 0,
                                        self.perplane_mgai_idx[j][0],
                                        self.perplane_mgdi_idx[j][0], width=0.075, zorder=60,
                                        alpha=0.99,
                                        edgecolor='orange', facecolor='orange')



        for j in range(self.planes):
            for i in range(self.plotlevels):
                if self.plotlevels > 1 and self.planes > 1:
                    if self.mgai_idx[0][i][j][0] > 0 and self.lmgdi_idx[0][i][j][0] > 0:
                        axs[j].scatter(self.mgai_idx[0][i][j][0], self.lmgdi_idx[0][i][j][0], color='red',
                                       marker='x', alpha=0.50, zorder=55)
                        axs[j].text(self.mgai_idx[0][i][j][0] + 0.10, self.lmgdi_idx[0][i][j][0], PlotLevelLabels[i],
                                    fontdict=None,
                                    color='red', fontsize=7, zorder=55)
                    if self.mgai_idx[0][i][j][0] > 0 and self.rmgdi_idx[0][i][j][0] > 0:
                        axs[j].scatter(self.mgai_idx[0][i][j][0], self.rmgdi_idx[0][i][j][0], color='blue', marker='o',
                                       alpha=0.50, zorder=55, facecolors='none', edgecolors='blue')
                        axs[j].text(self.mgai_idx[0][i][j][0] + 0.10, self.rmgdi_idx[0][i][j][0], PlotLevelLabels[i],
                                    fontdict=None,
                                    color='blue', fontsize=7, zorder=55)

        if ref_comp_caption == "":
            plt.savefig(self.graph_type + "_Perplane_ADPlotGraph.png")
        else:
            plt.savefig(self.graph_type + "_Perplane_ADPlotGraph" + "_" + self.graph_name+ "_vs_" + ref_comp_caption + ".png")


        if self.all_graphs != 1:
            plt.show()
        else:
            plt.close
        return "Done"



    def adplot_graphs(self):

        graphprefs = ff.getgraphprefs("ADPlot Graphs")
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

        fig.suptitle("AD plot Graphs " + self.graph_type + " " + self.graph_name, y=0.02, fontsize=8, color='gray')

        for i in range(self.plotlevels):
            for j in range(self.planes):
                if self.plotlevels > 1 and self.planes > 1:
                    if self.plot_names[i][j] > '':
                        axs[i, j].set_title(self.plot_names[i][j], fontsize=8)
                        text = self.plot_axis_xyz[i][j].split("|")
                        if len(text) > 1:
                            axs[i, j].set_ylabel(text[1], labelpad=0.2, fontsize=6)
                        axs[i, j].tick_params(axis='x', labelsize=6)
                        axs[i, j].tick_params(axis='y', labelsize=6)
                        axs[i, j].plot(self.x_data[0][0], [0] * 101, color='black', linewidth=0.5)
                        axs[i, j].set_xlim(0, 7)
                        axs[i, j].set_ylim(0, 7)
                        axs[i, j].set_ylabel('Deviation (SD)', fontsize=6)
                        axs[i, j].set_xlabel('Asymmetry (SD)', fontsize=6)
                        axs[i, j].linewidth = 0.50
                        axs[i, j].spines['right'].set_visible(False)
                        axs[i, j].spines['left'].set_visible(False)
                        axs[i, j].spines['top'].set_visible(False)
                        axs[i, j].spines['bottom'].set_visible(False)
                        axs[i, j].tick_params(axis='x', colors='gray')
                        axs[i, j].tick_params(axis='y', colors='gray')
                        axs[i, j].add_patch(
                            patches.Rectangle((0, 0), 1, 1, edgecolor='lightgreen', facecolor='lightgreen', fill=True,
                                              alpha=0.30, zorder=5))
                        axs[i, j].add_patch(
                            patches.Rectangle((1, 0), 7, 1, edgecolor='lightgray', facecolor='lightgray', fill=True,
                                              alpha=0.30, zorder=10))
                        axs[i, j].plot([0, 7], [0, 7], color='lightgray', linewidth=0.5)
                        t = "   L MGDI: " + str(round(self.lmgdi_idx[0][i][j][0], 2)) + " NSDs ±(" + str(
                            round(self.lmgdi_idx[0][i][j][1], 2)) + ")"
                        axs[i, j].text(1.2, 6.3, t, fontdict=None, color='red', fontsize=7, zorder=40, alpha=0.50)
                        t = "   R MGDI: " + str(round(self.rmgdi_idx[0][i][j][0], 2)) + " NSDs ±(" + str(
                            round(self.rmgdi_idx[0][i][j][1], 2)) + ")"
                        axs[i, j].text(1.2, 5.7, t, fontdict=None, color='blue', fontsize=7, zorder=40, alpha=0.50)
                        # t = "Mean MGDI: " + str(round(self.mgdi_idx[0][i][j][0], 2)) + " NSDs ±(" + str(round(self.mgdi_idx[0][i][j][1], 2)) + ")"
                        # axs[i, j].text(1.2, 5.0, t, fontdict=None, color='gray', fontsize=7, zorder=40, alpha=0.30)
                        t = "Mean MGAI: " + str(round(self.mgai_idx[0][i][j][0], 2)) + " NSDs ±(" + str(
                            round(self.mgai_idx[0][i][j][1], 2)) + ")"
                        axs[i, j].text(1.2, 0.3, t, fontdict=None, color='green', fontsize=7, zorder=40, alpha=0.30)
                        # axs[i, j].add_patch(patches.Rectangle((self.mgai_idx[0][i][j][0] - self.mgai_idx[0][i][j][1], self.lmgdi_idx[0][i][j][0] - self.lmgdi_idx[0][i][j][1]), 2 * self.mgai_idx[0][i][j][1], 2 * self.lmgdi_idx[0][i][j][1], color='red', zorder=0, alpha=0.20))
                        # axs[i, j].add_patch(patches.Rectangle((self.mgai_idx[0][i][j][0] - self.mgai_idx[0][i][j][1], self.rmgdi_idx[0][i][j][0] - self.rmgdi_idx[0][i][j][1]), 2 * self.mgai_idx[0][i][j][1], 2 * self.rmgdi_idx[0][i][j][1], color='blue', zorder=0, alpha=0.20))

                        a = list()
                        b = list()
                        c = list()
                        d = list()
                    else:
                        axs[i, j].set_visible(False)

        for l in range(len(self.lr_sets)):
            g =  self.lr_sets[l][0]
            k = self.lr_sets[l][1]

            for i in range(self.plotlevels):
                for j in range(self.planes):
                    if self.plotlevels > 1 and self.planes > 1:
                        if self.plot_names[i][j] > '':
                            if g == 0:
                                l = 1
                            else:
                                l = (g / 2) + 1

                            axs[i, j].scatter(self.asy_idx[g][i][j][0], self.dev_idx[g][i][j][0],
                                              color=self.line_colours[g][0], marker='x', alpha=0.50, zorder=30)
                            axs[i, j].text(self.asy_idx[g][i][j][0], self.dev_idx[g][i][j][0], int(l), fontdict=None,
                                           color=self.line_colours[g][0], fontsize=7, zorder=40)
                            axs[i, j].scatter(self.asy_idx[k][i][j][0], self.dev_idx[k][i][j][0], color='blue',
                                              marker='o', alpha=0.50, zorder=20, facecolors='none',
                                              edgecolors=self.line_colours[k][0])
                            axs[i, j].text(self.asy_idx[k][i][j][0], self.dev_idx[k][i][j][0], int(l), fontdict=None,
                                           color=self.line_colours[k][0], fontsize=7, zorder=40)

                    axs[i, j].scatter(self.mgai_idx[0][i][j][0], self.lmgdi_idx[0][i][j][0],
                                      color=self.line_colours[g][0],
                                      marker='*', alpha=0.50, zorder=30)
                    axs[i, j].scatter(self.mgai_idx[0][i][j][0], self.rmgdi_idx[0][i][j][0], color='blue', marker='*',
                                      alpha=0.50, zorder=20, facecolors='none', edgecolors=self.line_colours[k][0])
        plt.savefig(self.graph_type + "_ADPlotGraph.png")

        if self.all_graphs != 1:
            plt.show()
        else:
            plt.close
        return "Done"


    def adplot_boxes(self):

        graphprefs = ff.getgraphprefs("ADPlot Boxes")
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

        fig.suptitle("AD plot LR area " + self.graph_type + " " + self.graph_name,  y=0.02, fontsize=8, color='gray')
        for i in range(self.plotlevels):
            for j in range(self.planes):
                    if self.plot_names[i][j] > '':
                        axs[i, j].set_title(self.plot_names[i][j], fontsize=8)
                        text = self.plot_axis_xyz[i][j].split("|")
                        if len(text) > 1:
                            axs[i, j].set_ylabel(text[1], labelpad=0.2, fontsize=6)
                        axs[i, j].tick_params(axis='x', labelsize=6)
                        axs[i, j].tick_params(axis='y', labelsize=6)
                        axs[i, j].plot(self.x_data[0][0], [0] * 101, color='black', linewidth=0.5)
                        axs[i, j].set_xlim(0, 7)
                        axs[i, j].set_ylim(0, 7)
                        axs[i, j].set_ylabel('Deviation (SD)', fontsize=6)
                        axs[i, j].set_xlabel('Asymmetry (SD)', fontsize=6)
                        axs[i, j].linewidth = 0.50
                        axs[i, j].spines['right'].set_visible(False)
                        axs[i, j].spines['left'].set_visible(False)
                        axs[i, j].spines['top'].set_visible(False)
                        axs[i, j].spines['bottom'].set_visible(False)
                        axs[i, j].tick_params(axis='x', colors='gray')
                        axs[i, j].tick_params(axis='y', colors='gray')
                        axs[i, j].add_patch(patches.Rectangle((0, 0), 1, 1, edgecolor='lightgreen', facecolor='lightgreen', fill=True, alpha=0.30, zorder=5))
                        axs[i, j].add_patch(patches.Rectangle((1, 0), 7, 1, edgecolor='lightgray', facecolor='lightgray', fill=True, alpha=0.30, zorder=10))
                        axs[i, j].plot([0, 7], [0, 7], color='lightgray', linewidth=0.5)
                        t = "   L MGDI: " + str(round(self.lmgdi_idx[0][i][j][0], 2)) + " NSDs ±(" + str(round(self.lmgdi_idx[0][i][j][1], 2)) + ")"
                        axs[i, j].text(1.2, 6.3, t, fontdict=None, color='red', fontsize=7, zorder=40, alpha=0.50)
                        t = "   R MGDI: " + str(round(self.rmgdi_idx[0][i][j][0], 2)) + " NSDs ±(" + str(round(self.rmgdi_idx[0][i][j][1], 2)) + ")"
                        axs[i, j].text(1.2, 5.7, t, fontdict=None, color='blue', fontsize=7, zorder=40, alpha=0.50)
                        # t = "Mean MGDI: " + str(round(self.mgdi_idx[0][i][j][0], 2)) + " NSDs ±(" + str(round(self.mgdi_idx[0][i][j][1], 2)) + ")"
                        # axs[i, j].text(1.2, 5.0, t, fontdict=None, color='gray', fontsize=7, zorder=40, alpha=0.30)
                        t = "Mean MGAI: " + str(round(self.mgai_idx[0][i][j][0], 2)) + " NSDs ±(" + str(round(self.mgai_idx[0][i][j][1], 2)) + ")"
                        axs[i, j].text(1.2, 0.3, t, fontdict=None, color='green', fontsize=7, zorder=40, alpha=0.50)
                        axs[i, j].add_patch(patches.Rectangle((self.mgai_idx[0][i][j][0] - self.mgai_idx[0][i][j][1], self.lmgdi_idx[0][i][j][0] - self.lmgdi_idx[0][i][j][1]), 2 * self.mgai_idx[0][i][j][1], 2 * self.lmgdi_idx[0][i][j][1], color='red', zorder=20, alpha=0.20))
                        axs[i, j].add_patch(patches.Rectangle((self.mgai_idx[0][i][j][0] - self.mgai_idx[0][i][j][1], self.rmgdi_idx[0][i][j][0] - self.rmgdi_idx[0][i][j][1]), 2 * self.mgai_idx[0][i][j][1], 2 * self.rmgdi_idx[0][i][j][1], color='blue', zorder=25, alpha=0.20))
                        axs[i, j].scatter(self.mgai_idx[0][i][j][0], self.lmgdi_idx[0][i][j][0], color='red', marker='*', alpha=0.30, zorder=30)
                        axs[i, j].scatter(self.mgai_idx[0][i][j][0], self.rmgdi_idx[0][i][j][0], color='blue',marker='*', alpha=0.30, zorder=35)

                        a = list()
                        b = list()
                        c = list()
                        d = list()


                    else:
                        axs[i, j].set_visible(False)

        plt.savefig(self.graph_type + "_ADPlotBoxes.png")

        if self.all_graphs != 1:
            plt.show()
        else:
            plt.close
        return "Done"


    def adplot_grand_mean_boxes(self):
        ref_info = ""
        ref_path = ff.getfileparams("compare.ini", 0)
        ref_name = ff.getfileparams("compare.ini", 1)
        ref_comp_caption = ff.getfileparams("compare.ini", 2)
        ref_filename = ""
        if ref_name != '':
            for file in os.listdir(ref_path):
                if file.startswith("Reference_Kinematics_MGDI_MGAI_AllGraphs"):
                    ref_filename = file

            if ref_filename != "":
                ref_info = ref_filename.split("_")
                if os.path.isfile(ref_path + ref_filename):
                    infile = open(ref_path + ref_filename, 'rb')
                    ref_lmgdi_idx = pickle.load(infile)
                    ref_rmgdi_idx = pickle.load(infile)
                    ref_mgdi_idx = pickle.load(infile)
                    ref_mgai_idx = pickle.load(infile)
                    infile.close()

        graphprefs = ff.getgraphprefs("ADPlot Grand Mean Boxes")
        if len(graphprefs) > 0:
            fig, axs = plt.subplots(self.plotlevels, self.planes, figsize=(graphprefs[0], graphprefs[1]))
        else:
            fig, axs = plt.subplots(self.plotlevels, self.planes, figsize=(8, 9.5))

        fig.tight_layout(pad=self.graphs_space)

        fig.canvas.mpl_connect('button_press_event', on_click)
        plt.subplots_adjust(left=0.05,
                            bottom=0.06,
                            right=0.95,
                            top=0.94,
                            wspace=0.4,
                            hspace=0.4)
        if ref_name == "":
            fig.suptitle("AD plot LR area and Mean  " + self.graph_type + " " + self.graph_name,  y=0.02, fontsize=8, color='gray')
        else:
            fig.suptitle("AD plot LR area and Mean  " + self.graph_type + " " + self.graph_name + "_vs_" + ref_comp_caption, y=0.02, fontsize=8,
                         color='gray')
        for i in range(self.plotlevels):
            for j in range(self.planes):
                if self.plotlevels > 1 and self.planes > 1:
                    if self.plot_names[i][j] > '':
                        axs[i, j].set_title(self.plot_names[i][j], fontsize=8)
                        text = self.plot_axis_xyz[i][j].split("|")
                        if len(text) > 1:
                            axs[i, j].set_ylabel(text[1], labelpad=0.2, fontsize=6)
                        axs[i, j].tick_params(axis='x', labelsize=6)
                        axs[i, j].tick_params(axis='y', labelsize=6)
                        axs[i, j].plot(self.x_data[0][0], [0] * 101, color='black', linewidth=0.5)
                        axs[i, j].set_xlim(0, 7)
                        axs[i, j].set_ylim(0, 7)
                        axs[i, j].set_ylabel('Deviation (SD)', fontsize=6)
                        axs[i, j].set_xlabel('Asymmetry (SD)', fontsize=6)
                        axs[i, j].linewidth = 0.50
                        axs[i, j].spines['right'].set_visible(False)
                        axs[i, j].spines['left'].set_visible(False)
                        axs[i, j].spines['top'].set_visible(False)
                        axs[i, j].spines['bottom'].set_visible(False)
                        axs[i, j].tick_params(axis='x', colors='gray')
                        axs[i, j].tick_params(axis='y', colors='gray')
                        axs[i, j].add_patch(patches.Rectangle((0, 0), 1, 1, edgecolor='lightgreen', facecolor='lightgreen', fill=True, alpha=0.30, zorder=5))
                        axs[i, j].add_patch(patches.Rectangle((1, 0), 7, 1, edgecolor='lightgray', facecolor='lightgray', fill=True, alpha=0.30, zorder=10))
                        axs[i, j].plot([0, 7], [0, 7], color='lightgray', linewidth=0.5)
                        t = "Mean MGDI: " + str(round(self.mgdi_idx[0][i][j][0], 2)) + " NSDs ±(" + str(round(self.mgdi_idx[0][i][j][1], 2)) + ")"
                        axs[i, j].text(1.2, 6.3, t, fontdict=None, color='gray', fontsize=7, zorder=50, alpha=0.50)
                        t = "   L MGDI: " + str(round(self.lmgdi_idx[0][i][j][0], 2)) + " NSDs ±(" + str(round(self.lmgdi_idx[0][i][j][1], 2)) + ")"
                        axs[i, j].text(1.2, 5.7, t, fontdict=None, color='red', fontsize=7, zorder=50, alpha=0.50)
                        t = "   R MGDI: " + str(round(self.rmgdi_idx[0][i][j][0], 2)) + " NSDs ±(" + str(round(self.lmgdi_idx[0][i][j][1], 2)) + ")"
                        axs[i, j].text(1.2, 5.0, t, fontdict=None, color='blue', fontsize=7, zorder=50, alpha=0.50)
                        t = "Mean MGAI: " + str(round(self.mgai_idx[0][i][j][0], 2)) + " NSDs ±(" + str(round(self.mgai_idx[0][i][j][1], 2)) + ")"
                        axs[i, j].text(1.2, 0.3, t, fontdict=None, color='green', fontsize=7, zorder=50, alpha=0.50)
                        if ref_info != "":
                            axs[i, j].add_patch(patches.Rectangle((self.mgai_idx[0][i][j][0] - self.mgai_idx[0][i][j][1], self.lmgdi_idx[0][i][j][0] - self.lmgdi_idx[0][i][j][1]), 2 * self.mgai_idx[0][i][j][1], 2 * self.lmgdi_idx[0][i][j][1], color='red', zorder=40, alpha=0.15))
                            axs[i, j].add_patch(patches.Rectangle((self.mgai_idx[0][i][j][0] - self.mgai_idx[0][i][j][1], self.rmgdi_idx[0][i][j][0] - self.rmgdi_idx[0][i][j][1]), 2 * self.mgai_idx[0][i][j][1], 2 * self.rmgdi_idx[0][i][j][1], color='blue', zorder=40, alpha=0.15))
                        if ref_info == "":
                            axs[i, j].add_patch(patches.Rectangle((self.mgai_idx[0][i][j][0] - self.mgai_idx[0][i][j][1],self.mgdi_idx[0][i][j][0] - self.mgdi_idx[0][i][j][1]), 2 * self.mgai_idx[0][i][j][1],2 * self.mgdi_idx[0][i][j][1], color='darkgray', zorder=50, alpha=0.50))
                        # axs[i, j].scatter(self.mgai_idx[0][i][j][0], self.mgdi_idx[0][i][j][0], color='black', marker='*', alpha=0.50, zorder=60)


                        if ref_info != "":
                            # axs[i, j].add_patch(patches.Rectangle((ref_mgai_idx[0][i][j][0] - ref_mgai_idx[0][i][j][1], ref_lmgdi_idx[0][i][j][0] - ref_lmgdi_idx[0][i][j][1]), 2 * ref_mgai_idx[0][i][j][1], 2 * ref_lmgdi_idx[0][i][j][1], color='magenta', zorder=0, alpha=0.10))
                            # axs[i, j].add_patch(patches.Rectangle((ref_mgai_idx[0][i][j][0] - ref_mgai_idx[0][i][j][1], ref_rmgdi_idx[0][i][j][0] - ref_rmgdi_idx[0][i][j][1]), 2 * ref_mgai_idx[0][i][j][1], 2 * ref_rmgdi_idx[0][i][j][1], color='cyan', zorder=0, alpha=0.10))
                            axs[i, j].add_patch(patches.Rectangle((ref_mgai_idx[0][i][j][0] - ref_mgai_idx[0][i][j][1], ref_mgdi_idx[0][i][j][0] - ref_mgdi_idx[0][i][j][1]), 2 * ref_mgai_idx[0][i][j][1],2 * ref_mgdi_idx[0][i][j][1], color='yellow', zorder=10, alpha=0.40))
                            axs[i, j].plot([ref_mgai_idx[0][i][j][0] - ref_mgai_idx[0][i][j][1], ref_mgai_idx[0][i][j][0] + ref_mgai_idx[0][i][j][1]], [ref_mgdi_idx[0][i][j][0], ref_mgdi_idx[0][i][j][0]], color='green', zorder=15, alpha=0.80, linewidth=0.25)
                            axs[i, j].plot([ref_mgai_idx[0][i][j][0], ref_mgai_idx[0][i][j][0]], [ref_mgdi_idx[0][i][j][0] - ref_mgdi_idx[0][i][j][1], ref_mgdi_idx[0][i][j][0] + ref_mgdi_idx[0][i][j][1]], color='orange', zorder=15, alpha=0.80, linewidth=0.25)

                            #axs[i, j].scatter(ref_mgai_idx[0][i][j][0], ref_mgdi_idx[0][i][j][0], color='black', marker='+', alpha=0.60, zorder=50)
                            ref_caption = "   " + ref_info[3][0:len(ref_info[3])] + ", " + ref_info[2][0:len(ref_info[2])]
                            axs[i, j].text(ref_mgai_idx[0][i][j][0], ref_mgdi_idx[0][i][j][0], ref_caption + " (" + str(round(ref_mgai_idx[0][i][j][0], 2)) + ", " + str(round(ref_mgdi_idx[0][i][j][0], 2)) + ")", fontdict=None, color='black', fontsize=7, zorder=50, alpha=0.50)

                            if ref_mgai_idx[0][i][j][0] > 1 and ref_mgdi_idx[0][i][j][0] > 1:
                                axs[i, j].arrow(0, 0,
                                                ref_mgai_idx[0][i][j][0] ,
                                                ref_mgdi_idx[0][i][j][0] , width=0.075, zorder=50,
                                                alpha=0.99, edgecolor='red', facecolor='red')
                            elif ref_mgai_idx[0][i][j][0] < 1 and ref_mgdi_idx[0][i][j][0] < 1:
                                axs[i, j].arrow(0, 0,
                                                ref_mgai_idx[0][i][j][0],
                                                ref_mgdi_idx[0][i][j][0], width=0.075, zorder=50,
                                                alpha=0.99,
                                                edgecolor='green', facecolor='green')
                            else:
                                axs[i, j].arrow(0, 0,
                                                ref_mgai_idx[0][i][j][0] ,
                                                ref_mgdi_idx[0][i][j][0] , width=0.075, zorder=50,
                                                alpha=0.99,
                                                edgecolor='orange', facecolor='orange')



                            if self.mgai_idx[0][i][j][0] - ref_mgai_idx[0][i][j][0] > 0 and self.mgdi_idx[0][i][j][0] - \
                                    ref_mgdi_idx[0][i][j][0] > 0:
                                axs[i, j].arrow(ref_mgai_idx[0][i][j][0], ref_mgdi_idx[0][i][j][0],
                                                self.mgai_idx[0][i][j][0] - ref_mgai_idx[0][i][j][0],
                                                self.mgdi_idx[0][i][j][0] - ref_mgdi_idx[0][i][j][0], width=0.075, zorder=50,
                                                alpha=0.99, edgecolor='red', facecolor='red')
                            elif self.mgai_idx[0][i][j][0] - ref_mgai_idx[0][i][j][0] < 0 and self.mgdi_idx[0][i][j][
                                0] - ref_mgdi_idx[0][i][j][0] < 0:
                                axs[i, j].arrow(ref_mgai_idx[0][i][j][0], ref_mgdi_idx[0][i][j][0],
                                                self.mgai_idx[0][i][j][0] - ref_mgai_idx[0][i][j][0],
                                                self.mgdi_idx[0][i][j][0] - ref_mgdi_idx[0][i][j][0], width=0.075, zorder=50,
                                                alpha=0.99,
                                                edgecolor='green', facecolor='green')
                            else:
                                axs[i, j].arrow(ref_mgai_idx[0][i][j][0], ref_mgdi_idx[0][i][j][0],
                                                self.mgai_idx[0][i][j][0] - ref_mgai_idx[0][i][j][0],
                                                self.mgdi_idx[0][i][j][0] - ref_mgdi_idx[0][i][j][0], width=0.075, zorder=50,
                                                alpha=0.99,
                                                edgecolor='gray', facecolor='gray')


                            a = list()
                            b = list()
                            c = list()
                            d = list()
                        else:
                            if self.mgai_idx[0][i][j][0] > 1 and self.mgdi_idx[0][i][j][0] > 1:
                                axs[i, j].arrow(0, 0,
                                                self.mgai_idx[0][i][j][0] ,
                                                self.mgdi_idx[0][i][j][0] , width=0.075, zorder=50,
                                                alpha=0.99, edgecolor='red', facecolor='red')
                            elif self.mgai_idx[0][i][j][0] < 1 and self.mgdi_idx[0][i][j][0] < 1:
                                axs[i, j].arrow(0, 0,
                                                self.mgai_idx[0][i][j][0],
                                                self.mgdi_idx[0][i][j][0], width=0.075, zorder=50,
                                                alpha=0.99,
                                                edgecolor='green', facecolor='green')
                            else:
                                axs[i, j].arrow(0, 0,
                                                self.mgai_idx[0][i][j][0] ,
                                                self.mgdi_idx[0][i][j][0] , width=0.075, zorder=50,
                                                alpha=0.99,
                                                edgecolor='orange', facecolor='orange')

                    else:
                        axs[i, j].set_visible(False)
        if ref_comp_caption == "":
            plt.savefig(self.graph_type + "_ADPlotGrandMeanBoxes.png")
        else:
            plt.savefig(self.graph_type + "_ADPlotGrandMeanBoxes" +  "_" + self.graph_name+ "_vs_" + ref_comp_caption + ".png")
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

def on_pick(event):
    ax = event.artist.axes
    if (refno % 2) == 0:
        fixit = (int(refno / 2)) - 1
    else:
        fixit = (int(refno / 2))

    print_selected_line(int(ax.lines.index(event.artist) / 2)-((refno * 2) + fixit))

def print_selected_line(lineno):
    logging.info("selected line: " + str(lineno))

