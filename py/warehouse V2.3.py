
from pyModbusTCP.client import ModbusClient
import tkinter as tk
import math
import time
import pyautogui
import msvcrt
#from LineNotify import lineNotifyMessage
from msvcrt import getch 
from line_bot import linebotsendmessage
from tkinter import messagebox 



token= 'AFbeBzzgiiHCf7AUKl5kEgG0DsNQW3N5cd7TJDRoIXc'
window = tk.Tk()
window.title('Unmanned store')
#window.geometry('400x300')
window.configure(background='white')

HOST1 = "140.124.39.112"
PORT1 = 502

cost=0
c1 = ModbusClient()
c2 = ModbusClient()

pre_quantity=[0,0,0,0,0,0] 
# uncomment this line to see debug message
#c1.debug(True)
#c2.debug(True)

# define modbus server host, port
c1.host(HOST1)
#set UID to 1
c1.unit_id(1)




def purchase_window():   #進貨鎖定視窗 
    global merch
    text_set('Put mode. Wait for scanning barcode')
    merch=''
    merch_F.grid_forget()
    purchase_frame.grid(row=0)
    window.update()
    global flag,flag1
    flag1=True
    flag=False
    purchase_entry.focus()
    while (flag1==True):
        x=''
        while(len(x)<10):
            x=purchase_entry.get()
            time.sleep(0.1)
            window.update()
        
        merch=x
        merch_write=int(x[0])
        print(merch_write)
        full1=Read_register(4107,3)
        full2=Read_register(4117,3)
        full=1
        for i in range(3):
            full=full1[i]*full2[i]*full

        if full==0:
            if merch_write==1:
                text_set('條碼:'+merch)
                Write_register(4096,merch_write)
            elif merch_write==2:
                text_set('條碼:'+merch)
                Write_register(4096,merch_write)
            elif merch_write==3:
                text_set('條碼:'+merch)
                Write_register(4096,merch_write)
            elif merch_write==4:
                text_set('條碼:'+merch)
                Write_register(4096,merch_write)
            elif merch_write==5:
                text_set('條碼:'+merch)
                Write_register(4096,merch_write)
            elif merch_write==6:
                text_set('條碼:'+merch)
                Write_register(4096,merch_write)
        else:
            text_set('倉庫已滿')
            Write_register(4096,merch_write)
        merch=''
        
        purchase_entry.delete(0,'end')


def xpurchase(event):#進貨條碼設定
    
    window.update()
    x=event.char
    x=ord(x)
    global merch
    print(x)
    if x!=13:
        #break
        x=str(chr(x))
        merch=x+merch
        #print(merch)
        
    else:
        merch_write=int(merch[-1])
        print(merch_write)
        
        
#條碼區
#---------------------------------------------------------#
#價錢設定區
def merch_money():#價錢設定
    
    replenish_frame.grid_forget()
    merch_F.grid(row=0,column=0)
    merch1_M=int(merch1_M_entry.get())
    merch2_M=int(merch2_M_entry.get())
    merch3_M=int(merch3_M_entry.get())
    merch4_M=int(merch4_M_entry.get())
    merch5_M=int(merch5_M_entry.get())
    merch6_M=int(merch6_M_entry.get())
    
    merch1_Q=int(merch1_Q_entry.get())
    merch2_Q=int(merch2_Q_entry.get())
    merch3_Q=int(merch3_Q_entry.get())
    merch4_Q=int(merch4_Q_entry.get())
    merch5_Q=int(merch5_Q_entry.get())
    merch6_Q=int(merch6_Q_entry.get())
    
    merch_M=[merch1_M,merch2_M,merch3_M,merch4_M,merch5_M,merch6_M]
    merch_Q=[merch1_Q,merch2_Q,merch3_Q,merch4_Q,merch5_Q,merch6_Q]
    
    # if c1.open():
    #     text_set('已設定價錢')
    #     c1.write_multiple_registers(4147,merch_M)
    #     c1.write_multiple_registers(4157,merch_Q)
    #     c1.close()
   
    print(merch_M)
    main_window()

