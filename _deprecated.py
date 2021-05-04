# @dp.message_handler(content_types=[ContentType.TEXT, ContentType.PHOTO, ContentType.DOCUMENT])
# async def message_handler(message: types.Message):
#     user_tag = db.users.get_user_tag(message.from_user.id)
#     if message.chat.type == types.chat.ChatType.PRIVATE:
#         async with asyncio.Lock():
#             await bot.send_message(SUPPORT_CHAT_ID, f"[Сообщение от {message.from_user.full_name}:]"
#                                                     f'(tg://user?id={message.from_user.id}), чат "{user_tag or "бота"}',
#                                    parse_mode=types.ParseMode.MARKDOWN)
#             msg = await message.forward(SUPPORT_CHAT_ID)
#             messages.find_one_and_replace({'msg': msg.message_id},
#                                           {'msg': msg.message_id, 'uid': message.from_user.id}, upsert=True)
#     elif message.chat.id == SUPPORT_CHAT_ID:
#         if message.reply_to_message is not None and bot.id == message.reply_to_message.from_user.id:
#             msg = messages.find_one({'msg': message.reply_to_message.message_id})
#             if message.reply_to_message.forward_from is not None:
#                 uid = message.reply_to_message.forward_from.id
#             elif msg is not None:
#                 uid = msg['uid']
#             else:
#                 search = re.search(r'tg://user\?id=(?P<uid>\d+)', message.reply_to_message.md_text)
#                 if search:
#                     uid = int(search.group('uid'))
#                 else:
#                     return await message.reply('Сообщение не переслано - пользователь не найден')
#
#             if uid is not None:
#                 try:
#                     await bot.copy_message(uid)
#                 except exceptions.BotBlocked:
#                     await message.reply('Бот заблокирован у пользователя')
#                 except Exception as e:
#                     logger.exception(f'Exception in send_*: {e}')
