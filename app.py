from atexit import register
from flask import Flask,request,render_template
from linebot import *
from linebot.models import *
from liff import *
import sqlite3
import datetime
import requests
import json

app = Flask(__name__)
app.register_blueprint(liff)

line_bot_api = LineBotApi(
    '23b+nzrs7rNbbKUyD1Otoi2bKNtGGnkRCHAtW5nwwP/1oBJWyVYJSe5Rf6M9+Clf5ayjjTHq2MCWxEDYWRTFNP+aMvTPq5YqmURtFrMUpqBF1RiFhAxMRRRM9lvKWigQbiDqreHT6iEKwCfRLdK8HgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('f04224513e99f64fffea6104439212d6')

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/webhook', methods=['POST'] )
def hello():
    req = request.get_json(silent=True,force=True)
    intent = req['queryResult']['intent']['displayName']
    reply_token = req['originalDetectIntentRequest']['payload']['data']['replyToken']
    id_user = req['originalDetectIntentRequest']['payload']['data']['source']['userId']
    reply(intent,reply_token,req,id_user)
    return req

def reply(intent,reply_token,req,id_user):
    if intent =='intent-buy - custom':
        id_item = str(req['queryResult']['outputContexts'][0]['parameters']['id_item.original'])
        number = str(req['queryResult']['outputContexts'][0]['parameters']['number.original'])

        conn = sqlite3.connect('product.db')
        c = conn.cursor()
        c.execute("SELECT * FROM items WHERE id_item == '{}'".format(id_item))
        product = c.fetchall()
        print (id_item, number, product)
        if product == []:
            text_message = TextSendMessage(text='ไม่มีรหัส')
            line_bot_api.reply_message(reply_token,text_message)
        else:
            confirm_template_message = TemplateSendMessage(
                alt_text='Confirm template',
                template=ConfirmTemplate(
                    text='ต้องการซื้อรหัสสินค้า {} จำนวน {} ใช่หรือไม่'.format(id_item,number),
                    actions=[
                        MessageAction(
                            label='ใช่',
                            text='ซื้อสินค้ารหัส {} จำนวน {}'.format(id_item,number)
                        ),
                        MessageAction(
                            label='ไม่ใช่',
                            text='สั่งซื้อสินค้า'
                        )
                    ]
                )
            )
            line_bot_api.reply_message(reply_token,confirm_template_message)

    if intent =='intent-buy - custom - yes':
        id_item = str(req['queryResult']['outputContexts'][0]['parameters']['id_item.original'])
        number = str(req['queryResult']['outputContexts'][0]['parameters']['number.original'])

        conn = sqlite3.connect('product.db')
        c = conn.cursor()
        c.execute("SELECT * FROM items WHERE id_item == '{}'".format(id_item))
        product = c.fetchall()

        if int(number) > int(product[0][2]):
            text_message = TextSendMessage(text='จำนวนสินค้าไม่พอ')
            line_bot_api.reply_message(reply_token,text_message)
        else:
            total = int(product[0][2]) - int(number)

            conn = sqlite3.connect('product.db')
            c = conn.cursor()
            c.execute("""UPDATE items SET sum = ? WHERE id_item = ?""",(total, id_item))
            conn.commit()

            date = datetime.datetime.now()
            id = None
            conn = sqlite3.connect('product.db')
            c = conn.cursor()
            c.execute("""INSERT INTO oder VALUES(?,?,?,?,?)""",(id,id_user,id_item,number,date))
            conn.commit()

            text_message = TextSendMessage(text='บันทึกคำสั่งซื้อเรียบร้อยแล้ว')
            line_bot_api.reply_message(reply_token,text_message)

    if intent == 'Intent-order':
        conn = sqlite3.connect('product.db')
        c = conn.cursor()
        c.execute("SELECT * FROM oder WHERE id_user == '{}'".format(id_user))
        product = c.fetchall()

        if product == []:
            text_message = TextSendMessage(text='ยังไม่ได้สั่งซื้อสินค้า')
            line_bot_api.reply_message(reply_token,text_message)
        else:
            textlist = ''
            for i in product:
                textstring = 'รหัส {} จำนวน {} เวลา {} \n '.format(i[2],i[3],i[4])
                textlist = textlist + textstring
            text_message = TextSendMessage(text=textlist)
            line_bot_api.reply_message(reply_token,text_message)

    if intent == 'intent-items':
        conn = sqlite3.connect('product.db')
        c = conn.cursor()
        c.execute("SELECT * FROM items")
        product = c.fetchall()

        if product == []:
            text_message = TextSendMessage(text='ไม่มีสินค้า')
            line_bot_api.reply_message(reply_token,text_message)
        else:
            textlist = ''
            for i in product:
                textstring = 'รหัส {} จำนวน {}\n '.format(i[1],i[2])
                textlist = textlist + textstring
            text_message = TextSendMessage(text=textlist)
            line_bot_api.reply_message(reply_token,text_message)

    if intent == 'Intent-talk':
        line_bot_api.link_rich_menu_to_user(id_user, 'richmenu-bfceb94cf459af46c32a9cde221dc03b')
        text_message = TextSendMessage(text='พูดคุยได้เลย')
        line_bot_api.reply_message(reply_token,text_message)
    
    if intent == 'intent-talk-out':
        confirm_template_message = TemplateSendMessage(
            alt_text='Confirm template',
            template=ConfirmTemplate(
                text='ต้องการหยุดการสนทนาหรือไม่',
                actions=[
                    MessageAction(
                        label='ใช่',
                        text='ใช่'
                    ),
                    MessageAction(
                        label='ไม่ใช่',
                        text='พูดคุยทั่วไป'
                    )
                ]
            )
        )
        line_bot_api.reply_message(reply_token,confirm_template_message)

    if intent == 'intent-talk-out - yes':
        line_bot_api.unlink_rich_menu_from_user(id_user)

    if intent == 'intent-covid19':
        data = requests.get('https://covid19.ddc.moph.go.th/api/Cases/today-cases-all')
        json_data = json.loads(data.text)
        New_case = json_data[0]['new_case']
        New_death = json_data[0]['new_death']
        Update_date = json_data[0]['update_date']
        text_message = TextSendMessage(text='จำนวนผู้ติดเชื้อรายใหม่ :{}\n'
                                            'จำนวนผู้เสียชีวิตรายใหม่ :{}\n'
                                            'อัพเดทล่าสุด :{}'.format(New_case,New_death,Update_date))
        line_bot_api.reply_message(reply_token,text_message)
    
    if intent == 'intent-liff':
        carousel_template_message = TemplateSendMessage(
            alt_text='Carousel template',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url='https://1drv.ms/u/s!AoQU7MaJ_kg9g_oUXA-h4_u3QCuCyA',
                        title='My LIFF',
                        text='TEST',
                        actions=[
                            URIAction(
                                label='my liff',
                                uri='https://liff.line.me/1657118028-YpRr0WWp/liff'
                            ),
                            URIAction(
                                label='แบบประเมินความเครียร์',
                                uri='https://liff.line.me/1657118028-YpRr0WWp/st5'
                            )
                        ]
                    )
                ]
            )
        )
        line_bot_api.reply_message(reply_token, carousel_template_message) 

if __name__=='__main__':
    app.run(debug=True)
