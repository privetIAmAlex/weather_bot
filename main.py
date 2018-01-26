# -*- coding: utf-8 -*-  
#import constants
import telebot
import pyowm

class MyCity:
    owm = pyowm.OWM("e2cc4904ab9d8d9e2c4c5f8bf44bde99", language="ru")
    observation = owm.weather_at_place("Саянск")
    my_weather = observation.get_weather()
    status = my_weather.get_detailed_status()    

    def get_forecast(self):
        return self.owm.daily_forecast("Саянск", limit=6)

    def renaming(self, name):
        list1 = list("aуеыаоэяиюь")
        list2 = list(name)
        if list2[-1] in list1:
            list2[-1] = "e"
        else:
            list2 += "e"
        return "".join(list2)

    def get_weather(self):   
        return "Погода в <b>{0}</b> сейчас:\n\n{3}\n<i>Температура: </i> {1} °C\n<i>Ветер: </i> {2} м/с\n<i>Последнее обновление: </i> {4}".format(self.renaming("Саянск"), 
                                                                            self.my_weather.get_temperature("celsius")["temp"], 
                                                                            self.my_weather.get_wind()["speed"], 
                                                                            self.my_weather.get_detailed_status().title(),
                                                                            self.my_weather.get_reference_time(timeformat='date'))
    
    def get_sticker(self):
        if(self.status == "легкий дождь"):
            return "CAADAgADEwADn-jJF-fsRxrFhhlZAg"
        elif (self.status == "облачно"):
            return "CAADAgADEQADn-jJF1FfbuP1dormAg"
        elif (self.status == "ясно"):
            return "CAADAgADDwADn-jJF3eEyp2XvPhlAg"
        elif (self.status == "туманно") or (self.status == "слегка облачно"):
            return "CAADAgADEAADn-jJF1Es_DxZBlSJAg"
        elif (self.status == "пасмурно"):
            return "CAADAgADEgADn-jJFzNc_T-lE2l6Ag"
        else:
            return "CAADAgAD9wIAAlwCZQO1cgzUpY4T7wI"

def file_write(param1, param2):
    file = open("data.txt", 'a')
    file.write(f"{param1} : {param2};\n")  
    file.close()

def file_read():
    file = open("data.txt", 'r')
    data = ""
    ex = file.readlines()
    for i in range(len(ex)):
        data += ex[i]
    file.close()
    return data

if __name__ == "__main__":
    bot = telebot.TeleBot("399505636:AAFB3JnhsS6FaJdJtTAozDRKDVvYAG5s3iw")

    @bot.message_handler(commands=["start"])
    def handle_command(command):
        # Запись пользователей в файл
        try:
            file_write(command.chat.username, command.chat.id)
        except Exception as identifier:
            bot.send_message(command.chat.id, identifier)   

        keyboard = telebot.types.ReplyKeyboardMarkup(True)
        keyboard.row("Погода сейчас", "Погода завтра")
        bot.send_message(command.from_user.id, "Привет!\U0001f604", reply_markup=keyboard)

    @bot.message_handler(content_types=["text"])
    def handle_message(message):
        myCity = MyCity()
        if message.text == "hiked29hdknedf":
            try:
                data = file_read()
                bot.send_message(message.chat.id, data)
            except Exception as identifier:               
                bot.send_message(message.chat.id, identifier)
        elif message.text == "Погода сейчас":
            bot.send_message(message.chat.id, myCity.get_weather(), parse_mode="html")
            bot.send_sticker(message.chat.id, myCity.get_sticker())
        else:
            bot.send_message(message.chat.id, myCity.get_forecast())            
            bot.send_message(message.chat.id, "сломалось нахуй")            

    
    bot.polling(none_stop=True)