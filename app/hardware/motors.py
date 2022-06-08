
import RPi.GPIO as GPIO          
from time import sleep

class Motors:
  def__init__(self):
    in1 = 5
    in2 = 6
    ena = 18
    in3 = 20
    in4 = 21
    enb = 13
    temp1=1

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(in1,GPIO.OUT)
    GPIO.setup(in2,GPIO.OUT)
    GPIO.setup(ena,GPIO.OUT)
    GPIO.output(in1,GPIO.LOW)
    GPIO.output(in2,GPIO.LOW)
    p=GPIO.PWM(ena,1000)

    GPIO.setup(in3,GPIO.OUT)
    GPIO.setup(in4,GPIO.OUT)
    GPIO.setup(enb,GPIO.OUT)
    GPIO.output(in1,GPIO.LOW)
    GPIO.output(in2,GPIO.LOW)
    p2=GPIO.PWM(enb,1000)

    p.start(25)
    p2.start(25)
    print("\n")
    print("The default speed & direction of motor is LOW & Forward.....")
    print("r-run s-stop f-forward b-backward l-low m-medium h-high e-exit")
    print("\n")  
    
  def Forward(self):
    GPIO.output(in1,GPIO.HIGH)
    GPIO.output(in2,GPIO.LOW)
    GPIO.output(in3,GPIO.HIGH)
    GPIO.output(in4,GPIO.LOW)
    
  def Backward(self):
    GPIO.output(in1,GPIO.LOW)
    GPIO.output(in2,GPIO.HIGH)
    GPIO.output(in3,GPIO.LOW)
    GPIO.output(in4,GPIO.HIGH)   
  
  def Move(self, direction):


    elif direction=='s':
      print("stop")
      GPIO.output(in1,GPIO.LOW)
      GPIO.output(in2,GPIO.LOW)
      GPIO.output(in3,GPIO.LOW)
      GPIO.output(in4,GPIO.LOW)
      x='z'

    elif x=='f':
      print("forward")
      self.Forward()
      temp1=1
      x='z'

    elif x=='b':
      print("backward")
      self.Backward()
      temp1=0
      x='z'
    
    elif x=='rl':
      GPIO.output(in1,GPIO.HIGH)
      GPIO.output(in2,GPIO.LOW)
      GPIO.output(in3,GPIO.LOW)
      GPIO.output(in4,GPIO.HIGH)
      
    elif x=='rr':
      GPIO.output(in1,GPIO.LOW)
      GPIO.output(in2,GPIO.HIGH)
      GPIO.output(in3,GPIO.HIGH)
      GPIO.output(in4,GPIO.LOW) 
      
    elif x=='tl':
      if(temp1==1):
        self.Forward()
      else:
        self.Backward() 
      p.ChangeDutyCycle(75)
      p2.ChangeDutyCycle(25)
      
    elif x=='tr':
      if(temp1==1):
        self.Forward()
      else:
        self.Backward()
      p.ChangeDutyCycle(25)
      p2.ChangeDutyCycle(75)
    
  def Speed(self, speed):
     p.ChangeDutyCycle(speed)
     p2.ChangeDutyCycle(speed)
  
    


   
