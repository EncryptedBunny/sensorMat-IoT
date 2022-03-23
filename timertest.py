import threading
import keyboard  # using module keyboard

reset_time = 5.0

def reset_mat():
    print("reset")
    set_timer()

def set_timer():
    global timer

    timer = threading.Timer(reset_time, reset_mat)
    timer.start()

def reset_timer():
    
    global timer

    timer.cancel()
    timer = threading.Timer(reset_time, reset_mat)
    timer.start()


set_timer()


while True:  # making a loop

    try:  # used try so that if user pressed other than the given key error will not be shown
        if keyboard.is_pressed('q'):  # if key 'q' is pressed 
            reset_timer()
    except:
        break 