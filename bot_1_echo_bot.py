#!/usr/bin/python 3.9.16
from aiogram import Bot, Dispatcher, executor, types
API_TOKEN: str = ''

# create bot and dispatcher objects
bot: Bot = Bot(token=API_TOKEN)
dp: Dispatcher = Dispatcher(bot)

# This handler will fire on the /start command
async def process_start_command(message: types.Message):
    await message.answer('Hi!\nI am echobot!\n Write me pleas')

# This handler will fire on the /help command
async def process_help_command(message: types.Message):
    await message.answer('Write me something and in return I will send you your message')

# This handler will fire on the photo massage
async def send_photo_echo(message: types.Message):
    await message.answer_photo(message.photo[0].file_id)

# This handler will fire on the oll commands except start and help
async def send_eho(message: types.Message):
    await message.reply(message.text)

# Register hendlender
dp.register_message_handler(process_start_command, commands='start')
dp.register_message_handler(process_help_command, commands='help')
dp.register_message_handler(send_photo_echo, content_types=['photo'])
dp.register_message_handler(send_eho, content_types=['text'])

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)






