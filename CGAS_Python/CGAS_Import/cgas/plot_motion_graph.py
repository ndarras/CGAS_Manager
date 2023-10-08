import numpy as np
import pandas
from matplotlib import pyplot as plt

def plot_example(plotlevels, plotplanes, localdir, reference):
    ref_names_df = pandas.read_csv(localdir + '_REFERENCES\\' + reference +'\\ReferenceNames.ini', sep=', ', engine='python')
    excel_data_df = pandas.read_excel(localdir + '_REFERENCES\\' + reference + '\\' + reference + '.xlsx', sheet_name=reference )
    fig, axs = plt.subplots(plotlevels, plotplanes)
    axs[0, 0].fill_between(excel_data_df['Pcnt'],  excel_data_df['Pelvic Tilt Mean']-excel_data_df['Pelvic Tilt SD'] , excel_data_df['Pelvic Tilt Mean']+excel_data_df['Pelvic Tilt SD'], color='gray', alpha=0.2)
    axs[0 ,0].set_ylim(25, 50)
    axs[0 ,0].set_xlim(0, 100)
    axs[0, 1].fill_between(excel_data_df['Pcnt'],  excel_data_df['Pelvic Obliquity Mean']-excel_data_df['Pelvic Obliquity SD'] , excel_data_df['Pelvic Obliquity Mean']+excel_data_df['Pelvic Obliquity SD'], color='gray', alpha=0.2)
    axs[0, 1].set_ylim(-30, 30)
    axs[0, 1].set_xlim(0, 100)
    axs[0, 2].fill_between(excel_data_df['Pcnt'],  excel_data_df['Pelvic Rotation Mean']-excel_data_df['Pelvic Rotation SD'] , excel_data_df['Pelvic Rotation Mean']+excel_data_df['Pelvic Rotation SD'], color='gray', alpha=0.2)
    axs[0, 2].set_ylim(-30, 30)
    axs[0, 2].set_xlim(0, 100)
    axs[1, 0].fill_between(excel_data_df['Pcnt'],  excel_data_df['Hip Flex-Ext Mean']-excel_data_df['Hip Flex-Ext SD'] , excel_data_df['Hip Flex-Ext Mean']+excel_data_df['Hip Flex-Ext SD'], color='gray', alpha=0.2)
    axs[1, 0].set_ylim(-20, 80)
    axs[1, 0].set_xlim(0, 100)
    axs[1, 1].fill_between(excel_data_df['Pcnt'],  excel_data_df['Hip Add-Abd Mean']-excel_data_df['Hip Add-Abd SD'] , excel_data_df['Hip Add-Abd Mean']+excel_data_df['Hip Add-Abd SD'], color='gray', alpha=0.2)
    axs[1, 1].set_ylim(-30, 30)
    axs[1, 1].set_xlim(0, 100)
    axs[1, 2].fill_between(excel_data_df['Pcnt'],  excel_data_df['Hip Rotation Mean']-excel_data_df['Hip Rotation SD'] , excel_data_df['Hip Rotation Mean']+excel_data_df['Hip Rotation SD'], color='gray', alpha=0.2)
    axs[1, 2].set_ylim(-30, 30)
    axs[1, 2].set_xlim(0, 100)
    axs[2, 0].fill_between(excel_data_df['Pcnt'],  excel_data_df['Knee Flex-Ext Mean']-excel_data_df['Knee Flex-Ext SD'] , excel_data_df['Knee Flex-Ext Mean']+excel_data_df['Knee Flex-Ext SD'], color='gray', alpha=0.2)
    axs[2, 1].fill_between(excel_data_df['Pcnt'],  excel_data_df['Knee Valg-Var Mean']-excel_data_df['Knee Valg-Var SD'] , excel_data_df['Knee Valg-Var Mean']+excel_data_df['Knee Valg-Var SD'], color='gray', alpha=0.2)
    axs[2, 2].fill_between(excel_data_df['Pcnt'],  excel_data_df['Knee Rotation Mean']-excel_data_df['Knee Rotation SD'] , excel_data_df['Knee Rotation Mean']+excel_data_df['Knee Rotation SD'], color='gray', alpha=0.2)
    axs[3, 0].fill_between(excel_data_df['Pcnt'],  excel_data_df['Ankle Flex-Ext Mean']-excel_data_df['Ankle Flex-Ext SD'] , excel_data_df['Ankle Flex-Ext Mean']+excel_data_df['Ankle Flex-Ext SD'], color='gray', alpha=0.2)
   # axs[3, 1].fill_between(excel_data_df['Pcnt'],  excel_data_df['Ankle Valg-Var Mean']-excel_data_df['Ankle Valg-Var SD'] , excel_data_df['Ankle Valg-Var Mean']+excel_data_df['Ankle Valg-Var SD'], color='gray', alpha=0.2)
   # axs[3, 2].fill_between(excel_data_df['Pcnt'],  excel_data_df['Ankle Rotation Mean']-excel_data_df['Ankle Rotation SD'] , excel_data_df['Ankle Rotation Mean']+excel_data_df['Ankle Rotation SD'], color='gray', alpha=0.2)
   # axs[4, 2].fill_between(excel_data_df['Pcnt'],  excel_data_df['Foot Progression Int-Ext Mean']-excel_data_df['Foot Progression Int-Ext SD'] , excel_data_df['Foot Progression Int-Ext Mean']+excel_data_df['Foot Progression Int-Ext SD'], color='gray', alpha=0.2)
    plt.xlim(0, 100);
    plt.plot
    plt.show()

def get_ref_name(ref_names_df, graphlabel, plane):
    try:
        query_str = "GraphLabel ==  '" + graphlabel + "' & GraphPlane == " + str(plane)
        ref_name = ref_names_df.query(query_str)
        retval = ""
        retval = ref_name.GraphName.item()
        return retval

    except ValueError:
        retval = ""
        return retval
