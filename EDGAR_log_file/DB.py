# -*- coding:utf-8 -*-

import Tkinter
import tkMessageBox


def hello():
    tkMessageBox.showinfo("Say Hello", "Hello World")

if __name__ == "__main__":

    top = Tkinter.Tk()
    L1 = Tkinter.Label(top, text="User Name")
    L1.pack(side="left")
    E1 = Tkinter.Entry(top, bd=5)
    E1.pack(side="right")

    B1 = Tkinter.Button(text="Say Hello", command=hello)
    B1.pack()

    top.mainloop()
