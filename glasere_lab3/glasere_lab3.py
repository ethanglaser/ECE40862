import machine
from machine import Pin, TouchPad, Timer, RTC
from time import sleep
import esp32
import network
import ubinascii
import ntptime


def do_connect(name, pw):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect(name, pw)
        while not wlan.isconnected():
            pass
    print('Oh Yes! Get connected')
    print('Connected to ' + name)
    print('MAC Address: ' + ubinascii.hexlify(wlan.config('mac'), ":").decode())

    print('network config:' + wlan.ifconfig()[0])

button_0 = Pin(34, Pin.IN)
button_1 = Pin(39, Pin.IN)
led_grn = Pin(17, Pin.OUT)
led_red = Pin(16, Pin.OUT)

led_red.value(1)

t_0 = TouchPad(Pin(12))
t_1 = TouchPad(Pin(14))
#t_1.config(400)
t_0.config(400)


do_connect('Elite Longbowman', 'ageofempires')
ntptime.settime()
rtc = RTC()
#ntptime.settime()
esp32.wake_on_touch(t_0)
esp32.wake_on_ext1(pins = (button_0, button_1), level = esp32.WAKEUP_ANY_HIGH)
awake = {4: "Timer", 3: "Ext1", 5: "Touchpad"} #add for touchpad
tim0 = Timer(0)
tim0.init(period=15000, mode=Timer.PERIODIC, callback = lambda t: display())#15
tim1 = Timer(1)
tim1.init(period=10, mode=Timer.PERIODIC, callback = lambda t: touched())
tim2 = Timer(2)
tim2.init(period=30000, mode=Timer.PERIODIC, callback = lambda t: sleepy())#30

def display():
    a = rtc.datetime()
    print("Date: " + ("%02d" % (a[1],)) + '/' + ("%02d" % (a[2],)) + '/' + ("%02d" % (a[0],)))
    print("Time: " + ("%02d" % ((a[4] - 4) % 24,)) + ":" + ("%02d" % (a[5],)) + ":" + ("%02d" % (a[6],)) + " HRS")
def touched():
    if t_1.read() < 400:
        led_grn.value(1)
    else:
        led_grn.value(0)
def sleepy():
    print("I am awake. Going to sleep for 1 minute")
    sleep(0.05)
    machine.lightsleep(60000) #60
    led_red.value(1)
    print("Woke up due to " + awake[machine.wake_reason()])

        



