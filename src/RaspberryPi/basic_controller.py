#Rasperry Pi code, swithched from arduino due to available hardware
import RPI.GPIO
import time

#Pin definitions
in1 = 24 #L298N IN1 connected to GPIO24
in2 = 23 #L298N IN2 connected to GPIO23
enA = 25 #L298 ENA connected to GPIO25, the ENA connects to the first of two motors connected to the L298N

#RPI.GPIO Pin setup
RPI.GPIO.setmode(RPI.GPIO.BCM)
RPI.GPIO.setup(in1,RPI.GPIO.OUT)
RPI.GPIO.setup(in2,RPI.GPIO.OUT)
RPI.GPIO.setup(enA,RPI.GPIO.OUT) 
RPI.GPIO.output(in1,RPI.GPIO.LOW)
RPI.GPIO.output(in2,RPI.GPIO.LOW)
power=RPI.GPIO.PWM(enA,1000) #PWM frequency of 1000Hz, later power.changeDutyCycle(x) can be used to change the speed


#Main loop
while(1):
    print("placeholder")

