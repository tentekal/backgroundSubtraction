# Kyle Sullivan and Tanner Fink
# 3-24-2017

import pandas as pd
import numpy as np
import math 
import backSubWindow


def load(name):
    # load in a Excel workbook here, along with a specific sheet within the workbook
    spreadsheet = pd.read_excel(name, header=None)
    df = pd.DataFrame(data=spreadsheet)
    #print(df.head())
    return df


# takes in a DataFrame object and spits out another DataFrame containing a partition of the input and transposed
# modified to allow the ability to select other channels when calling func

def oneSignal(df, channel, selection2):
    # extracts every -selection2- rows starting from row 'channel' and compiles them into a new DataFrame called partition
    # program assumes 2 rows of "header" space at the top of excel file, as is typical in results from imageJ macros 
    partition = df.iloc[channel::selection2]
    transposed = partition.transpose()
    # removes zeroes from transposed and turns them into nan
    noNan = transposed[transposed != 0.0]
    return noNan
    

def insertColumns(name, selection):
    originalData = load(name)

    Channel1 = oneSignal(originalData, selection[0])
    Channel2 = oneSignal(originalData, selection[1])

    
    """Uncomment these in order to export the channel to an excel sheet (name them whatever you want)"""
    #Channel1.to_excel('channel1.xlsx')
    #Channel2.to_excel('channel2.xlsx')
    #Channel3.to_excel('channel3.xlsx')
    #Channel4.to_excel('channel4.xlsx')
    
    """This section is for generating a side-by-side excel sheet of two channels (i.e. ready for Prism)"""
    """Replace Channel1 and Channel2 with the Channels you're interested in comapring"""
    sidebySide = pd.concat([Channel1, Channel2], axis=1, keys=[1, 2]).stack(0)[Channel1.columns].unstack()
    sidebySide = pd.concat([Channel1, Channel2], axis=1).sort_index(axis=1)
    sidebySide.to_excel('sidebysidechannels.xlsx')
    return sidebySide
    

    """This function takes the last ROI value of whatever channel and subtracts it from all values prior"""
def backSub(name, selection, selection2):
    print('running backsub on' + name)
    originalData = load(name)
    oneChannel = oneSignal(originalData, selection[0], selection2[0])
    print('pass 0')
    #oneChannel2 = oneSignal(originalData, 3)
    if len(selection) == 1:
        print('only one selected, ommitting insertColumns()')
    else:
        oneChannel = insertColumns(name, selection)
    print('pass 1')
    # access number of rows and columns for transposed data
    allDims = oneChannel.shape
    numRows = allDims[0]
    numCols = allDims[1]
    # create an array to store background values
    backgroundVals = np.zeros(numCols)
    print('pass 2')
    # need a separate loop count, since col is iterating based on DataFrame of extracted channels, skipping 4 (3,7,11, etc)
    loopCount = 0
    for col in oneChannel:
        nonNaN = oneChannel[col].dropna()
        lastinCol = nonNaN.iloc[-1]
        backgroundVals[loopCount] = lastinCol
        loopCount += 1
    # this is how you index the top left cell only
    # test = oneChannel.iloc[0:1,0:1]

    # use iat [i,j] to access the actual values; iloc only gathers range
    # start at row 1 to avoid strings(header) in DataFrame
    print('pass 3')
    for j in range(0,numCols):
        for i in range(1, numRows):
            temp = oneChannel.iat[i,j]
            if temp != 0.0:
                oneChannel.iat[i,j] = oneChannel.iat[i,j] - backgroundVals[j]
            else:
                print ("failed")
    # remove all zeroes and turn them into nan
    finalTable = oneChannel[oneChannel != 0.0]
    finalTable.to_excel('background_subtracted.xlsx')
    print('exporting final table')
    
    
    
"""Segment for Quantile Range calculation"""


def get_lower_half(lst):
    mid_idx = math.floor(lst.count() / 2)    
    return(lst[0:mid_idx])


def get_upper_half(lst):
    mid_idx = math.ceil(lst.count() / 2)
    return(lst[mid_idx:])

def interQuartile(file):
    spreadsheet = pd.read_excel(file, header=None)
    df = pd.DataFrame(data=spreadsheet)
    partition2 = df.iloc[3:]

    ascending_df = pd.DataFrame({x: partition2[x].sort_values().values for x in partition2.columns.values})
    
    ascending_df.to_excel('iqr_ascending_order.xlsx')

    for col in ascending_df:
        Q1 = (get_lower_half(ascending_df[col])).median()
        Q3 = (get_upper_half(ascending_df[col])).median()
        IQR = Q3-Q1
        print(IQR)

 
    
