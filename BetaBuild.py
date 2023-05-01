##################################################################
# Name: Chase, Taylor, Memphis
# Date:
# Description: Final Project GUI v7.2
##################################################################
import tkinter as tk
import RPi.GPIO as GPIO
from threading import Thread
from time import sleep

# setting up program
xScore = 0
yScore = 0
win = False
num = 0
points = {}
GPIO.setmode(GPIO.BCM)
GPIO.setup(25, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
redLights = {"a1":17, "a2":4, "a3":11, "b1":13, "b2":7, "b3":20, "c1":6, "c2":10, "c3":23}
blueLights = {"a1":16, "a2":18, "a3":19, "b1":12, "b2":8, "b3":21, "c1":5, "c2":9, "c3":27}
for k in redLights.keys():
    GPIO.setup(redLights[k], GPIO.OUT)
    GPIO.output(redLights[k], 0)
for k in blueLights.keys():
    GPIO.setup(blueLights[k], GPIO.OUT)
    GPIO.output(blueLights[k], 0)
    


window = tk.Tk()
window.resizable(False,False)
window.title("TicTacToe v1.1")

Label1= tk.Label(window, text = "Tic Tac Toe", font=('Ariel',40)) # title display
Label1.pack()
label2= tk.Label(window, text = "Please click a box to start", font=('Ariel',20)) # display whose turn
label2.pack()

playArea= tk.Frame(window, width=600, height=600, bg='lightgray')

# two functions for different levels of restarts
def restart(): # restarts the game itself
    for x in range(1,4):
        for y in range(1,4): # the easiest way was to recreate the points over and over
            Point(x,y)       # and I have yet to run into any issues doin it
    global num
    global points
    points = {}
    num = 1
    for k in redLights.keys():
        GPIO.output(redLights[k], 0)
    for k in blueLights.keys():
        GPIO.output(blueLights[k], 0)
def mainRestart(): # restarts the entire program
    global xScore
    global yScore
    restart()
    xScore=0
    yScore=0


# the score board class
class ScoreBoard(): # simply the score board
    def __init__(self,x=0,y=0):
        self.xScore = x
        self.yScore = y
        self.labelx = tk.Label(playArea, text = "X:", font=('Ariel',32),bg='lightgray')
        self.labelx.grid(row=4, column=1)
        self.labely = tk.Label(playArea, text = "Y:", font=('Ariel',32),bg='lightgray')
        self.labely.grid(row=5, column=1)
        self.labelx1 = tk.Label(playArea, text = x, font=('Ariel',32),bg='lightgray')
        self.labelx1.grid(row=4, column=2)
        self.labely1 = tk.Label(playArea, text = y, font=('Ariel',32),bg='lightgray')
        self.labely1.grid(row=5, column=2)
        self.sign = tk.Label(playArea, text = "By: Taylor, Memphis,", font=('Ariel',15),bg='lightgray')
        self.sign.grid(row=4, column=3)
        self.sign2 = tk.Label(playArea, text = "and Chase", font=('Ariel',15),bg='lightgray')
        self.sign2.grid(row=5, column=3)
    def onClose(self):
        GPIO.cleanup()

# the points class the inherets the score board class
class Point(ScoreBoard):
    def __init__(self, x, y):
        ScoreBoard.__init__(self)
        self.x = x
        self.y = y
        self.value = None
        self.button = tk.Button(playArea,text="",bg='gray', width=8, height=6, font=('Ariel',32), command=self.setPoint)
        self.button.grid(row=x,column=y)
        column = ["a", "b", "c"]     # naming the points based on how we talked about         a1 a2 a3
        row = ["3","2","1"]          # naming the points based on how we taled about          b1 b2 b3
        self.point = column[x-1] + row[y-1] # naming the points base on how we talked about   c1 c2 c3

    def setPoint(self):
        if not self.value: # checks to see if button has already been used
            global xScore
            global yScore
            global num
            global win
            global points
            if (num % 2 == 0):
                self.button.configure(text="X",bg='white', fg='black') # sets the clor of lettering
                self.value = "X"
                points[self.point] = 'X' # plots the list in a dictionary based naming system ex a1: "X"
                print(points)
                #GPIO.output(redLights[self.point], 1)
                label2["text"] = "Y's Turn"             # changes the label 2 to the correct persons turn
                self.checkwin() # checks for win
                if win == True: # if win
                    xScore += 1
                    ScoreBoard(xScore,yScore)   
                    win = False
                    if xScore == 3: # after 5 wins, X has won
                        label2["text"] = "X has won"
                        mainRestart()
                
            elif(num % 2 != 0):
                self.button.configure(text="Y",bg='white', fg='black') # litterary copies the last section
                self.value = "Y"
                points[self.point] = 'Y'
                print(self.point)
                #GPIO.output(blueLights[self.point], 1)
                label2["text"] = "X's Turn"
                self.checkwin()
                if win == True:
                    yScore += 1
                    ScoreBoard(xScore,yScore)  
                    win = False
                    if yScore == 3:
                        label2["text"] = "Y has won"
                        mainRestart()
            num += 1
            for k in points.keys():
                if points[k] == "X":
                    GPIO.output(redLights[k], 1)
                if points[k] == "Y":
                    GPIO.output(blueLights[k], 1)

    def checkwin(self): # checks every possible win
        global num
        global win
        try:
            if(points["a1"] == points["b1"] == points["c1"]):
                win = True
                restart()
        except:
            pass
        try:
            if(points["a2"] == points["b2"] == points["c2"]):
                win = True
                restart()
        except:
            pass
        try:
            if(points["a3"] == points["b3"] == points["c3"]):
                win = True
                restart()
        except:
            pass
        try:
            if(points["a1"] == points["a2"] == points["a3"]):
                win = True
                restart()
        except:
            pass
        try:
            if(points["b1"] == points["b2"] == points["b3"]):
                win = True
                restart()
        except:
            pass
        try:
            if(points["c1"] == points["c2"] == points["c3"]):
                win = True
                restart()
        except:
            pass
        try:
            if(points["a1"] == points["b2"] == points["c3"]):
                win = True
                restart()
        except:
            pass
        try:
            if(points["a3"] == points["b2"] == points["c1"]):
                win = True
                restart()
        except:
            pass
        if (num == 8) and (win == False):
            restart()

class check_button(Thread): #class for button input
    def __init__(self):
        Thread.__init__(self)
    
    def checkLoop(self):
        while(True):
            text = input("reset? ")
            if (text == "yes"):
                mainRestart()
            '''
            if (GPIO.input(25) == GPIO.HIGH):
                mainRestart()
                sleep(2)'''


# actually creates the grid the firs ttime 
for x in range(1,4):
    for y in range(1,4):
        Point(x,y)

# actually creates the score board the first time
scoreboard = ScoreBoard()
    
check = check_button()
c1 = Thread(target=check.checkLoop)
c1.start()

#window.protocol("WM_DELETE_WINDOW",ScoreBoard.onClose())

playArea.pack(pady=10,padx=10)


window.mainloop()