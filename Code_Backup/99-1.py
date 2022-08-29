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
                '&pound;': '£', '&cent;': '￠', '&raquo;': '»', '&nbsp': ' ', u'\xa0': ' ',
                '\n': '', '\t': ' ', '    ': '', '&emsp': ' ', '  ': ' ',
                }
    for k, v in html_tag.items():
        str = str.replace(k, v)
        # str = str.replace(k[1:], v)
    str = str.strip('\n')
    str = str.strip(' ')

    return str


def SingleHTMLProcess(path):
    dic = {"Proposal Number": "", "Phase 1 Contract #": "", "Subtopic Title": "", "Proposal Title": "",
           "Small Business Concern_Firm": "", "Small Business Concern_Address": "", "Small Business Concern_Phone": "",
           "Principal Investigator_Name": "", "Principal Investigator_E-mail": "", "Principal Investigator_Address": "",
           "Principal Investigator_Phone": "",
           "Business Official_Name": "", "Business Official_E-mail": "", "Business Official_Address": "",
           "Business Official_Phone": "",
           "TRL_Begin": "", "TRL_End": "", "Technical Abstract": "", "Potential NASA applications": "",
           "Potential non-NASA applications": ""}

    # print(len(dic.keys()))

    htmlfile = open(path, 'r', encoding='unicode_escape')  # encoding = 'unicode_escape'
    html = htmlfile  # (htmlfile.replace('<br>','')).replace('<br/>','').read()
    # html=html.replace('<br>','')
    bs = BeautifulSoup(html, "html.parser")  # 缩进格式  from_encoding="utf-8"

    text = []
    paras = bs.find_all("p")
    flag = False
    i = 0
    while i < len(paras):
        if paras[i] is not None:
            line = ""
            item = paras[i].get_text()
            if item.find("TECHNICAL ABSTRACT (LIMIT 200 WORDS)") != -1:
                while paras[i + 1].get_text().find("POTENTIAL COMMERCIAL APPLICATIONS") == -1:
                    line = line.rstrip() + " " + paras[i + 1].get_text()
                    i += 1
                dic["Technical Abstract"] = filterHTMLstr(line)
            elif item.find("POTENTIAL COMMERCIAL APPLICATIONS") != -1:
                while paras[i + 1].get_text().find("NAME AND ADDRESS OF PRINCIPAL INVESTIGATOR") == -1:
                    line = line.rstrip() + " " + paras[i + 1].get_text()
                    i += 1
                dic["Potential non-NASA applications"] = filterHTMLstr(line)
            elif item.find("PROPOSAL NUMBER ") != -1:
                dic["Proposal Number"] = filterHTMLstr(item.replace("PROPOSAL NUMBER ", ""))
                flag = True
                # print("Find: " + dic["Proposal Number"])
            elif item.find("PROJECT TITLE") != -1:
                dic["Proposal Title"] = filterHTMLstr(paras[i + 1].get_text())
            elif item.find("NAME AND ADDRESS OF PRINCIPAL INVESTIGATOR") != -1:
                while i < len(paras) and paras[i].get_text().find("City/State/Zip") == -1:
                    i += 1
                if i >= len(paras):
                    break
                dic["Principal Investigator_Name"] = filterHTMLstr(paras[i + 1].get_text())
                dic["Principal Investigator_Address"] = filterHTMLstr(
                    paras[i + 3].get_text().rstrip() + ", " + paras[i + 4].get_text())
            if item.find("NAME AND ADDRESS OF OFFEROR") != -1:
                while i < len(paras) and paras[i].get_text().find("City/State/Zip") == -1:
                    i += 1
                if i >= len(paras):
                    break
                dic["Small Business Concern_Firm"] = filterHTMLstr(paras[i + 1].get_text())
                dic["Small Business Concern_Address"] = filterHTMLstr(
                    paras[i + 2].get_text().rstrip() + ", " + paras[i + 3].get_text())

            i += 1

    if not flag:
        f = open(path, 'r', encoding = 'unicode_escape')  # encoding = 'unicode_escape'
        str1 = f.read()
        str2 = str1.replace('<P>', '</P><P>').replace('<HR>', '</P><P>').replace('</FONT>', '</P></FONT>')\
            .replace('\t', '').replace('  ', ' ').replace('<br>', '\n').replace('<BR>', '\n')
        # 保存内容
        f = open('tmp.html', 'a', encoding='unicode_escape')  # f.seek(0)
        f.seek(0) # 0为从文档中字符第0位开始
        f.truncate() # 清空指令
        f.write(str2)
        f.close()

        htmlfile = open('tmp.html', 'r', encoding='unicode_escape')  # encoding = 'unicode_escape'
        html = htmlfile

        bs = BeautifulSoup(html, "html.parser")
        paras = bs.find_all("p")
        i = 0
        while i < len(paras):
            if paras[i] is not None:
                item = paras[i].get_text()
                if item.find("TECHNICAL ABSTRACT (LIMIT 200 WORDS)") != -1:
                    dic["Technical Abstract"] = filterHTMLstr(item.replace("TECHNICAL ABSTRACT (LIMIT 200 WORDS)", ""))
                elif item.find("POTENTIAL COMMERCIAL APPLICATIONS") != -1:
                    dic["Potential non-NASA applications"] = filterHTMLstr(item.replace("POTENTIAL COMMERCIAL APPLICATIONS", ""))
                elif item.find("PROPOSAL NUMBER") != -1:
                    dic["Proposal Number"] = filterHTMLstr(item.replace("PROPOSAL NUMBER: ", ""))
                elif item.find("PROJECT TITLE") != -1:
                    dic["Proposal Title"] = filterHTMLstr(item.replace("PROJECT TITLE: ", ""))
                elif item.find("NAME AND ADDRESS OF PRINCIPAL INVESTIGATOR") != -1:
                    items = item.split("\n")
                    name = ""
                    address = ""
                    counter = 0
                    for iter in items:
                        if iter.lstrip() != '':
                            if counter == 1:
                                name = iter
                            if counter == 3:
                                address = iter
                            if counter == 4:
                                address = address.rstrip() + ", " + iter
                            counter += 1
                    dic["Principal Investigator_Name"] = filterHTMLstr(name)
                    dic["Principal Investigator_Address"] = filterHTMLstr(address)
                elif item.find("NAME AND ADDRESS OF OFFEROR") != -1:
                    items = item.split("\n")
                    firm = ""
                    address = ""
                    counter = 0
                    for iter in items:
                        if iter.lstrip() != '':
                            if counter == 1:
                                firm = iter
                            if counter == 2:
                                address = iter
                            if counter == 3:
                                address = address.rstrip() + ", " + iter
                            counter += 1
                    dic["Small Business Concern_Firm"] = filterHTMLstr(firm)
                    dic["Small Business Concern_Address"] = filterHTMLstr(address)
                i += 1

    return dic


