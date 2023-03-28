from __future__ import unicode_literals
import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from pyModbusTCP.client import ModbusClient

import configparser
HOST1 = "140.124.39.112"
PORT1 = 502

cost=0
c1 = ModbusClient()
c2 = ModbusClient()

c1.host(HOST1)
c1.unit_id(1)

app = Flask(__name__)

# LINE 聊天機器人的基本資料
config = configparser.ConfigParser()
config.read('D:\專題1\python\LineBot\config.ini')
print(config.get('line-bot','channel_secret'))

line_bot_api = LineBotApi(config.get('line-bot', 'channel_access_token'))
handler = WebhookHandler(config.get('line-bot', 'channel_secret'))


def Read_register(reg,nb): #讀取暫存器

    # rd=0
    # rds=[] 

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
    pass
# 接收 LINE 的資訊
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    
    try:
        print(body, signature)
        handler.handle(body, signature)
        
    except InvalidSignatureError:
        abort(400)

    return 'OK'

# 學你說話
@handler.add(MessageEvent, message=TextMessage)
def pretty_echo(event):
    
    input_text=event.message.text
    quantity=Read_register(4157,6)
    money=Read_register(4147,6)
    money=[10,20,30,40,50,60]
    quantity=[1,2,1,1,2,3]

    situation_quan1=Read_register(4107,3)
    situation_quan1=[1,2,0]
    situation_quan2=Read_register(4117,3)
    situation_quan2=[2,5,5]
    situation_quan=situation_quan1+situation_quan2
    message=''
    if input_text=="Warehousing situation":
        for i in range(6):
            if situation_quan[i]==0:
                message+="Grid "+str(i+1)+" is empty"
            else:
                message+="Grid "+str(i+1)+" is item "+str(situation_quan[i])
            if i!=5:
                message+="\n"

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=message),
        ) 
        
    elif input_text=="Unmanned store situation":
        

        for i in range(6):

            message+="Item "+str(i+1)+" price："+str(money[i]) + "    Item "+str(i+1)+" amount："+str(quantity[i])

            if i!=5:
                message+="\n"
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=message),
        ) 


if __name__ == "__main__":
    app.run()