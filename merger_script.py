import os
from tkinter import Tk, Button, Label, Frame, LEFT


def preprocessing():
    # os.system(r"PreProcessingApp.exe")  # for compiled .exe
    os.system(r"python PreProcessingApp.py")  # for manual script

def calculate_corpus():
    # os.system(r"CalculateCorpusData.exe")  # for compiled .exe
    os.system(r"python CalculateCorpusData.py")  # for manual script

def calculate_keyness():
    # os.system(r"CalculateKeynessRelative_AddDictTextToIndex.exe")  # for compiled .exe
    os.system(r"python CalculateKeynessRelative_AddDictTextToIndex.py")  # for manual script





if __name__ == '__main__':
    win = Tk()

    win.title("Text processor")
    win.resizable(width=False, height=False)

    f = Frame(win)

    b1 = Button(f, text="PreProcessing(Step 1)", command=preprocessing)
    b2 = Button(f, text="CalculateCorpusDate(Step 2)", command=calculate_corpus)
    b3 = Button(f, text="CalculateStepKeynessRelative(Step 3)", command=calculate_keyness)

    b1.pack(side=LEFT)
    b2.pack(side=LEFT)
    b3.pack(side=LEFT)

    l = Label(win, text="Click buttons to launch programs")
    l.pack()

    f.pack()

    win.mainloop()
