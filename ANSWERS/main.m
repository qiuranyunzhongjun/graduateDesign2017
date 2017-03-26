load repeat_30patient_function_data;
time = [0,0,2,2,4,7].*30/365;
visual =func_data(1:6,3:56);
[s,pnd,slope]=ANSWERS(visual,time);
