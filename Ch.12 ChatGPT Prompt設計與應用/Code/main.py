from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *
import openai
import os

#GPT回復
from response import GPT

#取得相關的QA問題
from get_QA import get_QAlist
QA_list = get_QAlist('050-104-001.csv')

# 取得.env資料
from dotenv import load_dotenv
load_dotenv()

# 文本相似度檢測模型
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('DMetaSoul/sbert-chinese-general-v2')

app = Flask(__name__)

#linebot設定
line_bot_api = LineBotApi(os.getenv('ACCESS_TOKEN'))
handler = WebhookHandler(os.getenv('CHANNEL_SECRET'))

#GPT設定
openai.api_type = "azure"
openai.api_version = "2023-05-15" 
openai.api_base = os.getenv('API_ENDPOINT')
openai.api_key = os.getenv('API_KEY')
gpt_version = os.getenv('GPT_VERSION')

#建立用戶資料
user = {}

@app.route("/", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    #取得用戶對話與系統辨識ID
    msg, ID = event.message.text, event.source.user_id
    if ID not in user:
        user[ID] = [{"role": "user", "content": ''}]
        
    user[ID].append({"role": "user", "content": msg}) # 用戶輸入
    response = GPT(model, user[ID], QA_list, gpt_version) #GPT生成
    user[ID].append({"role": "assistant", "content": response}) #GPT回復
    
    #Line 回復
    message = TextSendMessage(text=response)
    line_bot_api.reply_message(event.reply_token, message)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80,debug=True)