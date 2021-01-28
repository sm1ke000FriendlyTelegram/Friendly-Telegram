from .. import loader
from telethon.tl.functions.channels import GetAdminedPublicChannelsRequest


def register(cb):
    cb(KaroLShipMod())
    
class KaroLShipMod(loader.Module):
    """Посмотреть хде я одмин."""
    strings = {'name': 'Karolship'}
    
    async def karolcmd(self, message):
        """Команда .karol выводит список где я Кароль  открытых чатов/каналов. """
        await message.edit('<b>Ищем владение...</b>')
        result = await message.client(GetAdminedPublicChannelsRequest())
        msg = ""
        count = 0
        for obj in result.chats:
            count += 1
            msg += f'\n• <a href="tg://resolve?domain={obj.username}">{obj.title}</a> <b>|</b> <code>{obj.id}</code>'
        await message.edit(f'<b>Хде я Кароль?: {count}</b>\n {msg}')