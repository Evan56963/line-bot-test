from flask import Flask, request
import json
import random
import os
from linebot import WebhookParser, LineBotApi
from linebot.models import MessageEvent, TextSendMessage

app = Flask(__name__)

# line settings
parser = WebhookParser("75069bdcd19f141d8e86437dd129107b")  # change to your line secretKey

# change to your line channel access token
line_bot_api = LineBotApi(
    "r3dtxCqBOw0pkkarOvnAsxDP0PDVKZhQzri0YJZXSpJf5PSEX1WpSMlvYev/oBz0VfyxEvGd5Geu+YhSjKJNmzoVRGDamXK3oj0H9QKH+jxHKJzJuUdEYdl8CZPRpoyQAl8LuMUherfoW7lC+6KDwgdB04t89/1O/w1cDnyilFU=")


@app.route("/lineHook", methods=['POST'])
def lineBot():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        events = parser.parse(body, signature)  # 傳入的事件
    except:
        return {"message": "failed"}

    for event in events:
        if isinstance(event, MessageEvent):  # 如果有訊息事件

            with open('dictionary.json', encoding='utf-8-sig') as file:
                data = json.load(file)

            if event.message.text in data:
                if len(data[event.message.text]) > 1:
                    responseNum = random.randint(0, len(data[event.message.text]) - 1)
                    responseText = data[event.message.text][responseNum]
                else:
                    responseText = data[event.message.text][0]

            else:
                responseText = "我聽不懂你說的話"

            line_bot_api.reply_message(  # 回覆傳入的訊息文字
                event.reply_token,
                TextSendMessage(text=responseText)
            )

    return {"message": "success"}

@app.route("/", methods=['GET'])
def test():
    text = request.args.get("text")

    with open('dictionary.json', encoding='utf-8-sig') as file:
        data = json.load(file)
    if text in data:
        if len(data[text]) > 1:
            responseNum = random.randint(0, len(data[text]) - 1)
            responseText = data[text][responseNum]
        else:
            responseText = data[text][0]
    else:
        responseText = "我聽不懂你說的話"
    print(responseText)
    return {"message": responseText}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
