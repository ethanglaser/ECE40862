import esp32
from machine import I2C, Pin, Timer, PWM
from time import sleep



class MPU:
    # Static MPU memory addresses
    ACC_X = 0x3B
    ACC_Y = 0x3D
    ACC_Z = 0x3F
    TEMP = 0x41
    GYRO_X = 0x43
    GYRO_Y = 0x45
    GYRO_Z = 0x47

    def acceleration(self):
        self.i2c.start()
        acc_x = self.i2c.readfrom_mem(self.addr, MPU.ACC_X, 2)
        acc_y = self.i2c.readfrom_mem(self.addr, MPU.ACC_Y, 2)
        acc_z = self.i2c.readfrom_mem(self.addr, MPU.ACC_Z, 2)
        self.i2c.stop()

        # Accelerometer by default is set to 2g sensitivity setting
        # 1g = 9.81 m/s^2 = 16384 according to mpu datasheet
        acc_x = self.__bytes_to_int(acc_x) / 16384 * 9.81
        acc_y = self.__bytes_to_int(acc_y) / 16384 * 9.81
        acc_z = self.__bytes_to_int(acc_z) / 16384 * 9.81

        return acc_x, acc_y, acc_z

    def temperature(self):
        self.i2c.start()
        temp = self.i2c.readfrom_mem(self.addr, self.TEMP, 2)
        self.i2c.stop()

        temp = self.__bytes_to_int(temp)
        return temp / 340 + 36.53
        #return self.__celsius_to_fahrenheit(temp / 340 + 36.53)
        #return temp

    def gyro(self):
        return self.pitch, self.roll, self.yaw

    def __init_gyro(self):
    # MPU must be stationary
        gyro_offsets = self.__read_gyro()
        self.pitch_offset = gyro_offsets[1]
        self.roll_offset = gyro_offsets[0]
        self.yaw_offset = gyro_offsets[2]

    def __read_gyro(self):
        self.i2c.start()
        gyro_x = self.i2c.readfrom_mem(self.addr, MPU.GYRO_X, 2)
        gyro_y = self.i2c.readfrom_mem(self.addr, MPU.GYRO_Y, 2)
        gyro_z = self.i2c.readfrom_mem(self.addr, MPU.GYRO_Z, 2)
        self.i2c.stop()

        # Gyro by default is set to 250 deg/sec sensitivity
        # Gyro register values return angular velocity
        # We must first scale and integrate these angular velocities over time before updating current pitch/roll/yaw
        # This method will be called every 100ms...
        gyro_x = self.__bytes_to_int(gyro_x) / 131 * 0.1
        gyro_y = self.__bytes_to_int(gyro_y) / 131 * 0.1
        gyro_z = self.__bytes_to_int(gyro_z) / 131 * 0.1

        return gyro_x, gyro_y, gyro_z

    def __update_gyro(self, timer):
        gyro_val = self.__read_gyro()
        self.pitch += gyro_val[1] - self.pitch_offset
        self.roll += gyro_val[0] - self.roll_offset
        self.yaw += gyro_val[2] - self.yaw_offset

    @staticmethod
    def __celsius_to_fahrenheit(temp):
        return temp * 9 / 5 + 32

    @staticmethod
    def __bytes_to_int(data):
        # Int range of any register: [-32768, +32767]
        # Must determine signing of int
        if not data[0] & 0x80:
            return data[0] << 8 | data[1]
        return -(((data[0] ^ 0xFF) << 8) | (data[1] ^ 0xFF) + 1)

    def __init__(self, i2c):
        # Init MPU
        self.i2c = i2c
        self.addr = i2c.scan()[0]
        self.i2c.start()
        self.i2c.writeto(0x68, bytearray([107,0]))
        self.i2c.stop()
        self.x_offset = 0
        self.y_offset = 0
        self.z_offset = 0
        print('Initialized MPU6050.')

                # Gyro values will be updated every 100ms after creation of MPU object
        self.pitch = 0
        self.roll = 0
        self.yaw = 0
        self.velocity = (0,0,0)
        self.pitch_offset = 0
        self.roll_offset = 0
        self.yaw_offset = 0
        self.__init_gyro()
        gyro_timer = Timer(3)
        gyro_timer.init(mode=Timer.PERIODIC, callback=self.__update_gyro, period=100)

