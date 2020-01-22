from gpiozero import LED
import time

led1 = LED(17)
led2= LED(27)
led1.on()
time.sleep(2)
led1.off()
led2.on()
time.sleep(2)
led2.off()