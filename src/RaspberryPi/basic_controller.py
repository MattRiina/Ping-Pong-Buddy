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

power.start(50) #start the motor at 50% power

#Main loop
while(1):
    command = input() #read user input
    if command == "r": #run
        RPI.GPIO.output(in1,RPI.GPIO.LOW)
        RPI.GPIO.output(in2,RPI.GPIO.HIGH)
        command = "."
    elif command == "q": #stop
        RPI.GPIO.output(in1,RPI.GPIO.LOW)
        RPI.GPIO.output(in2,RPI.GPIO.LOW)
        command = "."
    elif command == "x": #exit
        RPI.GPIO.cleanup()
        print("Exiting...Cleaining up GPIO")
        break
    elif command == "h": #highpower
        print("Changing to high power")
        power.ChangeDutyCycle(80)
        command = "."
    elif command == "m": #medium power
        print("Changing to medium power")
        power.ChangeDutyCycle(50)
        command = "."
    elif command == "l": #lowpower
        print("Changing to low power")
        power.ChangeDutyCycle(25)
        command = "."
    elif command.isdigit(): #if the user input is a number, change the speed\
        speed = int(command)
        print("Changing speed to " + command)
        if(speed > 100 or speed < 0):
            print("Speed must be between 0 and 100")
            continue
        power.ChangeDutyCycle(int(command))
        command = "."
    else:
        print("Invalid command")
