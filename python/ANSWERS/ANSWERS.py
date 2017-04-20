from numpy import *
from STTrendAnalysis import STTrendAnalysis
import csv

def ANSWERS(vf, time):
    if size(vf, 1) == 54:
        vf = delete(vf, 25, axis=1)
        vf = delete(vf, 33, axis=1)
    vf = vf + 1
    #load weibull_mixture_para_1offset.mat
    csv_reader = csv.reader(open('distPara_array.csv', encoding='utf-8'))
    csv_array = []
    for row in csv_reader:
        csv_array.append(list(map(float, row)))
    distPara_array = array(csv_array)
    csv_reader = csv.reader(open('pi_array.csv', encoding='utf-8'))
    csv_pi_array = []
    for row in csv_reader:
        csv_pi_array.append(list(map(float, row)))
    pi_array = array(csv_pi_array)
    [S, pnd, slope] = STTrendAnalysis(vf.T, time, distPara_array, pi_array, -0.0, 1.0, 1)
    pnd = pnd.T
    slope = slope.T
    return S,pnd,slope
