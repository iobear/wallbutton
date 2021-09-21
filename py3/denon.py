#!/usr/bin/env python3

import requests
import sys
import config

volume_step = config.denon_volume_step
volume_start = config.denon_volume_start
volume_diff = -80

amp = {
	"host":"http://" + config.denon_amp,
	"on":["MainZone","cmd0=PutZone_OnOff%2FON&cmd1=aspMainZone_WebUpdateStatus%2F"],
	"off":["MainZone","cmd0=PutZone_OnOff%2FOFF&cmd1=aspMainZone_WebUpdateStatus%2F"],
	"volume":["MainZone","cmd0=PutMasterVolumeSet%2F"],
	"mute":["MainZone","cmd0=PutVolumeMute%2Fon&cmd1=aspMainZone_WebUpdateStatus%2F"],
	"unmute":["MainZone","cmd0=PutVolumeMute%2Foff&cmd1=aspMainZone_WebUpdateStatus%2F"],
	"cd":["MainZone","cmd0=PutZone_InputFunction%2FCD&cmd1=aspMainZone_WebUpdateStatus%2F"],
	"iradio":["MainZone","cmd0=PutZone_InputFunction%2FIRADIO&cmd1=aspMainZone_WebUpdateStatus%2F"]
}

state = {
	"on": 0,
	"volume": 0,
	"iradio": 0,
	"cd": 0
}

def apiTalk(host, zone, postdata):
	uri = '/' + zone + '/index.put.asp'
	url = host + uri

	r = requests.post(url, data = postdata)


def power(on_off):
	if on_off == "on":
		apiTalk(amp['host'], amp['on'][0], amp['on'][1])
		state["on"] = 1
	else:
		apiTalk(amp['host'], amp['off'][0], amp['off'][1])    
		state["on"] = 0


def volume(up_down):
	if up_down == 'down' and state["volume"] > 0:
		state["volume"] = state["volume"] - volume_step

	if up_down == 'up' and state["volume"] < 100:
		state["volume"] = state["volume"] + volume_step

	setVolume(state["volume"])


def inputSelect(device):
	#input_select iradio or cd
	apiTalk(amp['host'], amp[device][0], amp[device][1])
	if state["cd"] == 1:
		state["cd"] = 0
	if state["iradio"] == 1:
		state["iradio"] = 0

	state[device] = 1


def setVolume(value):
	data = amp['volume'][1] + str(volume_diff + value)
	apiTalk(amp['host'], amp['volume'][0], data)
	state["volume"] = value


if __name__ == "__main__":
	if sys.argv[1] == 'on':
		power('on')
	if sys.argv[1] == 'off':
		power('off')