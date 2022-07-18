from flask import *
from linebot import *
from linebot.models import *
import sqlite3

liff = Blueprint('liff', __name__)

line_bot_api = LineBotApi(
    '23b+nzrs7rNbbKUyD1Otoi2bKNtGGnkRCHAtW5nwwP/1oBJWyVYJSe5Rf6M9+Clf5ayjjTHq2MCWxEDYWRTFNP+aMvTPq5YqmURtFrMUpqBF1RiFhAxMRRRM9lvKWigQbiDqreHT6iEKwCfRLdK8HgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('f04224513e99f64fffea6104439212d6')

@liff.route('/liff', methods=['POST','GET'])
def myliff():
    if request.method == 'POST':
        id_user = request.form['userId']
        displayName = request.form['displayName']
        
        id = None
        conn = sqlite3.connect('member.db')
        c = conn.cursor()
        c.execute("""INSERT INTO user VALUES(?,?,?)""",
                   (id, id_user, displayName))
        conn.commit()
        return render_template('close.html')
    else:
        return render_template('liff.html')

@liff.route('/st5', methods=['POST','GET'])
def st5():
    if request.method == 'POST':
        id_user = request.form['userId']
        q1 = int(request.form['q1'])
        q2 = int(request.form['q2'])
        q3 = int(request.form['q3'])
        q4 = int(request.form['q4'])
        q5 = int(request.form['q5'])
        sum = q1+q2+q3+q4+q5
        if sum <= 4:
            text_message = TextSendMessage(text='เครียดน้อย')
            line_bot_api.push_message(id_user, text_message)
        if sum > 4 and sum <= 7:
            text_message = TextSendMessage(text='เครียดปานกลาง')
            line_bot_api.push_message(id_user, text_message)
        if sum > 7 and sum <= 9:
            text_message = TextSendMessage(text='เครียดมาก')
            line_bot_api.push_message(id_user, text_message)   
        if sum > 9:
            text_message = TextSendMessage(text='เครียดมากที่สุด')
            line_bot_api.push_message(id_user, text_message)   
        return render_template('close.html')
    else:
        return render_template('st5.html')