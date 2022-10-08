####Only SBIR now
#### abstract can have "\n"
### The files can be dealed with: 12-04

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
                '\t':' ','    ':'','&emsp':' ',
                }
    for k, v in html_tag.items():
        str = str.replace(k, v)
        #str = str.replace(k[1:], v)
    str = str.strip('\n')
    str = str.strip(' ')

    return str

def SingleHTMLProcess(path):

    dic={"Higher Topic":"", "Focus Area":"", "Content":"","Subtopics":"","Subtopics_encoding":"","Subtopics_name":""}

    htmlfile = open(path, 'r', encoding='utf-8')
    html=htmlfile
    bs = BeautifulSoup(html, "html.parser")  # 缩进格式

    HigherTopics = []
    FocusAreas=[]
    Contents=[]

    Titles=bs.find_all("h4",{'class':"topicTitle"})  #  Focus Areas

    for i in range(len(Titles)):
        if(Titles[i] is not None):
            str=filterHTMLstr(Titles[i].get_text())
            #print(i, str)
            if(str.find("Topic")!=-1):
                str=str.replace(" PDF",'')
                FocusAreas.append(str)

    # for i in range(len(FocusAreas)):
    #     print(i, FocusAreas[i])

    texts = bs.find_all("div", {'class': 'topicDesc'})    #  Focus Area Contents

    for i in range(len(texts)):
        if (texts[i] is not None):
            str = filterHTMLstr(texts[i].get_text())
            # print(i, str)
            if(len(str)!=0):
                Contents.append(str)

    # for i in range(len(Contents)):
    #     print(i, Contents[i])

    #### Subtopics
    subs=bs.find_all("p",{'class':"subtopic"})  #,{'class':"view-content"}

    topics=[]
    encodings=[]
    subtopics_name=[]

    for i in range(len(Titles)):

        title=Titles[i]
        if(title is not None):
            title=filterHTMLstr(title.get_text())
            if(title.find("Topic")!=-1):
                HighTopic = Titles[i].find_previous("h2")
                #print(filterHTMLstr(HighTopic.get_text()))
                HigherTopics.append(filterHTMLstr(HighTopic.get_text()))

                temp = []
                temp2 = []
                temp3 = []
                #print(title)
                #print("###########################################")
                subtopics=Titles[i].find_next("div").next_sibling.find_all("p",{'class':"subtopic"})
                #codings=subs[i].next_sibling.find_all("span")
                for j in range(len(subtopics)):
                    if(subtopics[j] is not None):
                        str1 = subtopics[j].get_text()
                        #print(str1)
                        temp.append(filterHTMLstr(str1))
                        str2=subtopics[j].find("span").get_text()
                        temp2.append(filterHTMLstr(str2))
                        str3=str1.replace(str2,"")
                        temp3.append(filterHTMLstr(str3))
                topics.append(temp)
                encodings.append(temp2)
                subtopics_name.append(temp3)

    print(len(HigherTopics))
    print(len(FocusAreas))
    print(len(Contents))
    print(len(topics))
    print(len(encodings))
    print(len(subtopics_name))

    # for i in range(len(encodings)):
    #     print(encodings[i])

    # for i in range(len(topics)):
    #     print(topics[i])

    texts=bs.find_all("div",{'class': 'focusAreaDesc'})

    for i in range(len(texts)):
        if(texts[i] is not None):
            str=filterHTMLstr(texts[i].get_text())
            #print(i, str)
            Contents.append(str)

    # for i in range(len(Contents)):
    #     print(i, Contents[i])

    totaldata = []
    for i in range(len(FocusAreas)):
        dic["Higher Topic"] = HigherTopics[i]
        dic["Focus Area"]=FocusAreas[i]
        dic["Content"]=Contents[i]
        dic["Subtopics"] = '; '.join(topics[i])
        dic["Subtopics_encoding"] = '; '.join(encodings[i])
        dic["Subtopics_name"] = '; '.join(subtopics_name[i])
        dic1=dic.copy()
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
        data = SingleHTMLProcess(position)
        totaldata.append(data)

    return totaldata

def to_CSV(totaldata):
    pd.DataFrame(totaldata).to_csv('2004.csv', index=False)

if __name__ == '__main__':
    # path="Datasets/22/sbir/phase1/SBIR-22-1-A1.02-1831.html"
    path="Datasets/2004.html"
    totaldata=SingleHTMLProcess(path)

    to_CSV(totaldata)

