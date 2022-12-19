import csv
import os
import string
import re
from thefuzz import fuzz
import functools


src_path = "../gen_4/"
dst_path_pre = "../dst/combine"
somelogs_path = "../dst/somelogs.txt"
LIMIT = 5
THRESHOLD = 85

all_combinations = ["1", "2", "3", "4", 
                    "12", "13", "14", "23", "24", "34",
                    "123", "124", "134", "234",
                    "1234"]

def preprocess1(n):
    res = n.lower()
    del_list = [" pc.",
                "inc",
                " inc.",
                " INC",
                " INC.",
                " Inc",
                " Inc.",
                " LLC",
                " LLC.",
                " llc",
                " llc.",
                " l.l.c.",
                " usa.",
                " corp.",
                " ltd",
                " ltd.",
                " pllc.",
                "&amp",
                " assn.",
                " co.",
                " llp",
                ",",
                " ."]
    for w in del_list:
        res = res.replace(w, '')
    return res

def preprocess2(n):
    res = n.replace('-', ' ')
    del_list = [" pc.",
                "inc",
                " inc.",
                " INC",
                " INC.",
                " Inc",
                " Inc.",
                " LLC",
                " LLC.",
                " llc",
                " llc.",
                " l.l.c.",
                " usa.",
                " corp.",
                " ltd",
                " ltd.",
                " pllc.",
                "&amp",
                " assn.",
                " co.",
                " llp",
                ",",
                " ."]
    for w in del_list:
        res = res.replace(w, '')
    return res


def fuzz_score(combination, real_name, matching_name):
    ratio_list = []
    if 1 in combination:
        ratio_list.append(fuzz.ratio(real_name, matching_name))
    if 2 in combination:
        ratio_list.append(fuzz.partial_ratio(real_name, matching_name))
    if 3 in combination:
        ratio_list.append(fuzz.token_sort_ratio(real_name, matching_name))
    if 4 in combination:
        ratio_list.append(fuzz.token_set_ratio(real_name, matching_name))
    ratio = float(sum(ratio_list)) / float(len(ratio_list))
    return ratio

def process_one_line(line, combination):
    num_matching = int((len(line) - 2) / 2)
    if num_matching <= 0:
        return ["N/A"]

    real_name = line[0]
    processed_real_name = preprocess1(real_name)
    res = []
    res.append(processed_real_name)
    res.append(line[1])

    matching_list = []
    i = 2
    j = 3
    while i < len(line):
        temp = []
        temp.append(preprocess2(line[i]))
        temp.append(-1)
        temp.append(line[j])
        i += 2
        j += 2
        matching_list.append(temp)
    
    for m in matching_list:
        ratio = fuzz_score(combination, real_name, m[0])
        m[1] = ratio
    
    def cmp(m1, m2):
        if m1[1] < m2[1]:
            return 1
        if m1[1] > m2[1]:
            return -1
        return 0
    
    matching_list.sort(key = functools.cmp_to_key(cmp))

    flag = False
    for m in matching_list:
        if m[1] >= THRESHOLD:
            flag = True
            for mm in m:
                res.append(mm)
            break

    if flag:
        return res
    else:
        return ["N/A"]



def process_3(combination, dst_path):
    csv_data = []
    head = ["origin_name", "domain"]
    for i in range(0, LIMIT):
        head.append("permalink_" + str(i))
        head.append("uuid_" + str(i))

    for root, dirs, files in os.walk(src_path):
        for file_name in files:
            complete_file_name = src_path + file_name
            with open(complete_file_name, 'r') as rf:
                file_reader = csv.reader(rf)
                rows = [row for row in file_reader]
                for i in range(1, len(rows)):
                    csv_data.append(rows[i])
    
    processed_csv_data = []
    head = ["origin_name", "domain"]
    for i in range(0, LIMIT):
        head.append("permalink_" + str(i))
        head.append("score_" + str(i))
        head.append("uuid_" + str(i))
    processed_csv_data.append(head)

    sum_score = 0.0

    for line in csv_data:
        processed_line = process_one_line(line, combination)
        if processed_line[0] != "N/A":
            processed_csv_data.append(processed_line)
            sum_score += processed_line[3]

    with open(dst_path, 'w') as csv_file:
        file_writer = csv.writer(csv_file, delimiter = ',')
        for line in processed_csv_data:
            file_writer.writerow(line)
    
    num_orgs = len(processed_csv_data) - 1
    avg_score = sum_score / num_orgs
    log_to_write = "combination_"
    for idx in combination:
        log_to_write += str(idx)
    log_to_write += ": num_orgs: " + str(num_orgs) + " avg_score: " + str(avg_score) + "\n"
    with open(somelogs_path, 'a') as wf:
        wf.write(log_to_write)

def main():
    for str_combination in all_combinations:
        dst_path = dst_path_pre + str_combination + ".csv"
        cur_combination = []
        for ch_idx in str_combination:
            cur_combination.append(int(ch_idx))
        process_3(cur_combination, dst_path)
        print(dst_path + " success!\n")

main()
