#!/usr/bin/env python
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import argparse

# parameter
FILE_PATH = None
TARGET = None
METHOD = None

WINDOW_AUG={
    'working day': {
       1:('2017-08-10','2017-08-12'),
       2:('2017-08-14','2017-08-18'),
       3:('2017-08-21','2017-08-25'),
       4:('2017-08-29','2017-08-31'),
    },

    'weekend': {
       1:('2017-08-12','2017-08-13'),
       2:('2017-08-19','2017-08-20'),
       3:('2017-08-26','2017-08-27'),
    }
}

# temperature approx. working: 30 C, weekend : 30 C (the lowest one)
WINDOW_AUG_filter={
    'working day': {
       1:('2017-08-16','2017-08-18'),
       2:('2017-08-21','2017-08-25'),
       3:('2017-08-28','2017-08-30'),
    },

    'weekend': {
       1:('2017-08-12','2017-08-13'), # Aug : 31.37 Celsius
       2:('2017-08-19','2017-08-20'),
       3:('2017-08-26','2017-08-27'),
    }
}

WINDOW_SEP_filter={
    'working day': {
       1:('2017-09-05','2017-09-07'),
       2:('2017-09-11','2017-09-12'),
       3:('2017-09-20','2017-09-22'),
    },

    'weekend': {
       1:('2017-09-23','2017-09-24'), # SEP : 31.75 Celsius
    }
}
# temperature approx. working: 30 C, weekend : 27 C
WINDOW_SEP={
    'working day': {
       1:('2017-09-01','2017-09-02'),
       2:('2017-09-05','2017-09-09'),
       3:('2017-09-11','2017-09-15'),
       4:('2017-09-18','2017-09-22'),
       5:('2017-09-25','2017-09-29'),
    },

    'weekend': {
       1:('2017-09-03','2017-09-04'),
       2:('2017-09-09','2017-09-10'),
       3:('2017-09-16','2017-09-17'),
       4:('2017-09-23','2017-09-24')
    }
}

WINDOWS = { 'AUG': WINDOW_AUG,
            'SEP': WINDOW_SEP
}

def main():
    print '***********************************************************************\n'
    print '**************************** start ************************************\n'
    print '***********************************************************************\n'
    parse_args()
    print TARGET + '..........\n'
    df = load(FILE_PATH)
    Work_AUG, Weekend_AUG = Work_or_Weekend(df, WINDOW_AUG)
    Work_SEP, Weekend_SEP = Work_or_Weekend(df, WINDOW_SEP)
    Work_AUG = Hour_Index(Work_AUG)
    Weekend_AUG = Hour_Index(Weekend_AUG)
    Work_SEP = Hour_Index(Work_SEP)
    Weekend_SEP = Hour_Index(Weekend_SEP)

    if not os.path.isdir(os.path.join('plt',TARGET)):
        print "Creating dirs..."
        os.makedirs(os.path.join('plt',TARGET))


    print "Ploting for the pooling data..."
    Plot_Comparison(Work_AUG, Work_SEP, METHOD+'_Comparison_Work')
    Plot_Comparison(Weekend_AUG, Weekend_SEP, METHOD+'_Comparison_Weekend')
    Plot_diff(Work_AUG,Work_SEP, METHOD+'_difference_Work')
    Plot_diff(Weekend_AUG, Weekend_SEP, METHOD+'_difference_Weekend')

    print "Ploting for the filter data..."
    Work_AUG_filter, Weekend_AUG_filter = Work_or_Weekend(df, WINDOW_AUG_filter)
    Work_SEP_filter, Weekend_SEP_filter = Work_or_Weekend(df, WINDOW_SEP_filter)
    Work_AUG_filter = Hour_Index(Work_AUG_filter)
    Weekend_AUG_filter = Hour_Index(Weekend_AUG_filter)
    Work_SEP_filter = Hour_Index(Work_SEP_filter)
    Weekend_SEP_filter = Hour_Index(Weekend_SEP_filter)

    Plot_Comparison(Work_AUG_filter, Work_SEP_filter, METHOD+'_Comparison_Work_filter')
    Plot_Comparison(Weekend_AUG_filter, Weekend_SEP_filter, METHOD+'_Comparison_Weekend_filter')
    Plot_diff(Work_AUG_filter, Work_SEP_filter, METHOD+'_difference_Work_filter')
    Plot_diff(Weekend_AUG_filter, Weekend_SEP_filter, METHOD+'_difference_Weekend_filter')


    print "Ploting for weekly data...."
    for item, window in WINDOW_SEP['working day'].iteritems():
        start = window[0]
        end = window[-1]
        temp = df[start:end]
        temp = Hour_Index(temp)
        Plot_Comparison(Work_AUG, temp, METHOD+'_Comparison_Work_'+str(item))
        Plot_diff(Work_AUG,temp, METHOD+'_difference_Work_'+str(item))

    for item, window in WINDOW_SEP['weekend'].iteritems():
        start = window[0]
        end = window[-1]
        temp = df[start:end]
        temp = Hour_Index(temp)
        Plot_Comparison(Weekend_AUG, temp, METHOD+'_Comparison_Weekend_'+str(item))
        Plot_diff(Weekend_AUG,temp, METHOD+'_difference_Weekend_'+str(item))

    print '***********************************************************************\n'
    print '**************************** All Done *********************************\n'
    print '***********************************************************************\n'
 
