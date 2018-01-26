# -*- coding: utf-8 -*-  
#import constants
import telebot
import pyowm
import user_counts

class MyCity:
    stick_id = 0
    city = ""
    status = ""

    def __init__(self, name):
        self.city = name

    owm = pyowm.OWM("e2cc4904ab9d8d9e2c4c5f8bf44bde99", language="ru")

    def renaming(self, name):
        list1 = list("aуеыаоэяиюь")
        list2 = list(name)
        if list2[-1] in list1:
            list2[-1] = "e"
        else:
            list2 += "e"
        return "".join(list2)

    def send_weather(self):
        observation = self.owm.weather_at_place(self.city)
        my_weather = observation.get_weather()
        status = my_weather.get_detailed_status()
        self.status = self.get_sticker(status)
        return "Погода в <b>{0}</b> сейчас:\n\nТемпература: {1} °C\nВетер: {2} м/с\n{3}\n{4}".format(self.renaming(self.city), 
                                                                            my_weather.get_temperature("celsius")["temp"], 
                                                                            my_weather.get_wind()["speed"], 
                                                                            my_weather.get_detailed_status().title(),
                                                                            my_weather.get_reference_time(timeformat='iso'))
    
    def get_sticker(self, status):
        if(status == "легкий дождь"):
            stick_id = "CAADAgADEwADn-jJF-fsRxrFhhlZAg"
        elif (status == "облачно"):
            stick_id = "CAADAgADEQADn-jJF1FfbuP1dormAg"
        elif (status == "ясно"):
            stick_id = "CAADAgADDwADn-jJF3eEyp2XvPhlAg"
        elif (status == "туманно") or (status == "слегка облачно"):
            stick_id = "CAADAgADEAADn-jJF1Es_DxZBlSJAg"
        elif (status == "пасмурно"):
            stick_id = "CAADAgADEgADn-jJFzNc_T-lE2l6Ag"
        else:
            stick_id = "CAADAgAD9wIAAlwCZQO1cgzUpY4T7wI"
        return stick_id


if __name__ == "__main__":
    bot = telebot.TeleBot("399505636:AAFB3JnhsS6FaJdJtTAozDRKDVvYAG5s3iw")    

    @bot.message_handler(commands=["start"])
    def handle_command(command):
        if command.chat.id in user_counts.user_ID:
            pass
        else:
            user_counts.user_ID.append(command.chat.id)
            user_counts.user_count += 1
            upd = {command.chat.username : command.chat.id}
            user_counts.user_list.update(upd)
        keyboard = telebot.types.ReplyKeyboardMarkup(True)
        keyboard.row("Зима", "Саянск")
        bot.send_message(command.from_user.id, "Привет!\U0001f604", reply_markup=keyboard)

    @bot.message_handler(content_types=["text"])
    def handle_message(message):
        if message.text == "hiked29hdknedf":
            bot.send_message(message.chat.id, "{}\n{}".format(user_counts.user_count, user_counts.user_list))
        else:          
            myCity = MyCity(message.text)
            bot.send_message(message.chat.id, myCity.send_weather(), parse_mode="html")
            bot.send_sticker(message.chat.id, myCity.status)


    bot.polling(none_stop=True)

#command.chat.username