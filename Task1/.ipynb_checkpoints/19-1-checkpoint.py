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
                '\n':'','\t':'','    ':'','&emsp':' ',
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

    divs1 = bs.find_all("div")   #info
    Name=[]
    Email=[]
    Address=[]
    Phone=[]

    for i in range(len(divs1)):
        #str = divs1[i].string
        if (divs1[i] is not None):
            str = divs1[i].get_text()
            if (str.find("PROPOSAL NUMBER") != -1):
                # Proposal number
                str = filterHTMLstr(divs1[i+1].get_text())
                str = str.replace("19-1-", "19-1")
                dic["Proposal Number"]=str
            elif (str.find("Phase 1 Contract #") != -1):
                # Phase 1 Contract Number
                dic["Phase 1 Contract #"] = filterHTMLstr(divs1[i+1].get_text())
            elif (str.find("SUBTOPIC TITLE") != -1):
                # Subtopic Title
                dic["Subtopic Title"] = filterHTMLstr(divs1[i+1].get_text())
            elif (str.find("PROPOSAL TITLE") != -1):
                # Proposal Title
                dic["Proposal Title"] = filterHTMLstr(divs1[i+1].get_text())


    SBC=[]    # Small Business Concern
    brs=bs.find_all("br")
    for i in range(len(brs)):
        if (brs[i].next_sibling is not None):
            str=brs[i].next_sibling.get_text()
        # print(i," ",str)
        SBC.append(str)
    dic["Small Business Concern_Firm"] = filterHTMLstr(SBC[0])
    dic["Small Business Concern_Address"] = filterHTMLstr(SBC[1].rstrip()+", "+SBC[2])
    dic["Small Business Concern_Phone"] = filterHTMLstr(SBC[3])
    # print(dic["Small Business Concern_Firm"])
    # print(dic["Small Business Concern_Address"])
    # print(dic["Small Business Concern_Phone"])

    ###### TRL begin and end
    TRL_BE = (SBC[4]+SBC[5]).replace('\n', '').split()
    TRL_Begin = TRL_BE[1]
    TRL_End = TRL_BE[3]
    dic["TRL_Begin"] = TRL_Begin
    dic["TRL_End"] = TRL_End


    heads3=bs.find_all("h3")
    for i in range(len(heads3)):
        if(heads3[i].strong is not None):
            head=heads3[i].strong.get_text()
            next=heads3[i].find_next_sibling()
            head_divs=next.find_all("div")

            if(head.find("Principal Investigator") != -1):
                for j in range(len(head_divs)):
                    if (head_divs[j] is not None):
                        text = head_divs[j].get_text()
                        if (text.find("Name") != -1):
                            dic["Principal Investigator_Name"]=filterHTMLstr(head_divs[j+1].get_text())
                        elif (text.find("E-mail") != -1):
                            dic["Principal Investigator_E-mail"] = filterHTMLstr(head_divs[j+1].get_text())
                        elif (text.find("Address") != -1):
                            dic["Principal Investigator_Address"] = filterHTMLstr(head_divs[j+1].get_text())
                        elif (text.find("Phone") != -1):
                            dic["Principal Investigator_Phone"] = filterHTMLstr(head_divs[j+1].get_text())
            elif(head.find("Business Official") != -1):
                for j in range(len(head_divs)):
                    if (head_divs[j] is not None):
                        text = head_divs[j].get_text()
                        if (text.find("Name") != -1):
                            dic["Business Official_Name"] = filterHTMLstr(head_divs[j + 1].get_text())
                        elif (text.find("E-mail") != -1):
                            dic["Business Official_E-mail"] = filterHTMLstr(head_divs[j + 1].get_text())
                        elif (text.find("Address") != -1):
                            dic["Business Official_Address"] = filterHTMLstr(head_divs[j + 1].get_text())
                        elif (text.find("Phone") != -1):
                            dic["Business Official_Phone"] = filterHTMLstr(head_divs[j + 1].get_text())

    Abstract=[]
    NASA_applicants=[]
    Non_NASA_applicants=[]
    paras=bs.find_all("p")   #  Abstract, NASA applicants, Non-NASA applicants
    for i in range(len(paras)):
        #print(paras[i].string)
        if(paras[i] is not None):
            #print(paras[i].parent.get_text())
            para = paras[i].get_text()
            para = filterHTMLstr(para)
            para_parent_str=paras[i].parent.get_text()
            if(len(para)>0):
                if (para_parent_str.find("Technical Abstract") != -1):
                    Abstract.append(para)
                elif(para_parent_str.find("Potential NASA Applications") != -1):
                    NASA_applicants.append(para)
                elif(para_parent_str.find("Potential Non-NASA Applications") != -1):
                    Non_NASA_applicants.append(para)

    dic["Technical Abstract"]=" ".join(Abstract)
    dic["Potential NASA applications"]=" ".join(NASA_applicants)
    dic["Potential non-NASA applications"]=" ".join(Non_NASA_applicants)

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
    pd.DataFrame(totaldata).to_csv('./SBIRResult/19_SBIR_phase1.csv',index=False)

def to_json(totaldata):
    json_str = json.dumps(totaldata)
    with open('../test_data.json', 'w') as json_file:
        json_file.write(json_str)

if __name__ == '__main__':
    Directory_path = "../Datasets/19/sbir/phase1"
    files_position = ReadFiles(Directory_path)
    totaldata=MultipleFileProcess(files_position)
    to_CSV(totaldata)
    # dic=SingleHTMLProcess("Datasets/19/sbir/phase1/SBIR-19-1-A1.01-3664.html")
    # sample=[dic]
    # to_CSV(sample)

