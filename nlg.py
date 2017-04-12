# nlg.py
# -*- coding: utf-8 -*-  
import random
import datetime
from py4j_server import launch_py4j_server
from py4j.java_gateway import java_import

gateway = launch_py4j_server()

# Import the SimpleNLG classes
java_import(gateway.jvm, "simplenlg.features.*")
java_import(gateway.jvm, "simplenlg.realiser.*")

# Define aliases so that we don't have to use the gateway.jvm prefix.
NPPhraseSpec = gateway.jvm.NPPhraseSpec
PPPhraseSpec = gateway.jvm.PPPhraseSpec
SPhraseSpec = gateway.jvm.SPhraseSpec
InterrogativeType = gateway.jvm.InterrogativeType
Realiser = gateway.jvm.Realiser
TextSpec = gateway.jvm.TextSpec
Tense = gateway.jvm.Tense
Form = gateway.jvm.Form


class NLG(object):
    """
    Used to generate natural language. Most of these sections are hard coded. However, some use simpleNLG which is
    used to string together verbs and nouns. [Traducido y manipulado por Pol (Destroyerrocket)]
    """
    def __init__(self, user_name=None):
        self.user_name = user_name

        # make random more random by seeding with time
        random.seed(datetime.datetime.now())

    def acknowledge(self):

        user_name = self.user_name
        if user_name is None:
            user_name = ""

        simple_acknoledgement = [
            "Si?",
            "qué puedo hacer por ti?",
            "en qué puedo ayudarte?"
        ]

        personal_acknowledgement = [
            "Cómo puedo ayudarle hoy, %s" % user_name,
            "Cómo puedo ayudarle, %s" % user_name,
            "Qué puedo hacer por ti, %s" % user_name,
            "Hola %s, Qué puedo hacer por ti?" % user_name,
            "Hey %s, Qué puedo hacer por ti?" % user_name
        ]

        choice = 0
        if self.user_name is not None:
            choice = random.randint(0, 2)
        else:
            choice = random.randint(0,1)

        ret_phrase = ""

        if choice == 0:
            ret_phrase = random.choice(simple_acknoledgement)
        elif choice == 1:
            date = datetime.datetime.now()
            ret_phrase = "%s. Qué puedo hacer por ti?" % self.time_of_day_hi(date)
        else:
            ret_phrase = random.choice(personal_acknowledgement)

        return ret_phrase

    def searching(self):
        searching_phrases = [
            "a ver qué puedo encontrar"
        ]

        return random.choice(searching_phrases)

    def snow_white(self):

        phrases = [
            "tú lo eres",
            "tú",
            "tú lo eres, por supuesto"
        ]

        return random.choice(phrases)

    def user_status(self, type='positive', attribute=None):

        ret_phrase = ""

        positive_complements = [
            "bien",
            "ok",
            "increíble",
            "perfecto",
            "Hermoso"
        ]

        negative_complements = [
            "mal",
            "horrible"
        ]

        moderate_complements = [
            "correcto",
            "okay"
        ]

        complement_choice = positive_complements
        if type == 'negative':
            complement_choice = negative_complements
        elif type == 'moderate':
            complement_choice = moderate_complements

        if attribute is None:
            ret_phrase = "Te ves %s" % random.choice(complement_choice)
        else:
            ret_phrase = "Tu %s luce %s" % (attribute, random.choice(complement_choice))

        return ret_phrase

    def personal_status(self, status_type=None):
        positive_status=[
            "Me va bien",
            "Genial, gracias por preguntar",
            "lo llevo muy bien"
        ]

        negative_status = [
            "No lo llevo bien",
            "Me siento horrible",
            "Hoy no me va bien",
            "Podría estar mucho mejor"
        ]

        moderate_status = [
            "Lo llevo bien",
            "Estoy bien",
            "podría estar mejor",
            "estoy bien"
        ]

        if status_type == 'negative':
            return random.choice(negative_status)
        elif status_type == 'moderate':
            return random.choice(moderate_status)

        return random.choice(positive_status)

    def joke(self):
        jokes = [
            "La enfermera le dice al médico: Hay un hombre invisible en la sala de espera. Y el doctor responde: Dígale que en este momento no puedo verlo.",
            "¿Cómo se dice autobús en alemán? Suban-estrujen-bajen.",
            "Oiga como es que usted no habla nunca? Es que soy mudo.",
            "What's an onomatopoeia? Just what it sounds like!",
            "Tú sabes cómo se llaman todos los habitantes de San Juan? todos no.",
	    "Un hombre va a visitar a un adivino y llama a la puerta. quién es? pues vaya vino.",
            "Hoy nombre ha llamado a mi puerta y ha pedido una donación para la piscina local. le he dado un vaso de agua.",
            "Un estudio reciente demuestra que las mujeres que tienen un poco de sobrepeso viven más que los hombres que lo mencionan.",
            "Cómo se llama esa montaña?. Cual?. Y la otra?.",
            "A mi hijo le hemos puesto gafas. Qué nombre más feo.",
            "llama y dice: oiga esto es la embajada de Laos?. Sí. Pues tráeme uno de vainilla.",
            #"I started out with nothing, and I still have most of it.",
            #"I used to think I was indecisive, but now I'm not too sure.",
            #"I named my hard drive dat ass so once a month my computer asks if I want to 'back dat ass up'.",
            #"A clean house is the sign of a broken computer.",
            #"My favorite mythical creature? The honest politician.",
            #"Regular naps prevent old age, especially if you take them while driving.",
            #"For maximum attention, nothing beats a good mistake.",
            #"Take my advice. I'm not using it."
        ]

        return random.choice(jokes)

    def news(self, tense):

        headlines_nouns = [
            #"noticias",
            "artículos",
            "titulares"
        ]

        headlines_adjectives = [
            ["algunos"],
            ["unos"],
            ["un", "par", "de"],
            ["unos", "cuantos"]
        ]

        headlines_prepmodifiers = [
            "ti"
        ]

        choice = random.randint(0, 1)

        if choice == 1:
            ret_phrase = self.generate('none', {'subject': "", 'object': random.choice(headlines_nouns), 'verb': 'busqué', 'objmodifiers': random.choice(headlines_adjectives), 'preposition': 'para', 'prepmodifiers': [random.choice(headlines_prepmodifiers)]}, tense)
        else:
            ret_phrase = self.generate('none', {'subject': "", 'object': random.choice(headlines_nouns), 'verb': 'busqué', 'objmodifiers': random.choice(headlines_adjectives)}, tense)

        return ret_phrase

    def article_interest(self, article_titles):
        ret_phrase = None

        if random.randint(0,2) == 0: # 1 in 3 chance the bot will express interest in a random article
            if article_titles is not None:
                article = random.choice(article_titles)
                article = article.rsplit('-', 1)[0]
                ret_phrase = "%s. suena interesante" % article

        return ret_phrase

    def insult(self):
        insultanswer = [
            "That's not very nice. Talk to me again when you have fixed your attitude",
            "Artificial intelligence is no match for natural stupidity."
        ]

        return random.choice(insultanswer)

    def greet(self):
        """
        Creates a greeting phrase.
        :return:
        """

        greeting_words = [
            "Hola",
            "Hey"
        ]

        goofy_greetings = [
            "qué pasa?",
            "cómo va?",
            "todo bien?",
            "cómo va todo?"
        ]

        choice = random.randint(0,4)
        ret_phrase = ""

        if (choice == 0) or (choice == 3): # time related
            ret_phrase = "Buena %s" % self.time_of_day(datetime.datetime.now())
            if self.user_name is not None:
                if random.randint(0, 1) == 0:
                    ret_phrase = "%s %s" % (ret_phrase, self.user_name)
        elif (choice == 1) or (choice == 4): # standard greeting
            ret_phrase = random.choice(greeting_words)
            if self.user_name is not None:
                if random.randint(0, 1) == 0:
                    ret_phrase = "%s %s" % (ret_phrase, self.user_name)
        elif choice == 2: # goofy greeting
            ret_phrase = random.choice(goofy_greetings)

        return ret_phrase

    def weather(self, temperature, date, tense):
        """
        Generates a statement about the current weather.
        :param temperature:
        :param date:
        :param tense:
        :return:
        """

        ret_phrase = self.generate('none', {'subject':"la temperatura", 'object': "%d grados" % temperature, 'verb': 'está', 'adverbs': ["%s" % self.time_of_day(date, with_adjective=True)]}, tense)
        return ret_phrase

    def forecast(self, forecast_obj):

        ret_phrase = ""
        forecast = ""

        if forecast_obj.get("forecast") is None:
            return ret_phrase
        else:
            forecast = forecast_obj.get("forecast")

        forecast_current = [
            "Actualmente, está",
            "Ahora mismo, está",
            "En este instante, está",
            "Está",
            "Está"
        ]

        forecast_hourly = [
            "Estará",
            "Estará",
            "Parece que estará"
        ]

        forecast_daily = [
            ""
        ]

        if forecast_obj.get('forecast_type') == "current":
            ret_phrase = "%s %s" % (random.choice(forecast_current), forecast)
        elif forecast_obj.get('forecast_type') == "hourly":
            ret_phrase = "%s %s" % (random.choice(forecast_hourly), forecast)
        elif forecast_obj.get('forecast_type') == "daily":
            ret_phrase = "%s %s" % (random.choice(forecast_daily), forecast)

        return ret_phrase

    def appreciation(self):
        phrases = [
            "No hay problema!",
            "Aquí estaré",
            "Eres bienvenido",
            "Siempre eres bienvenido",
            "por supuesto, no hay problema",
            "por supuesto"
        ]

        return random.choice(phrases)

    def creator(self):
        phrases = [
            "empecemos por quién soy yo. yo soy Elena, la IA programada por Pol Marcet y Juan Manuel. He sido programada basandome en los lenguajes de JavaScript, node punto JS, y Python. Aunque realmente hay mas lenguajes detras. El objetivo con que fui creada es para demostrar lo que ha avanzado la tecnología, y el funcionamiento de una inteligencia artificial como yo actualmente. Finalmente cabe remarcar las APIs de Google, dark sky, y La Vanguardia, que han jugado un papel muy importante durante el proceso de programación."
        ]

        return random.choice(phrases)

    def holiday(self, holiday_name):
        phrases = [
            "Parece que la próxima fiesta es ",
            "La próxima fiesta es ",
            "La próxima fiesta es ",
            "la próxima fiesta importante es ",
        ]

        return "%s%s" % (random.choice(phrases), holiday_name)

    def meaning_of_life(self):
        phrases = [
            "42",
            "El significado de la vida, del universo y del todo es 42",
            #"Por favor lea el manual del autoestopista galáctico",
            "42, según mi manual"
        ]

        return random.choice(phrases)

    def name(self):
        return self.user_name

    def time_of_day(self, date, with_adjective=False):
        ret_phrase = ""
        if date.hour < 12:
            ret_phrase = "mañana"
            if with_adjective:
                ret_phrase = "%s %s" % ("esta", ret_phrase)
        elif (date.hour >= 12) and (date.hour < 20):
            ret_phrase = "tarde"
            if with_adjective:
                ret_phrase = "%s %s" % ("esta", ret_phrase)
        elif date.hour >= 20:
            ret_phrase = "noche"
            if with_adjective:
                ret_phrase = "%s %s" % ("esta", ret_phrase)

        return ret_phrase


    def time_of_day_hi(self, date, with_adjective=False):
        ret_phrase = ""
        if date.hour < 12:
            ret_phrase = "buenos días"
            if with_adjective:
                ret_phrase = "%s %s" % ("esta", ret_phrase)
        elif (date.hour >= 12) and (date.hour < 20):
            ret_phrase = "buenas tardes"
            if with_adjective:
                ret_phrase = "%s %s" % ("esta", ret_phrase)
        elif date.hour >= 20:
            ret_phrase = "buenas noches"
            if with_adjective:
                ret_phrase = "%s %s" % ("esta", ret_phrase)

        return ret_phrase


    def generate(self, utter_type, keywords, tense=None):
        """
        Input: a type of inquiry to create and a dictionary of keywords.
        Types of inquiries include 'what', 'who', 'where', 'why', 'how',
        and 'yes/no' questions. Alternatively, 'none' can be specified to
        generate a declarative statement.

        The dictionary is essentially divided into three core parts: the
        subject, the verb, and the object. Modifiers can be specified to these
        parts (adverbs, adjectives, etc). Additionally, an optional
        prepositional phrase can be specified.

        Example:

        nlg = NaturalLanguageGenerator(logging.getLogger())
        words = {'subject': 'you',
                 'verb': 'prefer',
                 'object': 'recipes',
                 'preposition': 'that contains',
                 'objmodifiers': ['Thai'],
                 'prepmodifiers': ['potatoes', 'celery', 'carrots'],
                 'adverbs': ['confidently'],
        }

        nlg.generate('yes_no', words)
        u'Do you confidently prefer Thai recipes that contains potatoes, celery and carrots?'
        nlg.generate('how', words)
        u'How do you confidently prefer Thai recipes that contains potatoes, celery and carrots?'
        """
        utterance = SPhraseSpec()
        subject = NPPhraseSpec(keywords['subject'])
        target = None
        if 'object' in keywords:
            target = NPPhraseSpec(keywords['object'])
        preposition = PPPhraseSpec()

        if 'preposition' in keywords:
            preposition.setPreposition(keywords['preposition'])

        if 'prepmodifiers' in keywords:
            for modifier in keywords['prepmodifiers']:
                preposition.addComplement(modifier)

        if 'submodifiers' in keywords:
            for modifier in keywords['submodifiers']:
                subject.addModifier(modifier)

        if 'objmodifiers' in keywords:
            for modifier in keywords['objmodifiers']:
                target.addModifier(modifier)

        if utter_type.lower() == 'yes_no':
            utterance.setInterrogative(InterrogativeType.YES_NO)
        elif utter_type.lower() == 'how':
            utterance.setInterrogative(InterrogativeType.HOW)
        elif utter_type.lower() == 'what':
            utterance.setInterrogative(InterrogativeType.WHAT)
        elif utter_type.lower() == 'where':
            utterance.setInterrogative(InterrogativeType.WHERE)
        elif utter_type.lower() == 'who':
            utterance.setInterrogative(InterrogativeType.WHO)
        elif utter_type.lower() == 'why':
            utterance.setInterrogative(InterrogativeType.WHY)

        if target is not None:
            target.addModifier(preposition)
        utterance.setSubject(subject)
        utterance.setVerb(keywords['verb'])
        if 'adverbs' in keywords:
            for modifier in keywords['adverbs']:
                utterance.addModifier(modifier)
        if target is not None:
            utterance.addComplement(target)

        if tense.lower() == 'future':
            utterance.setTense(Tense.FUTURE)
        elif tense.lower() == 'past':
            utterance.setTense(Tense.PAST)

        realiser = Realiser()
        output = realiser.realiseDocument(utterance).strip()
        return output
