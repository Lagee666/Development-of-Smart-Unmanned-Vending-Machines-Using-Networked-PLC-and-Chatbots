# -*- coding: utf-8 -*-
"""
Created on Wed Jul 15 20:04:17 2020

@author: Ben
"""

from pyModbusTCP.client import ModbusClient
import tkinter as tk
import math
import time
import pyautogui

window = tk.Tk()
window.title('Unmanned store')
#window.geometry('400x300')
window.configure(background='white')

HOST1 = "140.124.39.112"
PORT1 = 502

cost=50
c1 = ModbusClient()
c2 = ModbusClient()

# uncomment this line to see debug message
#c1.debug(True)
#c2.debug(True)

# define modbus server host, port
c1.host(HOST1)
#set UID to 1
c1.unit_id(1)


        
def comsumer():
    merch_F.grid_forget()
    pay_Frame.grid_forget()
    comsumer_F.grid(row=0,column=0)
    comsumer_cost()

def comsumer_cost():
    global flag
    flag=True

    
    while(flag==True):
        window.update()
        # if c1.open():
        #     cost=c1.read_holding_registers(4146,1)
        #     cost_label['text']=cost
        #     print(cost)
        #     c1.close()
        #     time.sleep(0.1)
        # else:
        #     print("connect fail")
    
def delay():
    time.sleep(1)
    comsumer_cost()


def check():
    global flag
    flag=False

    pay_Frame.grid(row=0,column=0)
    check_window()

def check_window():

    # if c1.open():
    #     cost=c1.read_holding_registers(4146,1)
    #     pay_label['text']=cost
    #     print(cost)
    #     c1.close()
    comsumer_F.forget()
    global merch
    merch=''
    event_label.focus_set()
    window.update()

def xcheck_window(event):

    window.update()
    x=event.char
    x=ord(x)
    #print(x) 
    global merch
    
    if x!=13:
        #break
        x=str(chr(x))
        merch=x+merch
       
    else:
        print(merch)
        #merch_write=int(merch[-1])
        #print(merch_write)

        
        merch=''
        # if c1.open():
        #     c1.write_single_register(4146,0)
        #     c1.close()
        
        comsumer()

        
merch_F = tk.Frame(window)
merch_F.grid(row=0,column=0)

comsumer_switch_btn=tk.Button(merch_F,text='開始',command=comsumer)
comsumer_switch_btn.grid(row=0,columnspan=4,sticky='wnes')



#-----------------------------------#
comsumer_F=tk.Frame(window)
cost_T_label=tk.Label(comsumer_F,text='Total cost:')
cost_T_label.grid(row=0,column=0,rowspan=5,columnspan=2,padx=5,pady=5,sticky='e')

cost_label=tk.Label(comsumer_F,text=cost)
cost_label.grid(row=0,column=2,rowspan=5,columnspan=2,padx=5,pady=5,sticky='w')

check_btn=tk.Button(comsumer_F,text='Pay',command=check)
check_btn.grid(row=5,column=0,columnspan=3,sticky='wnes')

#-------------------------------------#
pay_Frame=tk.Frame(window)
pay_T_label=tk.Label(pay_Frame,text='Total cost:')
pay_T_label.grid(row=0,column=0,rowspan=5,columnspan=2,padx=5,pady=5,sticky='e')

pay_label=tk.Label(pay_Frame,text=cost)
pay_label.grid(row=0,column=2,rowspan=5,columnspan=2,padx=5,pady=5,sticky='w')

event_label=tk.Label(pay_Frame,text='請放入卡片')
event_label.grid(row=5,column=0,columnspan=3,padx=10,pady=10)
event_label.bind("<Key>",xcheck_window)

pay_return_button=tk.Button(pay_Frame,text='返回',command=comsumer)
pay_return_button.grid(row=6,column=0,columnspan=3,sticky='wnes')
#-------------------------------------#
window.mainloop()
