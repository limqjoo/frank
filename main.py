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
character_list = ["priest","groom","bride","bidder1","bidder2","juror1","juror2","juror3","auctioneer","lawyer1","lawyer2","courtroomofficer"]
characters = {}

script_counter = 0
for line in script:
    line["id"] = script_counter
    script_counter += 1

def test_number(number):
    for v in characters.values():
        return v.get('phone', None) == number

app = Flask(__name__)

@app.route("/test_xml", methods=['GET','POST'])
def xml_test_handler():
    return "<Response><Pause length=\"2\" /><Say>Do this. do a thing</Say></Response>"

@app.route("/xml/<id>", methods=['GET','POST'])
def xml_handler(id):
    print id
    print script[int(id)]
    text = script[int(id)]["text"]
    return "<Response><Pause length=\"2\" /><Say>" + text + "</Say></Response>"

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
        # if (True):
            characters.update({ character_list[player_count]: { "phone": from_number } })
            print "added character", from_number, characters

            resp = MessagingResponse().message("You have joined the performance")

            player_count += 1
            if (player_count == len(character_list)):
                print "all characters filled"
                stage = 1
                game_sequence()
        else:
            resp = MessagingResponse().message("We heard you the first time. Wait for the performance to begin")

        return str(resp)
    elif (stage==1): #game is ON - receving name
        resp = MessagingResponse().message("The game is now full")
        return str(resp)

def game_sequence():
    threading.Thread(target=send_delayed_text).start()

def send_line_to_all(msg):
    print "send to all", msg
    for c in characters.values():
        message = client.api.account.messages.create(to=c["phone"], from_=twilio_number, body=msg)

def send_delayed_text():
    for line in script:
        time.sleep(int(line["delay"]))
        if (line["character"] == 'all'):
            send_line_to_all(line["text"])
            continue

        to = characters[line["character"]]["phone"]

        lineType = line.get("type", None)

        print "to:", characters[line["character"]], characters[line["character"]]["phone"], line["text"]

        if (lineType == 'text' or lineType == None):
            text = line["text"]
            message = client.api.account.messages.create(to=to, from_=twilio_number, body=text)
        elif (lineType == 'call'):
            url = "http://305cec03.ngrok.io/xml/" + str(line["id"])
            call = client.calls.create(to=to,
                                       from_=twilio_number,
                                       url=url)

if __name__ == "__main__":
    app.run(debug=True)
