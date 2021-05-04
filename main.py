import asyncio

from aiogram import types, exceptions
from aiogram.dispatcher import FSMContext
from aiogram.types import ContentType, ChatType

import keyboards as kb
from config import ADMINS, SUPPORT_CHAT_ID
from loader import dp, bot, logger, db
from utils import get_start_link, decode_start_command


class States:
    CHOOSE_TAG = 'choose:tag'


@dp.message_handler(commands='start')
async def start_handler(msg: types.Message):
    if msg.from_user.id in ADMINS:
        return await msg.reply('Админ панель:', reply_markup=kb.admin_panel)

    logger.info(msg.get_args())
    args = decode_start_command(msg.get_args(), 'Direct')
    logger.info(args)
    db.users.set_user_tag(msg.from_user.id, args)
    await msg.reply('Для разговора с техподдержкой напишите сообщение')


@dp.message_handler(button=kb.admin_panel.CREATE_LINK, user_id=ADMINS)
async def ask_to_send_tag(msg: types.Message, state: FSMContext):
    await msg.reply('Отправьте тег:')
    await state.set_state(States.CHOOSE_TAG)


@dp.message_handler(user_id=ADMINS, state=States.CHOOSE_TAG)
async def get_link(message: types.Message, state: FSMContext):
    try:
        start_link = await get_start_link(message.text)
        await message.reply(start_link)
        await state.finish()
    except ValueError:
        await message.reply(f'Слишком длинный тег!')


@dp.message_handler(content_types=ContentType.ANY, chat_type=ChatType.PRIVATE)
async def forwarded_from_user(msg: types.Message):
    user_tag = db.users.get_user_tag(msg.from_user.id)
    text = f'Сообщение с тегом "{user_tag}":' if user_tag else 'Сообщение без тега:'

    async with asyncio.Lock():
        await bot.send_message(SUPPORT_CHAT_ID, text)
        forwarded_msg = await msg.forward(SUPPORT_CHAT_ID)
        db.messages.set_target_user_for(forwarded_msg.message_id, msg.from_user.id)


@dp.message_handler(content_types=ContentType.ANY, chat_id=SUPPORT_CHAT_ID, is_reply=True)
async def forward_from_support(msg: types.Message, reply: types.Message):
    target_user_id = db.messages.get_target_user_id(reply.message_id)
    if reply.forward_from:
        target_user_id = reply.forward_from.id

    if target_user_id is None:
        return await msg.reply('Сообщение не переслано - пользователь не найден')

    try:
        await msg.copy_to(target_user_id)
    except exceptions.BotBlocked:
        await msg.reply('Бот заблокирован у пользователя')
    except Exception as e:
        logger.exception(f'Exception in send_*: {e}')


if __name__ == "__main__":
    dp.run_polling()
