import telebot
from telebot import types  # кнопки
from string import Template
import smtplib

bot = telebot.TeleBot('') # Токен от Telegram бота
user_dict = {}

class User:
    def __init__(self, product):
        self.product = product

        keys = ['userProduct', 'typeProduct', 'count', 'sale']

        for key in keys:
            self.key = None


# если /help, /start
@bot.message_handler(commands=['help', 'start', 'Привет', 'Старт'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    itembtn1 = types.KeyboardButton('/Информация')
    itembtn2 = types.KeyboardButton('/Заказ')
    itembtn3 = types.KeyboardButton('/Рекомендуем')
    markup.add(itembtn1, itembtn2, itembtn3)

    bot.send_message(message.chat.id, "Здравствуйте " + message.from_user.first_name + ", я бот, чтобы вы хотели узнать?", reply_markup=markup)


# /info
@bot.message_handler(commands=['Информация', 'info'])
def send_about(message):
    bot.send_message(message.chat.id, "Мы надежная компания. Более 20 лет на рынке автоматизации.")

# /zakaz
@bot.message_handler(commands=["Заказ", 'zakaz'])
def user_reg(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    itembtn1 = types.KeyboardButton(text='Хлеб')
    itembtn2 = types.KeyboardButton(text='Пироги')
    itembtn3 = types.KeyboardButton(text='Выпечка')
    itembtn4 = types.KeyboardButton(text='Отмена')
    markup.add(itembtn1, itembtn2, itembtn3, itembtn4)

    msg = bot.send_message(message.chat.id, 'Выберите товар:', reply_markup=markup)
    bot.register_next_step_handler(msg, process_product)

# /Рекомендуемый заказ
@bot.message_handler(commands=["Рекомендуем"])
def recomend(message):
    bot.send_message(message.chat.id, 'РЕКОМЕНДУЕМЫЙ ТОВАР:\r\n Продукт: Выпечка \r\nТип продукта: Пицца \r\nКоличество: 15',)
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    itembtn1 = types.KeyboardButton(text='Сделать заказ')
    itembtn2 = types.KeyboardButton(text='Отмена')
    markup.add(itembtn1, itembtn2)

    msg = bot.send_message(message.chat.id, 'Подтвердите заказ рекомендуемого заказа', reply_markup=markup)
    bot.register_next_step_handler(msg, send_recomend_email)

# Пробуем новую функцию
def process_product(message):
    try:
        chat_id = message.chat.id
        user_dict[chat_id] = User(message.text)

        if message.text == 'Отмена':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            itembtn1 = types.KeyboardButton('/Информация')
            itembtn2 = types.KeyboardButton('/Сделать заказ')
            itembtn3 = types.KeyboardButton('/Рекомендуем')
            markup.add(itembtn1, itembtn2, itembtn3)
            bot.send_message(chat_id, 'Отмена заказа', reply_markup=markup)
            bot.clear_step_handler(message)
        else:
            if message.text == 'Хлеб':
                markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
                itembtn1 = types.KeyboardButton(text='Белый')
                itembtn2 = types.KeyboardButton(text='Черный')
                itembtn3 = types.KeyboardButton(text='Булки')
                itembtn4 = types.KeyboardButton(text='Отмена')
                markup.add(itembtn1, itembtn2, itembtn3, itembtn4)
            elif message.text == 'Пироги':
                markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
                itembtn1 = types.KeyboardButton(text='С мясом')
                itembtn2 = types.KeyboardButton(text='С капустой')
                itembtn3 = types.KeyboardButton(text='С картошкой')
                itembtn4 = types.KeyboardButton(text='С вишней')
                itembtn5 = types.KeyboardButton(text='С яблоками')
                itembtn6 = types.KeyboardButton(text='С творогом')
                itembtn7 = types.KeyboardButton(text='Отмена')
                markup.add(itembtn1, itembtn2, itembtn3, itembtn4, itembtn5, itembtn6, itembtn7)
            elif message.text == 'Выпечка':
                markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
                itembtn1 = types.KeyboardButton(text='Сосиски в тесте')
                itembtn2 = types.KeyboardButton(text='Кексы ромовые')
                itembtn3 = types.KeyboardButton(text='Пирожки с яблоками')
                itembtn4 = types.KeyboardButton(text='Пицца')
                itembtn5 = types.KeyboardButton(text='Хот-дог')
                itembtn6 = types.KeyboardButton(text='Учпочмак')
                itembtn7 = types.KeyboardButton(text='Курник')
                itembtn8 = types.KeyboardButton(text='Беляш')
                itembtn9 = types.KeyboardButton(text='Самса')
                itembtn10 = types.KeyboardButton(text='Отмена')
                markup.add(itembtn1, itembtn2, itembtn3, itembtn4, itembtn5, itembtn6, itembtn7, itembtn8, itembtn9, itembtn10)
            msg = bot.send_message(chat_id, 'Выберите тип товара:', reply_markup=markup)
            bot.register_next_step_handler(msg, process_type_product)

    except Exception as e:
        bot.reply_to(message, 'Ошибка')


def process_type_product(message):
    try:
        chat_id = message.chat.id
        user = user_dict[chat_id]
        if message.text == 'Отмена':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            itembtn1 = types.KeyboardButton('/Информация')
            itembtn2 = types.KeyboardButton('/Сделать заказ')
            itembtn3 = types.KeyboardButton('/Рекомендуем')
            markup.add(itembtn1, itembtn2, itembtn3)
            bot.send_message(chat_id, 'Отмена заказа', reply_markup=markup)
            bot.clear_step_handler(message)
        else:
            user.typeProduct = message.text

            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            itembtn1 = types.KeyboardButton(text='5 штук')
            itembtn2 = types.KeyboardButton(text='10 штук')
            itembtn3 = types.KeyboardButton(text='15 штук')
            itembtn4 = types.KeyboardButton(text='20 штук')
            itembtn5 = types.KeyboardButton(text='25 штук')
            itembtn6 = types.KeyboardButton(text='30 штук')
            itembtn7 = types.KeyboardButton(text='40 штук')
            itembtn8 = types.KeyboardButton(text='50 штук')
            itembtn9 = types.KeyboardButton(text='Отмена')
            markup.add(itembtn1, itembtn2, itembtn3, itembtn4, itembtn5, itembtn6, itembtn7, itembtn8, itembtn9)

            msg = bot.send_message(chat_id, 'Выберите кол-во товара:', reply_markup=markup)
            bot.register_next_step_handler(msg, process_count_step)

    except Exception as e:
        bot.reply_to(message, 'Ошибка')

def process_count_step(message):
    try:
        chat_id = message.chat.id
        user = user_dict[chat_id]
        if message.text == 'Отмена':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            itembtn1 = types.KeyboardButton('/Информация')
            itembtn2 = types.KeyboardButton('/Сделать заказ')
            itembtn3 = types.KeyboardButton('/Рекомендуем')
            markup.add(itembtn1, itembtn2, itembtn3)
            bot.send_message(chat_id, 'Отмена заказа', reply_markup=markup)
            bot.clear_step_handler(message)
        else:
            user.count = message.text
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            itembtn1 = types.KeyboardButton(text='Мафины -10%')
            itembtn2 = types.KeyboardButton(text='Школьное -15%')
            itembtn3 = types.KeyboardButton(text='Пряники -5%')
            itembtn4 = types.KeyboardButton(text='Чак-чак -15%')
            itembtn5 = types.KeyboardButton(text='Зефир -10%')
            itembtn6 = types.KeyboardButton(text='Не надо')
            itembtn7 = types.KeyboardButton(text='Отмена')
            markup.add(itembtn1, itembtn2, itembtn3, itembtn4, itembtn5, itembtn6, itembtn7)

            msg = bot.send_message(chat_id, 'Выберите товары по акции:', reply_markup=markup)
            bot.register_next_step_handler(msg, process_action_product)

        # msg = bot.send_message(chat_id, getRegData(user, 'Ваша заявка', message.from_user.first_name), parse_mode="Markdown")
        # bot.register_next_step_handler(msg, process_action_product)
        # отправить в группу
        # bot.send_message(config.chat_id, getRegData(user, 'Заявка от бота', bot.get_me().username), parse_mode="Markdown")

    except Exception as e:
        bot.reply_to(message, 'Ошибка')

#Конец новой функции

#Акционные товары
def process_action_product(message):
    try:
        chat_id = message.chat.id
        user = user_dict[chat_id]
        if message.text == 'Отмена':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            itembtn1 = types.KeyboardButton('/Информация')
            itembtn2 = types.KeyboardButton('/Сделать заказ')
            itembtn3 = types.KeyboardButton('/Рекомендуем')
            markup.add(itembtn1, itembtn2, itembtn3)
            bot.send_message(chat_id, 'Отмена заказа', reply_markup=markup)
            bot.clear_step_handler(message)
        else:
            user.sale = message.text
            markup_hide = types.ReplyKeyboardRemove() #Скрытие клавиатуры
            bot.send_message(chat_id, getRegData(user, 'Ваш заказ отправлен менеджеру. В скором времени с вами свяжутся ', message.from_user.first_name), parse_mode="Markdown", reply_markup=markup_hide)

    except Exception as e:
        bot.reply_to(message, 'Ошибка')

# формирует вид заявки регистрации
# нельзя делать перенос строки Template
# в send_message должно стоять parse_mode="Markdown"

def send_zakaz(message):
    chat_id = message.chat.id
    user = user_dict[chat_id]
    if message.text == 'Отмена':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        itembtn1 = types.KeyboardButton('/Информация')
        itembtn2 = types.KeyboardButton('/Сделать заказ')
        itembtn3 = types.KeyboardButton('/Рекомендуем')
        markup.add(itembtn1, itembtn2, itembtn3)
        bot.send_message(chat_id, 'Отмена заказа', reply_markup=markup)
        bot.clear_step_handler(message)
    else:
        markup_hide = types.ReplyKeyboardRemove()  # Скрытие клавиатуры
        bot.send_message(chat_id, getRegData(user, 'Ваш заказ отправлен менеджеру. В скором времени с вами свяжутся ', message.from_user.first_name), parse_mode="Markdown", reply_markup=markup_hide)

def getRegData(user, title, name):
    t = Template(
        '$title *$name* \n Тип продукта: *$userProduct* \n Продукт: *$typeProduct* \n Кол-во: *$count* \n Акционный: *$sale*')

    # ПЫТАЕМСЯ ОТПРАВИТЬ РЕЗУЛЬТАТ НА ПОЧТУ --------------------------------------------------------
    sender = 'sender@gmail.com' # С какой почты отправляем информацию о заказе
    sender_password = 'PASSWORD' # Пароль от почты
    to_item = 'manager@gmail.com' # Кому отправляем письмо с заказов
    mail_lib = smtplib.SMTP_SSL('smtp.yandex.ru', 465) # Настройки почты
    mail_lib.login(sender, sender_password)
    msg = 'From: %s\r\nTo: %s\r\nContent-Type: text/plain; charset="utf-8"\r\nSubject: %s\r\n\r\n' % (sender, to_item, 'Новый заказ выпечки от ' + name)
    msg += 'НОВЫЙ ЗАКАЗ НА ДОСТАВКУ ПРОДУКТОВ:' + '\r\n\r\n' + 'Продукт: ' + user.product + '\r\n' + 'Тип продукта: ' + user.typeProduct + '\r\n' + 'Количество: '+ user.count + '\r\n' + 'Аукционный: '+ user.sale + '\r\n\r\n' + 'Телефон: +7 (347) 222-20-21 Почта: zakaz@soft-servis.ru' + '\r\n' + 'Адрес: г.Уфа, ул.Менделеева 134/7, 413 офис' #Текст сообщения
    mail_lib.sendmail(sender, to_item, msg.encode('utf8'))
    mail_lib.quit()
    # КОНЕЦ ПОПЫТКИ ОТПРАВИТЬ РЕЗУЛЬТАТ НА ПОЧТУ --------------------------------------------------------


    return t.substitute({
        'title': title,
        'name': name,
        'userProduct': user.product,
        'typeProduct': user.typeProduct,
        'count': user.count,
        'sale': user.sale,
    })

def send_recomend_email(message): # Используеться только для Рекомендовательного заказа
    # ОТПРАВЛЯЕМ РЕЗУЛЬТАТ НА ПОЧТУ  -------------------------------------------------------
    product = 'Выпечка' # Рекомендуемый товар, меняем сами
    typeProduct = 'Пицца' # Рекомендуемый товар, меняем сами
    count = '15 штук' # Рекомендуемый товар, меняем сами
    sender = 'sender@gmail.com' # Откуда отправлять
    sender_password = 'PASSWORD' # Пароль от почты
    to_item = 'manager@gmail.com' # Кому отправляем информацию о заказе
    mail_lib = smtplib.SMTP_SSL('smtp.yandex.ru', 465) # Настройки почты
    mail_lib.login(sender, sender_password)
    msg = 'From: %s\r\nTo: %s\r\nContent-Type: text/plain; charset="utf-8"\r\nSubject: %s\r\n\r\n' % (sender, to_item, 'Новый заказ выпечки') # + name)
    msg += 'НОВЫЙ ЗАКАЗ НА ДОСТАВКУ ПРОДУКТОВ:' + '\r\n\r\n' + 'Продукт: ' + product + '\r\n' + 'Тип продукта: ' + typeProduct + '\r\n' + 'Количество: '+ count + '\r\n\r\n' + 'Телефон: +7 (347) 222-20-21 Почта: zakaz@soft-servis.ru' + '\r\n' + 'Адрес: г.Уфа, ул.Менделеева 134/7, 413 офис' #Текст сообщения
    mail_lib.sendmail(sender, to_item, msg.encode('utf8'))
    mail_lib.quit()
    # КОНЕЦ ПОПЫТКИ ОТПРАВИТЬ РЕЗУЛЬТАТ НА ПОЧТУ --------------------------------------------------------
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    itembtn1 = types.KeyboardButton('/Информация')
    itembtn2 = types.KeyboardButton('/Сделать заказ')
    itembtn3 = types.KeyboardButton('/Рекомендуем')
    markup.add(itembtn1, itembtn2, itembtn3)
    bot.send_message(message.chat.id, 'Заказ успешно отправлен на электронную почту менеджеру.', reply_markup=markup)


# произвольный текст
@bot.message_handler(content_types=["text"])
def send_help(message):
    bot.send_message(message.chat.id, 'О нас - /info\nСделать заказ - /zakaz\nПомощь - /help')


# произвольное фото
@bot.message_handler(content_types=["photo"])
def send_help_text(message):
    bot.send_message(message.chat.id, 'Напишите текст')


# Enable saving next step handlers to file "./.handlers-saves/step.save".
# Delay=2 means that after any change in next step handlers (e.g. calling register_next_step_handler())
# saving will hapen after delay 2 seconds.
bot.enable_save_next_step_handlers(delay=2)

# Load next_step_handlers from save file (default "./.handlers-saves/step.save")
# WARNING It will work only if enable_save_next_step_handlers was called!
bot.load_next_step_handlers()

if __name__ == '__main__':
    bot.polling(none_stop=True)