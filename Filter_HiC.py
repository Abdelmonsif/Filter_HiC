
import os,sys,argparse
import pandas as pd
import time
from os import listdir
import numpy as np
import matplotlib.pyplot as plt


def filter_HiC(inputFile, outputFile, res):
    enh_pro = pd.read_csv(inputFile, delim_whitespace=True)
    enh_pro['chunk'] = (enh_pro['chr_pos'] / res).astype(int)
    enh_pro['chunk1_start'] = enh_pro['chunk'] * res
    enh_pro['chunk1_end'] = enh_pro['chunk1_start'] + res
    enh_pro['snp_mid_range'] = ((enh_pro['chunk1_start'] + enh_pro['chunk1_end']) / 2).astype(int)
    enh_pro['other_mid_range'] = ((enh_pro['chunk_start'] + enh_pro['chunk_end']) / 2).astype(int)
    enh_pro['distance'] = enh_pro['other_mid_range'] - enh_pro['snp_mid_range']
    enh_pro['distance'] = enh_pro['distance'].abs()
    list1 = enh_pro['Uploaded_variation'].unique()
    final = pd.DataFrame()
    for i in list1:
        df = enh_pro[enh_pro['Uploaded_variation'] == i]
        df = df.sort_values(by='neglogq-value')
        df = df.loc[df['neglogq-value'] == df['neglogq-value'].max()]
        maxDifference = 0
        df1 = df[df['distance'] == df['distance'].max()]
        final = final.append(df1, ignore_index=True)
    final.to_csv(outputFile, sep='\t', index=False)
    
    
 def getArgs():
    parser = argparse.ArgumentParser('python')
    parser.add_argument('-inputFile', required=True)
    parser.add_argument('-outputFile', required=True)
    parser.add_argument('-res', required=True)
    return parser.parse_args()

if __name__ == "__main__":
    args = getArgs()
    start = time.time()
    filename = nt_comp(args.inputFile, args.outputFile, args.res)
    end = time.time()
    print ('time elapsed:' + str(end - start))   
   
