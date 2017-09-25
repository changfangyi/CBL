#!/usr/bin/env python

import os
import pandas as pd
import xlrd
import argparse

# parameter
FILE_NAME= None
SHEET_NAME = None


def main():
    parse_args()
    print ("Loading...")
    file_name = os.path.join('data',FILE_NAME+'.xlsx')
    load_group(file_name)

# Argument parser
def parse_args():

    global FILE_NAME, SHEET_NAME

    parser = argparse.ArgumentParser()
    required_named_arguments = parser.add_argument_group('required named arguments')
    required_named_arguments.add_argument('-d', '--filename',
                                          help='file\'s name. For example, \'3_commerical\'.',
                                          required=True)
    required_named_arguments.add_argument('-s', '--sheetname',
                                          help='sheet\'s name. For example, \'0,1,2,..\'.',
                                          type=int,
                                          required=True)
    args = parser.parse_args()
    FILE_NAME = args.filename
    SHEET_NAME = args.sheetname


# load and group data 
def load_group(file_name):
    
    if SHEET_NAME==0:
        df=pd.read_excel(file_name, sheetname=SHEET_NAME, parse_cols=[1,2,3])
    else:
        df=pd.read_excel(file_name, sheetname=SHEET_NAME)

    for item in df.groupby(['deviceid']).groups:
        print item 
        temp = df.groupby(['deviceid']).get_group(item)
        # rename and save
        name=rename(item)
        print 'Saving ' + name + '...'
        save_file=os.path.join('data',name+'.csv')
        print save_file
        temp.to_csv(save_file)

# rename
def rename(item):
    
    if item == 'II12IIMSN-0059010201|01':
        rename = 'Sun_Whole_201'

    if item == 'II12IIMSN-0059010201|03':
        rename = 'Sun_Split_Type'

    if item == 'II12IIMSN-0122010102|03':
        rename = 'Hua_Whole_Light'

    if item == 'II12IIMSN-0059010301|04':
        rename = 'Sun_Four_Door_Fridge'

    if item == 'II12IIMSN-0059010301|03':
        rename = 'Sun_Double_Door_Fridge'

    if item == 'II12IIMSN-0122010101|01':
        rename = 'Hua_Whole_101'

    if item == 'BN11000D6F000AA54E24|00':
        rename = 'Sun_Whole_AC'

    if item == 'II12IIMSN-0122010101|03':
        rename = 'Hua_Cool_Water'

    if item == 'II12IIMSN-0122010101|04':
        rename = 'Hua_Cool_Tower'
    
    if item ==  'II09000D6F0003BB92C7':
        rename = 'Wang_Bedroom_AC'

    if item == 'II09000D6F0005A5DE25':
        rename = 'Wang_Major_Bedroom_AC_1'
    
    if item == 'II09000D6F0005A5CA59':
        rename = 'Wang_Dining_AC'
    
    if item == 'II09000D6F0003BB9B0D':
        rename = 'Wang_Whole_right'

    if item == 'II09000D6F0005A5E017':
        rename = 'Wang_Whole_left'

    if item == 'II09000D6F0005A5D494':
        rename = 'Wang_Major_Bedroom_AC_2'
    return rename
        
        
if __name__ == '__main__':
    main()
