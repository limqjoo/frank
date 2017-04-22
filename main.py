from flask import Flask, request
from twilio.twiml.voice_response import VoiceResponse
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
import threading
import time

twilio_number = "+441494372650"

account_sid = "AC1236670c86e97c36e0e77f6622ae9fb9"
auth_token = "5cb698f28a9fdc1dbbf147e95ef430b8"
client = Client(account_sid, auth_token)

stage = 0
player_count = 0
max_characters = 2
characters = {}

app = Flask(__name__)

# endpoint that receives texts
    # if game waiting (stage==0)
        # takes a phone number - if numbers == 2, start game
    # if waiting for description (stage==1)
        # takes a description - if numbers == 2, start game
    # wait for code word at end of story (stage==2)
        # send success/fail texts based on test
@app.route("/sms", methods=['GET', 'POST'])
def sms_receiver():
    """responds to text messages from players"""
    global stage
    global player_count

    if (stage==0): # signing up players
        from_number = request.values.get('From', None)
        characters[from_number] = {}
        resp = MessagingResponse().message("Thanks for joining the game. Please send your name.")

        player_count += 1
        if (player_count == max_characters):
            print "character limit reached"
            stage = 1
            game_sequence_1()

        return str(resp)
    elif (stage==1): #game is ON - receving name
        from_number = request.values.get('From', None)
        name = request.values.get('Body', None)
        characters[from_number]["name"] = name
        resp = MessagingResponse().message("You are " + name)
        return resp

def send_delayed_text():
    time.sleep(10)
    for k in characters.keys():
        message = client.api.account.messages.create(to=k, from_=twilio_number, body="this is text number 1")
    

def game_sequence_1():
    for k in characters.keys():
        threading.Thread(target=foo).start()

@app.route("/voice", methods=['GET', 'POST'])
def hello_monkey():
    """Respond to incoming requests."""
    resp = VoiceResponse()
    resp.say("Hello Tom. Your first clue is just around the corner. Walk a few meters and you shall see some trees. Press the key corresponding to the number of trees that you have seen. You're getting close. Be careful. Big sister is watching you!")

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
