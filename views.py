import os
import sys
import json
import re

import requests
from flask import Flask, request
from app import app, db
from models import *
import nextbus

@app.route('/', methods=['GET'])
def verify():
    # when the endpoint is registered as a webhook, it must echo back
    # the 'hub.challenge' value it receives in the query arguments
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == os.environ["VERIFY_TOKEN"]:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    # just testing, prints the first entry in the database
    last_message_text = Messages.query.get(1)
    return "<h1>{}</h1>".format(nextbus.keystop()), 200


@app.route('/', methods=['POST'])
def webhook():

    # endpoint for processing incoming messaging events

    data = request.get_json()
    log(data)  # you may not want to log every incoming message in production, but it's good for testing

    if data["object"] == "page":

        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:

                if messaging_event.get("message"):  # someone sent us a message
                    sender_id = messaging_event["sender"]["id"]        # the facebook ID of the person sending you the message
                    recipient_id = messaging_event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID

                    if messaging_event.get("message").get("text"): # someone sent us a message with text
                        message_text = messaging_event["message"]["text"]  # the message's text

                        # clean message
                        message_text = clean_message(message_text)

                        # if message is about the turtle/car, then either respond
                        # with where it is or store where it is now. If not then
                        # just do something goofy.
                        if message_text.lower() == 'undo':
                            # assume we're undo-ing the car location
                            # can build more sophisticated logic later
                            car_location = Car_Locations.query.get(1)
                            if car_location.last_location == '[empty]':
                                send_message(sender_id, 'cannot undo anymore')
                            else:
                                car_location.current_location = car_location.last_location
                                car_location.last_location = '[empty]'
                                db.session.commit()
                                send_message(sender_id, '%s (reverted back)' % car_location.current_location)

                        elif findword('car', message_text) or findword('turtle', message_text):
                            car_location = Car_Locations.query.get(1)
                            if '?' in message_text or message_text.lower() == 'car' or message_text.lower() == 'turtle':
                                send_message(sender_id, car_location.current_location)
                            else:
                                car_location.last_location = car_location.current_location
                                car_location.current_location = message_text
                                db.session.commit()
                                send_message(sender_id, '%s (type "undo" to undo)' % (car_location.current_location))
                        elif findword('bus', message_text):
                            send_message(sender_id, nextbus.keystop())
                        else:
                            # pull last message
                            last_message_text = Messages.query.get(1)
                            # send last message
                            send_message(sender_id, last_message_text.message)
                            # make this message the last message
                            last_message_text.message = message_text
                            db.session.commit()

                    else:
                        # test sending a quick reply
                        ask_location(sender_id)
                        # do_not_recognize = "I'm sorry I don't recognize that"
                        # send_message(sender_id, do_not_recognize)


                if messaging_event.get("delivery"):  # delivery confirmation
                    pass

                if messaging_event.get("optin"):  # optin confirmation
                    pass

                if messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
                    pass

    return "ok", 200


def ask_location(recipient_id):
    # send a "quick reply" request for location
    log("sending location quick reply to {recipient}".format(recipient=recipient_id))

    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message":{
            "text":"Pick a color:",
            "quick_replies":[
                {
                  "content_type":"location"
                }
            ]
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)

def ask_color(recipient_id):
    # send a "quick reply" example request, in this case asking for colors
    log("sending location quick reply to {recipient}".format(recipient=recipient_id))

    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message":{
            "text":"Pick a color:",
            "quick_replies":[
                {
                  "content_type":"text",
                  "title":"Red",
                  "payload":"DEVELOPER_DEFINED_PAYLOAD_FOR_PICKING_RED"
                },
                {
                  "content_type":"text",
                  "title":"Green",
                  "payload":"DEVELOPER_DEFINED_PAYLOAD_FOR_PICKING_GREEN"
                }
            ]
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)

def send_message(recipient_id, message_text):
    log("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))

    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)


def log(message):  # simple wrapper for logging to stdout on heroku
    print str(message)
    sys.stdout.flush()


def findword(word, sentence):
    # remove symbols and create a list of words in a sentence
    word_list = re.sub("[^\w]", " ",  sentence.lower()).split()
    if word.lower() in word_list:
        return True
    else:
        return False

def clean_message(message):
    # eventually we'll remove potentially harmful code
    return message


