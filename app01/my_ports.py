import json

import requests
import coder


def post_something():
    post_url = "http://127.0.0.1:8000/port/"
    key = coder.encode("the_long_dark", "coderX")
    headers = {'content-Type': 'application/json', 'Accept': '*/*'}
    data = {
        "ope": "buyOrder",
        "portKey": key,
        "load": [{"1": 1, "2": 2}, 123],
    }
    data = json.dumps(data)
    requests.post(url=post_url, data=data, headers=headers)
