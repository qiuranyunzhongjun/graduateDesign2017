import csv
from numpy import *
from ANSWERS import ANSWERS

csv_reader = csv.reader(open('repeat_30patient_function_data.csv', encoding='utf-8'))
data30_array = []
for row in csv_reader:
    data30_array.append(list(map(float, row)))
func_data = array(data30_array)
time = array([0,0,2,3,4,7])*30/365
visual =func_data[0:6,2:56]
[s,pnd,slope]=ANSWERS(visual,time)
print("s = %f\n" %s)
print(shape(pnd))
print(pnd)
print(shape(slope))
print(slope)