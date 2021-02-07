# Just calculator
# by @Sm1ke

from .. import loader, utils

import logging
import asyncio
import telethon

logger = logging.getLogger(__name__)

async def register(cb):
	cb(CALCULATORMod())

@loader.tds
class CALCULATORMod(loader.Module):
	"""Калькулятор модуль"""
	strings = {"name": "Calculator"}

	async def calcmd(self, message):
		"""This command can count a equality"""
		args = message.text.split(' ')
		if len(args)!=2:
			await utils.answer(message, "<strong>You didn't specifyed args</strong>")
			return
		argss=args[1].replace(' ','')
		if len(argss)<=2:
			await message.edit("<strong>I can't count this math expression(1)</strong>")
			return
		
		#Хули смотришь? Код смотри, а то боишься, ахахахах, лох ¯\_(ツ)_/¯		
		try:
			result=eval(argss)
		except:
			await message.edit("<strong>Укажите число которое надо подсчитать.(2)</strong>")
			return
		
		if type(result)==int:
			await message.edit(f'<strong>{argss}={int(result)}</strong>')
			return
		if type(result)==float:
			await message.edit(f'<strong>{argss}={float(result)}</strong>')
			return
		else:
			await message.edit("<strong>Укажите число которое надо подсчитать.(3)</strong>")
			return
		