def main_window():#主視窗
    replenish_frame.grid_forget()
    purchase_frame.grid_forget()
    store_True.grid_forget()
    store_False.grid_forget()
    input_btn.grid(row=7,columnspan=4,sticky='wnes')
    purchase_btn.grid(row=8,columnspan=4,sticky='wnes')
    replenish_btn.grid(row=9,columnspan=4,sticky='wnes')
    merch_F.grid(row=0,column=0)
    merch1_Q_entry['state']='disable'
    merch2_Q_entry['state']='disable'
    merch3_Q_entry['state']='disable'
    merch4_Q_entry['state']='disable'
    merch5_Q_entry['state']='disable'
    merch6_Q_entry['state']='disable'

    merch1_M_entry['state']='disable'
    merch2_M_entry['state']='disable'
    merch3_M_entry['state']='disable'
    merch4_M_entry['state']='disable'
    merch5_M_entry['state']='disable'
    merch6_M_entry['state']='disable'

    window.update()

    global flag,flag1
    flag1=False
    flag=True

    global pre_quantity
    pre_quantity[0]=int(merch1_Q_entry.get())
    pre_quantity[1]=int(merch2_Q_entry.get())
    pre_quantity[2]=int(merch3_Q_entry.get())
    pre_quantity[3]=int(merch4_Q_entry.get())
    pre_quantity[4]=int(merch5_Q_entry.get())
    pre_quantity[5]=int(merch6_Q_entry.get())
    while(flag==True):
        Quantity_Scan()

def Quantity_Scan():#掃描物品數量
    
    global pre_quantity

    window.update()
    quantity=Read_register(4157,6)
    quantity=[1,2,1,1,2,3]
    #print(quantity)
    quantity1=int(quantity[0])
    quantity2=int(quantity[1])
    quantity3=int(quantity[2])
    quantity4=int(quantity[3])
    quantity5=int(quantity[4])
    quantity6=int(quantity[5])
    
    money=Read_register(4147,6)
    money=[10,20,30,40,50,60]

    merch1_Q_entry['state']='normal'
    merch2_Q_entry['state']='normal'
    merch3_Q_entry['state']='normal'
    merch4_Q_entry['state']='normal'
    merch5_Q_entry['state']='normal'
    merch6_Q_entry['state']='normal'

    merch1_M_entry['state']='normal'
    merch2_M_entry['state']='normal'
    merch3_M_entry['state']='normal'
    merch4_M_entry['state']='normal'
    merch5_M_entry['state']='normal'
    merch6_M_entry['state']='normal'


    merch1_Q_entry.delete(0,"end")
    merch1_Q_entry.insert(0,quantity1)
    merch2_Q_entry.delete(0,"end")
    merch2_Q_entry.insert(0,quantity2)
    merch3_Q_entry.delete(0,"end")
    merch3_Q_entry.insert(0,quantity3)
    merch4_Q_entry.delete(0,"end")
    merch4_Q_entry.insert(0,quantity4)
    merch5_Q_entry.delete(0,"end")
    merch5_Q_entry.insert(0,quantity5)
    merch6_Q_entry.delete(0,"end")
    merch6_Q_entry.insert(0,quantity6)
    
    merch1_M_entry.delete(0,"end")
    merch1_M_entry.insert(0,money[0])
    merch2_M_entry.delete(0,"end")
    merch2_M_entry.insert(0,money[1])
    merch3_M_entry.delete(0,"end")
    merch3_M_entry.insert(0,money[2])
    merch4_M_entry.delete(0,"end")
    merch4_M_entry.insert(0,money[3])
    merch5_M_entry.delete(0,"end")
    merch5_M_entry.insert(0,money[4])
    merch6_M_entry.delete(0,"end")
    merch6_M_entry.insert(0,money[5])

    merch1_Q_entry['state']='disable'
    merch2_Q_entry['state']='disable'
    merch3_Q_entry['state']='disable'
    merch4_Q_entry['state']='disable'
    merch5_Q_entry['state']='disable'
    merch6_Q_entry['state']='disable'
    
    merch1_M_entry['state']='disable'
    merch2_M_entry['state']='disable'
    merch3_M_entry['state']='disable'
    merch4_M_entry['state']='disable'
    merch5_M_entry['state']='disable'
    merch6_M_entry['state']='disable'

    #print("pre=",pre_quantity,"   quan=",quantity)
    Linetext=''
    for i in range(6):
        if pre_quantity[i]!=quantity[i] and pre_quantity[i]>=0 and quantity[i]==0:
            pre_quantity[i]=-1

    for i in range(6):
        if pre_quantity[i]==-1:
            # Linetext+="商品"+str(i+1)+"缺貨"
            # linebotsendmessage(Linetext)
            # print(Linetext)
            # Linetext=''
            pre_quantity[i]=-2
    
    #time.sleep(10)
    window.update()

    
