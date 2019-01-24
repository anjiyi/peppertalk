from urllib import request as urlrequest
import apiai
import json
import pyowm
import random
import sys, requests, os
import urllib

CLIENT_ACCESS_TOKEN = os.environ["CLIENT_ACCESS_TOKEN"]
ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)
PAT = os.environ["PAT"]


def parse_user_message(user_text):
    """
    Send the message to API AI which invokes an intent
    and sends the response accordingly
    The bot response is appened with weaher data fetched from
    open weather map client
    """

    if request_quote(user_text):
        response = respond_quote()
        return response

    elif request_synonyms(user_text):
        try:
            max_words = [int(n) for n in user_text.split() if n.isdigit()][0]
        except:
            max_words = 3
        user_text = user_text.split("similar to ")[1]
        response = respond_synonyms(user_text, max_words)
        return response

    elif request_meaning(user_text):
        user_text = user_text.split("of ")[1]
        response = respond_meaning(user_text)
        return response

    else:

        request = ai.text_request()
        request.query = user_text

        response = json.loads(request.getresponse().read().decode("utf-8"))
        responseStatus = response["status"]["code"]
        if responseStatus == 200:

            print("API AI response", response["result"]["fulfillment"]["speech"])
            if "geo-city" in response["result"]["parameters"]:
                input_city = response["result"]["parameters"]["geo-city"]
                weather_report = respond_weather(input_city)

                return response["result"]["fulfillment"]["speech"] + weather_report

            else:
                return response["result"]["fulfillment"]["speech"]

        else:
            return "Sorry, I couldn't understand that question"


def send_message_response(sender_id, message_text):

    sentenceDelimiter = ". "
    messages = message_text.split(sentenceDelimiter)

    for message in messages:
        send_message(sender_id, message)


def send_message(sender_id, message_text):
    """
    Sending response back to the user using facebook graph API
    """
    r = requests.post(
        "https://graph.facebook.com/v2.6/me/messages",
        params={"access_token": PAT},
        headers={"Content-Type": "application/json"},
        data=json.dumps(
            {"recipient": {"id": sender_id}, "message": {"text": message_text}}
        ),
    )
    print(r.__dict__)


def respond_meaning(user_text):
    input_list = user_text.split()
    input_string = "+".join(input_list)

    print("Meaning requested for " + " ".join(input_list))
    output = urlrequest.urlopen(
        "https://api.datamuse.com/words?sp=" + input_string + "&md=d&max=1"
    ).read()

    defs = json.loads(output)[0]["defs"]
    defs = [d.replace("\t", ": ") for d in defs]
    defs = [d + ". " for d in defs]

    print("Meaning responded: " + "\n".join(defs))
    return "\n".join(defs)


def respond_synonyms(user_text, output_count=3):
    input_list = user_text.split()
    input_string = "+".join(input_list)

    print("Synonyms requested for " + " ".join(input_list))
    output = urlrequest.urlopen(
        "https://api.datamuse.com/words?ml="
        + input_string
        + "&max="
        + str(output_count)
    ).read()

    output_json = json.loads(output)
    words = []
    for word in output_json:
        words.append(word["word"])

    print("Synonyms responded: " + " ".join(words))
    return "\n".join(words)


def request_meaning(user_text):
    user_text = user_text.lower()
    if "meaning" in user_text:
        return True


def respond_quote():
    with open("quotes.json", encoding="utf-8") as f:
        quotes = json.load(f)["quotes"]

    quote = random.choice(quotes)
    print("Quote responded:", quote["quote"] + " --" + quote["author"])
    return quote["quote"] + " --" + quote["author"]


def request_synonyms(user_text):
    user_text = user_text.lower()
    if "words" in user_text and "similar to" in user_text:
        return True


def request_quote(user_text):
    user_text = user_text.lower()
    request_key_words = ["quote", "give me something spicy", "more spicy", "yes please"]
    for w in request_key_words:
        if w in user_text:
            return True
            print("Quote requested")
            break
    return False


def respond_weather(input_city):
    # Using open weather map client to fetch the weather report
    weather_report = ""

    print("City ", input_city)

    owm = pyowm.OWM(
        "edd197717da7951b85f8f6936fc27b13"
    )  # You MUST provide a valid API key

    forecast = owm.daily_forecast(input_city)

    observation = owm.weather_at_place(input_city)
    w = observation.get_weather()
    print(w)
    print(w.get_wind())
    print(w.get_humidity())
    max_temp = str(w.get_temperature("celsius")["temp_max"])
    min_temp = str(w.get_temperature("celsius")["temp_min"])
    current_temp = str(w.get_temperature("celsius")["temp"])
    wind_speed = str(w.get_wind()["speed"])
    humidity = str(w.get_humidity())

    weather_report = (
        "\n"
        + "Max temp: "
        + max_temp
        + "\n"
        + "Min temp: "
        + min_temp
        + "\n"
        + "Current temp: "
        + current_temp
        + "\n"
        + "Wind speed :"
        + wind_speed
        + "\n"
        + "Humidity "
        + humidity
        + "%"
    )
    print("Weather report ", weather_report)

    return weather_report