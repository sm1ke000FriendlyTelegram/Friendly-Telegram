#by Sm1ke
from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl.types import MessageMediaDocument
from .. import loader, utils
from time import sleep


def register(cb):
 cb(demotivator3Mod())


class demotivator3Mod(loader.Module):
    """Демотиватор 3.0 @super_rjaka_demotivator_bot"""

    strings = {'name': 'Демотиватор3.0'}

    def init(self):
        self.name = self.strings['name']
        self._me = None
        self._ratelimit = []

    async def client_ready(self, client, db):
        self._db = db
        self._client = client
        self.me = await client.get_me()

    async def democmd(self, message):
        """ .demo фотка или Гифка ибать"""
        
        args = utils.get_args_raw(message)
        reply = await message.get_reply_message()
        if not reply:
            await message.edit("<b>ДАЙ МНЕ РЕПЛАЙ, СЫН ШЛЮХИ </b>")
            return
        try:
           media = reply.media
        except:
            await message.edit("<b>ДАЙ МНЕ РЕПЛАЙ, СЫН ШЛЮХИ</b>")
            return           

        chat = '@super_rjaka_demotivator_bot'
        await message.edit('<b>ЖДИ ЕБАТЬ....</b>')
        async with message.client.conversation(chat) as conv:
            try:
                response = conv.wait_event(events.NewMessage(incoming=True, from_users=1016409811))
   
                await message.client.send_file(chat, media, caption = args)  
    
                response = await response
            except YouBlockedUserError:
                await message.reply('<b>Разблокируй @super_rjaka_demotivator_bot</b>')
                return

            await message.delete()
            await message.client.send_file(message.to_id, response.media, reply_to=await message.get_reply_message())