from functions import winder
import time
import keyboard

Xwinder = winder()

Xwinder.parameter_calculation()

Xwinder.hoop()
Xwinder.helical()
Xwinder.hoop()
Xwinder.helical()

print('-------Winding Done!!!-------')
print('press t to start tape winding')
print('press esc to start tape winding')



def t():
    Xwinder.tape_winding()

def exit():
    Xwinder.close_connection()
    quit()

keyboard.add_hotkey('t', t)
keyboard.add_hotkey('esc', exit)

while True:
    mywait()



