import urllib.request
import pandas as pd
import re

baseUrlPage = 'https://www.sbir.gov/sbirsearch/firm/all?firm=&uei=&city=&zip=&page='
baseUrl = 'https://www.sbir.gov/'
# pageList = [i for i in range(1, 610)]
pageList = [1, 2]

regTable = re.compile(r'<table class="table table-striped">(.*?)</table>', re.S)
regItem = re.compile(r'<tr>(.*?)</tr>', re.S)
regCompanyNameAndLink = re.compile(r'<a href="(.*?)">(.*?)</a>')
regNumberOfAwards = re.compile(r'<td align="center">([0-9]*)</td>')
regNumEmployee = re.compile(r'<p><strong># of Employees:</strong>(.*?)</p>', re.S)
regHUBZone = re.compile(r'<p><strong>HUBZone Owned:</strong>(.*?)</p>', re.S)
regSocialDisadvantage = re.compile(r'<p><strong>Socially and Economically Disadvantaged:</strong>(.*?)</p>', re.S)
regWomanOwned = re.compile(r'<p><strong>Woman Owned:</strong>(.*?)</p>', re.S)
counter = 0
page = 0
totalData = []
for i in pageList:
    urlPage = baseUrlPage + str(i)
    a = urllib.request.urlopen(urlPage)
    html = a.read().decode('utf-8')
    table = re.findall(regTable, html)
    tr = re.findall(regItem, table[0])
    for j in range(len(tr)):
        dic = {"Company Name": "", "Experience With SBIR Program": "", "Number of Employees": "", "Is Woman Owned": "",
               "Is Socially and Economically Disadvantaged": "", "Is HUBzone Owned": ""}
        nameAndLink = re.findall(regCompanyNameAndLink, tr[j])[
            0]  # nameAndLink = ('<link-to-detail-page>', 'companyName')
        numOfAwards = re.findall(regNumberOfAwards, tr[j])[0].strip()

        urlDetail = baseUrl + nameAndLink[0]
        detailRequest = urllib.request.urlopen(urlDetail)
        detailPage = detailRequest.read().decode('latin-1')
        numberEmployee = re.findall(regNumEmployee, detailPage)[0].strip()
        HUBZoneOwned = re.findall(regHUBZone, detailPage)[0].strip()
        socialDisadvantage = re.findall(regSocialDisadvantage, detailPage)[0].strip()
        womanOwned = re.findall(regWomanOwned, detailPage)[0].strip()
        dic["Company Name"] = nameAndLink[1].lstrip()
        dic["Experience With SBIR Program"] = numOfAwards
        dic["Number of Employees"] = numberEmployee
        dic["Is Woman Owned"] = womanOwned
        dic["Is Socially and Economically Disadvantaged"] = socialDisadvantage
        dic["Is HUBzone Owned"] = HUBZoneOwned
        totalData.append(dic)
        counter += 1
        # print(str(counter))
        # print(dic)
        if counter % 50 == 0:
            pd.DataFrame(totalData).to_csv('task8-AdditionalSBC-Info.csv', index=False, encoding="utf-8", mode='a')
            totalData = []
            page += 1
            print(str(counter) + " finished" + ", page: " + page)

print("Number of Company: " + str(counter))


# def to_CSV(totaldata):
#     pd.DataFrame(totaldata).to_csv('task8-AdditionalSBC-Info.csv', index=False, encoding="utf-8", mode='a')
#
#
# if __name__ == '__main__':
#     to_CSV(totalData)
