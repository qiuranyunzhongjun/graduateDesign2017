import csv
from numpy import *
from ANSWERS import ANSWERS

csv_reader = csv.reader(open('repeat_30patient_function_data.csv', encoding='utf-8'))
data30_array = []
for row in csv_reader:
    data30_array.append(list(map(float, row)))
func_data = array(data30_array)
time = [0,0,2,2,4,7]*30/365
visual =func_data[1:6,3:56]
[s,pnd,slope]=ANSWERS(visual,time)
print("s = %f\n" %s)
print("pnd = %f\n" %pnd)
print("slope = %f\n" %slope)