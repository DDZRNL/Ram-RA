import csv
import os

cols = ['Organization Name', 
        'Organization Name URL', 
        'Industries', 
        'Headquarters Location', 
        'Description', 
        'CB Rank (Company)', 
        'IPqwery - Total Patents', 
        'IPqwery - Patents Granted', 
        'IPqwery - Patents Pending', 
        'IPqwery - Total Trademarks', 
        'IPqwery - IP Activity Score', 
        'IPqwery - Trademarks Pending', 
        'IPqwery - Trademarks Registered', 
        'IPqwery - Most Popular Patent Class', 
        'IPqwery - Most Popular Class Description', 
        'IPqwery - Most Popular Trademark Class', 
        'Headquarters Regions', 
        'Diversity Spotlight (US Headquarters Only)', 
        'Estimated Revenue Range', 
        'Operating Status', 
        'Founded Date', 
        'Founded Date Precision', 
        'Exit Date', 
        'Exit Date Precision', 
        'Closed Date', 
        'Closed Date Precision', 
        'Company Type', 
        'Website', 
        'Twitter', 
        'Facebook', 
        'LinkedIn', 
        'Contact Email', 
        'Phone Number', 
        'Number of Articles', 
        'Hub Tags', 
        'Full Description', 
        'Actively Hiring', 
        'Investor Type', 
        'Investment Stage', 
        'Number of Portfolio Organizations', 
        'Number of Investments', 
        'Number of Lead Investments', 
        'Number of Diversity Investments', 
        'Number of Exits', 
        'Number of Exits (IPO)', 
        'Accelerator Program Type', 
        'Accelerator Application Deadline', 
        'Accelerator Duration (in weeks)', 
        'School Type', 
        'School Program', 
        'Number of Enrollments', 
        'School Method', 
        'Number of Founders (Alumni)', 
        'Number of Alumni', 
        'Industry Groups', 
        'Number of Founders', 
        'Founders', 
        'Number of Employees', 
        'Number of Funding Rounds', 
        'Funding Status', 
        'Last Funding Date', 
        'Last Funding Amount', 
        'Last Funding Amount Currency', 
        'Last Funding Amount Currency (in USD)', 
        'Last Funding Type', 
        'Last Equity Funding Amount', 
        'Last Equity Funding Amount Currency', 
        'Last Equity Funding Amount Currency (in USD)', 
        'Last Equity Funding Type', 
        'Total Equity Funding Amount', 
        'Total Equity Funding Amount Currency', 
        'Total Equity Funding Amount Currency (in USD)', 
        'Total Funding Amount', 
        'Total Funding Amount Currency', 
        'Total Funding Amount Currency (in USD)', 
        'Top 5 Investors', 
        'Number of Lead Investors', 
        'Number of Investors', 
        'Number of Acquisitions', 
        'Acquisition Status', 
        'Transaction Name', 
        'Transaction Name URL', 
        'Acquired by', 
        'Acquired by URL', 
        'Announced Date', 
        'Announced Date Precision', 
        'Price', 
        'Price Currency', 
        'Price Currency (in USD)', 
        'Acquisition Type', 
        'Acquisition Terms', 
        'IPO Status', 
        'IPO Date', 
        'Delisted Date', 
        'Delisted Date Precision', 
        'Money Raised at IPO', 
        'Money Raised at IPO Currency', 
        'Money Raised at IPO Currency (in USD)', 
        'Valuation at IPO', 
        'Valuation at IPO Currency', 
        'Valuation at IPO Currency (in USD)', 
        'Stock Symbol', 
        'Stock Symbol URL', 
        'Stock Exchange', 
        'Last Leadership Hiring Date', 
        'Last Layoff Mention Date', 
        'Number of Events', 
        'CB Rank (Organization)', 
        'CB Rank (School)', 
        'Trend Score (7 Days)', 
        'Trend Score (30 Days)', 
        'Trend Score (90 Days)', 
        'Similar Companies', 
        'Contact Job Departments', 
        'Number of Contacts', 
        'Number of Private Contacts', 
        'SEMrush - Monthly Visits', 
        'SEMrush - Average Visits (6 months)', 
        'SEMrush - Monthly Visits Growth', 
        'SEMrush - Visit Duration', 
        'SEMrush - Visit Duration Growth', 
        'SEMrush - Page Views / Visit', 
        'SEMrush - Page Views / Visit Growth', 
        'SEMrush - Bounce Rate', 
        'SEMrush - Bounce Rate Growth', 
        'SEMrush - Global Traffic Rank', 
        'SEMrush - Monthly Rank Change (#)', 
        'SEMrush - Monthly Rank Growth', 
        'BuiltWith - Tech Changes (%)', 
        'BuiltWith - Active Tech Count', 
        'Apptopia - Number of Apps', 
        'Apptopia - Downloads Last 30 Days', 
        'G2 Stack - Total Products Active', 
        'G2 Stack - Total Product Changes', 
        'Aberdeen - IT Spend', 
        'Aberdeen - IT Spend Currency', 
        'Aberdeen - IT Spend Currency (in USD)', 
        'Aberdeen - Software Spend', 
        'Aberdeen - Software Spend Currency', 
        'Aberdeen - Software Spend Currency (in USD)', 
        'Aberdeen - Communications Spend', 
        'Aberdeen - Communications Spend Currency', 
        'Aberdeen - Communications Spend Currency (in USD)', 
        'Aberdeen - Services Spend', 
        'Aberdeen - Services Spend Currency', 
        'Aberdeen - Services Spend Currency (in USD)', 
        'Aberdeen - Server Spend', 
        'Aberdeen - Server Spend Currency', 
        'Aberdeen - Server Spend Currency (in USD)', 
        'Aberdeen - PC Spend', 
        'Aberdeen - PC Spend Currency', 
        'Aberdeen - PC Spend Currency (in USD)', 
        'Aberdeen - Storage Spend', 
        'Aberdeen - Storage Spend Currency', 
        'Aberdeen - Storage Spend Currency (in USD)', 
        'Aberdeen - Other Hardware Spend', 
        'Aberdeen - Other Hardware Spend Currency', 
        'Aberdeen - Other Hardware Spend Currency (in USD)', 
        'Aberdeen - Other IT Spend', 
        'Aberdeen - Other IT Spend Currency', 
        'Aberdeen - Other IT Spend Currency (in USD)', 
        'Number of Private Notes', 
        'Tags']

