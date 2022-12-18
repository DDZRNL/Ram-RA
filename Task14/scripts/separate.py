import csv
import os

chosen_combinations = ["34", "4"]
src_path_pre = "../dst/combine"
dst_path_prepre = "../fuzzymatching_dst/combination_"
head = ["name", "domain"]

def process(combination):
    i = 0
    data_to_write = []
    data_to_write.append(head)
    src_path = src_path_pre + combination + ".csv"
    dst_path_pre = dst_path_prepre + combination + "_"

    with open(src_path, 'r') as rf:
        file_reader = csv.reader(rf)
        rows = [row for row in file_reader]

        for j in range(1, len(rows)):
            data_to_write.append([rows[j][2]])
            if len(data_to_write) == 1000 or j == len(rows) - 1:
                #write........
                dst_path = dst_path_pre + str(i) + ".csv"
                with open(dst_path, 'w') as csv_f:
                    file_writer = csv.writer(csv_f, delimiter = ',')
                    for csv_line in data_to_write:
                        file_writer.writerow(csv_line)
                #write........
                i += 1
                data_to_write = []
                data_to_write.append(head)

def main():
    for combination in chosen_combinations:
        process(combination)
        print("combination_" + combination + " success!\n")

main()
