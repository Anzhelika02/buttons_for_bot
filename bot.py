import telebot                                                        # alt+enter - установить библиотеку.
from telebot import types

BOT_TOKEN = "6045273383:AAHjGlsMn1PcfFnFVcCmJ_vujbFF_eK82do"          # здесь индивидуальный токен. 

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=["start"])                              # message_handler - декоратор, обрабатывает входящее сообщение от пользователя.
def start(message):                                                   # message - это объект, содержащий в себе инфу о сообщении (id пользователя, id чата, сам текст сообщения).
    chat_id = message.chat.id                                         # message.chat.id - идентификатор чата.
    first_name = message.chat.first_name                              # message.chat.first_name - имя пользователя.
    
    photo = open(r"C:\Users\Анжелика\Downloads\557440460.gif", "rb")  # загрузка фото.
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)          # ReplyKeyboardMarkup - та самая клавиатура.
    keyboard = types.KeyboardButton(text='Меню')                      
    markup.add(keyboard)
    
    inline_markup = types.InlineKeyboardMarkup(row_width=True)                                    # Inline кнопки = клавиатура, которая "прикрепляется" к отдельному сообщению.
    inline_keyboard = types.InlineKeyboardButton("Наш сайт", url="https://vk.com/kukuruzai")      # У кнопок есть много режимов, в зависимости от ВТОРОГО аргумента. Первая кнопка переводит на сайт компании, а вторая возвращает текстовое сообщение в чате.
    inline_keyboard2 = types.InlineKeyboardButton("Местоположение", callback_data=1)              # При нажатии на такую кнопку, боту нужно отдельно обрабатывать callback_data (обрабатывается в конце с помощью декоратора callback_query_handler...).
    inline_markup.add(inline_keyboard, inline_keyboard2)                                          # Добавляем эти 2 кнопки к сообщению.
    
    bot.send_photo(chat_id, photo=photo)                                                          # Отправляем приветственное фото.
    bot.send_message(chat_id, f'Привет, {first_name}!', reply_markup=markup)
    bot.send_message(chat_id, "Информация", reply_markup=inline_markup)                           # К сообщению "Информация" прикрепляются 2 кнопки: "Наш сайт" и "Местоположение".

@bot.message_handler(content_types=["text"])                                                      # Здесь обрабатывается работа кнопки "Меню".
def text(message):
    chat_id = message.chat.id
    if message.chat.type == 'private':
        if message.text == 'Меню':
            with open('dishes.txt', 'r', encoding='utf-8') as f:
                dishes = f.read()
                bot.send_message(chat_id, f"МЕНЮ:\n{dishes}")

@bot.callback_query_handler(func=lambda call: True)                                                # Аргумент func для "отсеивания" Call back запросов.
def callback_data(call):                                                                           # Здесь написана работа кнопки, которая возвращает текст.
    chat_id = call.message.chat.id
    if call.message:
        if call.data == '1':
            bot.send_message(chat_id, "Наш адрес: Пирогова 1, вход 3, эт 1.")

bot.polling(none_stop=True)                                                                        # Чтобы бот не отключался и ждал нового сообщения.
