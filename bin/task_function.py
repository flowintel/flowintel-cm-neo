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
    res = requests.post(f"{Config.FLOWINTEL_URL}/api/task/{url}", json=data, headers=headers)
    return res

def request_get_flowintel(url, matrix_id = None):
    if matrix_id:
        headers["MATRIX-ID"] = matrix_id
    res = requests.get(f"{Config.FLOWINTEL_URL}/api/task/{url}", headers=headers)
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

    
async def modify_task(bot, match, message, room, type):
    """Modify title or description of a case"""
    args_list = match.args()[1:]
    task_id = match.args()[0]

    data = {type: " ".join(arg for arg in args_list)}
    res = request_post_flowintel(f"{task_id}/edit", data)
    send_markdown(bot, message, room, res)


async def task_check(bot, match, message, room):
    """All ckeck for task part"""
    last_command = ""
    if match.command("create_task"):
        last_command = message
        if await check_format(bot, match, message, room, 1):
            res = await check_matrix_id(bot, message, room)
            if res:
                args_list = match.args()[1:]
                case_id = match.args()[0]
                data = {"title": " ".join(arg for arg in args_list)}

                headers["Content-Type"] = 'application/json'
                headers["MATRIX-ID"] = message.sender
                res = requests.post(f"{Config.FLOWINTEL_URL}/api/case/{case_id}/create_task", json=data, headers=headers)

                await send_markdown(bot, message, room, res)
            
    if match.command("task"):
        last_command = message
        if await check_format(bot, match, message, room, 1):
            res = request_get_flowintel(match.args()[0])
            await send_markdown(bot, message, room, res)

    if match.command("task_title"):
        last_command = message
        if await check_format(bot, match, message, room, 1):
            data = {"title": " ".join(arg for arg in match.args())}
            res = request_post_flowintel("title", data)
            await send_markdown(bot, message, room, res)   
    
    if match.command("my_assignment"):
        last_command = message
        res = await check_matrix_id(bot, message, room)
        if res:
            loc_res = res.json()

            res = requests.get(f"{Config.FLOWINTEL_URL}/api/my_assignment/user?user_id={loc_res['id']}", headers=headers)
            last_command = await send_markdown(bot, message, room, res)
        
    if match.command("modify_title"):
        last_command = message
        if await check_format(bot, match, message, room, 2):
            await modify_task(bot, match, message, room, "title")

    if match.command("modify_description"):
        last_command = message
        if await check_format(bot, match, message, room, 2):
            await modify_task(bot, match, message, room, "description")

    if match.command("complete_task"):
        last_command = message
        res = request_get_flowintel(f"{match.args()[0]}/complete")
        await send_markdown(bot, message, room, res)
    
    if match.command("create_note"):
        last_command = message
        if await check_format(bot, match, message, room, 2):
            task_id = match.args()[0]
            args_list = match.args()[1:]
            data = {"note": " ".join(arg for arg in args_list)}

            res = request_post_flowintel(f"{task_id}/create_note", data, matrix_id=message.sender)
            await send_markdown(bot, message, room, res)
    
    if match.command("task_get_all_notes"):
        last_command = message
        if await check_format(bot, match, message, room, 1):
            task_id = match.args()[0]

            res = request_get_flowintel(f"{task_id}/get_all_notes")
            await send_markdown(bot, message, room, res)

    if match.command("task_get_note"):
        last_command = message
        if await check_format(bot, match, message, room, 2):
            task_id = match.args()[0]
            note_id = match.args()[1]

            res = request_get_flowintel(f"{task_id}/get_note?note_id={note_id}")
            await send_markdown(bot, message, room, res)

    if match.command("task_modify_note"):
        last_command = message
        if await check_format(bot, match, message, room, 3):
            task_id = match.args()[0]
            note_id = match.args()[1]
            args_list = match.args()[2:]
            data = {"note_id": note_id, "note": " ".join(arg for arg in args_list)}

            res = request_post_flowintel(f"{task_id}/modif_note", data, matrix_id=message.sender)
            await send_markdown(bot, message, room, res)

    if match.command("delete_note"):
        last_command = message
        if await check_format(bot, match, message, room, 2):
            task_id = match.args()[0]
            note_id = match.args()[1]

            res = request_get_flowintel(f"{task_id}/delete_note?note_id={note_id}")
            await send_markdown(bot, message, room, res)

    if match.command("take_task"):
        last_command = message
        if await check_format(bot, match, message, room, 1):
            task_id = match.args()[0]

            res = request_get_flowintel(f"{task_id}/take_task", matrix_id=message.sender)
            await send_markdown(bot, message, room, res)

    if match.command("remove_assignment"):
        last_command = message
        if await check_format(bot, match, message, room, 1):
            task_id = match.args()[0]
            res = request_get_flowintel(f"{task_id}/remove_assignment", matrix_id=message.sender)
            await send_markdown(bot, message, room, res)

    if match.command("task_status"):
        last_command = message
        if await check_format(bot, match, message, room, 1):
            res = request_get_flowintel(match.args()[0])
            if "message" in res.json():
                loc_message = res.json()["message"]
            else:
                res_status = request_get_flowintel(f"list_status")
                loc_message = "Status not found"
                for status in res_status.json():
                    if status["id"] == res.json()["task"]["status_id"]:
                        loc_message = f"Task is `{status['name']}`"
            await bot.api.send_markdown_message(room.room_id, loc_message, reply_to=message.event_id)


    if match.command("task_modify_status"):
        last_command = message
        if await check_format(bot, match, message, room, 2):
            task_id = match.args()[0]
            status_id = match.args()[1]
            data = {"status_id": status_id}

            res = request_post_flowintel(f"{task_id}/change_status", data, matrix_id=message.sender)
            await send_markdown(bot, message, room, res)
        

    if last_command:
        return last_command