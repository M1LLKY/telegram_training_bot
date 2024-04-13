import os

import telebot

from dotenv import load_dotenv

import requests

load_dotenv() # Подгружаем API токен бота из .env файла

BOT_TOKEN = os.environ.get('BOT_TOKEN') # Записываем токен в BOT_TOKEN

bot = telebot.TeleBot(BOT_TOKEN) # Инициализируем бота

def get_daily_horoscope(sign: str, day: str) -> dict: # Функция получения "предсказания"
    """
    Get daily horoscope for a zodiac sign.
    Keyword arguments:
    sign:str - Zodiac sign
    day:str - Date in format (YYYY-MM-DD) OR TODAY OR TOMORROW OR YESTERDAY
    Return:dict - JSON data
    """
    url = "https://horoscope-app-api.vercel.app/api/v1/get-horoscope/daily"
    params = {"sign": sign, "day": day}
    response = requests.get(url, params)

    return response.json()

@bot.message_handler(commands=['horoscope']) # Инициализация команды для бота

def sign_handler(message): # Функция получения знака зодиака
    text = "What's your zodiac sign?\nChoose one: *Aries*, *Taurus*, *Gemini*, *Cancer,* *Leo*, *Virgo*, *Libra*, *Scorpio*, *Sagittarius*, *Capricorn*, *Aquarius*, and *Pisces*."
    sent_msg = bot.send_message(message.chat.id, text, parse_mode="Markdown")
    bot.register_next_step_handler(sent_msg, day_handler)

def day_handler(message): # Функция получения дня "предсказания"
    sign = message.text
    text = "What day do you want to know?\nChoose one: *TODAY*, *TOMORROW*, *YESTERDAY*, or a date in format YYYY-MM-DD."
    sent_msg = bot.send_message(
        message.chat.id, text, parse_mode="Markdown")
    bot.register_next_step_handler(
        sent_msg, fetch_horoscope, sign.capitalize())

def fetch_horoscope(message, sign): # Функция сборки и вывода сообщения с готовым гороскопом
    day = message.text
    horoscope = get_daily_horoscope(sign, day)
    data = horoscope["data"]
    horoscope_message = f'*Horoscope:* {data["horoscope_data"]}\n*Sign:* {sign}\n*Day:* {data["date"]}'
    bot.send_message(message.chat.id, "Here's your horoscope!")
    bot.send_message(message.chat.id, horoscope_message, parse_mode="Markdown")

if __name__ == "__main__": # Функция запуска бота
    bot.infinity_polling()