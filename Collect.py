import numpy as np
import cv2
import time
import os
import mss
from pynput.keyboard import Key, Listener

def on_press(key):
    with mss.mss() as sct:
            # 800x700 windowed mode
            monitor = {"top": 40, "left": 0, "width": 800, "height": 700}

            # Capture screen
            img = np.array(sct.grab(monitor))
            screen = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            screen = cv2.resize(screen, (120,120))

            # Record keypresses
            output = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
            action = False
            if key.char == ("d"):
                action = True
                output[2] = 1.0
            elif key.char == 'a':
                action = True
                output[0] = 1.0
            elif key.char == 'w':
                action = True
                output[1] = 1.0
            elif key.char == 'j':
                action = True
                output[3] = 1.0
            elif key.char == 'k':
                action = True
                output[4] = 1.0
            elif key.char == 'u':
                action = True
                output[5] = 1.0
            print(f"Output: {output} ")

            # If valid key is pressed, append pixels and keypress array to training data
            if action:
                training_data.append([screen, np.array(output)])
            print(f"Current Length: {len(training_data)}")
            
            # Save data
            if len(training_data) % 100 == 0:
                np.save(file_name,training_data) 
            print(len(training_data))

def on_release(key):
    print('{0} release'.format(
        key))
    if key == Key.esc:
        # Stop listener
        return False


file_name = 'training_data.npy'

if os.path.isfile(file_name):
    print('File exists, loading previous data!')
    training_data = list(np.load(file_name))
    
else:
    print('File does not exist, starting fresh!')
    training_data = []


def main():
    # Countdown!
    for i in list(range(4))[::-1]:
        print(i+1)
        time.sleep(1)
    # Listen for keypresses
    while True:
            with Listener(
                    on_press=on_press,
                    on_release=on_release) as listener:
                output = listener.join()          
            
main()
