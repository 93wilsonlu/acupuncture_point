from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, FlexSendMessage
from .config import config_dict
import os
import random
import json
from .flex_question import FlexQuestion

line_bot_api = LineBotApi(os.environ.get('CHANNEL_ACCESS_TOKEN'))
handler = WebhookHandler(os.environ.get('CHANNEL_SECRET'))

with open('data.json', 'r') as f:
    data = json.load(f)

context = {}


def handle_start(event):
    question_type = random.choice(['穴道','中藥'])
    options = random.sample(tuple(data[question_type].keys()), k=5)
    answer = random.choice(options)
    disease = random.choice(data[question_type][answer])
    context[event.source.user_id] = question_type, disease, answer

    flex = FlexQuestion(question_type, disease)
    for option in options:
        flex.add_item(option)

    line_bot_api.reply_message(event.reply_token, FlexSendMessage(alt_text='目前伺服器錯誤', contents=flex.message))


def handle_reply(event):
    question_type, disease, answer = context[event.source.user_id]
    if disease in data[question_type][event.message.text]:
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text='正確'))
    else:
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=f'錯誤，答案應為「{answer}」'))
    context.pop(event.source.user_id)


def handle_other(event):
    line_bot_api.reply_message(
        event.reply_token, TextSendMessage(text="無法處理這則訊息，請重新按「開始」"))


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
        except Exception as e:
            handle_other(event)
            print(e)

    return app
