﻿# creator by @Sm1ke

import asyncio
from asyncio import wait, sleep

from userbot import BOTLOG, BOTLOG_CHATID, CMD_HELP
from userbot.events import register






@register(outgoing=True, pattern="^.spam (.*)")
async def spammer(e):
    counter = int(e.pattern_match.group(1).split(' ', 1)[0])
    spam_message = str(e.pattern_match.group(1).split(' ', 1)[1])
    await e.delete()
    await asyncio.wait([e.respond(spam_message) for i in range(counter)])
    if BOTLOG:
        await e.client.send_message(BOTLOG_CHATID, "#SPAM\n"
                                    "Spam was executed successfully")




