from flask import Flask
from twilio.twiml.voice_response import VoiceResponse

app = Flask(__name__)

# endpoint that receives texts
    # if game started
        # do game logic
    # if game waiting
        # takes a phone number - if numbers == 2, start game

# game start
    # assign characters randomly
    # send welcome text
    # wait 30 seconds
    # send out exposition texts - send a text each to gf and mum
    # send a location of the library
    # wait 2 minutes
    # send, sorry cant come text, wait for other person
    #


@app.route("/", methods=['GET', 'POST'])
def hello_monkey():
    """Respond to incoming requests."""
    resp = VoiceResponse()
    resp.say("Hello Tom. Your first clue is just around the corner. Walk a few meters and you shall see some trees. Press the key corresponding to the number of trees that you have seen. You're getting close. Be careful. Big sister is watching you!")

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)

#https://demo.twilio.com/welcome/voice/
