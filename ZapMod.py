from telethon import events 
from .. import loader, utils 
import os 
import requests 
from PIL import Image 
from PIL import ImageFont 
from PIL import ImageDraw  
import re 
import io 
from textwrap import wrap 
 
def register(cb): 
 cb(ZapomniNaBudycheeMod()) 
  
class ZapomniMod(loader.Module): 
 """Запомни на будущее""" 
 strings = {'name': 'Запомни на будущее '} 
 def init(self): 
  self.name = self.strings['name'] 
  self._me = None 
  self._ratelimit = [] 
 async def client_ready(self, client, db): 
  self._db = db 
  self._client = client 
  self.me = await client.get_me() 
   
 async def zapcmd(self, message): 
  """.zap <reply to user/text>""" 
   
  ufr = requests.get("https://github.com/LaciaMemeFrame/FTG-Modules/raw/master/zfont.ttf") 
  f = ufr.content 
   
  reply = await message.get_reply_message() 
  txet = utils.get_args_raw(message) 
  if not txet: 
   if not reply: 
    await message.edit("text?") 
   else: 
    txt = reply.raw_text 
  else: 
   txt = utils.get_args_raw(message) 
 
 
  await message.edit("<b>Запомни...</b>") 
  pic = requests.get("https://imgur.com/Tk4klNN.jpg") 
  pic.raw.decode_content = True 
  img = Image.open(io.BytesIO(pic.content)).convert("RGB") 
  black = Image.new("RGBA", img.size, (0, 0, 0, 100)) 
  img.paste(black, (0, 0), black) 
  
  W, H = img.size 
  txt = txt.replace("\n", "𓃐") 
  text = "\n".join(wrap(txt, 40)) 
  t = "Запомни на будущее:\n" +text 
  t = t.replace("𓃐","\n") 
  draw = ImageDraw.Draw(img) 
  font = ImageFont.truetype(io.BytesIO(f), 32, encoding='UTF-8') 
  w, h = draw.multiline_textsize(t, font=font) 
  imtext = Image.new("RGBA", (w+20, h+20), (0, 0,0,0)) 
  draw = ImageDraw.Draw(imtext) 
  draw.multiline_text((10, 10),t,(255,255,255),font=font, align='center') 
  imtext.thumbnail((W, H)) 
  w, h = imtext.size 
  img.paste(imtext, ((W-w)//2,(H-h)//2), imtext) 
  out = io.BytesIO() 
  out.name = "out.jpg" 
  img.save(out) 
  out.seek(0) 
  await message.client.send_file(message.to_id, out, reply_to=reply) 
  await message.delete()