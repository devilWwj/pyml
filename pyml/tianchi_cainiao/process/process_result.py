#coding:utf8
import os
import traceback
import pdb

with open('d:/tianchi/result_last_two_week-adj.csv', 'r') as file:
    lines = file.readlines()

store = 0.0
all = 0.0

try:
    for line in lines:
        resut = line.split(',')
        if resut[1] == 'all':
            if resut[2].strip() != 'None':
                all += float(resut[2])
        else:
            if resut[2].strip() != 'None':
                store += float(resut[2])
except:
    pdb.set_trace()
    traceback.print_exc()

print 'store:', str(store)
print 'all', str(all)
