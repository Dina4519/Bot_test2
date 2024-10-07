import telebot
from telebot import types
from time import sleep

from config import TOKEN

import logging

logger = logging.getLogger(__name__)

bot = telebot.TeleBot(TOKEN)

questions = {
    0: {
        "question": "Вопрос первый: Какая группа животных тебе больше нравится?",
        "variants": ("Млекопитающие", "Птицы", "Рыбы", "Рептилии")
        },
    1: {
        "question": "Какой образ жизни ведет животное?",
        "variants": ("Ночной", "Дневной", "Смешанный", "Без разницы")
        },
    2: {
        "question": "Как выглядит животное?",
        "variants": ("Миленько", "Устрашающе", "Нейтрально", "Без разницы")
        },
    3: {
        "question": "Какой характер у животного?",
        "variants": ("Спокойный", "Игривый", "Дерзкий", "Милый")
        }
    }
answer_weights = {
    "Млекопитающие": 0, "Птицы": 1, "Рыбы": 2, "Рептилии": 3,
    "Ночной": 0, "Дневной": 1, "Смешанный": 2, "Без разницы": 3,
    "Миленько": 0, "Устрашающе": 1, "Нейтрально": 2,
    "Спокойный": 0, "Игривый": 1, "Дерзкий": 2, "Милый": 3,
    }


# Handles all text messages that contains the commands '/start' or '/help'.
# @bot.message_handler(commands=['start', 'help'])
# def send_welcome(message):
#     bot.reply_to(message, "Howdy, how are you doing?")


# @bot.message_handler(func=lambda message: True)
# def echo_all(message):
#     bot.reply_to(message, message.text)
# @bot.message_handler(commands = ['start', 'help'])
# def start(message: telebot.types.Message):
    # text = "Привет😃. Чтобы начать работу введите команду боту:\n/start - Чтобы увидеть доступные валюты\n/convert - Чтобы начать конвертацию"
    # bot.send_message(message.chat.id, text)

#
# @bot.message_handler(commands=['start', 'help'])
# def greetings(message):
#     print('Привет')

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    print('Привет')
    # bot.reply_to(message, "Привет")

    keyboard = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton(text="О Московском зоопарке", url="https://moscowzoo.ru/")
    btn2 = types.InlineKeyboardButton(text="О nрограмме опеки", url="https://moscowzoo.ru/my-zoo/become-a-guardian/")
    keyboard.add(btn1, btn2)
    logo = open('./cat.jpg', 'rb')
    # logo = open('/content/MZoo-logo-сircle-universal-small-preview.jpg', 'rb')
    bot.send_photo(message.chat.id, photo=logo, caption="Пpиветствую😃", reply_markup=keyboard)

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton(text="Haчать викторину"))
    msg = bot.send_message(message.chat.id, text="Пройди викторину и узнай своё тотемное животное!", reply_markup=keyboard)

    bot.register_next_step_handler(msg, ask_question)


@bot.message_handler(content_types=['text'])
def ask_question(message: types.Message, step=0, result=0):
    if step:
        result += answer_weights.get(message.text)

    question = questions.get(step)
    question_text = question.get('question')
    keyboard = create_keyboard(question)

    next_step = step + 1

    if next_step in questions:
        msg = bot.send_message(message.chat.id, text=question_text, reply_markup=keyboard)
        bot.register_next_step_handler(msg, ask_question, next_step, result)
    else:  # вопрос был последним
        msg = bot.send_message(message.chat.id, text=question_text, reply_markup=keyboard)
        bot.register_next_step_handler(msg, show_result, result)


