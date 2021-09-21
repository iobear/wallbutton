#!/usr/bin/env python3

from phue import Bridge
import config

b = Bridge(config.hue_bridge)

state = {
    "Spisebord": 0,
    "Hue lightstrip": 0,
    "BontjeStue": 0
}

result = ''
result = b.get_api()

def turn(lamp, on_off):
    if on_off == 'on':
        b.set_light(lamp, 'on', True)
        state[lamp] = 1
    else:
        b.set_light(lamp, 'on', False)
        state[lamp] = 0