# Argument parser
def parse_args():
    global FILE_PATH, TARGET, METHOD
    parser = argparse.ArgumentParser()
    required_named_arguments = parser.add_argument_group('required named arguments')
    required_named_arguments.add_argument('-d', '--filename',
                                          help='file\'s name. For example, \'Whole_light\'.',
                                          required=True)
    required_named_arguments.add_argument('-m', '--method',
                                          help='method\'s name. sum or mean',
                                          required=True)
    args = parser.parse_args()
    TARGET = args.filename
    FILE_PATH = os.path.join('data', TARGET +'.csv')
    METHOD = args.method

# load and nan.drop data
def load(file_path):  
    df=pd.read_csv(file_path)
    df.drop_duplicates
    index = pd.to_datetime(df['reporttime'].str[:-7])
    df = df['w']
    df.index = index
    if METHOD == 'sum':
        df = df.resample('60T').sum()
    if METHOD == 'mean':
        df = df.resample('60T').mean()
    df = df.fillna(0)
    return df

# split into week and weekend
def Work_or_Weekend(df, windows):  
    Work = pd.Series()
    Weekend = pd.Series()
    for work_or_weekend, time_intervals in windows.iteritems():
        #print 'Processing '+ work_or_weekend + '...\n'
        for __ ,interval in time_intervals.iteritems():               
            start = interval[0]
            end = interval[-1]
            #print 'start time is '+ start+'\n', 'end time is '+ end +'\n'
            temp=df[start:end]
            if work_or_weekend == 'working day':
                Work = Work.append(temp)
            if work_or_weekend == 'weekend':
                Weekend = Weekend.append(temp)
    print ' Work_or_Weekend Done !\n'
    return Work, Weekend

# reindex into hour-based
def Hour_Index(Work_or_Weekend):
    toPlot = pd.DataFrame(np.zeros(24))
    if Work_or_Weekend.empty:
        Work_or_Weekend.empty
    else:
        hour_Index =  Work_or_Weekend
        hour_Index.index = Work_or_Weekend.index.hour
        for i in range(23):
            if METHOD == 'sum':
                temp = hour_Index[i].sum()
                toPlot.iloc[i,0] = temp
            if METHOD == 'mean':  
                temp = hour_Index[i].mean()
                toPlot.iloc[i,0] = temp
    return toPlot

# Plot 
def Plot(toPlot, label):
    fig, axs = plt.subplots(1,1)
    axs.set_title(label)
    axs.plot(toPlot, 'bo-', linewidth=2.0)
    axs.grid()
    axs.set_xticks(range(24))
    axs.set_xlabel('Hour')
    axs.set_ylabel('Average W')
    plt.savefig(os.path.join('plt', TARGET, label))
    plt.clf()

# Plot_diff
def Plot_diff(toPlot_Aug, toPlot_Sep, label):
    toPlot = toPlot_Aug - toPlot_Sep

    fig, axs = plt.subplots(1,1)
    axs.set_title(label)
    axs.plot(toPlot, 'bo-', linewidth=2.0)
    axs.axhline(0, color='red', lw=2)
    axs.grid()
    axs.set_xticks(range(24))
    axs.set_xlabel('Hour')
    axs.set_ylabel('Average W')
    plt.savefig(os.path.join('plt', TARGET, label))
    plt.clf()

# Plot Comparison
def Plot_Comparison(window_aug, window_sep, kind):
    line1, = plt.plot(window_aug, 'bo-', label='AUG')
    line2, = plt.plot(window_sep,'ro-', label='SEP')
    plt.legend([line1,line2],['AUG','SEP'])
    plt.title(kind + '_' +TARGET)  
    plt.grid(True)
    plt.xticks(range(24))
    plt.xlabel('Hour')
    plt.ylabel('Average W')
    plt.savefig(os.path.join('plt', TARGET, kind))
    plt.clf() 

if __name__ == '__main__':
    main()