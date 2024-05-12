from collections import Counter
import os
import csv
import time
import re
import math
import time, threading

from tkinter import filedialog, Tk, Button, CENTER
from tkinter.ttk import Progressbar
from tkinter.messagebox import showinfo


def read_dict(path_info, path_dict):
    with open(path_info, 'r', newline='', encoding='utf-8') as info_file:
        reader = csv.reader(info_file)
        info = list()
        for row in reader:
            info.append(row[0])
    with open(path_dict, 'r', newline='', encoding='utf-8') as dict_file:
        reader = csv.reader(dict_file)
        word_dict = {}
        for row in reader:
            values = [int(row[1]), float(row[2]), float(row[3]), int(row[4]), float(row[5]), float(row[6]),
                      float(row[7]), float(row[8])]
            word_dict[row[0]] = values
    return int(info[1]), int(info[2]), word_dict


def read_text(path):
    pattern = r"[^\w\s\-\']"
    file = open(path, 'r', encoding='utf-8')
    text = file.read()
    file.close()
    lower_case_text = text.lower()
    prepared_text = re.sub(pattern, '', lower_case_text)
    splitted_text = prepared_text.split()
    stripped_text = [el.strip('\'-') for el in splitted_text]
    remove_chars_pattern = r"[\'\-]"
    cleared_text = [re.sub(remove_chars_pattern, '', el) for el in stripped_text]
    non_empty_text = [el for el in cleared_text if el]
    F_counter = Counter(non_empty_text)
    return F_counter


def save_rang_result(path, counter, F_counter, f_counter, top_n=None):
    with open(path, 'w', newline='', encoding='utf-8') as rang_file:
        writer = csv.writer(rang_file)
        if top_n is None:
            filtered_counter = Counter({k: v for k, v in counter.most_common()})
        else:
            filtered_counter = Counter({k: v for k, v in counter.most_common(top_n)})
        i = 1
        sumV = sum(filtered_counter.values())
        if path.endswith('rm4.csv'):
            print('sum=', sumV)
        for key, value in filtered_counter.most_common():
            writer.writerow([i, key, value, value / sumV, F_counter[key], f_counter[key]])
            i += 1


