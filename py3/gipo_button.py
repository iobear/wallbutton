#!/usr/bin/env python3

import hue
import denon
import config

import RPi.GPIO as GPIO  
import time

button1 = config.rpi_button1
button2 = config.rpi_button2
button3 = config.rpi_button3
button4 = config.rpi_button4

GPIO.setmode(GPIO.BCM)  # set up BCM GPIO numbering  

GPIO.setup(button1, GPIO.IN)
GPIO.setup(button2, GPIO.IN)
GPIO.setup(button3, GPIO.IN)
GPIO.setup(button4, GPIO.IN)

button_state = {
    "button1": 0,
    "button2": 0,
    "button3": 0,
    "button4": 0
}

def checkRules():
    if button_state["button1"] == 1: #Toggle Spisebord ON / Light Strip ON / Spisebord OFF / Light Strip OFF
        spisebord_state = ""
        lightstrip_state = ""

        if hue.state["Spisebord"] == 0 and hue.state["Hue lightstrip"] == 0:
            spisebord_state = "on"

        if hue.state["Spisebord"] == 1 and hue.state["Hue lightstrip"] == 0:
            lightstrip_state = "on"

        if hue.state["Spisebord"] == 1 and hue.state["Hue lightstrip"] == 1:
            spisebord_state = "off"

        if hue.state["Spisebord"] == 0 and hue.state["Hue lightstrip"] == 1:
            lightstrip_state = "off"

        if spisebord_state != "":
            hue.turn("Spisebord", spisebord_state)

        if lightstrip_state != "":
            hue.turn("Hue lightstrip", lightstrip_state)

    if button_state["button2"] == 1: #toggle ON / Radio / CD / OFF
        if denon.state["on"] == 0:
            denon.power('on')
            denon.setVolume(denon.volume_start)
            denon.inputSelect("iradio")
        elif denon.state["on"] == 1 and denon.state["iradio"] == 1:
            denon.inputSelect("cd")
        else:
            denon.power('off')

    if button_state["button3"] == 1: #Volume DOWN
        if denon.state["on"] == 1:
            denon.volume('down')

    if button_state["button4"] == 1: #Volume UP
        if denon.state["on"] == 1:
            denon.volume('up')
        

def change_state(button, state):
    if button_state[button] != state:
        button_state[button] = state
        checkRules()


hue.verifyState()
count = 0

while True:
    count = count + 1

    if GPIO.input(button1):
        change_state("button1", 1)

    if GPIO.input(button2):
        change_state("button2", 1)

    if GPIO.input(button3):
        change_state("button3", 1)

    if GPIO.input(button4):
        change_state("button4", 1)

    time.sleep(0.1)
    if button_state["button1"] == 1:
        if not GPIO.input(button1):
            change_state("button1", 0)
            #print("Button1 OFF")

    if button_state["button2"] == 1:
        if not GPIO.input(button2):
            change_state("button2", 0)
            #print("Button2 OFF")

    if button_state["button3"] == 1:
        if not GPIO.input(button3):
            change_state("button3", 0)
            #print("Button3 OFF")

    if button_state["button4"] == 1:
        if not GPIO.input(button4):
            change_state("button4", 0)
            #print("Button4 OFF")

    if count == config.hue_verify_state * 10:
        hue.verifyState()
        count = 0
