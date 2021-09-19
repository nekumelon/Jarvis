from lib.Modules._time import _time
from lib.Modules.greet import greet
from lib.Modules.date import day, week, month, year, date
from lib.Modules.ip import ip
from lib.Modules.shutdown import shutdown
from lib.Modules._wikipedia import _wikipedia
from lib.Modules.news import news
from lib.Modules.internetSpeed import upload, download
from lib.Modules.system import cpu, ram
from lib.Modules.weather import weather, temperature, airPressure, windSpeed, humidity
from lib.Modules.joke import joke
from lib.Modules.wolfram_alpha import wolfram
from lib.Modules.music import *
import json, _thread

file = open("lib/Speech/phrases.json", "r");
fileContents = file.read();
file.close();
phrases = json.loads(fileContents);
prefixes = {
    "jarvis",
    "arvest",
    "harvest",
    "garvis"
};

modules = {
    "time": _time,
    "day": day,
    "week": week,
    "month": month,
    "year": year,
    "date": date,
    "ip": ip,
    "shutdown": shutdown,
    "wikipedia": _wikipedia,
    "news": news,
    "upload": upload,
    "download": download,
    "ram": ram,
    "cpu": cpu,
    "weather": weather,
    "temperature": temperature,
    "air pressure": airPressure,
    "wind speed": windSpeed,
    "humidity": humidity,
    "joke": joke,
    "play": play,
    "pause": pause,
    "unpause": unpause,
    "restart": restart,
    "stop": stop,
    "volume": volume,
    "mute": mute
};

class Processor():
    def __init__(self, textToSpeech, sms, number):
        self.textToSpeech = textToSpeech;
        self.sms = sms;
        self.number = number;

        try:
            self.lastSMS = sms.receive(number)[0];
        except:
            self.lastSMS = "";

    def process(self, text):
        text = text.lower();
        tokens = self.tokenize(text);
        location = 0;
        prefixed = False;
        commandFound = False;

        for prefix in prefixes:
            if (prefix in tokens):
                prefixed = True;

        if (prefixed):
            while (not commandFound and location < len(tokens)):
                if (tokens[location] in phrases["greetings"]):
                    if (len(tokens) < 3):
                        greet(self.textToSpeech, phrases, tokens);
                        commandFound = True;

                        break;
                    else:
                        location += 1;

                try:
                    if (tokens[location + 1] in phrases["questionIdentifiers"]):
                        location += 2;

                        if (tokens[location] in modules):
                            module = modules[tokens[location]];
                            module(self.textToSpeech, phrases, tokens);
                            commandFound = True;

                            break;
                except:
                    errored = True;

                if (tokens[location] in modules):
                    module = modules[tokens[location]];
                    module(self.textToSpeech, phrases, tokens);
                    commandFound = True;

                    break;

                location += 1;   

            if (not commandFound):
                wolfram(self.textToSpeech, phrases, tokens);

    def tokenize(self, text):
        tokens = [];
        words = text.split(" ");

        for word in words:
            tokens.append(word);

        return tokens;

    def handleSMS(self):
        def smsThread(threadName, delay):
            while (True):
                messages = self.sms.receive(self.number);

                try:
                    lastMessage = messages[0];
                except:
                    lastMessage = "";

                if (lastMessage != self.lastSMS):
                    self.textToSpeech("You have a new text message from your twilio account. " + lastMessage);
                    self.lastSMS = lastMessage;

        _thread.start_new_thread(smsThread, ("Thread-2", 1, ));