def Write_register(reg,value): #輸入暫存器
    
    # if c1.open():
    #     c1.write_single_register(reg,value)
    #     c1.close()
    pass
    
def Read_register(reg,nb): #讀取暫存器

    
    rd=0
    rds=[] 

    # if c1.open():
    #     if nb==1:
    #         rd=c1.read_holding_registers(reg,nb)
    #     else:
    #         rds=c1.read_holding_registers(reg,nb)
    #     c1.close()

    # if nb==1:
    #     return rd[0]
    # else:
    #     return rds 
    




def Replenish():#補貨
    
    global flag,reple
    flag=False

    reple_list=[reple1.get(),reple2.get(),reple3.get(),reple4.get(),reple5.get(),reple6.get()]    
    print(reple_list)
    for i in range(6):
        time.sleep(0.2)
        if reple_list[i]==True:
            reple=str(i+1)
            if reple=='1':
                text_set('第1個貨架需要補貨')
                Write_register(4096,11)                     #第一個貨架缺貨
                while(True):
                    window.update()
                    if Read_register(4097,1) ==3:
                        Write_register(4096,0)
                        while (True):
                            window.update()
                            if Read_register(4097,1)==2:
                                text_set('第1個貨架已取出')
                                break
                        
                        break
                    elif Read_register(4097,1)==4:
                        messagebox.showinfo("缺貨","缺貨")
                        text_set('第1個貨架缺貨')
                        #跳通知
                        break
                

            if reple=='2':
                text_set('第2個貨架需要補貨')
                Write_register(4096,12)                     #第2個貨架缺貨
                while(True):
                    window.update()
                    if Read_register(4097,1) ==3:
                        Write_register(4096,0)
                        while (True):
                            window.update()
                            if Read_register(4097,1)==2:
                                text_set('第2個貨架已取出')
                                break
                        
                        break
                    elif Read_register(4097,1)==4:
                        messagebox.showinfo("缺貨","缺貨")
                        text_set('第2個貨架缺貨')
                        #跳通知
                        break

            if reple=='3':
                text_set('第3個貨架需要補貨')
                Write_register(4096,13)                     #第3個貨架缺貨
                while(True):
                
                    window.update()
                    if Read_register(4097,1) ==3:
                        Write_register(4096,0)
                        while (True):
                            window.update()
                            if Read_register(4097,1)==2:
                                text_set('第3個貨架已取出')
                                break
                        break
                    elif Read_register(4097,1)==4:
                        messagebox.showinfo("缺貨","缺貨")
                        text_set('第3個貨架缺貨')
                        #跳通知
                        break

            if reple=='4':
                text_set('第4個貨架需要補貨')
                Write_register(4096,14)                     #第4個貨架缺貨
                while(True):
                    window.update()
                    if Read_register(4097,1) ==3:
                        Write_register(4096,0)
                        while (True):
                            window.update()
                            if Read_register(4097,1)==2:
                                text_set('第4個貨架已取出')
                                break
                        
                        break
                    elif Read_register(4097,1)==4:
                        messagebox.showinfo("缺貨","缺貨")
                        text_set('第4個貨架缺貨')
                        #跳通知
                        break

            if reple=='5':
                text_set('第5個貨架需要補貨')
                Write_register(4096,15)                     #第5個貨架缺貨
                while(True):
                    
                    window.update()
                    if Read_register(4097,1) ==3:
                        Write_register(4096,0)
                        while (True):
                            window.update()
                            if Read_register(4097,1)==2:
                                text_set('第5個貨架已取出')
                                break
                        
                        
                        break
                    elif Read_register(4097,1)==4:
                        messagebox.showinfo("缺貨","缺貨")
                        text_set('第5個貨架缺貨')
                        #跳通知
                        break
            if reple=='6':
                text_set('第6個貨架需要補貨')
                Write_register(4096,16)                     #第6個貨架缺貨
                while(True):
                    
                    window.update()
                    if Read_register(4097,1) ==3:
                        Write_register(4096,0)
                        while (True):
                            window.update()
                            if Read_register(4097,1)==2:
                                text_set('第6個貨架已取出')
                                break
                        
                        
                        break
                    elif Read_register(4097,1)==4:
                        messagebox.showinfo("缺貨","缺貨")
                        text_set('第6個貨架缺貨')
                        #跳通知
                        break
    replenish_frame.grid_forget()
    merch_F.grid(row=0,column=0)
    main_window()

