from flask import Flask, request
from twilio.twiml.voice_response import VoiceResponse
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse

account_sid = "AC1236670c86e97c36e0e77f6622ae9fb9"
auth_token = "5cb698f28a9fdc1dbbf147e95ef430b8"
client = Client(account_sid, auth_token)

stage = 0
player_count = 0
characters = {
    0: {
        "name": "Charlie",
        "number": 0,
        "description": None,
    },
    1: {
        "name": "Lisa",
        "number": 0,
        "description": None,
    }
}

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

    if (stage==0):
        from_number = request.values.get('From', None)
        characters[player_count]["number"] = from_number
        player_count += 1
        resp = MessagingResponse().message("Thanks for joining the game, your character name is " + characters[player_count]["name"])
        return str(resp)
        if (player_count == len(characters)):

            stage = 1
            start_game()


    """ message = client.api.account.messages.create(to="+12316851234",
                                             from_="+15555555555",
                                             body="Hello there!")"""

def start_game():
    pass
    """ message = client.api.account.messages.create(to="+12316851234",
                                             from_="+15555555555",
                                             body="Hello there!")"""


@app.route("/voice", methods=['GET', 'POST'])
def hello_monkey():
    """Respond to incoming requests."""
    resp = VoiceResponse()
    resp.say("Hello Tom. Your first clue is just around the corner. Walk a few meters and you shall see some trees. Press the key corresponding to the number of trees that you have seen. You're getting close. Be careful. Big sister is watching you!")

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