auto_src_path = "../1205/auto/"
fuzzy_34_path = "../1205/f34/"
fuzzy_4_path = "../1205/f4/"
dst_path = "../1205/dst/auto_f4_f34.csv"



auto_data = []
f4_data = []
f34_data = []


def add_data(src_path):
    res = []
    for root, dirs, files in os.walk(src_path):
        for file_name in files:
            cur_file_path = os.path.join(root, file_name)
            print(cur_file_path + "  success!")
            with open(cur_file_path, 'r') as rf:
                file_reader = csv.reader(rf)
                rows = [row for row in file_reader]

                cur_row0 = rows[0]
                cur_col_idx = []
                for c in cols:
                    cur_col_idx.append(cur_row0.index(c))
                for i in range(1, len(rows)):
                    cur_row = []
                    for j in cur_col_idx:
                        cur_row.append(rows[i][j])
                    res.append(cur_row)
    return res

res_auto = add_data(auto_src_path)
res_f34 = add_data(fuzzy_34_path)
res_f4 = add_data(fuzzy_4_path)

auto_set = set()
f34_set = set()
f4_set = set()

all_set = set()
# all_dict = dict()

n_auto = 0
for line in res_auto:
    cur_org = line[0]
    auto_set.add(cur_org)
    all_set.add(cur_org)
    n_auto += 1
    # if cur_org not in all_dict:
    #     all_dict[cur_org] = 0
    # all_dict[cur_org] += 1

n_f4 = 0
for line in res_f4:
    cur_org = line[0]
    f4_set.add(line[0])
    all_set.add(cur_org)
    if cur_org not in auto_set:
        n_f4 += 1
    # if cur_org not in all_dict:
    #     all_dict[cur_org] = 0
    # all_dict[cur_org] += 1

n_f34 = 0
for line in res_f34:
    cur_org = line[0]
    f34_set.add(line[0])
    all_set.add(cur_org)
    if cur_org not in auto_set:
        if cur_org not in f4_set:
            n_f34 += 1
    # if cur_org not in all_dict:
    #     all_dict[cur_org] = 0
    # all_dict[cur_org] += 1


final_cols = [cols[0]] + ["matching type"] + cols[1:]
final_csv_data = []
final_csv_data.append(final_cols)
final_set = set()

# cnt = 0
for line in res_auto:
    cur_org = line[0]
    if cur_org in final_set:
        continue
    final_set.add(cur_org)
    cur_matching_type = "auto"
    if cur_org in f34_set:
        cur_matching_type += " fuzzy34"
    if cur_org in f4_set:
        cur_matching_type += " fuzzy4"
    final_line = [line[0]] + [cur_matching_type] + line[1:]
    final_csv_data.append(final_line)
    # cnt += 1
# print("cnt: ", cnt)
# print(n_auto)

# cnt = 0
for line in res_f4:
    cur_org = line[0]
    if cur_org in final_set:
        continue
    final_set.add(cur_org)
    if cur_org not in auto_set:
        cur_matching_type = "fuzzy4"
        if cur_org in f34_set:
            cur_matching_type += " fuzzy34"
        final_line = [line[0]] + [cur_matching_type] + line[1:]
        final_csv_data.append(final_line)
#         cnt += 1
# print("cnt: ", cnt)
# print(n_f4)

# cnt = 0
for line in res_f34:
    cur_org = line[0]
    if cur_org in final_set:
        continue
    final_set.add(cur_org)
    if cur_org in auto_set:
        continue
    if cur_org in f4_set:
        continue
    cur_matching_type = "fuzzy34"
    final_line = [line[0]] + [cur_matching_type] + line[1:]
    final_csv_data.append(final_line)
#     cnt += 1
# print("cnt: ", cnt)
# print(n_f34)

with open(dst_path, 'w') as csv_f:
    file_writer = csv.writer(csv_f, delimiter = ',')
    for line in final_csv_data:
        file_writer.writerow(line)

print(len(final_csv_data) - 1)
print(len(all_set))


# test_file = "/home/bdth333/2022ra/2022FRA/1205/combination-4-0-csv-12-5-2022.csv"
# with open(test_file, 'r') as rf:
#     file_reader = csv.reader(rf)
#     rows = [row for row in file_reader]
#     print(type(rows[0]))

# i = 0
# for key in all_set:
#     if key in auto_set:
#         i += 1
# print("i: ", i)

# i = 0
# for key in all_set:
#     if key in auto_set:
#         continue
#     if key in f4_set:
#         i += 1
# print("i: ", i)

# i = 0
# for key in all_set:
#     if key in auto_set:
#         continue
#     if key in f4_set:
#         continue
#     i += 1
# print("i: ", i)