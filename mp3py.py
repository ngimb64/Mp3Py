# pylint: disable=W0106
""" Built-in modules """
import os
import sys
import time
from re import match
from threading import Thread
# Third-party Modules #
from pyfiglet import Figlet
from pygame import mixer
from pynput.keyboard import Key, Listener


# Globals #
PAUSE, NXT, VOL, HALT = False, False, False, False
global KEY_LISTENER

# Pseudo constants #
STOP = -1


def pause_track(cmd: str):
    """
    Pauses the track until enter is hit to continue.

    :param cmd:  Clear display command syntax.
    :return:  Nothing
    """
    # Pause the music #
    mixer.music.pause()
    while True:
        prompt = input('\nHit enter to continue\n')
        # If enter is not detected #
        if prompt != '':
            # Call PrintError and re-iterate loop #
            print_err('Only hit enter, no data input needed', 2, cmd)
            continue

        break

    # Clear the display #
    os.system(cmd)
    # Re-display the menu #
    display()


def change_volume(cmd: str) -> float:
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
            # Sleep execution 2 seconds #
            time.sleep(2)
            # Clear the display #
            os.system(cmd)
            # Re-display the menu #
            display()
            break

        # Print error, sleep 2 seconds, and re-iterate input loop #
        print_err('Improper value detected .. volume unable to change', 2, cmd)
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


def print_err(msg, seconds: int, cmd: str):
    """
    Prints time controlled error message via stderr.

    :param msg:  The error message to be displayed via stderr.
    :param seconds:  The number of seconds the message to be displayed.
    :param cmd:  Clear display command syntax.
    :return:  Nothing
    """
    print(f'\n* [ERROR]: {msg} *\n', file=sys.stderr)
    time.sleep(seconds)

    # Clear display #
    os.system(cmd)
    # Re-display menu #
    display()


def media_player(tracks: list, path: str, cmd: str):
    """
    Facilitates the media player operation.

    :param tracks:  The list of tracks to be played.
    :param path:  The path where the tracks are stored.
    :param cmd:  Clear screen command syntax.
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

            # Play the current iteration of the track list #
            play_current_track(f'{path}{track}', volume)

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
                    volume = change_volume(cmd)
                    # Reset vol toggle #
                    VOL = False

                # While the pause toggle is true #
                while PAUSE:
                    pause_track(cmd)
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
    elif key == Key.right:
        NXT = True
        return NXT

    # If up arrow key is pressed #
    elif key == Key.up:
        VOL = True
        return VOL

    # If down arrow key is pressed #
    elif key == Key.down:
        HALT = True
        return HALT


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
    cwd = os.getcwd()
    # If the OS is Windows #
    if os.name == 'nt':
        track_path = f'{cwd}\\tracks\\'
    # If the Os is Linux #
    else:
        track_path = f'{cwd}/tracks/'

    # Set tuple of audio file extension types and command syntax #
    track_type = ('.mp3', '.mp4', '.wav', '.wma', '.m4a', '.flac')
    cmds = ('cls', 'clear')

    # If the OS is Windows #
    if os.name == 'nt':
        cmd = cmds[0]
    # For other OS's #
    else:
        cmd = cmds[1]

    # If tracks dir does not exist #
    if not os.path.isdir(track_path):
        # Create tracks dir #
        os.mkdir(track_path)
        print_err('tracks dir was missing but now exists, drag songs in the dir and restart program'
                  , 2, cmd)
        sys.exit(1)

    # Iterate through files in tracks directory #
    [tracks.append(file.name) for file in os.scandir(track_path) if file.name.endswith(track_type)]

    # Clear the display #
    os.system(cmd)

    # Display the menu #
    display()

    # Create the keystroke listener thread #
    KEY_LISTENER = Listener(on_press=on_press)
    # Create the media player thread #
    player = Thread(target=media_player, args=(tracks, track_path, cmd))

    try:
        # Start and join the threads #
        KEY_LISTENER.start()
        player.start()
        KEY_LISTENER.join()
        player.join()

    # If ctrl + c detected #
    except KeyboardInterrupt:
        print('\nCtrl + C detected .. exiting')

    # If unknown exception occurs #
    except Exception as err:
        print_err(f'Unknown exception occurred {err}', 4, cmd)
        ret = 2

    finally:
        # If the keystroke listener thread is alive #
        if KEY_LISTENER.is_alive():
            # Terminate the thread #
            KEY_LISTENER.stop()

    sys.exit(ret)


if __name__ == '__main__':
    main()
