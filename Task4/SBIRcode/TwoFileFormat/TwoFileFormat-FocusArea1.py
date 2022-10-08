####This file can deal: 22-17

import os
import pandas as pd
import csv
import json

def SingleFileProcess(path):
    df = pd.read_csv(path, sep=',')

def file1Process(df):
    # print(df['Focus Area'])
    totaldata = []
    for i in range(len(df['Focus Area'])):
        data = []
        data.append(df['Higher Topic'][i])
        components = df['Focus Area'][i].split()
        #print(components)
        num = components[0] + " " + components[1] + " " + components[2]
        data.append(num)
        name = df['Focus Area'][i].replace(num + " ", "")
        # print(i, name)
        data.append(name)
        data.append(df['Content'][i])
        # print(i, data)
        totaldata.append(data)
    df1 = pd.DataFrame(totaldata, columns=['Higher Topic','Focus Area Code', 'Focus Area name', 'Content'])
    #print(df1)
    return df1

def file2Process(df):
    totaldata = []
    for i in range(len(df['Focus Area'])):
        data = []
        components = df['Focus Area'][i].split()
        # print(components)
        num = components[0] + " " + components[1] + " " + components[2]
        data.append(num)

        data.append(df['Subtopics_encoding'][i])
        data.append(df['Subtopics_name'][i])
        # print(i, data)
        totaldata.append(data)
    df2 = pd.DataFrame(totaldata, columns=['Focus Area Code', 'Subtopic code', 'Subtopic name'])
    #print(df2)
    return df2

def to_CSV(df):
    df.to_csv('Result.csv', index=False)

if __name__ == '__main__':
    filename="2017.csv"

    path="Complete/Task4-SBIR/"+filename

    df = pd.read_csv(path, sep=',')

    df1=file1Process(df.copy())
    df1.to_csv('FinalResult/1/'+filename, index=False)

    df2=file2Process(df.copy())
    df2.to_csv('FinalResult/2/'+filename, index=False)


    #to_CSV(totaldata)

