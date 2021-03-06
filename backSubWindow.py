# -*- coding: utf-8 -*-
"""
Created on Mon Jul 17 11:37:17 2017

@author: Tanner
"""

import sys
from PyQt5.QtCore import QCoreApplication, Qt
from PyQt5.QtGui import QIcon, QColor
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QAction, QMessageBox
from PyQt5.QtWidgets import QCalendarWidget, QFontDialog, QColorDialog, QTextEdit, QFileDialog
from PyQt5.QtWidgets import QCheckBox, QProgressBar, QComboBox, QLabel, QStyleFactory, QLineEdit, QInputDialog
import backgroundSubtract


class window(QMainWindow):

    def __init__(self):
        super(window, self).__init__()
        self.setGeometry(50, 50, 300, 200)
        self.setWindowTitle('Python Background Subtractor v2.2')
        #self.setWindowIcon(QIcon('pic.png'))

        extractAction = QAction('&Close', self)
        extractAction.setShortcut('Ctrl+Q')
        extractAction.setStatusTip('leave the app')
        extractAction.triggered.connect(self.close_application)



        openFile = QAction('&Open File', self)
        openFile.setShortcut('Ctrl+O')
        openFile.setStatusTip('Open File')
        openFile.triggered.connect(self.file_open)
        

        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('&File')
        fileMenu.addAction(extractAction)

        fileMenu.addAction(openFile)



        self.home()


# name object here stores the filepath, important for connecting to backSub
    def file_open(self):

        self.name, _ = QFileDialog.getOpenFileName(self, 'Open File', options=QFileDialog.DontUseNativeDialog)
        


    def run_analysis(self):
        
        self.save_loc, _ = QFileDialog.getSaveFileName(self, "Excel Files (*.xlsx *.xls)",filter='Excel Files (*.xlsx)', options=QFileDialog.DontUseNativeDialog)
        print('analyzing file at' + self.name)
        print(self.selection[0])
        print(self.selection2[0])
        backgroundSubtract.load(self.name)
        backgroundSubtract.backSub(self.name, self.selection, self.selection2, self.save_loc)
        



    def home(self):
        btn = QPushButton('Quit', self)
        btn.clicked.connect(self.close_application)
        btn.resize(btn.sizeHint())
        btn.move(10, 80)
        
        btn2 = QPushButton('Open File', self)
        btn2.clicked.connect(self.file_open)
        btn2.resize(btn2.sizeHint())
        btn2.move(10,50)
        
        btn3 = QPushButton('Run Analysis', self)
        btn3.clicked.connect(self.run_analysis)
        btn3.resize(btn3.sizeHint())
        btn3.move(10, 110)
        

        textbox = QLabel(self)
        textbox.move(5, 10)
        textbox.resize(280, 40)
        textbox.setText('Please Select a File to Analyze.')
        

        checkBox = QCheckBox('Channel1', self)
        checkBox2 = QCheckBox('Channel2', self)
        checkBox3 = QCheckBox('Channel3', self)
        checkBox4 = QCheckBox('Channel4', self)
        
        checkChannel = QCheckBox('1 Channel', self)
        checkChannel2 = QCheckBox('2 Channels', self)
        checkChannel3 = QCheckBox('3 Channels', self)
        checkChannel4 = QCheckBox('4 Channels', self)
        
        # checkBox.toggle()  # if you want to be checked in in the begin
        checkChannel.move(200, 50)
        checkChannel2.move(200, 80)
        checkChannel3.move(200, 110)
        checkChannel4.move(200, 140)
        
        checkBox.move(100, 50)
        checkBox2.move(100, 80)
        checkBox3.move(100, 110)
        checkBox4.move(100, 140)
        
        checkBox.stateChanged.connect(self.checked_status1)
        checkBox2.stateChanged.connect(self.checked_status2)
        checkBox3.stateChanged.connect(self.checked_status3)
        checkBox4.stateChanged.connect(self.checked_status4)
        
        checkChannel.stateChanged.connect(self.checked_status5)
        checkChannel2.stateChanged.connect(self.checked_status6)
        checkChannel3.stateChanged.connect(self.checked_status7)
        checkChannel4.stateChanged.connect(self.checked_status8)

        self.show()

# Coded each checkbox separately, each chekced_status reports the current status of the box 
# each "selection" variable stores the number of channels compared and number of channels total, respectively 
        
        self.selection = []
        self.selection2 = []
        
    def checked_status1(self, state):
        if state == Qt.Checked:
            print('Channel 1 Selected')
            self.selection.append(1)
        else:
            self.selection.remove(1)
            print('Channel 1 Unchecked')
            
    def checked_status2(self, state):
        if state == Qt.Checked:
            print('Channel 2 Selected')
            self.selection.append(2)
        else:
            self.selection.remove(2)
            print('Channel 2 Unchecked')
            
    def checked_status3(self, state):
        if state == Qt.Checked:
            print('Channel 3 Selected')
            self.selection.append(3)           
        else:
            self.selection.remove(3)
            print('Channel 3 Unchecked')

   
    def checked_status4(self, state):
        if state == Qt.Checked:
            print('Channel 4 Selected')
            self.selection.append(4)
        else:
            self.selection.remove(4)
            print('Channel 4 Unchecked')

# begin section for num_channels output (tells program how many channels )   
    def checked_status5(self, state):
        if state == Qt.Checked:
            print('1 Channel present')
            self.selection2.append(1)
        else:
            self.selection2.remove(1)
            print('')
            
    def checked_status6(self, state):
        if state == Qt.Checked:
            print('2 Channel present')
            self.selection2.append(2)
        else:
            self.selection2.remove(2)
            print('')
            
    def checked_status7(self, state):
        if state == Qt.Checked:
            print('3 Channels present')
            self.selection2.append(3)           
        else:
            self.selection2.remove(3)
            print('')
            
    def checked_status8(self, state):
        if state == Qt.Checked:
            print('4 Channels present')
            self.selection2.append(4)
        else:
            self.selection2.remove(4)
            print('')
            

    def close_application(self):

        choice = QMessageBox.question(self, 'Message',
                                     "Are you sure to quit?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)

        if choice == QMessageBox.Yes:
            print('quit application')
            sys.exit()
        else:
            pass
        
        
def run():
    app = QApplication(sys.argv)
    Gui = window()
    sys.exit(app.exec_())

if __name__ == '__main__':
    
    print("Starting...")
    
    run()
    
    
    print("Done")



