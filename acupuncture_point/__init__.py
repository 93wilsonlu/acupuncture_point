from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, QuickReply, QuickReplyButton, MessageAction
from .config import config_dict
import os
import random
import json

line_bot_api = LineBotApi(os.environ.get('CHANNEL_ACCESS_TOKEN'))
handler = WebhookHandler(os.environ.get('CHANNEL_SECRET'))

with open('data.json', 'r') as f:
    data = json.load(f)

context = {}
feature_set = set()

for point in data:
    feature_set.update(point['feature'])


def handle_start(event):
    point = random.choice(data)
    context[event.source.user_id] = point

    answer = random.choice(point['feature'])
    options = random.sample(tuple(feature_set.difference({answer})), k=3)
    options.append(answer)

    quick_reply_items = []
    for option in options:
        quick_reply_items.append(QuickReplyButton(
            action=MessageAction(label=option, text=option)))

    line_bot_api.reply_message(event.reply_token, TextSendMessage(
        text=point['name'], quick_reply=QuickReply(items=quick_reply_items)))


def handle_reply(event):
    point = context[event.source.user_id]
    if event.message.text in point['feature']:
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text="正確"))
    else:
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text="錯誤"))
    context.pop(event.source.user_id)


def handle_other(event):
    line_bot_api.reply_message(
        event.reply_token, TextSendMessage(text="無法處理這則訊息"))


def create_app(config='develop'):
    app = Flask(__name__)
    app.config.from_object(config_dict[config])

    @app.route("/callback", methods=['POST'])
    def callback():
        signature = request.headers['X-Line-Signature']

        body = request.get_data(as_text=True)
        app.logger.info("Request body: " + body)

        try:
            handler.handle(body, signature)
        except InvalidSignatureError:
            abort(400)

        return 'OK'

    @app.shell_context_processor
    def make_shell_context():
        return dict(app=app)

    @handler.add(MessageEvent, message=TextMessage)
    def main_handler(event):
        try:
            if event.message.text == 'start':
                handle_start(event)
            elif context.get(event.source.user_id):
                handle_reply(event)
            else:
                handle_other(event)
        except:
            handle_other(event)

    return app
