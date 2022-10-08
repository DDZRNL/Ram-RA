####Only SBIR now
#### abstract can have "\n"
### The files can be dealed with:

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
    dic = {"Subtopics_name": "", "2022-focus area and code": "", "2021-focus area and code": "",
           "2020-focus area and code": "",
           "2019-focus area and code": "", "2018-focus area and code": "", "2017-focus area and code": "",
           "2016-focus area and code": "",
           "2015-focus area and code": "", "2014-focus area and code": "", "2012-focus area and code": "",
           "2011-focus area and code": "",
           "2010-focus area and code": "", "2009-focus area and code": "", "2008-focus area and code": "",
           "2007-focus area and code": "",
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
        for j in range(len(list1)):
            dic["Subtopics_name"]=list1[j]
            dic["2022-focus area and code"]=df["Focus Area"][i]+'; '+list2[j]
            dic1 = dic.copy()
            totaldata.append(dic1)

    return totaldata


def ReadFiles(Directory_path):     # Read all the html files
    path=Directory_path   # The directory
    file_names = os.listdir(path)  # 得到文件夹下的所有文件名称
    files_position=[]
    for file_name in file_names:
        position=path+"/"+file_name
        #print(position)
        files_position.append(position)

    print("Total number of HTML files: ", len(files_position))
    return files_position

def MultipleFileProcess(files_position):
    totaldata = []
    for position in files_position:
        df = pd.read_csv(position,sep=',')
        df1=df.copy()
        totaldata.append(df1)

    result=pd.concat(totaldata)

    return result

def to_CSV(totaldata):
    pd.DataFrame(totaldata).to_csv('Result.csv', index=False)


if __name__ == '__main__':
    # path="Datasets/22/sbir/phase1/SBIR-22-1-A1.02-1831.html"
    path= "Result"
    positions=ReadFiles(path)
    df=MultipleFileProcess(positions)
    df.fillna('')

    def concat_func(x):
        return pd.Series({
            '2022-focus area and code': ','.join('%s' %id for id in x['2022-focus area and code'].unique()),
            '2021-focus area and code': ','.join('%s' %id for id in x['2021-focus area and code'].unique()),
            '2020-focus area and code': ','.join('%s' %id for id in x['2020-focus area and code'].unique()),
            '2019-focus area and code': ','.join('%s' %id for id in x['2019-focus area and code'].unique()),
            '2018-focus area and code': ','.join('%s' % id for id in x['2018-focus area and code'].unique()),
            '2017-focus area and code': ','.join('%s' % id for id in x['2017-focus area and code'].unique()),
            '2016-focus area and code': ','.join('%s' % id for id in x['2016-focus area and code'].unique()),
            '2015-focus area and code': ','.join('%s' % id for id in x['2015-focus area and code'].unique()),
            '2014-focus area and code': ','.join('%s' % id for id in x['2014-focus area and code'].unique()),
            '2012-focus area and code': ','.join('%s' % id for id in x['2012-focus area and code'].unique()),
            '2011-focus area and code': ','.join('%s' % id for id in x['2011-focus area and code'].unique()),
            '2010-focus area and code': ','.join('%s' % id for id in x['2010-focus area and code'].unique()),
            '2009-focus area and code': ','.join('%s' % id for id in x['2009-focus area and code'].unique()),
            '2008-focus area and code': ','.join('%s' % id for id in x['2008-focus area and code'].unique()),
            '2007-focus area and code': ','.join('%s' % id for id in x['2007-focus area and code'].unique()),
            '2006-focus area and code': ','.join('%s' % id for id in x['2006-focus area and code'].unique()),
            '2005-focus area and code': ','.join('%s' % id for id in x['2005-focus area and code'].unique()),
            '2004-focus area and code': ','.join('%s' % id for id in x['2004-focus area and code'].unique()),
        }
        )


    result = df.groupby(df['Subtopics_name']).apply(concat_func).reset_index()

    for index, row in result.iterrows():
        for j in range(len(row)):
            list = row[j].split(',')
            row[j] = ''
            for k in range(len(list)):
                if (list[k] != 'nan'):
                    row[j] = list[k]

    result.to_csv('SBIR-Result.csv', index=False)

    #to_CSV(totaldata)

