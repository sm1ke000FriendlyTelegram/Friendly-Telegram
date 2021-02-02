#Changed by @Sm1ke (Telegram)
from telethon import events
from .. import loader, utils
import os
import requests
from PIL import Image,ImageFont,ImageDraw 
import re
import io
from textwrap import wrap

def register(cb):
 cb(StickMod())
 
class StickMod(loader.Module):
 """StickMod"""
 strings = {
  'name': 'StickMod',
  'usage': 'ТАК СЛОЖНО НАПИСАТЬ <code>.help StickMod</code>',
 }
 def init(self):
  self.name = self.strings['name']
  self._me = None
  self._ratelimit = []
 async def client_ready(self, client, db):
  self._db = db
  self._client = client
  self.me = await client.get_me()
  
 async def axcmd(self, message):
  """.ax<реплай на сообщение/свой текст"""
  
  ufr = requests.get("https://github.com/LaciaMemeFrame/FTG-Modules/raw/master/zfont.ttf")
  f = ufr.content
  
  reply = await message.get_reply_message()
  args = utils.get_args_raw(message)
  if not args:
   if not reply:
    await utils.answer(message, self.strings('usage', message))
    return
   else:
    txt = reply.raw_text
  else:
   txt = utils.get_args_raw(message)
  await message.edit("<b>Думаю...</b>")
  pic = requests.get("https://imgur.com/GUhwUAP.jpg")
  pic.raw.decode_content = True
  img = Image.open(io.BytesIO(pic.content)).convert("RGB")
 
  W, H = img.size
  #txt = txt.replace("\n", "𓃐")
  text = "\n".join(wrap(txt, 25))
  t = text + "\n"
  #t = t.replace("𓃐","\n")
  draw = ImageDraw.Draw(img)
  font = ImageFont.truetype(io.BytesIO(f), 32, encoding='UTF-8')
  w, h = draw.multiline_textsize(t, font=font)
  imtext = Image.new("RGBA", (w+10, h+10), (0, 0,0,0))
  draw = ImageDraw.Draw(imtext)
  draw.multiline_text((20, 20),t,(10,0,10),font=font, align='left')
  imtext.thumbnail((340, 182))
  w, h = 340, 182
  img.paste(imtext, (20,20), imtext)
  out = io.BytesIO()
  out.name = "@Sm1ke.jpg"
  img.save(out)
  out.seek(0)
  await message.client.send_file(message.to_id, out, reply_to=reply)
  await message.delete()