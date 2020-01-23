import RPi.GPIO as GPIO
import time
import os

#21es GPIO port beallitva nyomogombos bevitelre(high jel kuldese) 
GPIO.setmode(GPIO.BCM) 
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP)
while True:
    input_state = GPIO.input(21)
    if input_state == False:
        print('Button Pressed')
        #terminal parancs inditasa a gomb megnyomasara (tartalmazo mappaba
        #lepes .bashrc fajl atirasaval kerult megoldasra
        #command1 = "python3 /home/pi/home_secure_system/Programs/email-notification/emailnotification.py"
        #os.system(command1)
        command = "python pi_face_recognition.py --cascade haarcascade_frontalface_default.xml --encodings encodings.pickle"
        os.system(command)
        time.sleep(5)

    