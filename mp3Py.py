# Built-in Modules #
import os
import sys
from re import match
from shlex import quote
from time import sleep
from threading import Thread

# Third-party Modules #
from pyfiglet import Figlet
from pygame import mixer
from pynput.keyboard import Key, Listener

"""
##################
# Function Index #
########################################################################################################################
# PauseTrack(cmd) - Pauses the track until enter is hit to continue.
# ChangeVolume(cmd) - Re-set the tracks volume level.
# PlayCurrentTrack(path, vol) - Plays the current track in track list.
# PrintErr(msg, seconds) - Prints time controlled error message.
# MediaPlayer(tracks, path) - Facilitates the media player operation.
# OnPress(key) - Detects key strokes, setting corresponding boolean toggle.
# Display() - Displays the key listener options.
# main() - Gathers tracks in dir as list, displays menu, & starts threads.
########################################################################################################################
"""

# Globals #
pause, nxt, vol, halt = False, False, False, False
global key_listener

# Pseudo constants #
STOP = -1


'''
########################################################################################################################
Name:    PauseTrack
Purpose: Pauses the track until enter is hit to continue.
Params:  The command use to clear the screen.
Returns: None
########################################################################################################################
'''
def PauseTrack(cmd: str):
    # Pause the music #
    mixer.music.pause()
    while True:
        prompt = input('\nHit enter to continue\n')
        # If enter is not detected #
        if prompt != '':
            # Call PrintError and re-iterate loop #
            PrintErr('Only hit enter, no data input needed', 2, cmd)    
            continue

        break

    # Clear the display #
    os.system(cmd)
    # Re-display the menu #
    Display()


'''
########################################################################################################################
Name:    ChangeVolume
Purpose: Re-set the tracks volume level.
Params:  The command used to clear the screen.
Returns: Newly set volume level for storge in program.
########################################################################################################################
'''
def ChangeVolume(cmd: str) -> float:
    while True:
        # Prompt user for desired volume level #
        prompt = input('Enter volume 0, 1, or 0.1 to 0.9: ')
        
        # If the volume regex matches #
        if match(r'^(?:0\.[0-9]|[01])', prompt):
            # Print message and set the volume #
            print(f'\nChanging volume to {prompt}\n')
            # Re-set volume to new value #
            mixer.music.set_volume(float(prompt))        
            # Sleep execution 2 seconds #
            sleep(2)
            # Clear the display #
            os.system(cmd)
            # Re-display the menu #
            Display()
            break

        # Print error, sleep 2 seconds, and re-iterate input loop #
        PrintErr('Improper value detected .. volume unable to change', 2, cmd)
        continue

    return float(prompt)


'''
########################################################################################################################
Name:    PlayCurrentTrack
Purpose: Plays the current track in track list.
Params:  The path where the track is stored and the track volume.
Returns: None
########################################################################################################################
'''
def PlayCurrentTrack(path: str, volume: float):
    # Load the current track #
    mixer.music.load(path)
    # Set the track volume #
    mixer.music.set_volume(volume)
    # Play the track #
    mixer.music.play()


'''
########################################################################################################################
Name:    PrintErr
Purpose: Prints time controlled error message.
Params:  The error message to be printed and the number of seconds it should be displayed before clearing the screen, \
         and the command used to clear the display.
Returns: Exits program when Ctrl+C is pressed.
########################################################################################################################
'''
def PrintErr(msg, seconds: int, cmd: str):
    print(f'\n* [ERROR]: {msg} *\n', file=sys.stderr)
    sleep(seconds)

    # Clear display #
    os.system(cmd)
    # Re-display menu #
    Display()


