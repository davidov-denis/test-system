import logging
from subprocess import PIPE, STDOUT, Popen
import os
try:
    from tkinter import *
except:
    from Tkinter import *

def test(tech):
    files = os.listdir("./for-test")
    tests = os.listdir("./tests")

    log = logging.getLogger("tests")
    log.setLevel(logging.INFO)
    FH_log = logging.FileHandler("log.log", encoding="utf-8")
    format_log = logging.Formatter("'%(asctime)s : %(levelname)s : %(name)s : %(message)s'")
    FH_log.setFormatter(format_log)
    log.addHandler(FH_log)

    for file in files:
        ok = 0
        bad = 0
        number = 0
        for test in tests:
            f = open(f"./tests/{test}", encoding="utf-8")
            text = f.read().split("Вывод:")
            number += 1
            test = (text[0]).split("\n")
            ans = str(text[-1]).split("\n")
            test.pop(-1)
            ans.pop(0)
            args = "\n".join(test)
            p = Popen(['python', f'./for-test/{file}'], stdout=PIPE, stdin=PIPE, stderr=PIPE)
            p_stdout, p_errorout = p.communicate(input=bytes(args, encoding="cp1252"))
            out = p_stdout.decode('cp1252').strip()
            error = p_errorout.decode('cp1252').strip()
            if out.split("\r\n") == ans:
                log.info(f"Вердикт {number} по {file}: OK")
                ok += 1
            else:
                print("BAD")
                if error:
                    bad += 1
                    log.info(f"Вердикт {number} по {file}: Ошибка {error}")
                else:
                    bad += 1
                    log.info(f"Вердикт {number} по {file}: Bad")
        log.info(f"Вердикт по {file}: OK: {ok}, BAD: {bad}")
        log.info("-"*50)

def view_log(tech): 
    text = open('log.log', encoding='utf-8').readlines()
    text = ''.join(text)
    textbox.delete('1.0', 'end') 
    textbox.insert('1.0', text)

def clear_log(tech):
    file = open("log.log", "w")
    file.write("")
    file.close()

def del_test(tech):
    tests = os.listdir("./tests")
    for test in tests:
        os.remove(f"./tests/{test}")


root = Tk()

panelFrame = Frame(root, height = 60, width=600, bg = 'gray')
textFrame = Frame(root, height = 340, width = 600)

panelFrame.pack(side = 'top', fill = 'x')
textFrame.pack(side = 'bottom', fill = 'both', expand = 1)


textbox = Text(textFrame, font='Arial 14', wrap='word')
scrollbar = Scrollbar(textFrame)


scrollbar['command'] = textbox.yview
textbox['yscrollcommand'] = scrollbar.set

textbox.pack(side = 'left', fill = 'both', expand = 1)
scrollbar.pack(side = 'right', fill = 'y')

loadBtn = Button(panelFrame, text = 'Запуск теста')
saveBtn = Button(panelFrame, text = 'Просмотреть лог')
delBtn = Button(panelFrame, text = 'Очистить лог')
delTesBtn = Button(panelFrame, text = 'Удалить тесты')

loadBtn.bind("<Button-1>", test)
saveBtn.bind("<Button-1>", view_log)
delBtn.bind("<Button-1>", clear_log)
delTesBtn.bind("<Button-1>", del_test)

loadBtn.place(x = 10, y = 10, width = 100, height = 40)
saveBtn.place(x = 120, y = 10, width = 100, height = 40)
delBtn.place(x = 230, y = 10, width = 100, height = 40)
delTesBtn.place(x = 340, y = 10, width = 100, height = 40)

root.mainloop()