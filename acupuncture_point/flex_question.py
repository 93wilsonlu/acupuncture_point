class FlexQuestion:
    def __init__(self, question_type, disease):
        self.message = {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": f"下列哪個{question_type}可治{disease}？",
                        "weight": "bold",
                        "size": "md"
                    },
                ]
            }
        }

    def add_item(self, name):
        new_item = {
            "type": "box",
            "layout": "horizontal",
            "contents": [
                {
                    "type": "text",
                    "text": name,
                    "size": "md"
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {
                            "type": "text",
                            "text": "選擇",
                            "color": "#ffffff",
                            "align": "center"
                        }
                    ],
                    "backgroundColor": "#19c951",
                    "width": "60px",
                    "height": "35px",
                    "cornerRadius": "md",
                    "action": {
                        "type": "message",
                        "label": "action",
                        "text": name
                    },
                    "alignItems": "center"
                }
            ],
            "margin": "sm",
            "alignItems": "center"
        }
        self.message['body']['contents'].append(new_item)
