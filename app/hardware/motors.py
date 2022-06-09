import RPi.GPIO as GPIO

in1 = 5
in2 = 6
ena = 13
in3 = 20
in4 = 21
enb = 18
temp1 = 1


class Motors:
    def __init__(self):
        self.direction = None
        self.temp1 = 1

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(in1, GPIO.OUT)
        GPIO.setup(in2, GPIO.OUT)
        GPIO.setup(ena, GPIO.OUT)
        GPIO.output(in1, GPIO.LOW)
        GPIO.output(in2, GPIO.LOW)
        self.p = GPIO.PWM(ena, 1000)

        GPIO.setup(in3, GPIO.OUT)
        GPIO.setup(in4, GPIO.OUT)
        GPIO.setup(enb, GPIO.OUT)
        GPIO.output(in1, GPIO.LOW)
        GPIO.output(in2, GPIO.LOW)
        self.p2 = GPIO.PWM(enb, 1000)

        self.p.start(25)
        self.p2.start(25)

    def forward(self):
        GPIO.output(in1, GPIO.HIGH)
        GPIO.output(in2, GPIO.LOW)
        GPIO.output(in3, GPIO.HIGH)
        GPIO.output(in4, GPIO.LOW)

    def backward(self):
        GPIO.output(in1, GPIO.LOW)
        GPIO.output(in2, GPIO.HIGH)
        GPIO.output(in3, GPIO.LOW)
        GPIO.output(in4, GPIO.HIGH)

    def move(self, direction, speed):
        if direction == 's':
            print("stop")
            GPIO.output(in1, GPIO.LOW)
            GPIO.output(in2, GPIO.LOW)
            GPIO.output(in3, GPIO.LOW)
            GPIO.output(in4, GPIO.LOW)

        elif direction == 'f':
            print("forward")
            self.Forward()
            self.temp1 = 1

        elif direction == 'b':
            print("backward")
            self.Backward()
            self.temp1 = 0

        elif direction == 'rl':
            GPIO.output(in1, GPIO.HIGH)
            GPIO.output(in2, GPIO.LOW)
            GPIO.output(in3, GPIO.LOW)
            GPIO.output(in4, GPIO.HIGH)

        elif direction == 'rr':
            GPIO.output(in1, GPIO.LOW)
            GPIO.output(in2, GPIO.HIGH)
            GPIO.output(in3, GPIO.HIGH)
            GPIO.output(in4, GPIO.LOW)

        elif direction == 'tl':
            if self.temp1 == 1:
                self.forward()
            else:
                self.backward()
            self.p.ChangeDutyCycle(speed * 0.75)
            self.p2.ChangeDutyCycle(speed * 0.25)

        elif direction == 'tr':
            if self.temp1 == 1:
                self.forward()
            else:
                self.backward()
            self.p.ChangeDutyCycle(speed * 0.25)
            self.p2.ChangeDutyCycle(speed * 0.75)

    def speed(self, speed):
        self.p.ChangeDutyCycle(speed)
        self.p2.ChangeDutyCycle(speed)
