import tkinter
import time
from tkinter import ttk


def xFunc1(event):
    print(f"事件觸發鍵盤輸入:{event.char},對應的ASCII碼:{event.keycode}")


win = tkinter.Tk()
win.title("Kahn Software v1")    # #窗口標題
win.geometry("600x500+200+20")   # #窗口位置500後面是字母x
'''
響應所有事件(鍵盤)
<Key>   所有鍵盤按鍵會觸發

'''
xLabel = tkinter.Entry(win, text="KAHN Hello world")
xLabel.focus_set()
xLabel.pack()
xLabel.bind("<Key>", xFunc1)
xLabel = tkinter.Label(win, text="KAHN Hello world")
xLabel.pack()

win.mainloop()   # #窗口持久化