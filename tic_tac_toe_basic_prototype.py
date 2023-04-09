import RPi.GPIO as GPIO
from time import sleep
# set gpio pins



#set variables
red = 20
yellow = 12
yellowButton = 27
redButton = 17
resetButton = 4
isYellowButtonPressed = False
isRedButtonPressed = False
lights = []

# use broadcom pin mode
GPIO.setmode(GPIO.BCM)

# setup led and switch pins
GPIO.setup(yellowButton, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(redButton, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(red, GPIO.OUT)
GPIO.setup(yellow, GPIO.OUT)
GPIO.setup(resetButton, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

#default to LEDS off, just in case
GPIO.output(red, 0)
GPIO.output(yellow, 0)

#function used to reset LEDs and list
def resetGame():
    print("Resetting...")

    global lights
    for i in lights:
        lights.remove(i)
    global isRedButtonPressed
    global isYellowButtonPressed
    isRedButtonPressed = False
    isYellowButtonPressed = False
    GPIO.output(20, 0)
    GPIO.output(12, 0)
#this function sets booleans back to false, turns off LEDs, and erases each item in the list
    
    
try: #try except loop for main part of program
    while(True):
        if (GPIO.input(redButton) == GPIO.HIGH): #if button pressed, turn on LED and append to list
            GPIO.output(red, 1)
            if ("Red" in lights) == False:
                lights.append("Red")
            print(lights)
            sleep(0.25)

            
        if (GPIO.input(yellowButton) == GPIO.HIGH): #if button pressed, turn on LED and append to list
            isYellowButtonPressed = True
            GPIO.output(yellow, 1)
            if ("Yellow" in lights) == False:
                lights.append("Yellow")
            print(lights)
            sleep(0.25)
            
        if (GPIO.input(resetButton) == GPIO.HIGH): #if reset button pressed, call reset function
            resetGame()
            sleep(0.25)
            
#note that i added a sleep time of .25 seconds after each button detection--
#i added this for debouncing. without it, each button press would execute the loop
#multiple times
except KeyboardInterrupt:
    GPIO.cleanup()


