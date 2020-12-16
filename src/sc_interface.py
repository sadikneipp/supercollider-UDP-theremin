import pyOSC3
import time, random

IP = "127.0.0.1"
PORT = 57120


def connect():
    client = pyOSC3.OSCClient()
    client.connect((IP, PORT))
    return client


def send_message(tone, vol, client):
    msg = pyOSC3.OSCMessage()
    msg.setAddress("/theremin.freq")
    msg.append(tone)
    msg.append(vol)
    client.send(msg)
