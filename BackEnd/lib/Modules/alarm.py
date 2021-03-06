import json, re

def addAlarm(textToSpeech, phrases, text):
    textString = "";

    for index, string in enumerate(text):
        textString += string + (index == len(text) - 1 and "" or " ");

    textString = textString.replace("a.m.", "AM").replace("p.m.", "PM");
    alarmTime = textString.split(" at ")[1].upper().replace("PM ", "PM").replace("AM ", "AM"); # Jank AF
    speechString = "I have added a new alarm at " + alarmTime;
    textToSpeech(speechString);

    if ("AM" in alarmTime):
        alarmTime = alarmTime.replace(" AM", "") + ":59 AM";
    else:
        alarmTime = alarmTime.replace(" PM", "") + ":59 PM";

    file = open("data.json");
    fileContents = file.read();
    data = json.loads(fileContents);
    file.close();
    data["alarms"].append({
        # "sound": alarmSound, # Need to add custom alarm sounds
        "time": alarmTime
    });

    file = open("data.json", "w");
    file.write(json.dumps(data));
    file.close();

def removeAlarm(textToSpeech, phrases, text, server):
    textString = "";

    for index, string in enumerate(text):
        textString += string + (index == len(text) - 1 and "" or " ");

    textString = textString.replace("a.m.", "AM").replace("p.m.", "PM");
    alarmTime = textString.split(" at ")[1];
    speechString = "I have removed the alarm at " + alarmTime;
    textToSpeech(speechString);
    
    if ("AM" in alarmTime):
        alarmTime = alarmTime.replace(" AM", "") + ":59 AM";
    else:
        alarmTime = alarmTime.replace(" PM", "") + ":59 PM";

    file = open("data.json");
    fileContents = file.read();
    data = json.loads(fileContents);
    alarms = data["alarms"];
    
    for index, alarm in enumerate(alarms):
        if (alarm["time"] == alarmTime):
            data["alarms"][index] = None;
        
    file.write(json.dumps(data));
    file.close();