# name=YAMOPS - Midin3 (Oxygen Pro Mini)
# url=https://github.com/tirsod

# yet another m-audio oxygen pro script

import transport
import ui
import midi
import plugins
import channels

# BASIC TRANSPORT CONTROLS
Transport_START = 94
Transport_STOP = 93
Transport_RECORD = 95
Transport_RECORD_MiniPro = 116
Transport_Loop = 86
Transport_BACK = 91
Transport_FORWARD = 92

USE_LOOP_AS_PATTERN_BUTTON = True

MACKIE_HUI = 176

# What is conflictingPlaylistFocus?
# FORWARD / BACK transport buttons would not work unless Playlist focused
# Noticed Sytrus would also take focus, so also included if Sytrus is focused
def conflictingPlaylistFocus():
	
	# If Channel Rack (1) or Mixer (0) or Browser (4), or Conflicting Plugin, then return value
	doesItConflict = 0
	
	# ui.getFocused(#) is from "FL Window Constants" via the MIDI Scripting Help Page	
	# If true, Playlist Window will focus via ui.showWindow(2), then move 1 bar with ui.jog()
	if ui.getFocused(1) == 1 or ui.getFocused(0) == 1 or ui.getFocused(4) == 1 or ui.getFocusedPluginName() == 'Sytrus':
	
	# If conflicting window/plugin is focused, set true
		doesItConflict = 1
		print('[Playlist ~ Focused]')

	return doesItConflict

def playlistJog(midiEventData1):
	# If BACK or FORWARD button pressed, update playlistFocus state
	if midiEventData1 == Transport_BACK:
		playlistFocus = 'BACK] - 1 Bar Left'
		# Move BACK 1 Bar Left
		ui.jog(-1)
	if midiEventData1 == Transport_FORWARD:
		playlistFocus = 'FORWARD] - 1 Bar Right'
		# Move FORWARD 1 Bar Left
		ui.jog(1)
	# If in SONG MODE, Output text
	if transport.getLoopMode() == 1:
		print('[Playlist ' + playlistFocus)
	elif transport.getLoopMode() == 0:
		print('[Piano Roll ' + playlistFocus)


# insidePianoRoll() tests to see if user is actually in Piano Roll
def insidePianoRoll():
	# Used to clarify if User is in Piano Roll + Pattern Mode
	isPianoRollFocused = False
	
	# If in Piano Roll, set true
	if ui.getFocused(3) == 1:
		isPianoRollFocused = True
	
	return isPianoRollFocused

def OnMidiIn(event):
	event.handled = False

def OnMidiMsg(event):
	event.handled = False
	#print("event received ID:", event.midiId, event.data1, event.data2)

	if event.midiId == MACKIE_HUI:
		print("Mackie_HUI used: ", event.data1, event.data2)
		if (event.data2 == Transport_RECORD_MiniPro): # Record Button HUI
			transport.record()
			print("Pressed mackie/hui record button")
			event.handled = True
	elif event.midiId == midi.MIDI_NOTEON:
		print("Mackie used: ", event.data1)
		if event.data2 > 0:
			# Start and Stop are already handled by YAMOPS_Main
			if event.data1 == Transport_START:
				print("[Pressed PLAY on Keyboard] Check Main script")
				event.handled = True
			elif event.data1 == Transport_STOP:
				print("[Pressed STOP on Keyboard] Check by Main script")
				event.handled = True

			if event.data1 == Transport_RECORD:
				# Enable / Disable Record
				if transport.isRecording() == 0:
					print('[Pressed RECORD on Keyboard] ON')
				elif transport.isRecording() == 1:
					print('[Pressed RECORD on Keyboard] OFF')
				# Toggles Record Enabled/Disabled
				transport.record()
				event.handled = True

			# LOOP BUTTON
			elif event.data1 == Transport_Loop:
				if transport.getLoopMode() == 0:
					print('[Now in SONG MODE]')
					transport.setLoopMode()
					event.handled = True
				elif transport.getLoopMode() == 1:
					print('[Now in PATTERN MODE]')
					# Switch Between Pattern/Song Mode
					transport.setLoopMode()
					event.handled = True	
			# PLAYLIST BACK (LEFT) BUTTON
			elif event.data1 == Transport_BACK:
				# If in SONG MODE
				if transport.getLoopMode() == 1:
					# If Conflicting Window, Focus Playlist
					if conflictingPlaylistFocus() == 1:
						# Focus Playlist Window
						ui.showWindow(2)							
					# Move BACK 1 Bar Left
					playlistJog(event.data1)
					# COMPLETE Transport_BACK button
					event.handled = True

					# If in PATTERN MODE
				if transport.getLoopMode() == 0:						
					# If Piano Roll Focused, Stay in PATTERN MODE, respect normal FL Studio ways
					if insidePianoRoll() == True:
						# Move BACK 1 Bar Left
						playlistJog(event.data1)
						# COMPLETE Transport_BACK button
						event.handled = True

					# Else, if in Channel Rack or Mixer, Focus Playlist, then Move 1 Bar
					else:							
						# If conflicting window						
						if conflictingPlaylistFocus() == 1:
							# Focus Playlist Window
							ui.showWindow(2)							
						# Move BACK 1 Bar Left 
						playlistJog(event.data1)
						# COMPLETE Transport_BACK button
						event.handled = True
				# PLAYLIST FORWARD (RIGHT) BUTTON
			elif event.data1 == Transport_FORWARD:
				# If in SONG MODE
				if transport.getLoopMode() == 1:
					# If Conflicting Window, Focus Playlist
					if conflictingPlaylistFocus() == 1:
						# Focus Playlist Window
						ui.showWindow(2)							
					# Move FORWARD 1 Bar Right
					playlistJog(event.data1)
					# COMPLETE Transport_FORWARD button
					event.handled = True

				# If in PATTERN MODE
				if transport.getLoopMode() == 0:						
					# If Piano Roll Focused, Stay in PATTERN MODE, respect normal FL Studio ways
					if insidePianoRoll() == True:
						# Move FORWARD 1 Bar Right
						playlistJog(event.data1)
						# COMPLETE Transport_FORWARD button
						event.handled = True

					# Else, if in Channel Rack or Mixer, Focus Playlist, then Move 1 Bar
					else:							
						# If conflicting window						
						if conflictingPlaylistFocus() == 1:
							# Focus Playlist Window
							ui.showWindow(2)							
						# Move FORWARD 1 Bar Right
						playlistJog(event.data1)
						# COMPLETE Transport_FORWARD button
						event.handled = True
	else:
		print("Used a different event id ", event.midiId, event.data2)