def showVelocity(temp):
    a = mpu.acceleration()
    #print(a)

    a = (a[0] - mpu.x_offset if a[0] - mpu.x_offset > 0.1 or a[0] - mpu.x_offset < -0.1 else 0, a[1] - mpu.y_offset if a[1] - mpu.y_offset > 0.1 or a[1] - mpu.y_offset < -0.1 else 0, a[2] - mpu.z_offset - 9.81 if a[2] - mpu.z_offset - 9.81 > 0.1 or a[2] - mpu.z_offset - 9.81 < -0.1 else 0)
    
    #mpu.velocity = (mpu.velocity[0] + a[0] * 0.5 if mpu.velocity[0] + a[0] * 0.5 > 0.05 or mpu.velocity[0] + a[0] * 0.5 < -0.05 else 0, mpu.velocity[1] + a[1] * 0.5, mpu.velocity[2] + a[2] * 0.5)
    mpu.velocity = (a[0] * 0.5, a[1] * 0.5, a[2] * 0.5)

    if mpu.gyro()[0] > 30 or mpu.gyro()[0] < -30 or mpu.gyro()[1] > 30 or mpu.gyro()[1] < -30 or mpu.gyro()[2] > 30 or mpu.gyro()[2] < -30:
        led_ylw.value(1)
    else:
        led_ylw.value(0)
        
    if mpu.velocity[0] > 5 or mpu.velocity[0] < -5 or mpu.velocity[1] > 5 or mpu.velocity[1] < -5 or mpu.velocity[2] > 5:
        led_red.value(1)
    else:
        led_red.value(0)
        
    if mpu.velocity[0] > -0.2 and mpu.velocity[0] < 0.2 and mpu.velocity[1] > -0.2 and mpu.velocity[1] < 0.2 and mpu.velocity[2] > -0.2 and mpu.velocity[2] < 0.2:
        led_grn.value(1)
    else:
        led_grn.value(0)
    
    current_temp = mpu.temperature()
    if current_temp - temp <= -1 or current_temp - temp >= 1:
        pwm0.freq(10 + int(current_temp - temp()))

    print("Velocity: " + str(mpu.velocity))
    print("Angles: " + str(mpu.gyro()))
    print("Temperature: " + str(current_temp))
    
def set_onboard(btn):
    global state
    global pwm0
    if btn == 1:
        if state:
            pwm0.deinit()
        else:
            state = 1
        led_board = Pin(13, Pin.OUT)
        led_board.value(1)
    elif btn == 2:
        pwm0 = PWM(Pin(13), freq=10, duty=512)    
    
def b1_handler(pin):
    if button_1.value():
        #pwm0.deinit()
        #led_board.value(1)
        #calibrate sensors
        led_red.value(0)
        led_grn.value(0)
        led_ylw.value(0)
        set_onboard(1)
        zero = []
        one = []
        two = []
        tim0.deinit()
        for i in range(10):
            vals = mpu.acceleration()
            zero.append(vals[0])
            one.append(vals[1])
            two.append(vals[2])
            sleep(0.01)
        offsets = mpu.__read_gyro()
        mpu.pitch = 0
        mpu.roll = 0
        mpu.yaw = 0
        mpu.velocity = (0,0,0)
        mpu.x_offset = sum(zero) / 10
        mpu.y_offset = sum(one) / 10
        mpu.z_offset = sum(two) / 10 - 9.81
        print(mpu.acceleration()[0] - mpu.x_offset, mpu.acceleration()[1] - mpu.y_offset, mpu.acceleration()[2] - mpu.z_offset)
        print('Calibration complete.')
        
    
def b2_handler(pin):
    set_onboard(2)
    temp = mpu.temperature()
    tim0.init(period=500, mode=Timer.PERIODIC, callback = lambda t: showVelocity(temp))#15

led_grn = Pin(17, Pin.OUT)
led_ylw = Pin(16, Pin.OUT)
led_red = Pin(19, Pin.OUT)
button_1 = Pin(34, Pin.IN)
button_2 = Pin(39, Pin.IN)
i2c = I2C(scl=Pin(22), sda=Pin(23))
mpu = MPU(i2c)
tim0 = Timer(0)
state = 0
pwm0 = None

button_1.irq(trigger=Pin.IRQ_FALLING, handler=b1_handler)
button_2.irq(trigger=Pin.IRQ_FALLING, handler=b2_handler)


