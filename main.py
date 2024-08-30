from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import WebAppInfo
import config

# Инициализация бота и диспетчера
bot = Bot(config.BOT_TOKEN)
dp = Dispatcher(bot)

# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    # Создание клавиатуры
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Открыть сайт!', web_app=WebAppInfo(url='https://normansrgn.github.io/graduateWork/')))  # Замените на реальный URL

    # Форматирование строки для включения имени пользователя
    user_name = message.from_user.first_name
    response_text = f"Hello, {user_name}!"

    # Отправка сообщения с клавиатурой
    await message.answer(response_text, reply_markup=markup)



# Запуск polling
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)