@bot.message_handler(content_types=['text'])
def show_result(message: types.Message, result):
    result += answer_weights.get(message.text)

    text = f'Викторина завершена!\nТвой результат {result}.\nБарханный кот не впечатлён.'
    image = open('./cat.jpg', 'rb')
    bot.send_photo(message.chat.id, photo=image, caption=text)


    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton(text="Haчaть зaнoвo"))
    msg = bot.send_message(message.chat.id, text='Если хочешь пройти тест ещё раз, нажми "Начать заново"', reply_markup=keyboard)
    bot.register_next_step_handler(msg, ask_question)


    inline_keyboard = types.InlineKeyboardMarkup()
    url_button = types.InlineKeyboardButton(text="Поделиться в vk", url=f"https://vk.com/share.php?&title={result}")
    inline_keyboard.add(url_button)
    bot.send_message(msg.chat.id, "⬇️ Вы можете поделиться с друзьями в vk, нажав по кнопке ниже:", reply_markup=inline_keyboard)


    inline_keyboard2 = types.InlineKeyboardMarkup()
    url_button2 = types.InlineKeyboardButton(text="Оставить отзыв", url=f"https://vk.com/share.php?&title={result}")
    inline_keyboard2.add(url_button2)
    bot.send_message(msg.chat.id, '⬇️ Чтобы оставить отзыв, нажми "Оставить отзыв"', reply_markup=inline_keyboard2)

    # keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # keyboard.add(types.KeyboardButton(text="Оставить отзыв"))
    # msg = bot.send_message(message.chat.id, text='Чтобы оставить отзыв, нажми "Оставить отзыв"',
    #                        reply_markup=keyboard)
    # bot.register_next_step_handler(msg, ask_question)





# @bot.message_handler(commands=['test'])
# def review(message):
#     print('Еще привет')
#     keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
#     keyboard.add(types.KeyboardButton(text="Оставить отзыв"))
#     msg = bot.send_message(message.chat.id, text='Чтобы оставить отзыв, нажми "Оставить отзыв"',
#                            reply_markup=keyboard)
#     bot.register_next_step_handler(msg, ask_question)





def create_keyboard(question):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    buttons = []
    for var in question.get('variants'):
        buttons.append(types.KeyboardButton(text=var))
    keyboard.add(*buttons)
    return keyboard


bot.infinity_polling()













#
#
#
# questions = {
#     0: {
#         "question": "Вопрос первый: Какая группа животных тебе больше нравится?",
#         "variants": ("Млекопитающие", "Птицы", "Рыбы", "Рептилии")
#         },
#     1: {
#         "question": "Какой образ жизни ведет животное?",
#         "variants": ("Ночной", "Дневной", "Смешанный", "Без разницы")
#         },
#     2: {
#         "question": "Как выглядит животное?",
#         "variants": ("Миленько", "Устрашающе", "Нейтрально", "Без разницы")
#         },
#     3: {
#         "question": "Какой характер у животного?",
#         "variants": ("Спокойный", "Игривый", "Дерзкий", "Милый")
#         }
#     }
# answer_weights = {
#     "Млекопитающие": 0, "Птицы": 1, "Рыбы": 2, "Рептилии": 3,
#     "Ночной": 0, "Дневной": 1, "Смешанный": 2, "Без разницы": 3,
#     "Миленько": 0, "Устрашающе": 1, "Нейтрально": 2,
#     "Спокойный": 0, "Игривый": 1, "Дерзкий": 2, "Милый": 3,
#     }
#
#
#
#
# def review()

    # keyboard2 = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # keyboard2.add(types.KeyboardButton(text="Оставить отзыв"))
    # msg = bot.send_message(message.chat.id, text='Чтобы оставить отзыв, нажми "Оставить отзыв"',
    #                        reply_markup=keyboard)
    # bot.register_next_step_handler(msg, ask_question)


    # inline_keyboard2 = types.InlineKeyboardMarkup()
    # bot.send_message(msg.chat.id, "⬇️ Также можете оставить свой отзыв:", reply_markup=inline_keyboard2)
    # url_button2 = types.InlineKeyboardButton(text="Оставить отзыв", url={result})
    # inline_keyboard2.add(url_button2)
