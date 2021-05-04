import base64
from aiogram import Bot


async def get_start_link(payload: str):
    payload = encode_payload(payload)
    if len(payload) > 64:
        raise ValueError('Too long payload!')

    bot = await Bot.get_current().me
    return f'https://t.me/{bot.username}?start={payload}'


def decode_start_command(command_args: str, default=''):
    if not command_args:
        return default
    return decode_payload(command_args)


def encode_payload(payload: str):
    result: bytes = base64.urlsafe_b64encode(payload.encode())
    return result.decode()


def decode_payload(payload: str):
    result: bytes = base64.urlsafe_b64decode(payload.encode())
    return result.decode()
