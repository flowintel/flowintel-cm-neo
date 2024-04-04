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


async def task_check(bot, match, message, room):
    """All ckeck for task part"""
    last_command = ""
    if match.command("create_task"):
        args_list = match.args()[1:]
        case_id = match.args()[0]
        data = {"title": " ".join(arg for arg in args_list)}
        res = request_post_flowintel(f"{case_id}/create_task", data)
        if "message" in res.json():
            loc_message = res.json()["message"]
        else:
            loc_message = f"```JSON\n{json.dumps(res.json(), indent=2)}\n```"
        last_command = message
        await bot.api.send_text_message(room.room_id, loc_message, reply_to=message.event_id)
    
    if match.command("my_assignment"):
        res = requests.get(f"{Config.FLOWINTEL_URL}/api/admin/user_matrix_id?matrix_id={message.sender}", headers=headers)
        if "message" in res.json():
            loc_message = res.json()["message"]
            await bot.api.send_markdown_message(room.room_id, loc_message, reply_to=message.event_id)
        else:
            loc_res = res.json()

            res = requests.get(f"{Config.FLOWINTEL_URL}/api/my_assignment/user?user_id={loc_res['id']}", headers=headers)
            if "message" in res.json():
                loc_message = res.json()["message"]
            else:
                loc_message = f"```JSON\n{json.dumps(res.json(), indent=2)}\n```"
            await bot.api.send_markdown_message(room.room_id, loc_message, reply_to=message.event_id)
    
        last_command = message

    if last_command:
        return last_command