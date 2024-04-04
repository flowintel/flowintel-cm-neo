"""
Example Usage:

random_user
      !case something
"""

import simplematrixbotlib as botlib
import sys
import os
from os.path import dirname, abspath
d = dirname(dirname(abspath(__file__)))
sys.path.append(os.path.join(d, "config"))
import config as Config
from help import help

from case_function import case_check
from task_function import task_check

config = botlib.Config()
config.encryption_enabled = True  # Automatically enabled by installing encryption support
config.ignore_unverified_devices = True

creds = botlib.Creds(Config.MATRIX_SERVER, Config.MATRIX_USER, Config.MATRIX_PASSWORD, device_name=Config.MATRIX_DEVICE_NAME)
bot = botlib.Bot(creds, config)
PREFIX = '!'


last_command = ""


@bot.listener.on_message_event
async def echo(room, message):
    global last_command
    match = botlib.MessageMatch(room, message, bot, PREFIX)

    if match.is_not_from_this_bot() and match.prefix():
        if match.command("help"):
            loc_message = help()
            last_command = message
            await bot.api.send_markdown_message(room.room_id, loc_message, reply_to=message.event_id)

        if match.command("last_command"):
            if last_command:
                loc_message = f"```\n{last_command.body}```"
            else:
                loc_message = "```\nNo last command```"
            last_command = message
            await bot.api.send_markdown_message(room.room_id, loc_message, reply_to=message.event_id)
        
        if match.command("url"):
            loc_message = Config.FLOWINTEL_URL
            last_command = message
            await bot.api.send_text_message(room.room_id, loc_message, reply_to=message.event_id)

        loc = await case_check(bot, match, message, room)
        if loc:
            last_command = loc
        
        loc = await task_check(bot, match, message, room)
        if loc:
            last_command = loc

bot.run()
