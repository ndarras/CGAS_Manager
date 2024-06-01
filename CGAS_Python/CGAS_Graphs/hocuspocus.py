import os
import sys
import logging
import filefunctions as ff
from graphs import motiongraph as mg
from graphs import angletoangle as a2a
from graphs import adplot as ad
from graphs import gps
from graphs import arom as ar
from graphs import tsbars as ts

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    working_dir = sys.argv[1].replace("\\","//")

# Change to Local Directory
os.chdir(working_dir)

# os.remove("errors.log")
logging.basicConfig(filename='hocuspocus.log', level=logging.INFO)
logging.info("Setting Working Directory to: " + working_dir)

# Register the Local Directory
localdir = os.path.dirname(os.path.realpath(__file__))
logging.info("Local Directory is: " + localdir)

#Get Graph Type
Graph_Type = ff.getgraphparams(2)
Graph_Name = ff.getgraphparams(3)
Graph_List = ff.getgraphlist()

all_graphs = 1
for g in range(len(Graph_List)):
    if Graph_List[g][0] == " ":
        all_graphs = 0
        break

logging.info(Graph_Type)
logging.info(Graph_Name)
logging.info(Graph_List)

if 'Motion Analysis Graphs' in Graph_List:
    a = mg.GaitGraph(Graph_Type, Graph_Name, all_graphs)
    a.plotgraphs()

if 'Temporospatial' in Graph_List:
    a = ts.tsBarsData(Graph_Type, Graph_Name, all_graphs)
    a.plottsbars()

if 'AverageTemporospatial' in Graph_List:
    a = ts.tsBarsData(Graph_Type, Graph_Name, all_graphs)
    a.plotavgtsbars()

if 'Angle to Angle' in Graph_List:
    a = a2a.atoa(Graph_Type, Graph_Name, all_graphs)
    a.plotatoa()

try:
    #ADPlot Graph
    b = ad.ADplotData(Graph_Type, Graph_Name, all_graphs)
    b.all_graphs = all_graphs
except:
    logging.info("ADPlot data cannot be initialised")

if 'Motion Analysis Graphs + Indexes' in Graph_List:
    b.plotgraphsplusindexes()

if 'Deviation Graphs' in Graph_List:
    b.plotdeviationgraphs()

if 'Z Score Deviation Graphs' in Graph_List:
    b.plotzscoredeviationgraphs()

if 'Asymmetry Graphs' in Graph_List:
    b.plotasymmetrygraphs()

if 'Z Score Asymmetry Graphs' in Graph_List:
    b.plotzscoreasymmetrygraphs()

if 'ADPlot Graphs' in Graph_List:
    b.adplot_graphs()

if 'ADPlot Global Graph' in Graph_List:
    b.adplot_global_graph()

if 'ADPlot Triplane Graphs' in Graph_List:
    b.adplot_triplane_graphs()

if 'ADPlot Perplane Graphs' in Graph_List:
    b.adplot_perplane_graphs()

if 'ADPlot Boxes' in Graph_List:
    b.adplot_boxes()

if 'ADPlot Grand Mean Boxes' in Graph_List:
    b.adplot_grand_mean_boxes()

c = gps.GPSData(Graph_Type, Graph_Name, all_graphs)
if 'MAP and GVS' in Graph_List:
    c.map_bars()

try:
    d = ar.AROMData(Graph_Type, Graph_Name, all_graphs)
    d.calcromdata()
except:
    logging.info("ARom data cannot be initialised")

if 'Range Of Motion' in Graph_List:
    d.plotrom()

if 'Average Range Of Motion' in Graph_List:
    d.plotavgrom()