def ReadFiles(Directory_path):  # Read all the html files
    path = Directory_path  # The directory
    file_names = os.listdir(path)  # 得到文件夹下的所有文件名称
    files_position = []
    for file_name in file_names:
        position = path + "/" + file_name
        # print(position)
        files_position.append(position)

    print("Total number of HTML files: ", len(files_position))
    return files_position


def MultipleFileProcess(files_position):
    totaldata = []
    for position in files_position:
        data = SingleHTMLProcess(position)
        totaldata.append(data)
    # data = SingleHTMLProcess("../Datasets/99/sbir/phase1/SBIR-99-1-25.04-5700.html")
    # data = SingleHTMLProcess("../Datasets/99/sbir/phase1/SBIR-99-1-22.02-3555.html")
    # totaldata.append(data)

    return totaldata


def to_Excel(totaldata):
    output = open('data21_sbir_phase2.xls', 'w', encoding='utf-8')
    # the title of each column
    output.write(
        'Proposal Number\tPhase 1 Contract #\tSubtopic Title\tProposal Title\tSmall Business Concern_Firm\tSmall Business Concern_Address\tSmall Business Concern_Phone\t'
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
    pd.DataFrame(totaldata).to_csv('99_SBIR_phase1.csv', index=False, encoding="utf-8")


def to_json(totaldata):
    json_str = json.dumps(totaldata)
    with open('../test_data.json', 'w') as json_file:
        json_file.write(json_str)


if __name__ == '__main__':
    Directory_path = "../Datasets/99/sbir/phase1"
    files_position = ReadFiles(Directory_path)
    totaldata = MultipleFileProcess(files_position)
    to_CSV(totaldata)
