# -*- coding: utf-8 -*-  
import constants
import telebot
import pyowm

bot = telebot.TeleBot(constants.token_tlgrm)
owm = pyowm.OWM(constants.token_owm, language="ru")
stick_id = None

city = ["Зима", "Саянск"]

observation = owm.weather_at_place(city[0])
my_weather = observation.get_weather()

def renaming(name):
    list1 = list("aуеыаоэяиюь")
    list2 = list(name)
    if list2[-1] in list1:
        list2[-1] = "e"
    else:
        list2 += "e"
    return "".join(list2)

def get_sticker(status):
    if(status == "легкий дождь"):
        stick_id = "CAADAgADEwADn-jJF-fsRxrFhhlZAg"
    elif (status == "облачно"):
        stick_id = "CAADAgADEQADn-jJF1FfbuP1dormAg"
    elif (status == "ясно"):
        stick_id = "CAADAgADDwADn-jJF3eEyp2XvPhlAg"
    elif (status == "туманно") or (my_weather.get_detailed_status() == "слегка облачно"):
        stick_id = "CAADAgADEAADn-jJF1Es_DxZBlSJAg"
    elif (status == "пасмурно"):
        stick_id = "CAADAgADEgADn-jJFzNc_T-lE2l6Ag"
    else:
        stick_id = "CAADAgAD9wIAAlwCZQO1cgzUpY4T7wI"

def my_city(city1):
    letter = "Погода в <b>{0}</b> сейчас:\n\nТемпература: {1} °C\nВетер: {2} м/с\n{3}\n{4}".format(renaming(city1), 
                                                                            my_weather.get_temperature("celsius")["temp"], 
                                                                            my_weather.get_wind()["speed"], 
                                                                            my_weather.get_detailed_status().title(),
                                                                            my_weather.get_reference_time(timeformat='iso'))
    bot.send_message(message.from_user.id, letter, parse_mode="HTML")

@bot.message_handler(commands=["start"])
def handle_message(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row("Зима", "Саянск")
    bot.send_message(message.from_user.id, "Привет!\U0001f604", reply_markup=keyboard)

@bot.message_handler(content_types=["text"])
def handle_message(message):
    if message.text == "Зима":
        my_city(city[0])
    if message.text == "Саянск":
        my_city(city[1])            

    status = my_weather.get_detailed_status()
    get_sticker(status)

    bot.send_sticker(message.from_user.id, stick_id)

bot.polling(none_stop=True)