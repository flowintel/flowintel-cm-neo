import json
import requests
import sys
import os
from os.path import dirname, abspath
d = dirname(dirname(abspath(__file__)))
sys.path.append(os.path.join(d, "config"))
import config as Config

headers={'X-API-KEY': Config.FLOWINTEL_API_KEY}

def request_post_flowintel(url, data, content_type = 'application/json'):
    headers["Content-Type"] = content_type
    res = requests.post(f"{Config.FLOWINTEL_URL}/api/case/{url}", json=data, headers=headers)
    return res

def request_get_flowintel(url):
    res = requests.get(f"{Config.FLOWINTEL_URL}/api/case/{url}", headers=headers)
    return res


async def modify_case(bot, match, message, room, type):
    """Modify title or description of a case"""
    args_list = match.args()[1:]
    case_id = match.args()[0]

    data = {type: " ".join(arg for arg in args_list)}
    res = request_post_flowintel(f"{case_id}/edit", data)
    if "message" in res.json():
        loc_message = res.json()["message"]
    else:
        loc_message = f"```JSON\n{json.dumps(res.json(), indent=2)}\n```"
    last_command = message
    await bot.api.send_markdown_message(room.room_id, loc_message, reply_to=message.event_id)
    return last_command


async def case_check(bot, match, message, room):
    """All ckeck for case part"""
    last_command = ""
    if match.command("create_case"):
        data = {"title": " ".join(arg for arg in match.args())}
        res = request_post_flowintel("create", data)
        if "message" in res.json():
            loc_message = res.json()["message"]
        else:
            loc_message = f"```JSON\n{json.dumps(res.json(), indent=2)}\n```"
        last_command = message
        await bot.api.send_text_message(room.room_id, loc_message, reply_to=message.event_id)

    if match.command("case_title"):
        data = {"title": " ".join(arg for arg in match.args())}
        res = request_post_flowintel("title", data)
        if "message" in res.json():
            loc_message = res.json()["message"]
        else:
            loc_message = f"```JSON\n{json.dumps(res.json(), indent=2)}\n```"
        last_command = message
        await bot.api.send_markdown_message(room.room_id, loc_message, reply_to=message.event_id)

    if match.command("case_id"):
        res = request_get_flowintel(match.args()[0])
        if "message" in res.json():
            loc_message = res.json()["message"]
        else:
            loc_message = f"```JSON\n{json.dumps(res.json(), indent=2)}\n```"
        last_command = message
        await bot.api.send_markdown_message(room.room_id, loc_message, reply_to=message.event_id)

    if match.command("modify_title"):
        last_command = modify_case(bot, match, message, room, "title")

    if match.command("modify_description"):
        last_command = modify_case(bot, match, message, room, "description")

    if match.command("complete_case"):
        res = request_get_flowintel(f"{match.args()[0]}/complete")
        if "message" in res.json():
            loc_message = res.json()["message"]
        else:
            loc_message = f"```JSON\n{json.dumps(res.json(), indent=2)}\n```"
        last_command = message
        await bot.api.send_markdown_message(room.room_id, loc_message, reply_to=message.event_id)



    if last_command:
        return last_command