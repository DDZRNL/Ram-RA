####Only SBIR now
#### abstract can have "\n"
### 02-phase2 and phase2_additional

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

    htmlfile = open(path, 'r', encoding='utf-8')
    html=htmlfile  #(htmlfile.replace('<br>','')).replace('<br/>','').read()
    #html=html.replace('<br>','')
    bs = BeautifulSoup(html, "html.parser")  # 缩进格式

    tds = bs.find_all("td")   #info

    for i in range(len(tds)):
        #str = divs1[i].string
        if (tds[i] is not None):
            str = tds[i].get_text()
            if (str.find("PROPOSAL NUMBER") != -1):
                # Proposal number
                str=filterHTMLstr(tds[i+1].get_text())
                str=str.replace("II","2")
                dic["Proposal Number"]=str
            elif (str.find("PHASE-I CONTRACT NUMBER") != -1):
                # Phase 1 Contract Number
                dic["Phase 1 Contract #"] = filterHTMLstr(tds[i+1].get_text())
            elif (str.find("SUBTOPIC TITLE") != -1):
                # Subtopic Title
                dic["Subtopic Title"] = filterHTMLstr(tds[i+1].get_text())
            elif (str.find("PROPOSAL TITLE") != -1):
                # Proposal Title
                dic["Proposal Title"] = filterHTMLstr(tds[i+1].get_text())


    details=[]    # Small Business Concern, principal investigator, business official
    brs=bs.find_all("br")
    for i in range(len(brs)):
        if (brs[i].next_sibling is not None):
            str=brs[i].next_sibling.get_text()
        #print(i, " ", len(str)," ",str)
            if(str.strip() is not None):
                str=str.strip()
                if(len(str)>0):
                    details.append(str)
                    #print(i, " ", len(str), " ", str)
                #print(i, " ",len(str.strip())," ", str.strip())
    #print(dic["Proposal Number"])
    # for i in range(len(details)):
    #     print(i,details[i])

    dic["Small Business Concern_Firm"] = filterHTMLstr(details[0])
    dic["Small Business Concern_Address"] = filterHTMLstr(details[1].rstrip() + ", " + details[2])
    dic["Small Business Concern_Phone"] = filterHTMLstr(details[3])
    dic["Principal Investigator_Name"] = filterHTMLstr(details[4])
    dic["Principal Investigator_E-mail"] = filterHTMLstr(details[5])
    dic["Principal Investigator_Address"] = filterHTMLstr(details[6].rstrip() + ", " + details[7])
    dic["Principal Investigator_Phone"] = filterHTMLstr(details[8])


    text=[]
    paras = bs.find_all("p")
    for i in range(len(paras)):
        if (paras[i] is not None):
            str = paras[i].get_text()
            #print(i, " ", len(str)," ",str)
            text.append(str)

    ###### TRL end
    # str = text[2].replace(text[3], '')
    # TRL_End = str.replace('\n', '').replace('\t','').split(":")
    # TRL_End = TRL_End[-1]
    #
    # dic["TRL_End"] = filterHTMLstr(TRL_End)

    str = text[2].replace(text[3], '')
    str = str.replace("TECHNICAL ABSTRACT (LIMIT 200 WORDS)", '')
    dic["Technical Abstract"] = filterHTMLstr(str)
    str=text[3].replace(text[4],'')
    str=str.replace("POTENTIAL NASA COMMERCIAL APPLICATION(S) (LIMIT 150 WORDS)",'')
    dic["Potential NASA applications"] = filterHTMLstr(str)
    str=text[4].replace(text[5],'')
    str = str.replace("POTENTIAL NON-NASA APPLICATION(S) (LIMIT 150 WORDS)",'')
    dic["Potential non-NASA applications"] = filterHTMLstr(str)


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
    pd.DataFrame(totaldata).to_csv('02_SBIR_phase2.csv',index=False, encoding="utf-8")

def to_json(totaldata):
    json_str = json.dumps(totaldata)
    with open('../test_data.json', 'w') as json_file:
        json_file.write(json_str)

if __name__ == '__main__':
    Directory_path = "Datasets/02/sbir/phase2"
    files_position = ReadFiles(Directory_path)
    totaldata=MultipleFileProcess(files_position)
    to_CSV(totaldata)