def Replenish_window(): #補貨頁面設定
   
    global reple
    
    merch_F.grid_forget()
    replenish_frame.grid(row=0,column=0)
    window.update()

def text_set(text): #訊息設定
    event_text.insert('end','\n')
    event_text.insert('end',time.strftime("<%H:%M:%S>", time.localtime()))
    event_text.insert('end',text)
    event_text.see(1000.0)

def start_funtion(): #起始狀態
    event_text.insert('end','Start')
    Quantity_Scan()
    main_window()

def store():  #補貨  取消迴圈
    
    global reple,flag
    flag=False
   

    purchase_btn.grid_forget()
    input_btn.grid_forget()
    replenish_btn.grid_forget()
    
    store_True.grid(row=7,columnspan=4,sticky='wnes')
    store_False.grid(row=8,columnspan=4,sticky='wnes')
    merch1_Q_entry['state']='normal'
    merch2_Q_entry['state']='normal'
    merch3_Q_entry['state']='normal'
    merch4_Q_entry['state']='normal'
    merch5_Q_entry['state']='normal'
    merch6_Q_entry['state']='normal'
    
    merch1_M_entry['state']='normal'
    merch2_M_entry['state']='normal'
    merch3_M_entry['state']='normal'
    merch4_M_entry['state']='normal'
    merch5_M_entry['state']='normal'
    merch6_M_entry['state']='normal'

    window.update()

merch_F=tk.Frame(window)
merch_F.grid(row=0,column=0)
merch1_M_label = tk.Label(merch_F, text='Price of item 1')
merch1_M_label.grid(row=1,column=0)
merch1_M_entry = tk.Entry(merch_F,width=6)
merch1_M_entry.grid(row=1,column=1)
merch1_M_entry.insert(0,"0")
merch1_Q_label = tk.Label(merch_F, text='Amound of item 1')
merch1_Q_label.grid(row=1,column=2)
merch1_Q_entry = tk.Entry(merch_F,width=6)
merch1_Q_entry.grid(row=1,column=3)
merch1_Q_entry.insert(0,"0")

merch2_M_label = tk.Label(merch_F, text='Price of item 2')
merch2_M_label.grid(row=2,column=0)
merch2_M_entry = tk.Entry(merch_F,width=6)
merch2_M_entry.grid(row=2,column=1)
merch2_M_entry.insert(0,"0")
merch2_Q_label = tk.Label(merch_F, text='Amound of item 2')
merch2_Q_label.grid(row=2,column=2)
merch2_Q_entry = tk.Entry(merch_F,width=6)
merch2_Q_entry.grid(row=2,column=3)
merch2_Q_entry.insert(0,"0")

merch3_M_label = tk.Label(merch_F, text='Price of item 3')
merch3_M_label.grid(row=3,column=0)
merch3_M_entry = tk.Entry(merch_F,width=6)
merch3_M_entry.grid(row=3,column=1)
merch3_M_entry.insert(0,"0")
merch3_Q_label = tk.Label(merch_F, text='Amound of item 3')
merch3_Q_label.grid(row=3,column=2)
merch3_Q_entry = tk.Entry(merch_F,width=6)
merch3_Q_entry.grid(row=3,column=3)
merch3_Q_entry.insert(0,"0")

merch4_M_label = tk.Label(merch_F, text='Price of item 4')
merch4_M_label.grid(row=4,column=0)
merch4_M_entry = tk.Entry(merch_F,width=6)
merch4_M_entry.grid(row=4,column=1)
merch4_M_entry.insert(0,"0")
merch4_Q_label = tk.Label(merch_F, text='Amound of item 4')
merch4_Q_label.grid(row=4,column=2)
merch4_Q_entry = tk.Entry(merch_F,width=6)
merch4_Q_entry.grid(row=4,column=3)
merch4_Q_entry.insert(0,"0")

