# Mp3Py
![alt text](https://github.com/ngimb64/Mp3Py/blob/main/mp3Py.png?raw=true)
![alt text](https://github.com/ngimb64/Mp3Py/blob/main/Mp3Py.png?raw=true)

&#9745;&#65039; Bandit verified<br>
&#9745;&#65039; Synk verified<br>
&#9745;&#65039; Pylint verified 9.37/10

## Prereqs
Program runs on Windows and Linux, written in Python 3.8

## Purpose
This program is a command line based mp3 player that uses a listener to detect keystrokes.
The arrow keys are tied to this listener with static text flags used to control execution.

## Installation
- Run the setup.py script to build a virtual environment and install all external packages in the created venv.

> Example: `python3 setup.py venv`

- Once virtual env is built traverse to the (Scripts-Windows or bin-Linux) directory in the environment folder just created.
- For Windows in the Scripts directory, for execute the `./activate` script to activate the virtual environment.
- For Linux in the bin directory, run the command `source activate` to activate the virtual environment.

## How to use
- Open up Command Prompt or terminal
- Traverse to the directory containing program & create folder name tracks
- Place songs to be played in the tracks folder
- Execute program
- Check out the control menu and use the arrow keys accordingly to control track execution

## Function Layout
-- mp3py.py --
> pause_track &nbsp;-&nbsp; Pauses the track until enter is hit to continue.

> change_volume &nbsp;-&nbsp; Re-set the tracks volume level.

> play_current_track &nbsp;-&nbsp; Plays the current track in track list.

> print_err &nbsp;-&nbsp; Prints time controlled error message.

> media_player &nbsp;-&nbsp; Facilitates the media player operation.

> on_press &nbsp;-&nbsp; Detects key strokes, setting corresponding boolean toggle.

> display &nbsp;-&nbsp; Displays the key listener options.

> main &nbsp;-&nbsp; Gathers tracks in dir as list, displays menu, & starts threads.

## Exit Codes
> 0 - Operation successful<br>
> 1 - The track's directory was missing, it needs songs to proceed<br>
> 2 - Unexpected error occurred main program execution