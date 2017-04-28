from flask import Flask, request
from twilio.twiml.voice_response import VoiceResponse
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
import threading
import time
import json
from pprint import pprint

twilio_number = "+441494372650"

account_sid = "....."
auth_token = "......"
client = Client(account_sid, auth_token)

call = client.calls.create(to=".......",
                           from_=twilio_number,
                           url="http://305cec03.ngrok.io/test_xml")

print(call.sid)
