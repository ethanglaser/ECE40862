from machine import Timer
import network
from time import sleep
import esp32
import socket


def internet(name, pw):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect(name, pw)
        while not wlan.isconnected():
            pass
    print('Connected to ' + name)

def measure():
    HALL = esp32.hall_sensor()
    TEMP = esp32.raw_temperature()
    print("Temp: " + str(TEMP))
    print("Hall: " + str(HALL))
    api_key = 'F1Z7M4ES4TCB1UFO'
    host = 'api.thingspeak.com'
    path = 'update?api_key=' + api_key + '&field1=' + str(TEMP) + '&field2=' + str(HALL)
    try:
        addr = socket.getaddrinfo(host, 80)[0][-1]
        s = socket.socket()
        s.connect(addr)
        s.send(bytes('GET /' + path + ' HTTP/1.0\r\n\r\n', 'utf8'))
        s.close()
        sleep(0.1)
    except Exception as e: # Here it catches any error.
        print(e)

internet('Glaser-Laptop', '9}5U068f')
tim0 = Timer(0)
tim0.init(period=15000, mode=Timer.PERIODIC, callback = lambda t: measure())
