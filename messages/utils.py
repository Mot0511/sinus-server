import json


def get_broadcast_message(type, content):
    return json.dumps({
        'type': type,
        'content': content
    })