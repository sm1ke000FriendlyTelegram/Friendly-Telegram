﻿#    Friendly Telegram (telegram userbot)
#    Copyright (C) 2018-2019 The Authors

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.

#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

from .. import loader, utils, security
import logging

from telethon.tl.types import ChatAdminRights, ChatBannedRights, PeerUser, PeerChannel
from telethon.errors import BadRequestError
from telethon.tl.functions.channels import EditAdminRequest, EditBannedRequest
from telethon.tl.functions.messages import EditChatAdminRequest

logger = logging.getLogger(__name__)


@loader.tds
class AdminToolsMod(loader.Module):
    """Админтулс"""
    strings = {"name": "AdminTools",
               "not_supergroup": "<b>Это не супергруппа, даун!</b>",
               "not_group": "<b>Это не группа, даун!</b>",
               "ban_none": "<b>Кого банить, даун?</b>",
               "unban_none": "<b>Кого разбанить, даун?</b>",
               "kick_none": "<b>Кого мне кикать, даун??</b>",
               "promote_none": "<b>Кому давать далбоебку?</b>",
               "demote_none": "<b>Укажи с кого снять далбоебку, даун?</b>",
               "who": "<b>Кого...?</b>",
               "not_admin": "<b>Я не администратор, даун...</b>",
               "banned": "<code>{}</code> <b>Получил бан в ебало!</b>\n<b>ID:</b> <code>{}</code>",
               "unbanned": "<code>{}</code> <b>Получил разбан за отсос!</b>\n<b>ID:</b> <code>{}</code>",
               "kicked": "<code>{}</code> <b>Был послан нахуй!</b>\n<b>ID:</b> <code>{}</code>",
               "promoted": "<code>{}</code> <b>Получил права Далбоеба!</b>\n<b>ID:</b> <code>{}</code>",
               "demoted": "<code>{}</code> <b>Потерял права далбоеба!</b>\n<b>ID:</b> <code>{}</code>"}

    @loader.group_admin_ban_users
    @loader.ratelimit
    async def bancmd(self, message):
        """Бан в ебало"""
        if not isinstance(message.to_id, PeerChannel):
            return await utils.answer(message, self.strings("not_supergroup", message))
        if message.is_reply:
            user = await utils.get_user(await message.get_reply_message())
        else:
            args = utils.get_args(message)
            if len(args) == 0:
                return await utils.answer(message, self.strings("ban_none", message))
            if args[0].isdigit():
                who = int(args[0])
            else:
                who = args[0]
            user = await self.client.get_entity(who)
        if not user:
            return await utils.answer(message, self.strings("who", message))
        logger.debug(user)
        try:
            await self.client(EditBannedRequest(message.chat_id, user.id,
                                                ChatBannedRights(until_date=None, view_messages=True)))
        except BadRequestError:
            await utils.answer(message, self.strings("not_admin", message))
        else:
            await self.allmodules.log("ban", group=message.chat_id, affected_uids=[user.id])
            await utils.answer(message,
                               self.strings("banned", message).format(utils.escape_html(user.first_name), user.id))

    @loader.group_admin_ban_users
    @loader.ratelimit
    async def unbancmd(self, message):
        """Разбан в ебало"""
        if not isinstance(message.to_id, PeerChannel):
            return await utils.answer(message, self.strings("not_supergroup", message))
        if message.is_reply:
            user = await utils.get_user(await message.get_reply_message())
        else:
            args = utils.get_args(message)
            if len(args) == 0:
                return await utils.answer(message, self.strings("unban_none", message))
            if args[0].isdigit():
                who = int(args[0])
            else:
                who = args[0]
            user = await self.client.get_entity(who)
        if not user:
            return await utils.answer(message, self.strings("who", message))
        logger.debug(user)
        try:
            await self.client(EditBannedRequest(message.chat_id, user.id,
                              ChatBannedRights(until_date=None, view_messages=False)))
        except BadRequestError:
            await utils.answer(message, self.strings("not_admin", message))
        else:
            await self.allmodules.log("unban", group=message.chat_id, affected_uids=[user.id])
            await utils.answer(message,
                               self.strings("unbanned", message).format(utils.escape_html(user.first_name), user.id))

    @loader.group_admin_ban_users
    @loader.ratelimit
    async def kickcmd(self, message):
        """Послать нахуй"""
        if isinstance(message.to_id, PeerUser):
            return await utils.answer(message, self.strings("not_group", message))
        if message.is_reply:
            user = await utils.get_user(await message.get_reply_message())
        else:
            args = utils.get_args(message)
            if len(args) == 0:
                return await utils.answer(message, self.strings("kick_none", message))
            if args[0].isdigit():
                who = int(args[0])
            else:
                who = args[0]
            user = await self.client.get_entity(who)
        if not user:
            return await utils.answer(message, self.strings("who", message))
        logger.debug(user)
        if user.is_self:
            if not (await message.client.is_bot()
                    or await self.allmodules.check_security(message, security.OWNER | security.SUDO)):
                return
        try:
            await self.client.kick_participant(message.chat_id, user.id)
        except BadRequestError:
            await utils.answer(message, self.strings("not_admin", message))
        else:
            await self.allmodules.log("kick", group=message.chat_id, affected_uids=[user.id])
            await utils.answer(message,
                               self.strings("kicked", message).format(utils.escape_html(user.first_name), user.id))

    @loader.group_admin_add_admins
    @loader.ratelimit
    async def promotecmd(self, message):
        """Дать далбоебку"""
        if message.is_reply:
            user = await utils.get_user(await message.get_reply_message())
        else:
            args = utils.get_args(message)
            if not args:
                return await utils.answer(message, self.strings("promote_none", message))
            if args[0].isdigit():
                who = int(args[0])
            else:
                who = args[0]
            user = await self.client.get_entity(who)
        if not user:
            return await utils.answer(message, self.strings("who", message))
        rank = ""
        if len(args) >= 1:
            rank = ' '.join(args[1:])
        logger.debug(user)
        try:
            if message.is_channel:
                await self.client(EditAdminRequest(message.chat_id, user.id,
                                                   ChatAdminRights(post_messages=None,
                                                                   add_admins=None,
                                                                   invite_users=None,
                                                                   change_info=None,
                                                                   ban_users=None,
                                                                   delete_messages=True,
                                                                   pin_messages=True,
                                                                   edit_messages=None), rank))
        except BadRequestError:
            await utils.answer(message, self.strings("not_admin", message))
        else:
            await self.allmodules.log("promote", group=message.chat_id, affected_uids=[user.id])
            await utils.answer(message,
                               self.strings("promoted", message).format(utils.escape_html(user.first_name), user.id))

    @loader.group_admin_add_admins
    async def demotecmd(self, message):
        """Забрать далбоебку"""
        if message.is_reply:
            user = await utils.get_user(await message.get_reply_message())
        else:
            args = utils.get_args(message)
            if len(args) == 0:
                return await utils.answer(message, self.strings("demote_none", message))
            if args[0].isdigit():
                who = int(args[0])
            else:
                who = args[0]
            user = await self.client.get_entity(who)
        if not user:
            return await utils.answer(message, self.strings("who", message))
        logger.debug(user)
        try:
            if message.is_channel:
                await self.client(EditAdminRequest(message.chat_id, user.id,
                                                   ChatAdminRights(post_messages=None,
                                                                   add_admins=None,
                                                                   invite_users=None,
                                                                   change_info=None,
                                                                   ban_users=None,
                                                                   delete_messages=None,
                                                                   pin_messages=None,
                                                                   edit_messages=None), ""))
            else:
                await self.client(EditChatAdminRequest(message.chat_id, user.id, False))
        except BadRequestError:
            await utils.answer(message, self.strings("not_admin", message))
        else:
            await self.allmodules.log("demote", group=message.chat_id, affected_uids=[user.id])
            await utils.answer(message,
                               self.strings("demoted", message).format(utils.escape_html(user.first_name), user.id))

    async def client_ready(self, client, db):
        self.client = client
