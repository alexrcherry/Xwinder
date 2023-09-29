from PyQt5 import QtWidgets, uic
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtGui import QKeySequence
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QShortcut
import pickle

from functions import winder

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__() # Call the inherited classes __init__ method
        uic.loadUi('WindingSoftware.ui', self) # Load the .ui file
        self.show() # Show the GUI

        #connect and disconnect USB devices
        self.pushButton_Connect.clicked.connect(self.ConnectFunc)
        self.pushButton_Disconnect.clicked.connect(self.DisconnectFunc)

        ## update winding parameters when values change
        #Run Tab
        self.doubleSpinBox_Radius.valueChanged.connect(self.CalcValureChangedFunc)
        self.doubleSpinBox_Length.valueChanged.connect(self.CalcValureChangedFunc)
        self.doubleSpinBox_Alpha.valueChanged.connect(self.CalcValureChangedFunc)
        #Parameters Tab
        self.doubleSpinBox_FiberWidthHoop.valueChanged.connect(self.CalcValureChangedFunc)
        self.doubleSpinBox_FiberWidthHelical.valueChanged.connect(self.CalcValureChangedFunc)
        self.doubleSpinBox_LinearVelocityHoop.valueChanged.connect(self.CalcValureChangedFunc)
        self.doubleSpinBox_LinearVelocityHelical.valueChanged.connect(self.CalcValureChangedFunc)

        #add layers to stackup
        self.pushButton_Hoop.clicked.connect(self.HoopFunc)
        self.pushButton_Helical.clicked.connect(self.HelicalFunc)

        #start/stop resume/pause/tape
        self.pushButton_Start.clicked.connect(self.StartFunc)
        self.pushButton_Stop.clicked.connect(self.StopFunc)
        self.pushButton_Pause.clicked.connect(self.StopFunc)
        self.pushButton_Resume.clicked.connect(self.ResumeFunc)
        self.pushButton_tapeWinding.clicked.connect(self.TapeWinding
                                                    )
        ##calibration tab
        #move 100 degs
        self.pushButton_100degs.clicked.connect(self.Mv100degs)
        #reset total
        self.pushButton_ResetTotal.clicked.connect(self.ResetTotal)
        #change motor direction
        self.checkBox_Mandrel_Dir.stateChanged.connect(self.ReverseMandrel)
        self.checkBox_Carriage_Dir.stateChanged.connect(self.ReverseCarriage)
        self.checkBox_Head_Dir.stateChanged.connect(self.ReverseHead)


        #disable buttons that require USB connection
        enabled = False
        self.pushButton_Disconnect.setEnabled(enabled)
        self.pushButton_Start.setEnabled(enabled)
        self.pushButton_Stop.setEnabled(enabled)
        self.pushButton_Pause.setEnabled(enabled)
        self.pushButton_Resume.setEnabled(enabled)
        self.pushButton_MandrelP.setEnabled(enabled)
        self.pushButton_MandrelN.setEnabled(enabled)
        self.pushButton_CarriageP.setEnabled(enabled)
        self.pushButton_CarriageN.setEnabled(enabled)
        self.pushButton_HeadP.setEnabled(enabled)
        self.pushButton_HeadN.setEnabled(enabled)
        self.pushButton_100degs.setEnabled(enabled)

        ##Jogging
        #mandrel
        self.pushButton_MandrelP.clicked.connect(self.MandrelPFunc)
        self.pushButton_MandrelN.clicked.connect(self.MandrelNFunc)
        # carriage
        self.pushButton_CarriageP.clicked.connect(self.CarriagePFunc)
        self.pushButton_CarriageN.clicked.connect(self.CarriageNFunc)
        #head
        self.pushButton_HeadP.clicked.connect(self.HeadPFunc)
        self.pushButton_HeadN.clicked.connect(self.HeadNFunc)


        #starts in not running state
        self.running = False

        # #creates winder object and runs initial parameter calculation
        # self.Xwinder = winder()
        # self.Xwinder.parameter_calculation()
        #load winder object
        with open(f'test.pickle', 'rb') as file:
            self.Xwinder = pickle.load(file)

        #Zero calibration moved distance
        self.Xwinder.Mv100degs = 0
        self.label_DegsMoved.setText(str(self.Xwinder.Mv100degs))
        # #load rescale factors
        self.doubleSpinBox_RF_Mandrel.setValue(self.Xwinder.RF_Mandrel)
        self.doubleSpinBox_RF_Carriage.setValue(self.Xwinder.RF_Carriage)
        self.doubleSpinBox_RF_Head.setValue(self.Xwinder.RF_Head)

        #change in dist moved or rescale factor
        self.doubleSpinBox_DM_Mandrel.valueChanged.connect(self.DM_changed)
        self.doubleSpinBox_DM_Carriage.valueChanged.connect(self.DM_changed)
        self.doubleSpinBox_DM_Head.valueChanged.connect(self.DM_changed)

        self.doubleSpinBox_RF_Mandrel.valueChanged.connect(self.RF_changed)
        self.doubleSpinBox_RF_Carriage.valueChanged.connect(self.RF_changed)
        self.doubleSpinBox_RF_Head.valueChanged.connect(self.RF_changed)

        #set up shortcut to enable using the Del key to delete items in the list of layers
        shortcut = QKeySequence('Del')
        self.shortcut = QShortcut(shortcut, self)
        self.shortcut.activated.connect(self.deleteRow)


    def ConnectFunc(self):
        try:
            self.Xwinder.connect(
                 mandrel_SN=615813, mandrel_factor=self.Xwinder.RF_Mandrel,
                 carriage_SN=615519, carriage_factor=self.Xwinder.RF_Carriage,
                 head_SN=616004, head_factor=self.Xwinder.RF_Head)
        except:
            raise Exception('Could not connect to all USB devices')
        #enable buttons that require USB connection
        enabled = True
        self.pushButton_Disconnect.setEnabled(enabled)
        self.pushButton_Start.setEnabled(enabled)
        self.pushButton_Stop.setEnabled(enabled)
        self.pushButton_Pause.setEnabled(enabled)
        self.pushButton_Resume.setEnabled(enabled)
        self.pushButton_MandrelP.setEnabled(enabled)
        self.pushButton_MandrelN.setEnabled(enabled)
        self.pushButton_CarriageP.setEnabled(enabled)
        self.pushButton_CarriageN.setEnabled(enabled)
        self.pushButton_HeadP.setEnabled(enabled)
        self.pushButton_HeadN.setEnabled(enabled)
        self.pushButton_100degs.setEnabled(enabled)


    def DisconnectFunc(self):
        self.Xwinder.close_connection()


    def CalcValureChangedFunc(self):
        self.Xwinder.parameter_calculation(
                              alpha_desired = self.doubleSpinBox_Alpha.value(),
                              radius = self.doubleSpinBox_Radius.value(),
                              fiber_thickness_hoop = self.doubleSpinBox_FiberWidthHoop.value(),
                              linear_velocity_hoop = .8,
                              travel_distance = self.doubleSpinBox_Length.value(),
                              fiber_thickness_helical = self.doubleSpinBox_FiberWidthHelical.value(),
                              linear_velocity_helical = .02
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
        layer_list = [self.listWidget.item(x).text() for x in range(self.listWidget.count())]
        layer_list.reverse()

        print('Winding Started')

        for layer in layer_list:
            print('Starting Layer Type:', layer)
            if layer == 'Hoop':
                self.Xwinder.hoop()
            elif layer == 'Helical':
                self.Xwinder.helical()

        print('Winding Ended')


    def StopFunc(self):
        print('stop')
        self.Xwinder.disengage_motors()


    def ResumeFunc(self):
        print('stop')
        self.Xwinder.engage_motors()


    def TapeWinding(self):
        self.Xwinder.tape_winding()


    def MandrelPFunc(self):
        print(self.Xwinder.RF_Mandrel)
        dist = self.Xwinder.mandrel.getPosition()
        print(dist)
        self.Xwinder.mandrel.setTargetPosition(dist+90)
        self.Xwinder.mandrel.setEngaged(True)
    def MandrelNFunc(self):
        self.Xwinder.mandrel.setTargetPosition(self.Xwinder.mandrel.getPosition()-90)
        self.Xwinder.mandrel.setEngaged(True)

    def CarriagePFunc(self):
        print('carriage P')
        self.Xwinder.carriage.setTargetPosition(self.Xwinder.carriage.getPosition()+1)
        self.Xwinder.carriage.setEngaged(True)
    def CarriageNFunc(self):
        self.Xwinder.carriage.setTargetPosition(self.Xwinder.carriage.getPosition()-1)
        self.Xwinder.carriage.setEngaged(True)

    def HeadPFunc(self):
        self.Xwinder.head.setTargetPosition(self.Xwinder.head.getPosition()+90)
        self.Xwinder.head.setEngaged(True)
    def HeadNFunc(self):
        self.Xwinder.head.setTargetPosition(self.Xwinder.head.getPosition()-90)
        self.Xwinder.head.setEngaged(True)

    def Mv100degs(self):

        if self.checkBox_Mandrel.isChecked():
            self.Xwinder.carriage.setRescaleFactor(.1125)
            self.Xwinder.mandrel.setTargetPosition(self.Xwinder.mandrel.getPosition()+100)
            self.Xwinder.Mv100degs += 100
            self.label_DegsMoved.setText(str(self.Xwinder.Mv100degs))

        elif self.checkBox_Carriage.isChecked():
            self.Xwinder.carriage.setRescaleFactor(.1125)
            self.Xwinder.carriage.setTargetPosition(self.Xwinder.carriage.getPosition()+100)
            self.Xwinder.Mv100degs += 100
            self.label_DegsMoved.setText(str(self.Xwinder.Mv100degs))

        elif self.checkBox_Head.isChecked():
            self.Xwinder.head.setRescaleFactor(.1125)
            self.Xwinder.head.setTargetPosition(self.Xwinder.head.getPosition()+100)
            self.Xwinder.Mv100degs += 100
            self.label_DegsMoved.setText(str(self.Xwinder.Mv100degs))

    def DM_changed(self):
        #calculate the rescale factor one the use enters a distance moved then reset the total moved distance
        if self.doubleSpinBox_DM_Mandrel.value() != 0:

            self.Xwinder.RF_Mandrel = .1125*(self.doubleSpinBox_DM_Mandrel.value()/self.Xwinder.Mv100degs)
            self.doubleSpinBox_RF_Mandrel.setValue(self.Xwinder.RF_Mandrel)
            self.Xwinder.mandrel.setRescaleFactor(self.Xwinder.RF_Mandrel)

        if self.doubleSpinBox_DM_Carriage.value() != 0:
            self.Xwinder.RF_Carriage = .1125*(self.doubleSpinBox_DM_Carriage.value()/self.Xwinder.Mv100degs)
            self.doubleSpinBox_RF_Carriage.setValue(self.Xwinder.RF_Carriage)
            self.Xwinder.carriage.setRescaleFactor(self.Xwinder.RF_Carriage)


        if self.doubleSpinBox_DM_Head.value() != 0:
            self.Xwinder.RF_Head = .1125*(self.doubleSpinBox_DM_Head.value()/self.Xwinder.Mv100degs)
            self.doubleSpinBox_RF_Head.setValue(self.Xwinder.RF_Head)
            self.Xwinder.head.setRescaleFactor(self.Xwinder.RF_Head)


    def RF_changed(self):
        #set rescale factors if they are entered by the user
        print('rf changed')
        if self.doubleSpinBox_RF_Mandrel.value() != 0:
            self.Xwinder.RF_Mandrel = self.doubleSpinBox_RF_Mandrel.value()
            self.Xwinder.mandrel.setRescaleFactor(self.Xwinder.RF_Mandrel)

        if self.doubleSpinBox_RF_Carriage.value() != 0:
            self.Xwinder.RF_Carriage = self.doubleSpinBox_RF_Carriage.value()
            self.Xwinder.carriage.setRescaleFactor(self.Xwinder.RF_Carriage)

        if self.doubleSpinBox_RF_Head.value() != 0:
            self.Xwinder.RF_Head = self.doubleSpinBox_RF_Head.value()
            self.Xwinder.head.setRescaleFactor(self.Xwinder.RF_Head)

    def ResetTotal(self):
        self.Xwinder.Mv100degs = 0
        self.label_DegsMoved.setText('0')

    def ReverseMandrel(self):
        self.Xwinder.RF_Mandrel =self.Xwinder.RF_Mandrel * -1
        self.doubleSpinBox_RF_Mandrel.setValue(self.Xwinder.RF_Mandrel)
        self.Xwinder.mandrel.setRescaleFactor(self.Xwinder.RF_Mandrel)


    def ReverseCarriage(self):
        self.Xwinder.RF_Carriage *= -1
        self.doubleSpinBox_RF_Carriage.setValue(self.Xwinder.RF_Carriage)
        self.Xwinder.carriage.setRescaleFactor(self.Xwinder.RF_Carriage)

    def ReverseHead(self):
        self.Xwinder.RF_Head *= -1
        self.doubleSpinBox_RF_Head.setValue(self.Xwinder.RF_Head)
        self.Xwinder.head.setRescaleFactor(self.Xwinder.RF_Head)


    def closeEvent(self, event):
        self.Xwinder.mandrel = None
        self.Xwinder.carriage = None
        self.Xwinder.head = None

        with open(f'test.pickle', 'wb') as file:
            pickle.dump(self.Xwinder, file)



app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()
