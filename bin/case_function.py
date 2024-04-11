import json
import requests
import sys
import os
from os.path import dirname, abspath
d = dirname(dirname(abspath(__file__)))
sys.path.append(os.path.join(d, "config"))
import config as Config

headers={'X-API-KEY': Config.FLOWINTEL_API_KEY}

def request_post_flowintel(url, data, content_type = 'application/json', matrix_id = None):
    headers["Content-Type"] = content_type
    if matrix_id:
        headers["MATRIX-ID"] = matrix_id
    res = requests.post(f"{Config.FLOWINTEL_URL}/api/case/{url}", json=data, headers=headers)
    return res

def request_get_flowintel(url, matrix_id = None):
    if matrix_id:
        headers["MATRIX-ID"] = matrix_id
    res = requests.get(f"{Config.FLOWINTEL_URL}/api/case/{url}", headers=headers)
    return res

async def check_format(bot, match, message, room, size):
    if not len(match.args()) >= size:
        await bot.api.send_text_message(room.room_id, "Not enough argument", reply_to=message.event_id)
        return False
    return True

async def check_matrix_id(bot, message, room):
    res = requests.get(f"{Config.FLOWINTEL_URL}/api/admin/user_matrix_id?matrix_id={message.sender}", headers=headers)
    if "message" in res.json():
        loc_message = res.json()["message"]
        await bot.api.send_markdown_message(room.room_id, loc_message, reply_to=message.event_id)
        return False
    return res


async def send_markdown(bot, message, room, res):
    if "message" in res.json():
        loc_message = res.json()["message"]
    else:
        loc_message = f"```JSON\n{json.dumps(res.json(), indent=2)}\n```"
    await bot.api.send_markdown_message(room.room_id, loc_message, reply_to=message.event_id)


async def modify_case(bot, match, message, room, type):
    """Modify title or description of a case"""
    args_list = match.args()[1:]
    case_id = match.args()[0]

    data = {type: " ".join(arg for arg in args_list)}
    res = request_post_flowintel(f"{case_id}/edit", data, matrix_id=message.sender)
    return send_markdown(bot, message, room, res)


async def case_check(bot, match, message, room):
    """All ckeck for case part"""
    last_command = ""
    if match.command("create_case"):
        last_command = message
        if await check_format(bot, match, message, room, 1):
            data = {"title": " ".join(arg for arg in match.args())}
            res = request_post_flowintel("create", data, matrix_id=message.sender)
            if "message" in res.json():
                loc_message = res.json()["message"]
            else:
                loc_message = f"```JSON\n{json.dumps(res.json(), indent=2)}\n```"
            await bot.api.send_text_message(room.room_id, loc_message, reply_to=message.event_id)

    if match.command("case_title"):
        last_command = message
        if await check_format(bot, match, message, room, 1):
            data = {"title": " ".join(arg for arg in match.args())}
            res = request_post_flowintel("title", data)
            await send_markdown(bot, message, room, res)            

    if match.command("case"):
        last_command = message
        if await check_format(bot, match, message, room, 1):
            res = request_get_flowintel(match.args()[0])
            await send_markdown(bot, message, room, res)
            

    if match.command("modify_title"):
        last_command = message
        if await check_format(bot, match, message, room, 2):
            await modify_case(bot, match, message, room, "title")
            
    if match.command("modify_description"):
        if await check_format(bot, match, message, room, 2):
            await modify_case(bot, match, message, room, "description")

    if match.command("complete_case"):
        last_command = message
        if await check_format(bot, match, message, room, 1):
            res = request_get_flowintel(f"{match.args()[0]}/complete", matrix_id=message.sender)
            await send_markdown(bot, message, room, res)

    if match.command("case_tasks"):
        last_command = message
        if await check_format(bot, match, message, room, 1):
            res = request_get_flowintel(f"{match.args()[0]}/tasks")
            await send_markdown(bot, message, room, res)

    if match.command("case_note"):
        last_command = message
        if await check_format(bot, match, message, room, 1):
            res = request_get_flowintel(f"{match.args()[0]}/get_note")
            await send_markdown(bot, message, room, res)

    if match.command("case_modify_note"):
        last_command = message
        if await check_format(bot, match, message, room, 2):
            args_list = match.args()[1:]
            case_id = match.args()[0]
            data = {"note": " ".join(arg for arg in args_list)}
            res = request_post_flowintel(f"{case_id}/modif_case_note", data, matrix_id=message.sender)
            await send_markdown(bot, message, room, res)
            

    if match.command("case_all_notes"):
        last_command = message
        if await check_format(bot, match, message, room, 1):
            res = request_get_flowintel(f"{match.args()[0]}/all_notes")
            await send_markdown(bot, message, room, res)

    if match.command("case_all_users"):
        last_command = message
        if await check_format(bot, match, message, room, 1):
            res = request_get_flowintel(f"{match.args()[0]}/get_all_users")
            await send_markdown(bot, message, room, res)

    if match.command("list_status"):
        last_command = message
        if await check_format(bot, match, message, room, 1):
            res = request_get_flowintel(f"list_status")
            await send_markdown(bot, message, room, res)

    if match.command("case_status"):
        last_command = message
        if await check_format(bot, match, message, room, 1):
            res = request_get_flowintel(match.args()[0])
            if "message" in res.json():
                loc_message = res.json()["message"]
            else:
                res_status = request_get_flowintel(f"list_status")
                loc_message = "Status not found"
                for status in res_status.json():
                    if status["id"] == res.json()["status_id"]:
                        loc_message = f"Case is `{status['name']}`"
            await bot.api.send_markdown_message(room.room_id, loc_message, reply_to=message.event_id)

    if match.command("case_modify_status"):
        last_command = message
        if await check_format(bot, match, message, room, 2):
            case_id = match.args()[0]
            status_id = match.args()[1]
            data = {"status_id": status_id}

            res = request_post_flowintel(f"{case_id}/change_status", data, matrix_id=message.sender)
            await send_markdown(bot, message, room, res)


    if last_command:
        return last_command
    