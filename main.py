from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import WebAppInfo
import config

bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)

USER_SUPPORT_ID = 481356531  
user_questions = {}  
user_state = {}  
question_id_counter = 57869  

async def on_startup(_):
    print("Бот успешно запущен и готов к работе!")

@dp.message_handler(commands=['start'])
async def start(message: types.Message):

    user_state[message.from_user.id] = None
    
    start_parameter = message.get_args()
    if start_parameter:
        print(f"Параметр команды /start: {start_parameter}")
    
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = [
        types.KeyboardButton(text="👟Каталог", web_app=WebAppInfo(url="https://normansrgn.github.io/graduateWork/")),
        types.KeyboardButton(text="🛒Корзина"),
        types.KeyboardButton(text="📲Контакты"),
        types.KeyboardButton(text="💬Поддержка")
    ]
    keyboard.add(*buttons)

    user_name = message.from_user.first_name
    response_text = (
        f"👟 Привет, {user_name}!\n\n"
        f"🔥 Давно хочешь найти свою идеальную пару?\n\n"
        f"Переходи в наш каталог и выбери то, что сделает твой стиль уникальным.\n"
        f"И не забудь, у нас всегда есть что-то особенное для тебя!"
    )

    await message.answer(response_text, reply_markup=keyboard)

@dp.message_handler(lambda message: message.text in ["🛒Корзина", "📲Контакты", "💬Поддержка"])
async def handle_menu_buttons(message: types.Message):
    user_id = message.from_user.id
    
    if message.text == "🛒Корзина":
        await message.answer("Ваша корзина пока пуста.")
        user_state[user_id] = None
    elif message.text == "📲Контакты":
        await message.answer("Свяжитесь с нами по телефону: +77777777777")
        user_state[user_id] = None
    elif message.text == "💬Поддержка":
        await message.answer("Пожалуйста, напишите свой вопрос. Мы свяжемся с вами как можно скорее.")

        global question_id_counter
        user_questions[user_id] = {
            'name': message.from_user.first_name,
            'question': None,
            'question_id': question_id_counter
        }
        user_state[user_id] = 'support'
        question_id_counter += 1

@dp.message_handler(lambda message: user_state.get(message.from_user.id) == 'support')
async def handle_user_questions(message: types.Message):
    user_id = message.from_user.id
    question = message.text

    if user_id in user_questions:
        user_questions[user_id]['question'] = question
        question_id = user_questions[user_id]['question_id']
        formatted_question_id = f"{question_id:05}"  
        try:
            await bot.send_message(
                USER_SUPPORT_ID, 
                f"Обращение №{formatted_question_id} от пользователя {user_questions[user_id]['name']} (ID: {user_id}):\n\n{question}\n\nОтветьте на него."
            )
            await message.answer(f"Ваше обращение (№{formatted_question_id}) отправлено в поддержку. Мы свяжемся с вами как можно скорее.")

            user_state[user_id] = None
        except Exception as e:
            print(f"Failed to send question to support: {e}")

@dp.message_handler(lambda message: message.from_user.id == USER_SUPPORT_ID)
async def handle_support_replies(message: types.Message):
    response_text = message.text
    # Отправляем ответ только последнему пользователю, который задал вопрос
    for user_id, info in user_questions.items():
        if info['question']:
            question_id = info['question_id']
            formatted_question_id = f"{question_id:05}"  
            try:
                await bot.send_message(user_id, f"Ответ на ваше обращение №{formatted_question_id} от поддержки ({info['name']}):\n\n{response_text}")
                
                del user_questions[user_id]

                await bot.send_message(USER_SUPPORT_ID, "Ответ доставлен клиенту.")

                break  
            except Exception as e:
                print(f"Failed to send message to user {user_id}: {e}")
                continue

# Обработчик сообщений, которые не являются командами или кнопками
@dp.message_handler(lambda message: message.text not in ["Корзина", "Контакты", "Поддержка", "/start"])
async def handle_unknown_messages(message: types.Message):
    await message.answer("Выберите действие")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)