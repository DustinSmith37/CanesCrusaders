import RPi.GPIO as GPIO

player1 = [18,19,20,21]
p1butts = [23,22]
player2 = [17,16,13,12]
p2butts = [6,5]
playersel = [24,25]

GPIO.setmode(GPIO.BCM)
GPIO.setup(p1butts, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(p2butts, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(playersel, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(player1, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(player2, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

def joystick(direction):
    if(direction == 3):
        return "Right"
    elif(direction == 2):
        return "Left"
    elif(direction == 1):
        return "Down"
    elif(direction ==0):
        return "Up"

def playerbuttons(button):
    if (button == 1):
        return "Black"
    elif(button == 0):
        return "Red"

def playeramount(button):
    if(button ==1):
        return "2 Players"
    elif(button == 0):
        return "1 Player"

try:
    while(True):
        for i in range(len(p1butts)):
            if(GPIO.input(p1butts[i])):
               print("{}".format(playerbuttons(i)))
               
        for i in range(len(p2butts)):
            if(GPIO.input(p2butts[i])):
               print("{}".format(playerbuttons(i)))
               
        for i in range(len(playersel)):
            if(GPIO.input(playersel[i])):
               print("{}".format(playeramount(i)))
               
        for i in range(len(player1)):
            if(GPIO.input(player1[i])):
               print("{}".format(joystick(i)))

        for i in range(len(player2)):
            if(GPIO.input(player2[i])):
               print("{}".format(joystick(i)))

except KeyboardInterrupt:
    GPIO.cleanup()
    print("DONE")