'''
########################################################################################################################
Name:    MediaPlayer
Purpose: Facilitates the media player operation.
Params:  A list of tracks to be played, the current working directory, and the command used for clearing the display.
Returns: None
########################################################################################################################
'''
def MediaPlayer(tracks: list, path: str, cmd: str):
    global pause, nxt, vol, halt, key_listener

    # Initial volume setting (1 is max) #
    volume = 0.5
    # Initialize the mixer #
    mixer.init()

    # Infinite loop replays track list when complete #
    while True:
        # Iterate through each track in track list #
        for track in tracks:
            # Reset nxt toggle per iteration #
            nxt = False
            # Play the current iteration of the track list #
            PlayCurrentTrack(f'{path}\\tracks\\{track}', volume)

            # While the track is playing and the nxt & exit toggles are False #
            while mixer.music.get_pos() != STOP and not nxt and not halt:
                # While the track is playing and the pause, nxt, exit, and volume are False #
                while mixer.music.get_pos() != STOP and not pause and not nxt and not halt and not vol:
                    continue

                # If the pause toggle is equal to false and the music has stopped playing #
                if not pause and mixer.music.get_pos() == STOP:
                    break

                # While the vol toggle is set to True and the music is playing #
                while vol and mixer.music.get_pos() != STOP:
                    # Reset the volume level #
                    volume = ChangeVolume(cmd)
                    # Reset vol toggle #
                    vol = False

                # While the pause toggle is true #
                while pause:
                    PauseTrack(cmd)
                    break

                # Reset pause toggle & continue music #
                pause = False
                mixer.music.unpause()
                continue

            # If the exit toggle is set #
            if halt:
                # Stop the music #
                mixer.music.stop()

                # If the key listener thread is alive #
                if key_listener.is_alive():
                    # Stop the key listener thread #
                    key_listener.stop()

                # Exit program with success code #
                sys.exit(0)


'''
########################################################################################################################
Name:    OnPress
Purpose: Detects key strokes, setting corresponding boolean toggle.
Params:  Key press that is detected.
Returns: Set toggle switch of pressed key.
########################################################################################################################
'''
def OnPress(key) -> bool:
    global pause, nxt, vol, halt

    # If left arrow key is pressed #
    if key == Key.left:
        pause = True
        return pause   

    # If right arrow key is pressed #
    elif key == Key.right:
        nxt = True
        return nxt 

    # If up arrow key is pressed #
    elif key == Key.up:
        vol = True
        return vol

    # If down arrow key is pressed #
    elif key == Key.down:
        halt = True
        return halt


'''
########################################################################################################################
Name:    Display
Purpose: Displays the key listener options.
Params:  None
Returns: None
########################################################################################################################
'''
def Display():
    # Set the display banner & print #
    custom_fig = Figlet(font='fraktur', width=117)
    print(custom_fig.renderText('* Mp3Py *'))
    print('''\n
    #============#>
    |  Controls:  |
    #=8=8=8=8=8=8=#=8=8=8=8=8=8=8=8=8=8=8>
    |  Press Left Arrow to pause         |
    |  Press Right Arrow to change track |
    |  Press Up Arrow to change volume   |
    |  Press Down Arrow to exit          |
    #===================================#>
''')


'''
########################################################################################################################
Name:    main
Purpose: Gathers tracks in dir as list, displays menu, & starts threads.
Params:  None
Returns: Exits program when Ctrl+C is pressed.
########################################################################################################################
'''
def main():
    global key_listener

    tracks = []
    # Get current working directory #
    path = os.getcwd()
    # Set tuple of audio file extension types #
    track_type = ('.mp3', '.mp4', '.wav', '.wma', '.m4a', '.flac')

    # If the OS is Windows #
    if os.name == 'nt':
        cmd = quote('cls')
    # For other OS's #
    else:
        cmd = quote('clear')

    # If tracks dir does not exist #
    if not os.path.isdir(f'{path}\\tracks'):
        # Create tracks dir #
        os.mkdir(f'{path}\\tracks')

    # Iterate through files in tracks directory #
    [tracks.append(str(file.name)) for file in os.scandir(f'{path}\\tracks') if str(file.name).endswith(track_type)]

    # Clear the display #
    os.system(cmd)

    # Display the menu #
    Display()

    # Create the keystroke listener thread #
    key_listener = Listener(on_press=OnPress)
    # Create the media player thread #
    player = Thread(target=MediaPlayer, args=(tracks, path, cmd))

    try:
        # Start and join the threads #
        key_listener.start()
        player.start()
        key_listener.join()
        player.join()

    # If ctrl + c detected #
    except KeyboardInterrupt:
        print('\nCtrl + C detected .. exiting')
    # If unknown exception occurs #
    except Exception as err:
        PrintErr(err, 4, cmd)

    finally:
        # If the keystroke listener thread is alive #
        if key_listener.is_alive():
            # Terminate the thread #
            key_listener.stop()


if __name__ == '__main__':
    main()
