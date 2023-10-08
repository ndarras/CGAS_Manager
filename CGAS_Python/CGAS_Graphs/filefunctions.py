import os
import pickle
import logging

def getselectedgroups():
    selectedGroups = []
    groupColours = []
    if os.path.isfile("PlotGroups.ini"):
        f = open("PlotGroups.ini", "r")
        if f.mode == 'r':
            fl = f.readlines()

            for x in fl:
                prepgroup = []
                prepcolour = []
                co = ''
                fields = x.split(',')
                prepgroup.append(fields[0])
                selectedGroups.append(prepgroup[0])
                co = fields[1].strip('\n')
                co = co.strip('"')
                prepcolour.append(co.strip("'\n'"))
                groupColours.append(prepcolour[0])
    return selectedGroups, groupColours

def getselectedc3ds():
    selectedC3Ds = []
    linecolours = []
    if os.path.isfile("PlotGraphs.ini"):
        f = open("PlotGraphs.ini", "r")
        if f.mode == 'r':
            fl = f.readlines()

            for x in fl:
                preprow = []
                prepcolourrow = []
                co = ''
                fields = x.split(',')
                preprow.append(fields[0].strip('"'))
                preprow.append(fields[1].strip('"'))
                co = fields[2].strip('\n')
                co = co.strip('"')
                preprow.append(co.strip("'\n'"))
                selectedC3Ds.append(preprow)

                co = fields[3].strip('\n')
                co = co.strip('"')
                prepcolourrow.append(co.strip("'\n'"))
                linecolours.append(prepcolourrow)

    return selectedC3Ds, linecolours


def getgraphparams(lineno):
    # If Connection File Exists read Database name
    graph_param = ''
    if os.path.isfile("PlotParams.ini"):
        f = open("PlotParams.ini", "r")
        if f.mode == 'r':
            fl = f.readlines()
            graph_param = fl[lineno].rstrip("\n")
        else:
            logging.info("Cannot find PlotParams")
    return(graph_param)


def getfileparams(filename, lineno):
    # If Connection File Exists read Database name
    file_param = ''
    if os.path.isfile(filename):
        f = open(filename, "r")
        if f.mode == 'r':
            fl = f.readlines()
            file_param = fl[lineno].rstrip("\n")
        else:
            logging.info("Cannot find File Params")
    return(file_param)


def getgraphlist():
    graphList = []
    if os.path.isfile("PlotGraphList.ini"):
        f = open("PlotGraphList.ini", "r")
        if f.mode == 'r':
            fl = f.readlines()
            for x in fl:
                fields = x.split('|')
                graphList.append(fields[0].rstrip("\n"))
    return graphList

def getgraphprefs(graphname):
    graphprefs = []
    if os.path.isfile("PlotGraphList.ini"):
        f = open("PlotGraphList.ini", "r")
        if f.mode == 'r':
            fl = f.readlines()
            for x in fl:
                fields = x.split('|')
                if fields[0].rstrip("\n") == graphname:
                    graphprefs.append(float(fields[1].rstrip("\n")))
                    graphprefs.append(float(fields[2].rstrip("\n")))
    return graphprefs



def savedata(savefolder, savename, savedata):

    if not os.path.exists(savefolder):
        os.makedirs(savefolder)

    savefile = open(savefolder + "\\" + savename, 'wb')
    pickle.dump(savedata, savefile)
    savefile.close


def getdata( getfolder, getname):

    if not os.path.exists(getfolder):
        getdata = False
        return getdata

    if not os.path.isfile(getfolder + "\\"  + getname):
        getdata = False
        return getdata

    infile = open(getfolder + "\\" + getname, 'rb')
    loadeddata = pickle.load(infile)
    infile.close
    return loadeddata


