from machine import Pin
from time import sleep

button_grn = Pin(34, Pin.IN)
button_red = Pin(39, Pin.IN)
led_grn = Pin(17, Pin.OUT)
led_red = Pin(16, Pin.OUT)
green = 0
red = 0
green_total = 0
red_total = 0

while(1):
    if button_grn.value() == 1 and green == 0:
        green_total += 1
        if green_total == 10:
            break
    if button_red.value() == 1 and red == 0:
        red_total += 1
        if red_total == 10:
            break
    if button_grn.value() == button_red.value():
        led_grn.value(0)
        led_red.value(0)
    else:            
        led_grn.value(button_grn.value())
        led_red.value(button_red.value())
    green = button_grn.value()
    red = button_red.value()
    sleep(0.05)
    
led_grn.value(1)
led_red.value(0)
while(1):
    if (green_total == 10 and button_red.value()) or (red_total == 10 and button_grn.value()):
        break
    led_grn.value(not led_grn.value())
    led_red.value(not led_red.value())
    sleep(0.5)

led_grn.value(0)
led_red.value(0)
print("You have successfully implemented LAB1 DEMO!!!")