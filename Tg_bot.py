import telebot
from telebot import types

API_TOKEN = 'API'  # Замените на ваш токен
bot = telebot.TeleBot(API_TOKEN)

# Словарь для хранения данных пользователей
user_data = {}

# Создаем клавиатуру
keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
button_calculate = types.KeyboardButton('Рассчитать')
button_info = types.KeyboardButton('Информация')
keyboard.add(button_calculate, button_info)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привет! Я бот, помогающий твоему здоровью.", reply_markup=keyboard)


@bot.message_handler(func=lambda message: message.text == 'Рассчитать')
def ask_gender(message):
    bot.send_message(message.chat.id, "Введите ваш пол (мужчина/женщина):")
    bot.register_next_step_handler(message, process_gender)


def process_gender(message):
    user_id = message.chat.id
    gender = message.text.lower()
    if gender in ['мужчина', 'женщина']:
        user_data[user_id] = {'gender': gender}
        bot.send_message(user_id, "Введите свой возраст:")
        bot.register_next_step_handler(message, set_age)
    else:
        bot.send_message(user_id, "Пожалуйста, введите 'мужчина' или 'женщина'.")
        bot.register_next_step_handler(message, process_gender)


def set_age(message):
    user_id = message.chat.id
    try:
        age = int(message.text)
        user_data[user_id]['age'] = age
        bot.send_message(user_id, "Введите свой рост в сантиметрах:")
        bot.register_next_step_handler(message, process_growth)
    except ValueError:
        bot.send_message(user_id, "Пожалуйста, введите корректный возраст (число).")
        bot.register_next_step_handler(message, set_age)


def process_growth(message):
    user_id = message.chat.id
    try:
        growth = int(message.text)
        user_data[user_id]['growth'] = growth
        bot.send_message(user_id, "Введите свой вес в килограммах:")
        bot.register_next_step_handler(message, process_weight)
    except ValueError:
        bot.send_message(user_id, "Пожалуйста, введите корректный рост (число).")
        bot.register_next_step_handler(message, process_growth)


def process_weight(message):
    user_id = message.chat.id
    try:
        weight = int(message.text)
        user_data[user_id]['weight'] = weight

        # Извлечение данных
        age = user_data[user_id]['age']
        growth = user_data[user_id]['growth']
        weight = user_data[user_id]['weight']
        gender = user_data[user_id]['gender']

        # Формулы для расчета калорий
        if gender == 'мужчина':
            calories = 10 * weight + 6.25 * growth - 5 * age + 5
        elif gender == 'женщина':
            calories = 10 * weight + 6.25 * growth - 5 * age - 161

        bot.send_message(user_id, f"Ваша норма калорий: {calories:.2f} ккал.")

        # Удаляем данные после использования
        del user_data[user_id]
    except ValueError:
        bot.send_message(user_id, "Пожалуйста, введите корректный вес (число).")
        bot.register_next_step_handler(message, process_weight)


@bot.message_handler(func=lambda message: message.text == 'Информация')
def info(message):
    bot.send_message(message.chat.id, "Этот бот помогает вам рассчитать вашу суточную норму калорий.")


@bot.message_handler(func=lambda message: True)
def all_messages(message):
    bot.send_message(message.chat.id, "Выберите действие с помощью кнопок.", reply_markup=keyboard)


if __name__ == '__main__':
    bot.polling(none_stop=True)
