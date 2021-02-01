from .. import loader, utils 
 
@loader.tds 
class LinkSTextMod(loader.Module): 
 strings = {"name": "LinksTextMod"} 
 @loader.owner 
 async def texcmd(self, message): 
  text = utils.get_args_raw(message) 
  link=text.split(' ')[0] 
  text=text.split(' ')[1] 
  await message.edit(f'<a href="{link}">{text}</a>')