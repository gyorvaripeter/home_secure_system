from gpiozero import LED
import time

led1 = LED(17)
led2= LED(27)
led1.on()
time.sleep(5)
led1.off()
led2.on()
time.sleep(5)
led2.off()