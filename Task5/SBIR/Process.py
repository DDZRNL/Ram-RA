####Only SBIR now
#### abstract can have "\n"
### The files can be dealed with:all
### A smail problem when deal with 2005 SBIR file

from bs4 import BeautifulSoup
import os
import pandas as pd
import csv
import json

def filterHTMLstr(str):
    html_tag = {'&#xA;': '\n', '&quot;': '\"', '&amp;': '', '&lt;': '<', '&gt;': '>',
                '&apos;': "'", '&nbsp;': ' ', '&yen;': '¥', '&copy;': '©', '&divide;': '÷'
        , '&times;': 'x', '&trade;': '™', '&reg;': '®', '&sect;': '§', '&euro;': '€',
                '&pound;': '£', '&cent;': '￠', '&raquo;': '»','&nbsp':' ',u'\xa0': ' ',
                '\n':' ','\t':' ','    ':'','&emsp':' ',
                }
    for k, v in html_tag.items():
        str = str.replace(k, v)
        #str = str.replace(k[1:], v)
    str = str.strip('\n')
    str = str.strip(' ')

    return str

def SingleHTMLProcess(path):

    dic={"Subtopics_name":"", "2022-focus area and code":"", "2021-focus area and code":"", "2020-focus area and code":"",
         "2019-focus area and code":"", "2018-focus area and code":"", "2017-focus area and code":"", "2016-focus area and code":"",
         "2015-focus area and code":"", "2014-focus area and code":"","2012-focus area and code": "", "2011-focus area and code": "",
         "2010-focus area and code": "", "2009-focus area and code": "", "2008-focus area and code": "", "2007-focus area and code": "",
         "2006-focus area and code": "", "2005-focus area and code": "", "2004-focus area and code": ""
         }

    Subtopic_name=[]

    df = pd.read_csv(path,sep=',')    #header=None

    #print(df["Subtopics_encoding"])

    totaldata = []
    for i in range(len(df["Subtopics_name"])):
        list1 = df["Subtopics_name"][i].split('; ')
        #print(list1)
        list2=df["Subtopics_encoding"][i].split('; ')
        #print(list2)
        for j in range(len(list1)):    # A smail problem when deal with 2005 SBIR file
            dic["Subtopics_name"]=list1[j]
            dic["2015-focus area and code"]=df["Focus Area"][i]+'; '+list2[j]
            dic1 = dic.copy()
            totaldata.append(dic1)

    return totaldata

def to_CSV(totaldata):
    pd.DataFrame(totaldata).to_csv('Result/result_2015.csv', index=False)

if __name__ == '__main__':
    # path="Datasets/22/sbir/phase1/SBIR-22-1-A1.02-1831.html"
    path= "SBIR/2015.csv"
    totaldata=SingleHTMLProcess(path)

    to_CSV(totaldata)

