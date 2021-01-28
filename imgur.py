
from asyncio import sleep
import random
from telethon import functions
from userbot.events import register
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon import events
from .. import loader, utils
import io
from io import BytesIO
from PIL import Image


def register(cb):
    cb(ImgurMod())

class ImgurMod(loader.Module):
    """ты еблан да?"""
    strings = {'name': 'Imgur HAHA'}

    def __init__(self):
        self.name = self.strings['name']
        self._me = None
        self._ratelimit = []

    async def client_ready(self, client, db):
        self._db = db
        self._client = client

    async def imgurcmd(self, event):
        chat = '@ImgUploadBot'
        reply = await event.get_reply_message()
        async with event.client.conversation(chat) as conv:

            if not reply:
                await event.edit("где реплай на медиа.")
                return
            else:
                pic = await check_media(event, reply)
                if not pic:
                    await utils.answer(event, 'это не изображение, лол.')
                    return
            await event.edit("Подождите немножечка 😘")
            try:
                what = lol(pic)
                response = conv.wait_event(events.NewMessage(incoming=True, from_users=985223903))
                await event.client.send_file(chat, what)
                response = await response
            except YouBlockedUserError:
                await event.edit('<code>Разблокируй @imgurbot_bot</code>')
                return
            await event.edit("<b>Ссылка на изображение Imgur - </b>" + response.text)

def lol(reply):
    scrrrra = Image.open(BytesIO(reply))
    out = io.BytesIO()
    out.name = "outsider.png"
    scrrrra.save(out)
    return out.getvalue()




async def check_media(message, reply):
	if reply and reply.media:
		if reply.photo:
			data = reply.photo
		elif reply.document:
			if reply.gif or reply.video or reply.audio or reply.voice:
				return None
			data = reply.media.document
		else:
			return None
	else:
		return None
	if not data or data is None:
		return None
	else:
		data = await message.client.download_file(data, bytes)
		try:
			Image.open(io.BytesIO(data))
			return data
		except:
			return None