# from functions import winder
# import time
# import keyboard

# Xwinder = winder()

# Xwinder.parameter_calculation()

# Xwinder.hoop()
# Xwinder.helical()
# Xwinder.hoop()
# Xwinder.helical()

# print('-------Winding Done!!!-------')
# print('press t to start tape winding')
# print('press esc to start tape winding')



# def t():
#     Xwinder.tape_winding()

# def exit():
#     Xwinder.close_connection()
#     quit()

# keyboard.add_hotkey('t', t)
# keyboard.add_hotkey('esc', exit)

# while True:
#     mywait()



from PyQt5 import QtWidgets, uic
import sys

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__() # Call the inherited classes __init__ method
        uic.loadUi('WindingSoftware.ui', self) # Load the .ui file
        self.show() # Show the GUI


app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()
