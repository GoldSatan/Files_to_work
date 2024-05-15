import sys
import time
import shutil
import os
import re
import nltk
from enum import Enum
from tkinter import Button, Tk, Entry, Label, W, E, IntVar, StringVar, filedialog
from tkinter.ttk import Combobox, Progressbar
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from collections import Counter
import pymorphy2
import pymorphy2_dicts_ru
import pymorphy2_dicts_uk


class Language(Enum):
    English_E = 1
    Russian_R = 2
    Ukrainian_U = 3


class StopWordMode(Enum):
    Remove_D = 1
    Replace_R = 2
    AsIs_A = 3


class ProcessingMode(Enum):
    Stemmer_S = 1
    Lemmatizer_L = 2
    AsIs_A = 3


class SentenceTerminatorMode(Enum):
    Remove_D = 1
    Replace_R = 2


class CipherMode(Enum):
    Remove_D = 1
    AsIs_A = 2


class PreProcessApp(Tk):
    def __init__(self):
        super().__init__()
        self.stop_list = []
        self.selected_stop_list_file = None
        self.selected_in_folder = None
        self.selected_out_folder = None
        self.stop_word_replacer = StringVar()
        self.sentence_terminator_replacer = StringVar()
        self.progress_var = IntVar()
        self.status_var = StringVar()

        self.title("Text pre processing app - Step 1/3")

        self.stop_list_file_btn = Button(self, text="Select stop list file", width=30,
                                         command=self.select_stop_list_file)
        self.stop_list_file_btn.grid(column=0, row=0, padx=5, pady=5, sticky=W + E)
        self.stop_list_file_lbl = Label(self, text="Selected stop list file: None")
        self.stop_list_file_lbl.grid(column=1, row=0, padx=5, pady=5, sticky=W + E)

        self.in_folder_btn = Button(self, text="Select source folder", width=30, command=self.select_in_folder)
        self.in_folder_btn.grid(column=0, row=1, padx=5, pady=5, sticky=W)
        self.in_folder_lbl = Label(self, text="Selected source folder: None")
        self.in_folder_lbl.grid(column=1, row=1, padx=5, pady=5, sticky=W + E)

        self.out_folder_btn = Button(self, text="Select target folder", width=30, command=self.select_out_folder)
        self.out_folder_btn.grid(column=0, row=2, padx=5, pady=5, sticky=W)
        self.out_folder_lbl = Label(self, text="Selected target folder: None")
        self.out_folder_lbl.grid(column=1, row=2, padx=5, pady=5, sticky=W + E)

        self.language_mode_lbl = Label(self, text="Select language:")
        self.language_mode_lbl.grid(column=0, row=3, padx=5, pady=5, sticky=W)
        self.language_mode_combo = Combobox(self)
        # self.language_mode_combo['values'] = (Language.English_E, Language.Russian_R, Language.Ukrainian_U)
        self.language_mode_combo['values'] = (Language.English_E, Language.Ukrainian_U)
        self.language_mode_combo.set(Language.English_E)
        self.language_mode_combo.grid(column=1, row=3, padx=5, pady=5, sticky=W + E)

        self.stop_word_mode_lbl = Label(self, text="Select stop word mode:")
        self.stop_word_mode_lbl.grid(column=0, row=4, padx=5, pady=5, sticky=W)
        self.stop_word_mode_combo = Combobox(self)
        self.stop_word_mode_combo['values'] = (StopWordMode.Remove_D, StopWordMode.Replace_R, StopWordMode.AsIs_A)
        self.stop_word_mode_combo.set(StopWordMode.AsIs_A)
        self.stop_word_mode_combo.grid(column=1, row=4, padx=5, pady=5, sticky=W + E)

        self.stop_word_rpl_lbl = Label(self, text="Replace stop words as:")
        self.stop_word_rpl_lbl.grid(column=0, row=5, padx=5, pady=5, sticky=W)
        self.stop_word_rpl_ent = Entry(self, textvariable=self.stop_word_replacer)
        self.stop_word_rpl_ent.grid(column=1, row=5, padx=5, pady=5, sticky=W + E)

        self.pre_proc_mode_lbl = Label(self, text="Select processing mode:")
        self.pre_proc_mode_lbl.grid(column=0, row=6, padx=5, pady=5, sticky=W)
        self.pre_proc_mode_combo = Combobox(self)
        self.pre_proc_mode_combo['values'] = (
        ProcessingMode.Stemmer_S, ProcessingMode.Lemmatizer_L, ProcessingMode.AsIs_A)
        self.pre_proc_mode_combo.set(ProcessingMode.Lemmatizer_L)
        self.pre_proc_mode_combo.grid(column=1, row=6, padx=5, pady=5, sticky=W + E)

        self.sentence_terminator_mode_lbl = Label(self, text="Select sentence terminator mode:")
        self.sentence_terminator_mode_lbl.grid(column=0, row=7, padx=5, pady=5, sticky=W)
        self.sentence_terminator_mode_combo = Combobox(self)
        self.sentence_terminator_mode_combo['values'] = (
        SentenceTerminatorMode.Remove_D, SentenceTerminatorMode.Replace_R)
        self.sentence_terminator_mode_combo.set(SentenceTerminatorMode.Remove_D)
        self.sentence_terminator_mode_combo.grid(column=1, row=7, padx=5, pady=5, sticky=W + E)

        self.sentence_terminator_rpl_lbl = Label(self, text="Replace sentence terminators (.!?) as:")
        self.sentence_terminator_rpl_lbl.grid(column=0, row=8, padx=5, pady=5, sticky=W)
        self.sentence_terminator_rpl_ent = Entry(self, textvariable=self.sentence_terminator_replacer)
        self.sentence_terminator_rpl_ent.grid(column=1, row=8, padx=5, pady=5, sticky=W + E)

        self.cipher_mode_lbl = Label(self, text="Select cipher (0-9) mode:")
        self.cipher_mode_lbl.grid(column=0, row=9, padx=5, pady=5, sticky=W)
        self.cipher_mode_combo = Combobox(self)
        self.cipher_mode_combo['values'] = (CipherMode.AsIs_A, CipherMode.Remove_D)
        self.cipher_mode_combo.set(CipherMode.AsIs_A)
        self.cipher_mode_combo.grid(column=1, row=9, padx=5, pady=5, sticky=W + E)

        self.process_btn = Button(self, text="Do texts pre processing", command=self.do_pre_processing)
        self.process_btn.grid(columnspan=2, column=0, padx=5, pady=5, row=10)

        self.bar = Progressbar(self, length=100, variable=self.progress_var, mode='determinate')
        self.bar.grid(columnspan=2, column=0, row=11, padx=5, pady=5, sticky=W + E)

        self.status_lbl = Label(self, textvariable=self.status_var)
        self.status_lbl.grid(columnspan=2, column=0, padx=5, pady=5, row=12, sticky=W)

        self.stop_word_replacer.set('stopword')
        self.sentence_terminator_replacer.set('.')
        self.progress_var.set(0)
        self.status_var.set(
            'Select file with stop words, source folder, target folder, parameters and press "Do text pre processing"')

        for i in range(1, 3):
            self.columnconfigure(i, weight=1)
        for j in range(1, 12):
            self.rowconfigure(j, weight=1)

    @staticmethod
    def get_wordnet_pos(treebank_tag):

        if treebank_tag.startswith('J'):
            return wordnet.ADJ
        elif treebank_tag.startswith('V'):
            return wordnet.VERB
        elif treebank_tag.startswith('N'):
            return wordnet.NOUN
        elif treebank_tag.startswith('R'):
            return wordnet.ADV
        else:
            return wordnet.NOUN

    def select_stop_list_file(self):
        if self.selected_stop_list_file:
            current_folder = os.path.basename(self.selected_stop_list_file)
        else:
            current_folder = os.getcwd()
        res = filedialog.askopenfilename(initialdir=current_folder, title='Please select a file with stop words')
        if res:
            self.selected_stop_list_file = res
            in_folder_str = "Selected stop list file: " + self.selected_stop_list_file
            self.stop_list_file_lbl.configure(text=in_folder_str)

    def select_in_folder(self):
        current_folder = self.selected_in_folder if self.selected_in_folder else os.getcwd()
        res = filedialog.askdirectory(initialdir=current_folder, title='Please select a directory with raw texts')
        if res:
            self.selected_in_folder = res
            in_folder_str = "Selected source folder: " + self.selected_in_folder
            self.in_folder_lbl.configure(text=in_folder_str)

    def select_out_folder(self):
        current_folder = self.selected_out_folder if self.selected_out_folder else os.getcwd()
        res = filedialog.askdirectory(initialdir=current_folder, title='Please select a directory for processed texts')
        if res:
            self.selected_out_folder = res
            out_folder_str = "Selected target folder: " + self.selected_out_folder
            self.out_folder_lbl.configure(text=out_folder_str)

    def do_pre_processing(self):
        langMode = Language[self.language_mode_combo.get().split('.')[1]]
        stopWordMode = StopWordMode[self.stop_word_mode_combo.get().split('.')[1]]
        processingMode = ProcessingMode[self.pre_proc_mode_combo.get().split('.')[1]]
        sentenceTerminatorMode = SentenceTerminatorMode[self.sentence_terminator_mode_combo.get().split('.')[1]]
        cipherMode = CipherMode[self.cipher_mode_combo.get().split('.')[1]]
        stopWordReplacer = self.stop_word_replacer.get()
        sentenceTerminatorReplacer = self.sentence_terminator_replacer.get()
        if not self.selected_in_folder:
            self.status_var.set("Error: Source folder was not selected")
            return
        if not self.selected_out_folder:
            self.status_var.set("Error: Target folder was not selected")
            return
        if not self.are_paths_valid(self.selected_in_folder, self.selected_out_folder):
            self.status_var.set("Error: Source/target folders was not correctly selected")
            return
        if stopWordMode != StopWordMode.AsIs_A:
            if self.selected_stop_list_file:
                try:
                    self.read_stopwords(self.selected_stop_list_file)
                except:
                    self.status_var.set("Error: File with stop words cannot be read")
                    return
            else:
                self.status_var.set("Error: File with stop words was not selected")
                return
        if processingMode == ProcessingMode.Stemmer_S and langMode != Language.English_E:
            self.status_var.set("Error: Stemming is supported only for English. Other languages do not supported yet")
            return
        try:
            self.create_folder_structure(self.selected_in_folder, self.selected_out_folder)
            if langMode == Language.English_E:
                nltk.download('wordnet')
                stemmer = PorterStemmer()
                lemmatizer = WordNetLemmatizer()
            else:
                morph = pymorphy2.MorphAnalyzer(path=os.getcwd() + '\\pymorphy2_dicts_uk\\data', lang='uk') \
                    if langMode == Language.Ukrainian_U \
                    else pymorphy2.MorphAnalyzer(path=os.getcwd() + '\\pymorphy2_dicts_ru\\data', lang='ru')
        except PermissionError:
            self.status_var.set("Permission error:" + str(sys.exc_info()[1]))
            return
        except:
            self.status_var.set("Unexpected error:" + str(sys.exc_info()[1]))
            return
        n = 0
        for root, dirs, files in os.walk(self.selected_in_folder):
            for name in files:
                n += 1
        processed = 0
        start_time = time.time()
        only_word_symbols_pattern = r"[^\w\s\-\']" if cipherMode == CipherMode.AsIs_A else r"\d|[^\w\s\-\']"
        for root, dirs, files in os.walk(self.selected_in_folder):
            for name in files:
                file = open(os.path.join(root, name), 'r', encoding='utf-8')
                # try:
                if file:
                    text = file.read()
                    file.close()
                    lower_case_text = text.lower()
                    re_split = re.split(r"[.!?]+", lower_case_text, 0, re.IGNORECASE)
                    output_list = []
                    for sentence in re_split:
                        cleared_sentence = re.sub(only_word_symbols_pattern, '', sentence, 0, re.IGNORECASE)
                        if cipherMode == CipherMode.Remove_D:
                            cleared_sentence = re.sub(r"\d", '', cleared_sentence, 0, re.IGNORECASE)
                        if cleared_sentence:
                            single_words = cleared_sentence.split()
                            words = single_words
                            if processingMode == ProcessingMode.Lemmatizer_L:
                                words = []
                                if langMode == Language.English_E:
                                    tagged_words = nltk.pos_tag(single_words)
                                    for item in tagged_words:
                                        word = item[0]
                                        if word:
                                            pos_tag = self.get_wordnet_pos(item[1])
                                            lemma = lemmatizer.lemmatize(word, pos_tag)
                                            words.append(lemma)
                                else:
                                    for item in single_words:
                                        p = morph.parse(item)[0]
                                        words.append(p.normal_form)
                            for word in words:
                                stripped_word = re.sub(r"[\'\-]", '', word)
                                if not stripped_word:
                                    continue
                                if stopWordMode != StopWordMode.AsIs_A and stripped_word in self.stop_list:
                                    if stopWordMode == StopWordMode.Remove_D:
                                        continue
                                    if stopWordMode == StopWordMode.Replace_R:
                                        output_list.append(stopWordReplacer)
                                else:
                                    out_word = stripped_word
                                    if processingMode == ProcessingMode.Stemmer_S:
                                        out_word = stemmer.stem(stripped_word)
                                    if processingMode == ProcessingMode.Lemmatizer_L:
                                        out_word = stripped_word
                                    output_list.append(out_word)
                                if len(output_list) > 0 and output_list[-1] != ' ':
                                    output_list.append(' ')
                            if sentenceTerminatorMode == SentenceTerminatorMode.Replace_R:
                                if len(output_list) > 1 and output_list[-1] != sentenceTerminatorReplacer and \
                                        output_list[-2] != sentenceTerminatorReplacer:
                                    output_list.append(sentenceTerminatorReplacer)
                                if len(output_list) > 0 and output_list[-1] != ' ':
                                    output_list.append(' ')
                    output_text = ''.join(output_list)
                    new_file_path = os.path.join(root.replace(self.selected_in_folder, self.selected_out_folder, 1),
                                                 name)
                    new_file = open(new_file_path, 'w', encoding='utf-8')
                    new_file.write(output_text)
                    new_file.close()
                # except UnicodeDecodeError as ude:
                #    print("UnicodeDecodeError: {0}".format(ude))
                # except:
                #    print("Unexpected error: ", sys.exc_info()[0])
                processed += 1
                processedPercent = int(round(processed / n * 100.0))
                self.progress_var.set(processedPercent)
                status = "Processed:" + str(processedPercent) + "%"
                self.status_var.set(status)
                self.bar.update()
        finish_time = time.time()
        diff = finish_time - start_time
        self.status_var.set("Processing finished! Elapsed seconds: " + str(diff))

    def are_paths_valid(self, src_path, dest_path):
        next_level_folder = 'new_folder'
        src = str(os.path.join(src_path, next_level_folder))
        dest = str(os.path.join(dest_path, next_level_folder))
        if src == dest:
            self.status_var.set("Error: source folder and target folder are the same")
            return False
        if src.startswith(dest):
            self.status_var.set("Error: source folder is nested in target folder")
            return False
        if dest.startswith(src):
            self.status_var.set("Error: target folder is nested to source folder")
            return False
        return True

    def create_folder_structure(self, src_path, dest_path):
        if os.path.isdir(dest_path):
            shutil.rmtree(dest_path)
            time.sleep(1)
        os.mkdir(dest_path)
        for root, folders, files in os.walk(src_path):
            for folder in folders:
                main_path = root.replace(src_path, dest_path)
                new_full_path = os.path.join(main_path, folder)
                os.mkdir(new_full_path)

    def read_stopwords(self, path):
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
        self.stop_list = list(F_counter)


if __name__ == '__main__':
    app = PreProcessApp()
    app.mainloop()
