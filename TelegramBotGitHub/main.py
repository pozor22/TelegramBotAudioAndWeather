import telebot
from telebot import types
import requests
import random
from translate import Translator
import moviepy.editor
import os
import token_and_id

bot = telebot.TeleBot(token_and_id.token)

#до написания первого сообщения
@bot.message_handler(commands=["start"])
def start(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('/commands')
    item2 = types.KeyboardButton('/weather')
    keyboard.add(item1, item2)

    bot.send_message(message.chat.id, f"Привет, {message.from_user.first_name}, что ты хочешь?", reply_markup=keyboard)
##

#команды
@bot.message_handler(commands=["weather"])
def weather(message):
    s_city = "Moscow"
    res = requests.get("http://api.openweathermap.org/data/2.5/weather",params={'q': s_city, 'units': 'metric', 'lang': 'ru','APPID': "90384875b2584c9b256f52cc3d19bdfb"})
    data = res.json()
    bot.send_message(message.chat.id, f"City: {s_city} \r\nTemp: {data['main']['temp']} \r\nWeather: {data['weather'][0]['description']}")

@bot.message_handler(commands=["commands"])
def help(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('/help')
    item2 = types.KeyboardButton('/time')
    back = types.KeyboardButton('/back')
    keyboard.add(item1, item2, back)
    bot.send_message(message.chat.id, 'Вот такие команды я еще умею выполнять!', reply_markup=keyboard)

@bot.message_handler(commands=['back'])
def back(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('/help')
    item2 = types.KeyboardButton('/weather')
    keyboard.add(item1, item2)

    bot.send_message(message.chat.id, f"Снова привет, {message.from_user.first_name}", reply_markup=keyboard)

@bot.message_handler(commands=['help'])
def commands(message):
    bot.send_message(message.chat.id, 'Я умею: '
                                      '\r\nПоказывать погоду /weather '
                                      '\r\nОтделять аудиодорожку от видео, просто отправь мне видео'
                                      '\r\nПереводить с инглиша на русский')

@bot.message_handler(commands=['time'])
def nax(message):
    bot.send_message(message.chat.id, "привет, я пока этого не умею:(")
##

# Отделение аудиодорожки от видео
@bot.message_handler(content_types=["video"])
def audio(message):
    file_name = message.json['video']['file_name']
    file_info = bot.get_file(message.video.file_id)
    with open(file_name, "wb") as f:
        file_content = bot.download_file(file_info.file_path)
        f.write(file_content)

    video = moviepy.editor.VideoFileClip(file_name)
    audio = video.audio
    audio.write_audiofile(file_name + ".mp3")
    MesAudio = open(file_name + ".mp3", "rb")
    bot.send_audio(message.chat.id, MesAudio)
    os.remove(file_name)
    os.remove(file_name + ".mp3")

#не команды, а просто сообщения
@bot.message_handler()
def get_user_text(message):
    flag = random.randint(0, 100)
    if message.text == "лизка":
        bot.send_message(message.chat.id, "Вовка её любит", parse_mode="html")
    elif message.text == "привет":
        bot.send_message(message.chat.id, "привет")
    if flag == 56:
        bot.send_message(message.chat.id, 'лизка много пукает')
    translator = Translator(from_lang="eng", to_lang="rus")
    translation = translator.translate(message.text)
    bot.send_message(message.chat.id, translation)
##

#конец, бот не останавливается
if __name__ == '__main__':
    bot.polling()
##