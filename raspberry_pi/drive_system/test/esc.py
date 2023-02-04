import Adafruit_PCA9685

pwm = Adafruit_PCA9685.PCA9685()
import time, curses, sys, os

pwm.set_pwm_freq(60)

screen = curses.initscr()
curses.noecho()
curses.cbreak()

screen.keypad(True)

running = True
fwdmax = 600
revmax = 200
inc = 20
spinup = 1
stop = 400
go = 400
steering_value = 500
steering_value_init = steering_value
steering_max_left = 380
steering_max_right = 620

def printscreen():
        os.system('clear')
        print("============ RC car controller ============\r")
        print(u"\u2191/\u2193: accelerate/brake\r")
        print(u"\u2190/\u2192: left/right\r")
        print("q:   stops the motor\r")
        print("x:   exit the program\r")
        print("b:   boot the esc\r")        
        print("============== speed display ==============\r")
        print("speed dc motor: "+str(go-stop)+"\r")
        print("steering angle: "+str(steering_value-steering_value_init)+"\r")

def bootup():
    boot = 200
    while boot < fwdmax:
        boot += inc
        pwm.set_pwm(0,0,boot)
        time.sleep(0.1)
        if boot > fwdmax:
            while boot > revmax:
                 boot -= inc
                 pwm.set_pwm(0,0,boot)
                 time.sleep(0.1)
                 if boot < revmax:
                     boot = 400
                     pwm.set_pwm(0,0,boot)
                     spinup = 0
                     break

while running:
    printscreen()
    char = screen.getch()
    if char == ord('q'):
            go = stop
            steering_value = steering_value_init
    elif char == ('b') and spinup == 1:
        bootup()
    elif char == ord('x'):
        go = stop
        steering_value =  steering_value_init
        print("Program Ended\r")
        time.sleep(1)
        running=False
    elif char == curses.KEY_UP:
            if go == 400:
                time.sleep(0.2)
            if go < fwdmax:
                    go += inc
    elif char == curses.KEY_DOWN:
            if go == 400:
                time.sleep(0.2)        
            if go > revmax:
                    go -= inc
    elif char == curses.KEY_LEFT:
            steering_value = steering_value - 10
            if steering_value > steering_value_init:
                steering_value = steering_value_init                
            if steering_value < steering_max_left:
                    steering_value = steering_max_left                   
    elif char == curses.KEY_RIGHT:                       
            steering_value = steering_value + 10
            if steering_value < steering_value_init:
                steering_value = steering_value_init                 
            if steering_value > steering_max_right:
                    steering_value = steering_max_right
    printscreen()
    pwm.set_pwm(0, 0, go)
    pwm.set_pwm(1, 0, steering_value)

curses.nocbreak(); screen.keypad(0); curses.echo()
curses.endwin()