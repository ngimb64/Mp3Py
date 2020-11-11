import os, re, sys, time
from pyfiglet import Figlet
from pygame import mixer
from pynput.keyboard import Key, Listener
from threading import Thread

def display():
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


def on_press(key):
    global pause, nxt, vol, exit

    if key == Key.left:
        pause = 'yes'
        return pause   

    elif key == Key.right:
        nxt = 'yes'
        return nxt 

    elif key == Key.up:
        vol = 'yes'
        return vol

    elif key == Key.down:
        exit = 'yes'
        return exit

def media_player(tracks, path):
    global pause, nxt, vol, exit, key_listener 
    mixer.init()
    for track in tracks:
        nxt = 'no'
        mixer.music.load(path + '\\tracks\\' + track)
        mixer.music.set_volume(0.5)
        mixer.music.play()
        while mixer.music.get_pos() != -1 and  nxt != 'yes' and exit != 'yes':
            while mixer.music.get_pos() != -1 and pause != 'yes' and nxt != 'yes' \
                and exit != 'yes' and vol != 'yes':
                continue

            if pause != 'yes' and mixer.music.get_pos() == -1:
                break

            while vol == 'yes' and mixer.music.get_pos() != -1:
                re_float = re.compile(r'(?:(?:^0$|^1$)|(^0\.[0-9]$))')
                os.system('cls')
                v = input('Enter volume 0, 1, or 0.1 to 0.9: \n')
                if re_float.match(v):
                    mixer.music.set_volume(float(v))
                    os.system('cls')
                    print('Volume has changed')
                    time.sleep(3)
                    os.system('cls')
                    display()
                    break

                print('* Inproper value detected .. volume unable to change *')
                time.sleep(3)
                continue

            vol = 'no'

            while pause == 'yes':
                mixer.music.pause()
                while True:
                    os.system('cls')  
                    prompt = input('Hit enter to continue\n')
                    if prompt != '':                      
                        print('* Only hit enter, no data input needed *')
                        time.sleep(3)
                        continue

                    break
                
                os.system('cls')
                display()
                break

            pause = 'no'
            mixer.music.unpause()
            continue

        if exit == 'yes':
            mixer.music.stop()

            if key_listener.is_alive():
                key_listener.stop()

            sys.exit(0)

    if key_listener.is_alive():
        key_listener.stop()

    sys.exit(0)

def main():
    global pause, nxt, vol, exit, key_listener
    try:
        pause = ''
        nxt = ''
        vol = ''
        exit = ''
        tracks = []
        path = os.getcwd()
        re_track = re.compile(r'^.+\.(?:mp3|mp4|wav)')

        for dirpath, dirnames, filenames in os.walk(path + '\\tracks'):
            [ tracks.append(file) for file in filenames if re_track.match(file) ]
        
        display()
        key_listener = Listener(on_press=on_press)
        player = Thread(target=media_player, args=(tracks,path)) 
        key_listener.start() ; player.start()
        key_listener.join() ; player.join()

    except KeyboardInterrupt:
        print('Program exiting ..')
        if key_listener.is_alive():
            key_listener.stop()

if __name__ == '__main__':
    main()