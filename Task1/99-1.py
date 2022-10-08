####Only SBIR now
#### abstract can have "\n"
###

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

    dic={"Proposal Number":"", "Phase 1 Contract #":"","Subtopic Title":"","Proposal Title":"","Small Business Concern_Firm":"","Small Business Concern_Address":"","Small Business Concern_Phone":"",
         "Principal Investigator_Name":"","Principal Investigator_E-mail":"","Principal Investigator_Address":"","Principal Investigator_Phone":"",
         "Business Official_Name":"","Business Official_E-mail":"","Business Official_Address":"","Business Official_Phone":"",
         "TRL_Begin":"","TRL_End":"","Technical Abstract":"","Potential NASA applications":"","Potential non-NASA applications":"",
         "Technology Taxonomy Mapping":""}

    #print(len(dic.keys()))

    htmlfile = open(path, 'r', encoding='unicode_escape')   # encoding = 'unicode_escape'
    html=htmlfile  #(htmlfile.replace('<br>','')).replace('<br/>','').read()
    #html=html.replace('<br>','')
    bs = BeautifulSoup(html, "html.parser")  # 缩进格式  from_encoding="utf-8"

    text = []
    paras = bs.find_all("p")
    i=0
    while(i<len(paras)):
        if (paras[i] is not None):
            #str = paras[i].get_text()
            #print(i, " ", len(str)," ",str)
            str=""
            if(paras[i].get_text().find("TECHNICAL ABSTRACT (LIMIT 200 WORDS)")!=-1):
                while(paras[i+1].get_text().find("POTENTIAL COMMERCIAL APPLICATIONS")==-1):
                    str = str.rstrip() + " " + paras[i+1].get_text()
                    i+=1
            elif(paras[i].get_text().find("POTENTIAL COMMERCIAL APPLICATIONS")!=-1):
                while(paras[i+1].get_text().find("NAME AND ADDRESS OF PRINCIPAL INVESTIGATOR")==-1):
                    str = str.rstrip() + " " + paras[i+1].get_text()
                    i+=1
            else:
                str = paras[i].get_text()

            text.append(str)
            i+=1

    # for i in range(len(text)):
    #     print(i," ", len(text[i])," ",text[i])
    dic["Proposal Number"] = filterHTMLstr(text[0].replace("PROPOSAL NUMBER ",""))
    dic["Proposal Title"] = filterHTMLstr(text[2])
    dic["Technical Abstract"] = filterHTMLstr(text[3])
    dic["Potential non-NASA applications"] = filterHTMLstr(text[4])

    dic["Principal Investigator_Name"] = filterHTMLstr(text[7])
    dic["Principal Investigator_Address"] = filterHTMLstr(text[9].rstrip() + ", " + text[10])
    dic["Small Business Concern_Firm"] = filterHTMLstr(text[12])
    dic["Small Business Concern_Address"] = filterHTMLstr(text[13].rstrip() + ", " + text[14])

    #print(dic["Proposal Number"])

    return dic

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

def to_Excel(totaldata):
    output = open('data21_sbir_phase2.xls', 'w', encoding='utf-8')
    # the title of each column
    output.write('Proposal Number\tPhase 1 Contract #\tSubtopic Title\tProposal Title\tSmall Business Concern_Firm\tSmall Business Concern_Address\tSmall Business Concern_Phone\t'
                 'Principal Investigator_Name\tPrincipal Investigator_E-mail\tPrincipal Investigator_Address\tPrincipal Investigator_Phone\t'
                 'Business Official_Name\tBusiness Official_E-mail\tBusiness Official_Address\tBusiness Official_Phone\t'
                 'TRL_Begin\tTRL_End\tTechnical Abstract\tPotential NASA applications\tPotential non-NASA applications\n')

    for i in range(len(totaldata)):
        for j in range(len(totaldata[i])):
            output.write(str(totaldata[i][j]))  # write函数不能写int类型的参数，所以使用str()转化
            output.write('\t')  # 相当于Tab一下，换一个单元格
        output.write('\n')  # 写完一行立马换行
    output.close()

def to_CSV(totaldata):
    pd.DataFrame(totaldata).to_csv('99_SBIR_phase1.csv',index=False, encoding="utf-8")

def to_json(totaldata):
    json_str = json.dumps(totaldata)
    with open('../test_data.json', 'w') as json_file:
        json_file.write(json_str)

if __name__ == '__main__':
    Directory_path = "Datasets/99/sbir/phase1"
    files_position = ReadFiles(Directory_path)
    totaldata=MultipleFileProcess(files_position)
    to_CSV(totaldata)


