import os
import pickle


def getfileparams(filename, lineno):
    # If Connection File Exists read Database name
    file_param = ''
    if os.path.isfile(filename):
        f = open(filename, "r")
        if f.mode == 'r':
            fl = f.readlines()
            file_param = fl[lineno].rstrip("\n")
        else:
            print ("Cannot find File Params")
    return(file_param)


def getfilterdata():
    ImportFilter = []
    if os.path.isfile("ReImport.ini"):
        f = open("ReImport.ini", "r")
        if f.mode == 'r':
            fl = f.readlines()
            for x in fl:
                fields = x.split('|')
                ImportLine = []
                ImportLine.append(fields[0].rstrip("\n"))
                ImportLine.append(fields[1].rstrip("\n"))
                ImportLine.append(fields[2].rstrip("\n"))
                ImportLine.append(fields[3].rstrip("\n"))
                ImportFilter.append(ImportLine)
    return ImportFilter



def savedata(savefolder, savename, savedata):

    if not os.path.exists(savefolder):
        os.makedirs(savefolder)

    savefile = open(savefolder + "\\" + savename, 'wb')
    pickle.dump(savedata, savefile)
    savefile.close


def getdata(getfolder, getname):

    if not os.path.exists(getfolder):
        getdata = False
        return getdata

    if not os.path.isfile(getfolder + "\\"  + getname):
        getdata = False
        return getdata

    infile = open(getfolder + "\\" +  getname, 'rb')
    loadeddata = pickle.load(infile)
    infile.close
    return loadeddata