def calculation():
    useOnlyPositive = False
    useDict = True
    useMinF = True
    minF = 5
    useMinf = False
    minf = 2.0e-5
    topN = None
    sumOfUsedOptions = int(1 if useMinF else 0) + int(1 if useMinf else 0)
    if sumOfUsedOptions > 1:
        useMinF, useMinf = False, False
        print('You can use only one option. Else program will use no option')
    start_time = time.perf_counter()
    showinfo("Info", 'load _info file')
    info_path = filedialog.askopenfilename()
    showinfo("Info", 'load _dict file')
    dict_path = filedialog.askopenfilename()
    pb['value'] += 10
    showinfo("Info", 'Loading dictionary...')
    n, sum_L, words_corpora = read_dict(info_path, dict_path)
    pb['value'] += 10
    showinfo("Info", 'Dictionary loaded')
    pb['value'] += 10
    showinfo("Info", 'Loading text...')
    text_path = filedialog.askopenfilename()
    F_counter = read_text(text_path)
    pb['value'] += 10
    showinfo("Info", 'Text loaded.')
    F_filtered_counter = F_counter
    La = sum(F_counter.values())
    if useMinF:
        F_filtered_counter = Counter({k: v for k, v in F_counter.items() if v >= minF})
    if useMinf:
        F_filtered_counter = Counter({k: v for k, v in F_counter.items() if v / La >= minf})

    f_counter = Counter({k: v / La for k, v in F_filtered_counter.most_common()})
    if useDict:
        F_filtered_dict_counter = Counter(list(F_filtered_counter))
    else:
        F_filtered_dict_counter = F_filtered_counter
    La = sum(F_filtered_dict_counter.values())
    f_dict_counter = Counter({k: v / La for k, v in F_filtered_dict_counter.most_common()})
    f_sq_counter = Counter({k: v ** 2 for k, v in f_dict_counter.most_common()})
    unique_words = {word for word in f_dict_counter if word not in words_corpora}
    nc = n + 1
    Lc = sum_L + La
    print(F_filtered_dict_counter)
    add_text_words_stats = {}
    for key in f_dict_counter:
        Fa = F_filtered_dict_counter[key]
        fa = f_dict_counter[key]
        fq = f_sq_counter[key]
        if key in unique_words:
            # print(key)
            Fc = Fa
            fc = fa / nc
            fwc = Fa / Lc
            ntc = 1
            fs = ((Fa ** 2) / (La ** 2)) / nc
            fws = ((Fa ** 2) / La) / Lc
            sigma_c = math.sqrt((fq / nc) - (fc ** 2))
        else:
            Fc = words_corpora[key][0] + Fa
            fc = (words_corpora[key][1] * n + fa) / nc
            fwc = (words_corpora[key][0] + Fa) / Lc
            ntc = words_corpora[key][3] + 1
            fs = (words_corpora[key][7] + ((Fa ** 2) / (La ** 2))) / nc
            fws = (words_corpora[key][6] + ((Fa ** 2) / La)) / Lc
            sigma_c = math.sqrt(fs - (fc ** 2))
        sigma_wc = math.sqrt(fws - (fwc ** 2))
        add_text_words_stats[key] = [Fc, fc, fwc, ntc, sigma_c, sigma_wc]

    rm1_counter = Counter({k: f * math.log(nc / add_text_words_stats[k][3], 10) for k, f in f_counter.items()})

    rm3_counter = Counter({k: (f - add_text_words_stats[k][1]) / add_text_words_stats[k][4]
                           for k, f in f_counter.items() if (f - add_text_words_stats[k][1]) > 0})
    rm3w_counter = Counter({k: (f - add_text_words_stats[k][2]) / add_text_words_stats[k][5]
                            for k, f in f_counter.items() if (f - add_text_words_stats[k][2]) > 0})

    rm5_counter = Counter({k: ((f - add_text_words_stats[k][1]) / add_text_words_stats[k][4]) *
                              math.log(nc / add_text_words_stats[k][3]) for k, f in f_counter.items()
                           if (f - add_text_words_stats[k][1]) > 0
                           })
    rm5w_counter = Counter({k: ((f - add_text_words_stats[k][2]) / add_text_words_stats[k][5]) *
                               math.log(nc / add_text_words_stats[k][3]) for k, f in f_counter.items()
                            if (f - add_text_words_stats[k][2]) > 0
                            })

    rm8_counter = Counter({k: f * ((f - add_text_words_stats[k][1]) / add_text_words_stats[k][4])
                           for k, f in f_counter.items() if (f - add_text_words_stats[k][1]) > 0})
    rm8w_counter = Counter({k: f * ((f - add_text_words_stats[k][2]) / add_text_words_stats[k][5])
                            for k, f in f_counter.items() if (f - add_text_words_stats[k][2]) > 0})

    rm9_counter = Counter({k: f * ((f - add_text_words_stats[k][1]) / add_text_words_stats[k][4]) *
                              math.log(nc / add_text_words_stats[k][3])
                           for k, f in f_counter.items() if (f - add_text_words_stats[k][1]) > 0})
    rm9w_counter = Counter({k: f * ((f - add_text_words_stats[k][2]) / add_text_words_stats[k][5]) *
                               math.log(nc / add_text_words_stats[k][3])
                            for k, f in f_counter.items() if (f - add_text_words_stats[k][2]) > 0})
    rm10_counter = Counter({k: f * ((f - add_text_words_stats[k][2]) / add_text_words_stats[k][5]) *
                               math.log(nc / add_text_words_stats[k][3])
                            for k, f in f_counter.items() if (f - add_text_words_stats[k][2]) > 0})


    pb['value'] += 10
    new_path = 'Result_of_Keyness_Relative'
    if not os.path.exists(new_path):
        os.makedirs(new_path)
    save_rang_result(os.path.join(new_path, 'rm1_tf-idf.csv'), rm1_counter, F_filtered_counter, f_counter, topN)
    save_rang_result(os.path.join(new_path, 'rm2_z.csv'), rm3_counter, F_filtered_counter, f_counter, topN)
    save_rang_result(os.path.join(new_path, 'rm3_zw.csv'), rm3w_counter, F_filtered_counter, f_counter, topN)
    save_rang_result(os.path.join(new_path, 'rm4_idf-z.csv'), rm5_counter, F_filtered_counter, f_counter, topN)
    save_rang_result(os.path.join(new_path, 'rm5_idf-zw.csv'), rm5w_counter, F_filtered_counter, f_counter, topN)
    save_rang_result(os.path.join(new_path, 'rm6_tf-z.csv'), rm8_counter, F_filtered_counter, f_counter, topN)
    save_rang_result(os.path.join(new_path, 'rm7_tf-zw.csv'), rm8w_counter, F_filtered_counter, f_counter, topN)
    save_rang_result(os.path.join(new_path, 'rm8_tf-idf-z.csv'), rm9_counter, F_filtered_counter, f_counter, topN)
    save_rang_result(os.path.join(new_path, 'rm9_tf-idf-zw.csv'), rm9w_counter, F_filtered_counter, f_counter, topN)
    save_rang_result(os.path.join(new_path, 'rm910_tf-idf4.csv'), rm10_counter, F_filtered_counter, f_counter, topN)
    pb['value'] += 25
    showinfo("Info", 'n={0}, sum L={1}'.format(nc, Lc))
    pb['value'] += 25
    showinfo("Info", f"Time elapsed  {time.perf_counter() - start_time} s")


if __name__ == "__main__":
    app = Tk()
    app.geometry("200x150")
    app.resizable(width=False, height=False)

    app.title("Calculate Keyness Relative app - Step 2/3")

    main_corpora_data_path = 'files/'

    corpora_name = 'Our Text Base'

    command_button = Button(app, text="Calculate Keyness Relative", command=calculation)
    command_button.place(relx=0.5, rely=0.5, anchor=CENTER)
    pb = Progressbar(app, mode="determinate")
    pb.place(relx=0.5, rely=0.7, anchor=CENTER)

    app.mainloop()
