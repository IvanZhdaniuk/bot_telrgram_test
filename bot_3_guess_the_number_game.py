import random
from aiogram import Bot, Dispatcher, executor
from aiogram.types import Message
from aiogram.dispatcher.filters import Text

BOT_TOKEN: str = ''

# Create objects dispatcher and bot
bot: Bot = Bot(BOT_TOKEN)
dp: Dispatcher = Dispatcher(bot)

# Create count from subsequently
ATTEMPTS: int = 5

# Create dict(to do: db) from User
user: dict ={}

# Create function from create random numbers from 1 to 100
def get_random_numbers():
    return random.randint(1, 100)

# Create handler from command start
async def process_start_command(message: Message):
    await message.answer('Привет!\nДавай сыграем в игру "Угадай число"?\n\nЧтобы получить правила игры и список доступных команд - отправьте команду /help')
    if message.from_user.id not in user:
        user[message.from_user.id] = {
            'in_game': False,
            'secret_number': None,
            'attempts': None,
            'total_game': 0,
            'wins': 0
        }

# Create handler from command help
async def process_help_command(message: Message):
    await message.answer(f'Правила игры:\n\nЯ загадываю число от 1 до 100, а вам нужно его угадать\nУ вас '
                         f'есть {ATTEMPTS} попыток\n\nДоступные команды:\n/help - правила игры и список '
                         f'команд\n/cancel - выйти из игры\n/stat - посмотреть статистику\n\nДавай сыграем?')

# Create handler from command stat
async def process_stat_command(message: Message):
    await message.answer(f'Всего игр сыграно: {user["total_game"]}\n Игр выиграно: {user["wins"]}')

# Create handler from command cancel
async def process_cancel_game_command(message: Message):
    if user[message.from_user.id]["in_game"]:
        await message.answer('Вы вышли из игры. Если захотите сыграть снова - напишите об этом')
        user[message.from_user.id]["in_game"] = False
    else:
        await message.answer('А мы и так с вами не играем. Может, сыграем разок?')

# Create handler from command start
async def process_positive_number(message: Message):
    if not user[message.from_user.id]['in_game']:
        await message.answer('Ура!\n\nЯ загадал число от 1 до 100, попробуй угадать!')
        user[message.from_user.id]['in_game'] = True
        user[message.from_user.id]['secret_number'] = get_random_numbers()
        user[message.from_user.id]['attempts'] = ATTEMPTS
    else:
        await message.answer('Пока мы играем в игру я могу реагировать только на числа от 1 до 100 и команды /cancel и /stat')

# Create handler from cansel the game
async def process_cansel_the_game(message: Message):
    if not user[message.from_user.id]['in_game']:
        await message.answer('Жаль :(\n\nЕсли захотите поиграть - просто напишите об этом')
    else:
        await message.answer('Мы же сейчас с вами играем. Присылайте, пожалуйста, числа от 1 до 100')


# Create handler from input int from 1 to 100
async def process_numbers_answer(message: Message):
        if user[message.from_user.id]['in_game']:
            if int(message.text) == user[message.from_user.id]['secret_number']:
                await message.answer(f'Ура!!! Вы угадали число! Было загадаго число: {user["secret_number"]}\n\nМожет, сыграем еще?')
                user[message.from_user.id]['in_game'] = False
                user[message.from_user.id]['total_game'] += 1
                user[message.from_user.id]['wins'] += 1
            elif int(message.text) > user[message.from_user.id]['secret_number']:
                await message.answer('Мое число меньше')
                user[message.from_user.id]['attempts'] -= 1

            elif int(message.text) < user[message.from_user.id]['secret_number']:
                await message.answer('Мое число больше')
                user[message.from_user.id]['attempts'] -= 1

            if user[message.from_user.id]['attempts'] == 0:
                await message.answer(f'К сожалению, у вас больше не осталось попыток. Вы проиграли :(\n\nМое число '
                                     f'было {user[message.from_user.id]["secret_number"]}\n\nДавайте сыграем еще?')
                user[message.from_user.id]['in_game'] = False
                user[message.from_user.id]['total_game'] += 1

        else:
            await message.answer('Мы еще не играем. Хотите сыграть?')

# Create handler from input everything except for int
async def process_other_text_answers(message: Message):
    if user[message.from_user.id]['in_game']:
        await message.answer('Мы же сейчас с вами играем. Присылайте, пожалуйста, числа от 1 до 100')
    else:
        await message.answer('Я довольно ограниченный бот, давайте просто сыграем в игру?')



dp.register_message_handler(process_help_command, commands='help')
dp.register_message_handler(process_start_command, commands='start')
dp.register_message_handler(process_stat_command, commands='stat')
dp.register_message_handler(process_cansel_the_game, commands='cancel')
dp.register_message_handler(process_positive_number, Text(equals=['Да', 'Давай'], ignore_case=True))
dp.register_message_handler(process_numbers_answer, lambda x: x.text.isdigit() and 1 <= int(x.text) <= 100)
dp.register_message_handler(process_other_text_answers)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)