#
#
#
# @bot.message_handler(commands=['start', 'help'])
# def greetings(message: types.Message):
#     print('Привет')
#     keyboard = types.InlineKeyboardMarkup(row_width=2)
#     btn1 = types.InlineKeyboardButton(text="О Московском зоопарке", url="https://moscowzoo.ru/")
#     btn2 = types.InlineKeyboardButton(text="О nрограмме опеки", url="https://moscowzoo.ru/my-zoo/become-a-guardian/")
#     keyboard.add(btn1, btn2)
#     # logo = open('/content/MZoo-logo-сircle-universal-small-preview.jpg', 'rb')
#     bot.send_photo(message.chat.id, photo='logo', caption="Пpиветствие", reply_markup=keyboard)
#
#     keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
#     keyboard.add(types.KeyboardButton(text="Haчать викторину"))
#     msg = bot.send_message(
#         message.chat.id,
#         text="Пройди викторину и узнай своё тотемное животное!",
#         reply_markup=keyboard)
#
#     # bot.register_next_step_handler(msg, ask_question)
#
#
# @bot.message_handler(content_types=['text'])
# def ask_question(message: types.Message, step=0, result=0):
#     if step:
#         result += answer_weights.get(message.text)
#
#     question = questions.get(step)
#     question_text = question.get('question')
#     keyboard = create_keyboard(question)
#
#     next_step = step + 1
#
#     if next_step in questions:
#         msg = bot.send_message(message.chat.id, text=question_text, reply_markup=keyboard)
#         bot.register_next_step_handler(msg, ask_question, next_step, result)
#     else:  # вопрос был последним
#         msg = bot.send_message(message.chat.id, text=question_text, reply_markup=keyboard)
#         bot.register_next_step_handler(msg, show_result, result)
#
#
# @bot.message_handler(content_types=['text'])
# def show_result(message: types.Message, result):
#     result += answer_weights.get(message.text)
#
#     text = f'Викторина завершена!\nТвой результат {result}.\nБарханный кот не впечатлён.'
#     image = open('/content/barhanniy-kot6.jpeg', 'rb')
#     bot.send_photo(message.chat.id, photo=image, caption=text)
#
#     keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
#     keyboard.add(types.KeyboardButton(text="Haчaть зaнoвo"))
#     msg = bot.send_message(
#         message.chat.id,
#         text='Если хочешь пройти тест ещё раз, нажми "Начать заново"',
#         reply_markup=keyboard)
#     bot.register_next_step_handler(msg, ask_question)
#
#     inline_keyboard = types.InlineKeyboardMarkup()
#     url_button = types.InlineKeyboardButton(text="Поделиться в vk", url=f"https://vk.com/share.php?&title={result}")
#     inline_keyboard.add(url_button)
#     bot.send_message(msg.chat.id, "⬇️ Вы можете поделиться с друзьями в vk, нажав по кнопке ниже:",
#                      reply_markup=inline_keyboard)
#
#
# def create_keyboard(question):
#     keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
#     buttons = []
#     for var in question.get('variants'):
#         buttons.append(types.KeyboardButton(text=var))
#     keyboard.add(*buttons)
#     return keyboard
#
#





# def cache(func):
#     cache_dict = {}  # {n_1: result_1, n_2: result_2}
#
#     def wrapper(n):
#         if n not in cache_dict:
#             cache_dict[n] = func(n)
#         return cache_dict[n]
#
#     return wrapper
#
#
# @cache
# def pow_99(n):
#     sleep(2)
#     return n**99
#
#
# @cache
# def fibonacci(n):
#     if n <= 1:
#         return n
#     num = fibonacci(n - 1) + fibonacci(n - 2)
#     return num
#
#
# print(fibonacci(100))  # 0 1 1 2 3 5 8 13 21 34 55



# import asyncio
# import logging
# from aiogram import Bot, Dispatcher, types
# from aiogram.filters.command import Command
#
# # Включаем логирование, чтобы не пропустить важные сообщения
# logging.basicConfig(level=logging.INFO)
# # Объект бота
# bot = Bot(token="12345678:AaBbCcDdEeFfGgHh")
# # Диспетчер
# dp = Dispatcher()
#
# # Хэндлер на команду /start
# @dp.message(Command("start"))
# async def cmd_start(message: types.Message):
#     await message.answer("Hello!")
#
# # Запуск процесса поллинга новых апдейтов
# async def main():
#     await dp.start_polling(bot)
#
# if __name__ == "__main__":
#     asyncio.run(main())
#
#
# # Хэндлер на команду /test1
# @dp.message(Command("test1"))
# async def cmd_test1(message: types.Message):
#     await message.reply("Test 1")
#
# # Хэндлер на команду /test2
# async def cmd_test2(message: types.Message):
#     await message.reply("Test 2")
#
# bot.polling()