#!/usr/bin/env python3

from phue import Bridge
import config

b = Bridge(config.hue_bridge)

state = config.hue_lamps

result = ''
result = b.get_api()

def turn(lamp, on_off):

    if on_off == 'on':
        b.set_light(lamp, 'on', True)
        state[lamp] = 1
    else:
        b.set_light(lamp, 'on', False)
        state[lamp] = 0


def verifyState():

    for lamp in state:
        realstate = b.get_light(lamp)['state']['on']

        if realstate == True:
            state[lamp] = 1
        else:
            state[lamp] = 0
