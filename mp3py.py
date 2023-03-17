# pylint: disable=W0106,E0401
""" Built-in modules """
import os
import sys
import time
from pathlib import Path
from re import match
from shlex import quote
from threading import Thread
# Third-party Modules #
from pyfiglet import Figlet
from pygame import mixer
from pynput.keyboard import Key, Listener


# Globals #
global KEY_LISTENER
PAUSE, NXT, VOL, HALT = False, False, False, False
STOP = -1
# If the OS is Windows #
if os.name == 'nt':
    # Shell-escape command syntax #
    CMD = quote('cls')
# If the OS is Linux #
else:
    # Shell-escape command syntax #
    CMD = quote('clear')


def display_wrapper(func):
    """
    Decorator function for automatically handling cleaning up the display and re-displaying.

    :param func:  The function to be decorated by this procedure.
    """
    def display_handler(*args, **kwargs):
        """
        Clears the display via shell-escaped syntax and re-displays menu after function call.

        :param args:  Args passed into to the handler function.
        :param kwargs:  Keyword args passed into to the handler function.
        :return:  The finished decorator reference back to main.
        """
        # Execute the passed in function with whatever args #
        ret = func(*args, **kwargs)
        # Clear the display and re-display the main menu #
        os.system(CMD)
        display()
        # If there is a return value #
        if ret:
            return ret

    return display_handler


@display_wrapper
def pause_track():
    """
    Pauses the track until enter is hit to continue.

    :return:  Nothing
    """
    # Pause the music #
    mixer.music.pause()
    while True:
        prompt = input('\nHit enter to continue\n')
        # If enter is not detected #
        if prompt != '':
            # Call PrintError and re-iterate loop #
            print_err('Only hit enter, no data input needed', 2)
            continue

        break


@display_wrapper
def change_volume() -> float:
    """
    Re-set the track's volume level.

    :param cmd:  Clear display command syntax.
    :return:  Newly set volume level for storge in program.
    """
    while True:
        # Prompt user for desired volume level #
        prompt = input('Enter volume 0, 1, or 0.1 to 0.9: ')

        # If the volume regex matches #
        if match(r'^(?:0\.\d|[01])', prompt):
            # Print message and set the volume #
            print(f'\nChanging volume to {prompt}\n')
            # Re-set volume to new value #
            mixer.music.set_volume(float(prompt))
            break

        # Print error, sleep 2 seconds, and re-iterate input loop #
        print_err('Improper value detected .. volume unable to change', 2)
        continue

    return float(prompt)


def play_current_track(path: str, volume: float):
    """
    Plays the current track in track list.

    :param path:  The path where the track is stored.
    :param volume:  The volume the track is to be played at.
    :return:
    """
    # Load the current track #
    mixer.music.load(path)
    # Set the track volume #
    mixer.music.set_volume(volume)
    # Play the track #
    mixer.music.play()


@display_wrapper
def print_err(msg, seconds: int):
    """
    Prints time controlled error message via stderr.

    :param msg:  The error message to be displayed via stderr.
    :param seconds:  The number of seconds the message to be displayed.
    :return:  Nothing
    """
    print(f'\n* [ERROR]: {msg} *\n', file=sys.stderr)
    time.sleep(seconds)


def media_player(tracks: list, path: Path):
    """
    Facilitates the media player operation.

    :param tracks:  The list of tracks to be played.
    :param path:  The path where the tracks are stored.
    :return:  Nothing
    """
    global PAUSE, NXT, VOL, HALT, KEY_LISTENER

    # Initial volume setting (1 is max) #
    volume = 0.5
    # Initialize the mixer #
    mixer.init()

    # Infinite loop replays track list when complete #
    while True:
        # Iterate through each track in track list #
        for track in tracks:
            # Reset nxt toggle per iteration #
            NXT = False
            # Format file path based on current iteration #
            track_file = path / track

            # Play the current iteration of the track list #
            play_current_track(str(track_file), volume)

            # While the track is playing and the nxt & exit toggles are False #
            while mixer.music.get_pos() != STOP and not NXT and not HALT:
                # While the track is playing and the pause, nxt, exit, and volume are False #
                while mixer.music.get_pos() != STOP and not PAUSE and not NXT and \
                not HALT and not VOL:
                    continue

                # If the pause toggle is equal to false and the music has stopped playing #
                if not PAUSE and mixer.music.get_pos() == STOP:
                    break

                # While the vol toggle is set to True and the music is playing #
                while VOL and mixer.music.get_pos() != STOP:
                    # Reset the volume level #
                    volume = change_volume()
                    # Reset vol toggle #
                    VOL = False

                # While the pause toggle is true #
                while PAUSE:
                    pause_track()
                    break

                # Reset pause toggle & continue music #
                PAUSE = False
                mixer.music.unpause()
                continue

            # If the exit toggle is set #
            if HALT:
                # Stop the music #
                mixer.music.stop()

                # If the key listener thread is alive #
                if KEY_LISTENER.is_alive():
                    # Stop the key listener thread #
                    KEY_LISTENER.stop()

                # Exit program with success code #
                sys.exit(0)


def on_press(key) -> bool:
    """
    Detects key strokes, setting corresponding boolean toggle.

    :param key:  Key press that is detected.
    :return:  The set toggle switch of pressed key.
    """
    global PAUSE, NXT, VOL, HALT

    # If left arrow key is pressed #
    if key == Key.left:
        PAUSE = True
        return PAUSE

    # If right arrow key is pressed #
    if key == Key.right:
        NXT = True
        return NXT

    # If up arrow key is pressed #
    if key == Key.up:
        VOL = True
        return VOL

    # If down arrow key is pressed #
    if key == Key.down:
        HALT = True
        return HALT

    # For pylint return all or none rule #
    return None


def display():
    """
    Displays the key listener options.

    :return:  Nothing
    """
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


def main():
    """
    Gathers tracks in dir as list, displays menu, & starts threads.

    :return:  Nothing
    """
    global KEY_LISTENER

    ret = 0
    tracks = []
    # Get current working directory #
    cwd = Path.cwd()
    track_path = cwd / 'tracks'
    # Set tuple of audio file extension types and command syntax #
    track_type = ('.mp3', '.mp4', '.wav', '.wma', '.m4a', '.flac')

    # If tracks dir does not exist #
    if not track_path.exists():
        # Create tracks dir #
        track_path.mkdir()
        # Print error and exit #
        print_err('tracks dir was missing but now exists, drag songs in the dir and '
                  'restart the program', 2)
        sys.exit(1)

    # Iterate through files in tracks directory #
    [tracks.append(file.name) for file in os.scandir(track_path) if file.name.endswith(track_type)]
    # Display the menu #
    display()

    # Create the keystroke listener thread #
    KEY_LISTENER = Listener(on_press=on_press)
    # Create the media player thread #
    player = Thread(target=media_player, args=(tracks, track_path))

    try:
        # Start and join the threads #
        KEY_LISTENER.start()
        player.start()
        KEY_LISTENER.join()
        player.join()

    # If ctrl + c detected #
    except KeyboardInterrupt:
        print('\n[!] Ctrl + C detected .. exiting')

    # If unknown exception occurs #
    except Exception as err:
        print_err(f'Unknown exception occurred {err}', 2)
        ret = 2

    finally:
        # If the keystroke listener thread is alive #
        if KEY_LISTENER.is_alive():
            # Terminate the thread #
            KEY_LISTENER.stop()

    sys.exit(ret)


if __name__ == '__main__':
    main()
