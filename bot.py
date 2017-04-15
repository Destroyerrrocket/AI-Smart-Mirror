# bot.py
# -*- coding: utf-8 -*-
# speechrecognition, pyaudio, brew install portaudio
import sys
reload(sys)
sys.setdefaultencoding('utf8')
sys.path.append("./")

import requests
import datetime
import dateutil.parser
import json
import traceback
from nlg import NLG
from speech import Speech
from knowledge import Knowledge
from vision import Vision

my_name = "Pol"
launch_phrase = "ok elena"
use_launch_phrase = True
weather_api_token = "86ac0cf3006b2a3c9ac8234270d81c05"
wit_ai_token = "Bearer OAEDKP5G7KCTUSJ5IXAHT5N4EHV7OVFH"
debugger_enabled = True
camera = 0


class Bot(object):
    def __init__(self):
        self.nlg = NLG(user_name=my_name)
        self.speech = Speech(launch_phrase=launch_phrase, debugger_enabled=debugger_enabled)
        self.knowledge = Knowledge(weather_api_token)
        self.vision = Vision(camera=camera)

    def start(self):
        """
        Main loop. Waits for the launch phrase, then decides an action.
        :return:
        """
        while True:
            requests.get("http://localhost:8080/clear")
            if self.vision.recognize_face():
                print "Found face"
                if use_launch_phrase:
                    recognizer, audio = self.speech.listen_for_audio()
                    if self.speech.is_call_to_action(recognizer, audio):
                        self.__acknowledge_action()
                        self.decide_action()
                else:
                    self.decide_action()

    def decide_action(self):
        """
        Recursively decides an action based on the intent.
        :return:
        """
        recognizer, audio = self.speech.listen_for_audio()

        # received audio data, now we'll recognize it using Google Speech Recognition
        speech = self.speech.google_speech_recognition(recognizer, audio)

        if speech is not None:
            try:
                r = requests.get('https://api.wit.ai/message?v=20160918&q=%s' % speech,
                                 headers={"Authorization": wit_ai_token})
                print r.text
                json_resp = json.loads(r.text)
                entities = None
                intent = None
                if 'entities' in json_resp and 'Intent' in json_resp['entities']:
                    entities = json_resp['entities']
                    intent = json_resp['entities']['Intent'][0]["value"]

                print intent
                if intent == 'greeting':
                    self.__text_action(self.nlg.greet())
                elif intent == 'snow white':
                    self.__text_action(self.nlg.snow_white())
                elif intent == 'weather':
                    self.__weather_action(entities)
                elif intent == 'news':
                    self.__news_action()
                elif intent == 'maps':
                    self.__maps_action(entities)
                elif intent == 'holidays':
                    self.__holidays_action()
                elif intent == 'appearance':
                    self.__appearance_action()
                elif intent == 'user status':
                    self.__user_status_action(entities)
                elif intent == 'user name':
                    self.__user_name_action()
                elif intent == 'personal status':
                    self.__personal_status_action()
                elif intent == 'joke':
                    self.__joke_action()
                elif intent == 'insult':
                    self.__insult_action()
                    return
                elif intent == 'Dirt':
                    self.__Dirt_action()
                    return
                elif intent == 'Hi':
                    self.__Hi_action()
                    return
                elif intent == 'years':
                    self.__years_action()
                    return
                elif intent == 'livelocation':
                    self.__livelocation_action()
                    return
                elif intent == 'Private':
                    self.__Private_action()
                    return
                elif intent == 'rantime':
                    self.__rantime_action()
                    return
                elif intent == 'appreciation':
                    self.__appreciation_action()
                    return
                elif intent == 'creator':
                    self.__creator_action()
                    return
                elif intent == 'meaning of life':
                    self.__meaning_action()
                    return
                elif intent == 'Futbol':
                    self.__Futbol_action()
                    return
                elif intent == 'filosofy':
                    self.__filosofy_action()
                    return
                elif intent == 'RandomNum':
                    self.__RandomNum_action()
                    return
                else:
                    self.__nonerror_action()
                    return

            except Exception as e:
                print "wit ha fallado, Pol, QUÉ HACES?!"
                print(e)
                traceback.print_exc()
                self.__text_action("Lo siento, no te he entendido.")
                return

            self.decide_action()

    def __joke_action(self):
        joke = self.nlg.joke()

        if joke is not None:
            self.__text_action(joke)
        else:
            self.__text_action("Lo siento, no he encontrado ninguna broma.")

    def __user_status_action(self, nlu_entities=None):
        attribute = None

        if (nlu_entities is not None) and ("Status_Type" in nlu_entities):
            attribute = nlu_entities['Status_Type'][0]['value']

        self.__text_action(self.nlg.user_status(attribute=attribute))

    def __user_name_action(self):
        if self.nlg.user_name is None:
            self.__text_action("No sé tu nombre. puedes configurarlo en bot.py")

        self.__text_action(self.nlg.user_name)

    def __appearance_action(self):
        requests.get("http://localhost:8080/face")
        self.speech.synthesize_text(self.nlg.appearance())
    def __appreciation_action(self):
        self.__text_action(self.nlg.appreciation())

    def __creator_action(self):
    	requests.get("http://localhost:8080/creator")
    	self.speech.synthesize_text(self.nlg.creator())



    def __acknowledge_action(self):
        self.__text_action(self.nlg.acknowledge())
    def __Private_action(self):
        self.__text_action(self.nlg.Private())
    def __rantime_action(self):
        self.__text_action(self.nlg.rantime())
    def __meaning_action(self):
        self.__text_action(self.nlg.meaning_of_life())

    def __insult_action(self):
        self.__text_action(self.nlg.insult())

    def __Dirt_action(self):
        self.__text_action(self.nlg.Dirt())

    def __Hi_action(self):
        self.__text_action(self.nlg.Hi())

    def __Futbol_action(self):
        self.__text_action(self.nlg.Futbol())

    def __RandomNum_action(self):
        self.__text_action(self.nlg.RandomNum())

    def __filosofy_action(self):
        self.__text_action(self.nlg.filosofy())

    def __years_action(self):
        self.__text_action(self.nlg.years())

    def __livelocation_action(self):
        self.__text_action(self.nlg.livelocation())

    def __personal_status_action(self):
        self.__text_action(self.nlg.personal_status())

    def __nonerror_action(self):
        self.__text_action(self.nlg.nonerror())

    def __text_action(self, text=None):
        if text is not None:
            requests.get("http://localhost:8080/statement?text=%s" % text)
            self.speech.synthesize_text(text)

    def __news_action(self):
        headlines = self.knowledge.get_news()

        if headlines:
            requests.post("http://localhost:8080/news", data=json.dumps({"articles":headlines}))
            self.speech.synthesize_text(self.nlg.news("past"))
            interest = self.nlg.article_interest(headlines)
            if interest is not None:
                self.speech.synthesize_text(interest)
        else:
            self.__text_action("He tenido problemas encontrando noticias.")

    def __weather_action(self, nlu_entities=None):

        current_dtime = datetime.datetime.now()
        skip_weather = False # used if we decide that current weather is not important

        weather_obj = self.knowledge.find_weather()
        temperature = weather_obj['temperature']
        icon = weather_obj['icon']
        wind_speed = weather_obj['windSpeed']

        weather_speech = self.nlg.weather(temperature, current_dtime, "present")
        forecast_speech = None

        if nlu_entities is not None:
            if 'datetime' in nlu_entities:
                if 'grain' in nlu_entities['datetime'][0] and nlu_entities['datetime'][0]['grain'] == 'day':
                    dtime_str = nlu_entities['datetime'][0]['value'] # 2016-09-26T00:00:00.000-07:00
                    dtime = dateutil.parser.parse(dtime_str)
                    if current_dtime.date() == dtime.date(): # hourly weather
                        forecast_obj = {'forecast_type': 'hourly', 'forecast': weather_obj['daily_forecast']}
                        forecast_speech = self.nlg.forecast(forecast_obj)
                    elif current_dtime.date() < dtime.date(): # sometime in the future ... get the weekly forecast/ handle specific days
                        forecast_obj = {'forecast_type': 'daily', 'forecast': weather_obj['weekly_forecast']}
                        forecast_speech = self.nlg.forecast(forecast_obj)
                        skip_weather = True
            if 'Weather_Type' in nlu_entities:
                weather_type = nlu_entities['Weather_Type'][0]['value']
                print weather_type
                if weather_type == "current":
                    forecast_obj = {'forecast_type': 'current', 'forecast': weather_obj['current_forecast']}
                    forecast_speech = self.nlg.forecast(forecast_obj)
                elif weather_type == 'today':
                    forecast_obj = {'forecast_type': 'hourly', 'forecast': weather_obj['daily_forecast']}
                    forecast_speech = self.nlg.forecast(forecast_obj)
                elif weather_type == 'tomorrow' or weather_type == '3 day' or weather_type == '7 day':
                    forecast_obj = {'forecast_type': 'daily', 'forecast': weather_obj['weekly_forecast']}
                    forecast_speech = self.nlg.forecast(forecast_obj)
                    skip_weather = True


        weather_data = {"temperature": temperature, "icon": icon, 'windSpeed': wind_speed, "hour": datetime.datetime.now().hour}
        requests.post("http://localhost:8080/weather", data=json.dumps(weather_data))

        if not skip_weather:
            self.speech.synthesize_text(weather_speech)

        if forecast_speech is not None:
            self.speech.synthesize_text(forecast_speech)

    def __maps_action(self, nlu_entities=None):

        location = None
        map_type = None
        if nlu_entities is not None:
            if 'location' in nlu_entities:
                location = nlu_entities['location'][0]["value"]
            if "Map_Type" in nlu_entities:
                map_type = nlu_entities['Map_Type'][0]["value"]

        if location is not None:
            maps_url = self.knowledge.get_map_url(location, map_type)
            maps_action = "por supuesto. aquí tienes un mapa de %s." % location
            body = {'url': maps_url}
            requests.post("http://localhost:8080/image", data=json.dumps(body))
            self.speech.synthesize_text(maps_action)
        else:
            self.__text_action("Lo siento, no encontré la localización que querías.")

    def __holidays_action(self):
        holidays = self.knowledge.get_holidays()
        next_holiday = self.__find_next_holiday(holidays)
        requests.post("http://localhost:8080/holidays", json.dumps({"holiday": next_holiday}))
        self.speech.synthesize_text(self.nlg.holiday(next_holiday['localName']))

    def __find_next_holiday(self, holidays):
        today = datetime.datetime.now()
        for holiday in holidays:
            date = holiday['date']
            if (date['day'] > today.day) and (date['month'] > today.month):
                return holiday

        # next year
        return holidays[0]

if __name__ == "__main__":
    bot = Bot()
    bot.start()
