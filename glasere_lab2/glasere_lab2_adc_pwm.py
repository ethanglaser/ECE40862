from machine import Pin, Timer, PWM, RTC, ADC
from time import sleep

button = Pin(34, Pin.IN)

year = int(input("Year? "))
month = int(input("Month? "))
day = int(input("Day? "))
weekday = int(input("Weekday? "))
hour = int(input("Hour? "))
minute = int(input("Minute? "))
second = int(input("Second? "))
microsecond = int(input("Microsecond? "))

rtc = RTC()
rtc.datetime((year, month, day, weekday, hour, minute, second, microsecond))
adc = ADC(Pin(36))
adc.atten(ADC.ATTN_11DB)
tim0 = Timer(0)
week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
tim0.init(period=30000, mode=Timer.PERIODIC, callback = lambda t: display())
tim1 = Timer(1)
tim1.init(period=100, mode=Timer.PERIODIC, callback = lambda t: choice())
pwm0 = PWM(Pin(16), freq=10, duty=256)
pwm1 = PWM(Pin(17), freq=10, duty=256)
mode = 0
prev = 0

def choice():
    if mode == 1:
        pwm1.freq(int(4 + adc.read() / 120))
    if mode == 2:
        pwm0.duty(int(adc.read() / 10))
        
def display():
    a = rtc.datetime()
    print(week[a[3]] + ", " + str(a[1]) + '/' + str(a[2]) + '/' + str(a[0]) + ', ' + str(a[4]) + ':' + ("%02d" % (a[5],)) + ':' + ("%02d" % (a[6],)) + '.' + str(a[7]))

while(1):
    if button.value() and prev == 0:
        if mode != 1:
            mode = 1
        else:
            mode = 2
    prev = button.value()
    sleep(0.02)

'''
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
print("You have successfully implemented LAB1 DEMO!!!")'''
