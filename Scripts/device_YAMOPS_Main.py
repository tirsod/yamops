# name=YAMOPS - Oxygen Pro 61
# url=https://github.com/tirsod

# yet another m-audio oxygen pro script

import transport
import ui
import midi
import plugins
import channels
import patterns

CHANNEL_16 = 159

STOP_BUTTON = 252
PLAY_BUTTON = 250

SEQUENCER_CHANNEL = CHANNEL_16

DEBUG = True

CH_UP = 16
CH_DOWN = 17

NAV_UP = 21
NAV_LEFT = 22
NAV_DOWN = 23
NAV_RIGHT = 24

def SendToNavigator(note, value):
	if note is NAV_UP:
		ui.up()
	elif note is NAV_LEFT:
		ui.left()
	elif note is NAV_RIGHT:
		ui.right()
	elif note is NAV_DOWN:
		ui.down()
			

def SendToSequencer(note, value):

	sc = channels.selectedChannel(0, 0, 0)
	if (note == CH_UP):
		if sc > 0:
			channels.selectOneChannel(sc-1)
	elif (note == CH_DOWN):
		if sc < channels.channelCount(1)-1:
			channels.selectOneChannel(sc+1)
	sc = channels.selectedChannel(0, 0, 0)

	ui.crDisplayRect(0, sc, 16, 1, 5000)

	print(sc)

	if (note < 16):
		if (channels.getGridBit(sc, note) == 0):
			valueToSet = 127
		else:
			valueToSet = 0
		print("setting to", valueToSet)
		channels.setGridBit(sc, note, valueToSet)

def OnMidiIn(event):

	event.handled = False
	printOut = ""

	if event.status == STOP_BUTTON:
		printOut += "[Pressed STOP on Keyboard]"
		if (transport.getSongPos() > 0): printOut += " []"
		else: printOut += " [] x 2"
		transport.stop()
		event.handled = True

	elif event.status == PLAY_BUTTON:
		printOut += "[Pressed PLAY on Keyboard]"
		if (transport.isPlaying()): printOut += " ||"
		else: printOut += " >"
		transport.start()
		event.handled = True

	elif event.status == SEQUENCER_CHANNEL:
		print("Got a note from the sequencer bank")
		note = event.data1
		value = event.data2
		if (note < 20):
			SendToSequencer(note, value)
		elif (note < 30):
			SendToNavigator(note, value)
		event.handled = True

	elif DEBUG:
		printOut += "[Unhandled MidiIn event]"
		print(event.midiId, event.data1, event.data2, event.status, event.note, event.controlNum, event.controlVal)

	print(printOut)



def OnMidiMsg(event):
	print("[MidiMsg]")
	event.handled = False