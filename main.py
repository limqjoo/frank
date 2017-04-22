from flask import Flask, request
from twilio.twiml.voice_response import VoiceResponse
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
import threading
import time
import json
from pprint import pprint

with open('script.json') as data_file:
    global script
    script = json.load(data_file)

twilio_number = "+441494372650"

account_sid = "AC1236670c86e97c36e0e77f6622ae9fb9"
auth_token = "5cb698f28a9fdc1dbbf147e95ef430b8"
client = Client(account_sid, auth_token)

stage = 0
player_count = 0
characters = {
    0: {
        "name": "John"
    }
    # 1: {
    #     "name": "Patrick"
    # }
}

def test_number(number):
    for v in characters.values():
        return v.get('phone', None) == number

app = Flask(__name__)

@app.route("/sms", methods=['GET', 'POST'])
def sms_receiver():
    """responds to text messages from players"""
    global stage
    global player_count

    if (not request.values.get('From', None)):
        print "NO NUMBER"
        return "no number given"

    if (stage==0): # signing up players
        from_number = request.values.get('From', None)
        print characters
        print "new player, number in db?", test_number(from_number)
        if (not test_number(from_number)):
            characters[player_count]["number"] = from_number

            resp = MessagingResponse().message("You have joined the performance")

            player_count += 1
            if (player_count == len(characters)):
                print "all characters filled"
                stage = 1
                game_sequence()
        else:
            resp = MessagingResponse().message("We heard you the first time. Wait for the performance to begin")

        return str(resp)
    elif (stage==1): #game is ON - receving name
        resp = MessagingResponse().message("The game is now full")
        return resp

def game_sequence():
    threading.Thread(target=send_delayed_text).start()

def send_delayed_text():
    for line in script:
        print "SAY LINE", line
        to = characters[line["character"]]["number"]
        print "SEND LINE TO", to
        time.sleep(line["delay"])
        if (line["type"] == 'sms'):
            message = client.api.account.messages.create(to=to, from_=twilio_number, body=line["text"])
        elif (line["type"] == 'phone'):
            pass

if __name__ == "__main__":
    app.run(debug=True)
