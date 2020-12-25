import esp32
from machine import Pin, Timer
import network
import socket


def internet(name, pw):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect(name, pw)
        while not wlan.isconnected():
            pass
    print(wlan.ifconfig())
    print('Connected to ' + name)

def web_page(temp, hall, red_led_state, green_led_state, switch1, switch2):
    """Function to build the HTML webpage which should be displayed
    in client (web browser on PC or phone) when the client sends a request
    the ESP32 server.
    
    The server should send necessary header information to the client
    (YOU HAVE TO FIND OUT WHAT HEADER YOUR SERVER NEEDS TO SEND)
    and then only send the HTML webpage to the client.
    
    Global variables:
    TEMP, HALL, RED_LED_STATE, GREEN_LED_STAT
    """
    
    html_webpage = """<!DOCTYPE HTML><html>
    <head>
    <title>ESP32 Web Server</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.7.2/css/all.css" integrity="sha384-fnmOCqbTlWIlj8LyTjo7mOUStjsKC4pOpQbqyi7RrhN7udi9RwhKkMHpvLbHG9Sr" crossorigin="anonymous">
    <style>
    html {
     font-family: Arial;
     display: inline-block;
     margin: 0px auto;
     text-align: center;
    }
    h1 { font-size: 3.0rem; }
    p { font-size: 3.0rem; }
    .units { font-size: 1.5rem; }
    .sensor-labels{
      font-size: 1.5rem;
      vertical-align:middle;
      padding-bottom: 15px;
    }
    .button {
        display: inline-block; background-color: #e7bd3b; border: none; 
        border-radius: 4px; color: white; padding: 16px 40px; text-decoration: none;
        font-size: 30px; margin: 2px; cursor: pointer;
    }
    .button2 {
        background-color: #4286f4;
    }
    </style>
    </head>
    <body>
    <h1>ESP32 WEB Server</h1>
    <p>
    <i class="fas fa-thermometer-half" style="color:#059e8a;"></i> 
    <span class="sensor-labels">Temperature</span> 
    <span>"""+str(temp)+"""</span>
    <sup class="units">&deg;F</sup>
    </p>
    <p>
    <i class="fas fa-bolt" style="color:#00add6;"></i>
    <span class="sensor-labels">Hall</span>
    <span>"""+str(hall)+"""</span>
    <sup class="units">V</sup>
    </p>
    <p>
    SWITCH1 Current State: <strong>""" + switch1 + """</strong>
    </p>
    <p>
    SWITCH2 Current State: <strong>""" + switch2 + """</strong>
    </p>
    <p>
    RED LED Current State: <strong>""" + str(red_led_state) + """</strong>
    </p>
    <p>
    <a href="/?red_led=on"><button class="button">RED ON</button></a>
    </p>
    <p>
    <a href="/?red_led=off"><button class="button button2">RED OFF</button></a>
    </p>
    <p>
    GREEN LED Current State: <strong>""" + str(green_led_state) + """</strong>
    </p>
    <p>
    <a href="/?green_led=on"><button class="button">GREEN ON</button></a>
    </p>
    <p>
    <a href="/?green_led=off"><button class="button button2">GREEN OFF</button></a>
    </p>
    </body>
    </html>"""
    return html_webpage


internet('Elite Longbowman', 'ageofempires')
led_grn = Pin(17, Pin.OUT)
led_red = Pin(16, Pin.OUT)
button_0 = Pin(34, Pin.IN)
button_1 = Pin(39, Pin.IN)
addr = socket.getaddrinfo('', 80)[0][-1]

s = socket.socket()
s.bind(addr)
s.listen(1)

print('listening on', addr)

while True:
    cl, addr = s.accept()
    val = ''
    data = cl.recv(1024)
    val += str(data, 'utf8')
    try:
        action = val.split(' HTTP')[0].split('?')[1]
        if action == 'red_led=on':
            led_red.value(1)
        elif action == 'red_led=off':
            led_red.value(0)
        elif action == 'green_led=on':
            led_grn.value(1)
        elif action == 'green_led=off':
            led_grn.value(0)
    except:
        pass

    HALL = esp32.hall_sensor()
    TEMP = esp32.raw_temperature()
    if button_0.value():
        b0 = 'ON'
    else:
        b0 = 'OFF'
    if button_1.value():
        b1 = 'ON'
    else:
        b1 = 'OFF'
    pg = web_page(TEMP, HALL, led_red.value(), led_grn.value(), b0, b1)
    cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
    cl.send(pg)
    cl.close()

