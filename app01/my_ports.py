import json

import requests
import coder


def my_post(url, ope, load="") -> requests.Response:
    key = coder.encode("the_long_dark", "coderX")
    headers = {'content-Type': 'application/json', 'Accept': '*/*'}
    data = {
        "ope": ope,
        "portKey": key,
        "load": load,
    }
    data = json.dumps(data)
    return requests.post(url=url, data=data, headers=headers)
