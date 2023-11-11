# yamops
Yet Another M-Audio Oxygen Pro Script

# What
A series of custom python scripts that use the FL Studio MIDI scripting API.
This brings some much needed functionality to this series of keyboards like:

- Functioning PLAY, STOP, LOOP, and RECORD buttons
- Playlist position controls
- Performance and Arrangement tools (WIP)
- Pattern making by using the pads
- Plugin nagivation and pattern creation through the pads and hotkeys

which would bring it closer to something like the Novation FL Key devices.

# How

- Update your keyboard's software
- Set your keyboard's DAW to FL Studio
- Use preset mode
- Open up the PRESET EDITOR app for your specific keyboard and load the included preset 
  - You might need to make one for your keyboard. You can reference the values used in the script from the manual.
- Move the .py scripts into their own folder in C:\Users\<user>\Documents\Image-Line\FL Studio\Settings\Hardware\YAMOPS
- In FL Studio, open your MIDI settings and set:
  - Oxygen Pro: Enabled - No port - YAMOPS-Oxygen Pro 61
  - MIDIIN2: Disabled
  - MIDIIN3: Enabled - No port - YAMOPS-MIDIIN 3
  - MIDIIN4: Disabled

**You're done!**

*A full document with the midi values used by the keyboard + a manual to set up the
keyboard and preset for use with the script will be made available as a PDF download.*

# Why

To make a script/preset combo that would let you make music without touching your QWERTY keyboard or your mouse.

*Or at least reduce how much you'd have to engage with those inputs by a large percent.*

# Demo

https://www.youtube.com/watch?v=M7MtQT1Vpjk
