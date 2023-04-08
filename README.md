<div align="center" style="font-family: monospace">
<h1>Mp3Py</h1>
&#9745;&#65039; Bandit verified &nbsp;|&nbsp; &#9745;&#65039; Synk verified &nbsp;|&nbsp; &#9745;&#65039; Pylint verified 9.53/10
</div><br>

![alt text](https://github.com/ngimb64/Mp3Py/blob/main/mp3_Py.png?raw=true)
![alt text](https://github.com/ngimb64/Mp3Py/blob/main/mp3Py.png?raw=true)

## Purpose
This program is a command line based mp3 player that uses a listener to detect keystrokes.
The arrow keys are tied to this listener with static boolean flags used to control execution.

### License
The program is licensed under [GNU Public License v3.0](LICENSE.md)

### Contributions or Issues
[CONTRIBUTING](CONTRIBUTING.md)

## Prereqs
Program runs on Windows 10 and Debian-based Linux, written in Python 3.8 and updated to version 3.10.6

## Installation
- Run the setup.py script to build a virtual environment and install all external packages in the created venv.

> Examples:<br> 
>       &emsp;&emsp;- Windows:  `python setup.py venv`<br>
>       &emsp;&emsp;- Linux:  `python3 setup.py venv`

- Once virtual env is built traverse to the (Scripts-Windows or bin-Linux) directory in the environment folder just created.
- For Windows, in the venv\Scripts directory, execute `activate` or `activate.bat` script to activate the virtual environment.
- For Linux, in the venv/bin directory, execute `source activate` to activate the virtual environment.
- If for some reason issues are experienced with the setup script, the alternative is to manually create an environment, activate it, then run pip install -r packages.txt in project root.
- To exit from the virtual environment when finished, execute `deactivate`.

## How to use
- Open up Command Prompt or terminal
- Traverse to the directory containing program & create folder name tracks
- Place songs to be played in the tracks folder
- Execute program
- Check out the control menu and use the arrow keys accordingly to control track execution

## Function Layout
-- mp3py.py --
> display_wrapper &nbsp;-&nbsp; Decorator function for automatically handling cleaning up the display and re-displaying.
>
> display_handler &nbsp;-&nbsp; Clears the display via shell-escaped syntax and re-displays menu after function call.

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
