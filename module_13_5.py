from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import asyncio

#    Измените massage_handler для функции set_age.
#    Теперь этот хэндлер будет реагировать на текст 'Рассчитать', а не на 'Calories'.
#    Создайте клавиатуру ReplyKeyboardMarkup и 2 кнопки KeyboardButton на ней со следующим текстом:
#       'Рассчитать' и 'Информация'.
#        Сделайте так, чтобы клавиатура подстраивалась под размеры интерфейса устройства при
#        помощи параметра resize_keyboard.
#    Используйте ранее созданную клавиатуру в ответе функции start, используя параметр reply_markup.
#
# В итоге при команде /start у вас должна присылаться клавиатура с двумя кнопками.
# При нажатии на кнопку с надписью 'Рассчитать' срабатывает функция set_age
# с которой начинается работа машины состояний для age, growth и weight.



api = ''
bot = Bot(token = api)
dp = Dispatcher(bot, storage = MemoryStorage())

kb = ReplyKeyboardMarkup(resize_keyboard=True)
button1 = KeyboardButton(text='Расчитать')
button2 = KeyboardButton(text='Информация')

kb.insert(button1)
kb.insert(button2)

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

@dp.message_handler(commands='start')
async def start_message(message):
    await message.answer('Привет! Я бот, помогающий твоему здоровью.', reply_markup=kb)

@dp.message_handler(text = 'Расчитать')
async def set_age(message):
    await message.answer('Введите свой возраст:')
    await UserState.age.set()

@dp.message_handler(state = UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer(f"Введите свой рост:")
    await UserState.growth.set()

@dp.message_handler(state = UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer(f"Введите свой вес:")
    await UserState.weight.set()

@dp.message_handler(state = UserState.weight)
async def set_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    bmr = int(data['weight']) * 10 + 6.25 * int(data['growth']) - 5 * int(data['age']) + 5
    await message.answer(f"Ваша норма калорий: {bmr}")
    await state.finish()

@dp.message_handler()
async def start_message(message):
    await message.answer('Введите команду /start, чтобы начать общение.')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)