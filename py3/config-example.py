#!/usr/bin/env python3

#Raspberry Pi pin number, for GiPO ports
rpi_button1 = 22
rpi_button2 = 17
rpi_button3 = 24
rpi_button4 = 18

hue_bridge = "10.10.3.11" #Philips Hue bridge IP
hue_verify_state = 600 #seconds
hue_lamps = {
    "Spisebord": 0,
    "Hue lightstrip": 0
}

denon_amp = "10.10.3.201" #Denon receiver IP
denon_volume_step = 3
denon_volume_start = 31
