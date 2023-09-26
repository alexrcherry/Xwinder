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
from functions import winder


from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtGui import QKeySequence
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QShortcut

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__() # Call the inherited classes __init__ method
        uic.loadUi('WindingSoftware.ui', self) # Load the .ui file
        self.show() # Show the GUI

        self.pushButton_Connect.clicked.connect(self.ConnectFunc)
        self.pushButton_Disconnect.clicked.connect(self.DisconnectFunc)
        self.doubleSpinBox_Radius.valueChanged.connect(self.RadiusChangedFunc)
        self.doubleSpinBox_Length.valueChanged.connect(self.LengthChangedFunc)
        self.pushButton_Hoop.clicked.connect(self.HoopFunc)
        self.pushButton_Helical.clicked.connect(self.HelicalFunc)
        self.pushButton_Start.clicked.connect(self.StartFunc)
        self.pushButton_Stop.clicked.connect(self.StopFunc)
        self.pushButton_Pause.clicked.connect(self.StopFunc)
        self.pushButton_Resume.clicked.connect(self.ResumeFunc)

        self.running = False

        self.Xwinder = winder()
        self.Xwinder.parameter_calculation()

        #set up shortcut to enable using the Del key to delete items in the list of layers
        shortcut = QKeySequence('Del')
        self.shortcut = QShortcut(shortcut, self)
        self.shortcut.activated.connect(self.deleteRow)
        print('init')


    def ConnectFunc(self):
        self.Xwinder.connect()


    def DisconnectFunc(self):
        self.Xwinder.close_connection()


    def RadiusChangedFunc(self):
        self.Xwinder.parameter_calculation(
                              alpha_desired = 55,
                              radius = self.doubleSpinBox_Radius.value(),
                              fiber_thickness_hoop = .152,
                              linear_velocity_hoop = .2,
                              travel_distance = self.doubleSpinBox_Length.value(),
                              fiber_thickenss_helical = .16,
                              linear_velocity_helical=1.6
                              )


    def LengthChangedFunc(self):
        self.Xwinder.parameter_calculation(
                              alpha_desired = 55,
                              radius = self.doubleSpinBox_Radius.value(),
                              fiber_thickness_hoop = .152,
                              linear_velocity_hoop = .2,
                              travel_distance = self.doubleSpinBox_Length.value(),
                              fiber_thickenss_helical = .16,
                              linear_velocity_helical=1.6
                              )


    def HoopFunc(self):
        self.listWidget.insertItem(0, 'Hoop')


    def HelicalFunc(self):
        self.listWidget.insertItem(0, 'Helical')


    def deleteRow(self):
        current_row = self.listWidget.currentRow()
        if current_row != -1:
            item = self.listWidget.takeItem(current_row)
            item = None


    def StartFunc(self):
        print('start')
        layer_list = [self.listWidget.item(x).text() for x in range(self.listWidget.count())]
        layer_list.reverse()

        print(layer_list)
        for layer in layer_list:
            if layer == 'Hoop':
                print('hoop')
                self.Xwinder.hoop()
            elif layer == 'Helical':
                print('helical')
                self.Xwinder.helical()


    def StopFunc(self):
        print('stop')
        self.Xwinder.disengage_motors()


    def ResumeFunc(self):
        print('stop')
        self.Xwinder.engage_motors()


app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()
