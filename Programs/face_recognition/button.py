import RPi.GPIO as GPIO
import time
import os

#21-es GPIO port beállítva nyomógombos bevitelre(high jel küldése) 
GPIO.setmode(GPIO.BCM) 
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP)
while True:
    input_state = GPIO.input(21)
    if input_state == False:
        print('Button Pressed')
        #terminal parancs indítása a gomb megnyomására (tartalmazó mappába
        #lépés .bashrc fájl átírásával került megoldásra
        command = "python pi_face_recognition.py --cascade haarcascade_frontalface_default.xml --encodings encodings.pickle"
        os.system(command)
        time.sleep(5)

                