merch5_M_label = tk.Label(merch_F, text='Price of item 5')
merch5_M_label.grid(row=5,column=0)
merch5_M_entry = tk.Entry(merch_F,width=6)
merch5_M_entry.grid(row=5,column=1)
merch5_M_entry.insert(0,"0")
merch5_Q_label = tk.Label(merch_F, text='Amound of item 5')
merch5_Q_label.grid(row=5,column=2)
merch5_Q_entry = tk.Entry(merch_F,width=6)
merch5_Q_entry.grid(row=5,column=3)
merch5_Q_entry.insert(0,"0")

merch6_M_label = tk.Label(merch_F, text='Price of item 6')
merch6_M_label.grid(row=6,column=0)
merch6_M_entry = tk.Entry(merch_F,width=6)
merch6_M_entry.grid(row=6,column=1)
merch6_M_entry.insert(0,"0")
merch6_Q_label = tk.Label(merch_F, text="Amound of item 6")
merch6_Q_label.grid(row=6,column=2)
merch6_Q_entry = tk.Entry(merch_F,width=6)
merch6_Q_entry.grid(row=6,column=3)
merch6_Q_entry.insert(0,"0")

input_btn = tk.Button(merch_F, text='Enter', command=store,width=30)
input_btn.grid(row=7,columnspan=4,sticky='wnes')
purchase_btn = tk.Button(merch_F, text='Put mode', command=purchase_window)
purchase_btn.grid(row=8,columnspan=4,sticky='wnes')
replenish_btn = tk.Button(merch_F, text='Take out mode', command=Replenish_window)
replenish_btn.grid(row=9,columnspan=4,sticky='wnes')

replenish_frame=tk.Frame(window)
replenish_label=tk.Label(replenish_frame,text='Take out')
replenish_label.grid(row=0,column=0,columnspan=2,sticky='wens')
reple1=tk.BooleanVar()
reple1.set(False)
reple2=tk.BooleanVar()
reple2.set(False)
reple3=tk.BooleanVar()
reple3.set(False)
reple4=tk.BooleanVar()
reple4.set(False)
reple5=tk.BooleanVar()
reple5.set(False)
reple6=tk.BooleanVar()
reple6.set(False)
reple_1=tk.Checkbutton(replenish_frame,text='Take out item 1',var=reple1)
reple_1.grid(row=1,column=0)
reple_2=tk.Checkbutton(replenish_frame,text='Take out item 2',var=reple2)
reple_2.grid(row=2,column=0)
reple_3=tk.Checkbutton(replenish_frame,text='Take out item 3',var=reple3)
reple_3.grid(row=3,column=0)
reple_4=tk.Checkbutton(replenish_frame,text='Take out item 4',var=reple4)
reple_4.grid(row=1,column=1)
reple_5=tk.Checkbutton(replenish_frame,text='Take out item 5',var=reple5)
reple_5.grid(row=2,column=1)
reple_6=tk.Checkbutton(replenish_frame,text='Take out item 6',var=reple6)
reple_6.grid(row=3,column=1)
reple_bt=tk.Button(replenish_frame,text='Take out',command=Replenish,width=30)
reple_bt.grid(row=4,column=0,columnspan=2,sticky='wens')
#---------------------------------------#


event_frame=tk.Frame(window)
event_frame.grid(row=0,column=1)
event_label=tk.Label(event_frame,text="Message")
event_label.grid(row=0,column=4,columnspan=1,sticky='wnes')


event_text=tk.Text(event_frame,width=40)
event_text.grid(row=1,column=4,rowspan=15,columnspan=1)

#-------------------------------------#
store_True=tk.Button(merch_F,text='Enter',command=merch_money)
store_False=tk.Button(merch_F,text='Cancel',command=main_window)

#-------------------------------------#
purchase_frame=tk.Frame(window)
purchase_label=tk.Label(purchase_frame,text='Enter the item',width=30)
purchase_label.grid(row=0,column=0,sticky='wens')
purchase_entry=tk.Entry(purchase_frame)
purchase_entry.grid(row=1,column=0,sticky='wens')
purchase_back_btn=tk.Button(purchase_frame,text='Back',command=main_window)
purchase_back_btn.grid(row=2,column=0,sticky='wens')
purchase_label.bind("<Key>",xpurchase)

start_funtion()
window.mainloop()