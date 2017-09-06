# -*- coding: utf-8 -*-
"""
Created on Thu Aug 31 13:20:09 2017

@author: adm_cbrown
"""
import sys
import os
from qtpy import QtGui, QtWidgets, QtCore

class Logger(QtWidgets.QWidget):
    """Class to provide text file logger widget.
    """
    def __init__(self, parent):
        QtWidgets.QWidget.__init__(self)
        self.setParent(parent)
        self.srcFile = r"C:\Users\Public\Documents\LCLS2017\manager_log.txt"
        self.text = ""
        QtWidgets.QWidget.setSizePolicy(self,
                                        QtWidgets.QSizePolicy.Expanding,
                                        QtWidgets.QSizePolicy.Expanding)
        self.drawUI()
        self.implementUI()
        self.loadTxt()

    def drawUI(self):
        vbox = QtWidgets.QVBoxLayout(self)
        self.setLayout(vbox)
        self.textbox = QtWidgets.QTextEdit(self)
        self.textbox.setReadOnly(True)

        ctrlbox = QtWidgets.QHBoxLayout(self)
        srclbl = QtWidgets.QLabel("Source: ", self)
        self.srcbox = QtWidgets.QLineEdit(self.srcFile, self)
        self.browsebtn = QtWidgets.QPushButton("Browse...", self)
        self.reloadbtn = QtWidgets.QPushButton("Reload", self)
        self.commentbtn = QtWidgets.QPushButton("Add Comment...", self)
        self.newbtn = QtWidgets.QPushButton("New File...", self)
        self.disablechk = QtWidgets.QCheckBox("Disable Inputs", self,
                                              checked=False)
        ctrlbox.addWidget(srclbl)
        ctrlbox.addWidget(self.srcbox, stretch=1)
        ctrlbox.addWidget(self.browsebtn)
        ctrlbox.addWidget(self.reloadbtn)
        ctrlbox.addWidget(self.commentbtn)
        ctrlbox.addWidget(self.newbtn)
        ctrlbox.addWidget(self.disablechk)
        vbox.addWidget(QtWidgets.QLabel("Logger - 2017 CRDB"))
        vbox.addLayout(ctrlbox)
        vbox.addWidget(self.textbox)

    def implementUI(self):
        self.srcbox.textChanged.connect(self.changeSrc)
        self.browsebtn.clicked.connect(self.browsePress)
        self.reloadbtn.clicked.connect(self.reloadPress)
        self.commentbtn.clicked.connect(self.commentPress)
        self.newbtn.clicked.connect(self.newPress)
        self.disablechk.stateChanged.connect(self.disableInput)

    def loadTxt(self):
        self.text = open(self.srcFile, 'r').read()
        self.textbox.setText(self.text)
        self.textbox.moveCursor(QtGui.QTextCursor.End)

    def writeEntry(self, entry):
        now = QtCore.QDateTime.currentDateTime()
        stampedentry = str(now.toString(format=QtCore.Qt.ISODate))+": "+entry +"\n"
        textFile = open(self.srcFile, "a")
        textFile.write(stampedentry)
        textFile.close()
        self.loadTxt()

    def changeSrc(self, newsrc):
        self.srcFile = newsrc
        self.reloadbtn.setDisabled(True)
        self.commentbtn.setDisabled(True)
        if os.path.exists(self.srcFile):
            self.reloadbtn.setDisabled(False)
            self.commentbtn.setDisabled(False)
            self.loadTxt()

    def browsePress(self):
        pathname = QtWidgets.QFileDialog.getOpenFileName(self, "Choose Source File")
        print pathname[0]
        if pathname:
            self.srcbox.setText(pathname[0])

    def reloadPress(self):
        if os.path.exists(self.srcFile):
            self.loadTxt()
        else:
            pass #QtWidgets.QMessageBox(self, "Warning", "File does not exist")

    def commentPress(self):
        text, ok = QtWidgets.QInputDialog.getText(self, "Input Comment", "Comment to log:")
        if ok:
            self.writeEntry(text)

    def newPress(self):
        #QtWidgets.QFileDialog.getSaveFileName
        pathname = QtWidgets.QFileDialog.getSaveFileName(self, "Create New Log")
        print pathname
        if pathname[0] != u'':
            textFile = open(pathname[0], "w")
            textFile.close()
            self.srcbox.setText(pathname[0])
            self.writeEntry("New log started")

    def disableInput(self, e):
        self.reloadbtn.setDisabled(e)
        self.commentbtn.setDisabled(e)
        self.newbtn.setDisabled(e)
        self.browsebtn.setDisabled(e)
        self.srcbox.setDisabled(e)

if __name__ == "__main__":
    qApp = QtWidgets.QApplication(sys.argv)
    lgr = Logger(None)
    lgr.show()
    sys.exit(qApp.exec_())
