import csv 
import json
import pandas as pd
import sys
sys.path


def read():
    # f = open('read.csv', 'r')
    # csv_f = csv.reader(f)
    

    # for row in csv_f:
    #     #print(row[0])
    #     if row[0] == 'physics':
    #         print(row)
    #         print("made it")
    # f.close()

    #sched = pd.DataFrame([['english'], ['M'], ['2'], ['3']])
    # sched = pd.DataFrame('english', 'M', '2', '3')
    # sched.to_csv('data.csv', mode = 'a', header=False, index=False)

    # with open('data.csv') as csvfile:
    #     csv_reader = csv.reader(csvfile)
    #     for row in csv_reader:
    #         print(row)
            
    #     print(row[0])

    data = pd.read_csv('data.csv')

    # read row line by line
    for d in data.values:
    # read column by index
        print(d[2])














    # for i in range(len(data)):
    #     data[i] = data[i].strip()
    
    # #print(data)
    # for i in range(len(data)):
    #     row = data[i]
    #     items = row.split(',')
    #     subject = items[0]
    #     days = items[1]
    #     start = items[2]
    #     end = items[3]

    # for row in data:
    #     print(row[0])
    #print(row)
    # print(items)
    # print(data)
    #print(subject)
    # print(days)
    # print(start)
    # print(end)

read()

def write():
    subject = 'math'
    days = 'M'
    start = '2'
    end = '4'
    f = open('read.csv', 'a')
    f.writelines(['\n', subject + ',' + days + ',' + start + ',' + end])
    f.close()

#write()