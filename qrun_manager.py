# -*- coding: utf-8 -*-
"""
Created on Wed Aug 30 01:29:20 2017

@author: adm_cbrown
"""

# TODO Make default picture adorable Kieran pic
# TODO Make PEP 8 compliant :-)

import sys
import os
import glob as glob
import shutil
from qtpy import QtGui, QtWidgets, QtCore
import numpy as np
from scipy import signal
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.image as mplimage
from lclstools import logger, lineout, rotate_array


class LastImageCanvas(FigureCanvas):
    def __init__(self, parent):
        self.fig = Figure()
        self.axes = self.fig.add_subplot(111)
        self.title = "Nothing done yet!"
        self.currim = mplimage.imread(r"C:\Users\Public\Documents\Python\Testing\test.tiff")
        self.axes.imshow(self.currim)
        self.axes.set_title(self.title)
        FigureCanvas.__init__(self, self.fig)

        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.fig.tight_layout()
        
    def updateImage(self, newimage, title):
        #print newimage
        self.title = title
        self.currim = newimage
        self.fig.clf()
        self.axes = self.fig.add_subplot(111)
        self.axes.imshow(self.currim)
        self.axes.set_title(self.title)
        self.draw()


class LineoutCanvas(FigureCanvas):
    def __init__(self, parent):
        self.fig = Figure()
        self.axes = self.fig.add_subplot(111)
        t = np.arange(0.0, 3.0, 0.01)
        s = np.cos(2*np.pi*t)
        self.axes.plot(t, s)

        FigureCanvas.__init__(self, self.fig)

        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def updateLineout(self, lineout, title):
        self.fig.clf()
        self.axes = self.fig.add_subplot(111)
        self.axes.set_title(title)
        self.axes.plot(lineout)
        self.draw()

class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        QtWidgets.QMainWindow.setFixedSize(self,1400,800)
        self.setWindowTitle("QRun Manager")
        self.main_widget = QtWidgets.QWidget(self)
        self.runno = int(0)
        self.eventno = int(1)
        self.srcdir = "O:/"  # "C:/Users/Public/Documents/Python/Testing/"
        self.destdir = "C:/Users/Public/Documents/LCLS2017/"
        self.dest_path = r""
        self.autoalign = False
        self.draw_ui()
        self.initFileWatcher()

        self.main_widget.setFocus()
        self.setCentralWidget(self.main_widget)
        self.setRunno(1)
        self.numevents = 0
        self.lastimage = mplimage.imread(r"C:\Users\Public\Documents\Python\Testing\test.tiff")
        self.qmc2.updateImage(self.lastimage, "Nothing done yet!!!")

        self.xminbox.setRange(0, len(self.lastimage[0,:]) - 1)
        self.xmaxbox.setRange(0, len(self.lastimage[0,:]) - 1)
        self.yminbox.setRange(0, len(self.lastimage[:,0]) - 1)
        self.ymaxbox.setRange(0, len(self.lastimage[:,0]) - 1)

        self.xminbox.setValue(0)
        self.xmaxbox.setValue(len(self.lastimage[0,:]) - 1)
        self.yminbox.setValue(0)
        self.ymaxbox.setValue(len(self.lastimage[:,0]) - 1)

        self.updateLineout()
        self.filewatcher.blockSignals(True)

    def draw_ui(self):
        vbl = QtWidgets.QVBoxLayout(self.main_widget)
        self.qmc = LineoutCanvas(self.main_widget)
        self.qmc2 = LastImageCanvas(self.main_widget)
        ntb = NavigationToolbar(self.qmc, self.main_widget)
        ntb2 = NavigationToolbar(self.qmc2, self.main_widget)

        #Lineout controls
        self.xminbox = QtWidgets.QSpinBox(self.main_widget)
        self.xminbox.setRange(0,2195)
        self.xmaxbox = QtWidgets.QSpinBox(self.main_widget)
        self.xmaxbox.setRange(0,2)
        self.yminbox = QtWidgets.QSpinBox(self.main_widget)
        self.yminbox.setRange(0,2000)
        self.ymaxbox = QtWidgets.QSpinBox(self.main_widget)
        self.ymaxbox.setRange(0,2000)

        self.locumradio = QtWidgets.QRadioButton("Cumulative", self.main_widget)
        self.lolastshotradio = QtWidgets.QRadioButton("Last shot", self.main_widget, checked = True)
        self.autochk = QtWidgets.QCheckBox("Auto align", self.main_widget, checked = False)
        self.loupdatebutton = QtWidgets.QPushButton("Update", self.main_widget)
        
        lineouthbl = QtWidgets.QHBoxLayout(self.main_widget)
        lineouthbl.addWidget(QtWidgets.QLabel("X min:"))
        lineouthbl.addWidget(self.xminbox)
        lineouthbl.addWidget(QtWidgets.QLabel("X max:"))
        lineouthbl.addWidget(self.xmaxbox)
        lineouthbl.addWidget(QtWidgets.QLabel("Y min:"))
        lineouthbl.addWidget(self.yminbox)
        lineouthbl.addWidget(QtWidgets.QLabel("Y max:"))
        lineouthbl.addWidget(self.ymaxbox)
        lineouthbl.addWidget(self.locumradio)
        lineouthbl.addWidget(self.lolastshotradio)
        lineouthbl.addWidget(self.autochk)
        lineouthbl.addWidget(self.loupdatebutton)
        lineouthbl.addStretch(1)

#        self.xminbox.valueChanged.connect(self.updateLineout)
#        self.xmaxbox.valueChanged.connect(self.updateLineout)
#        self.yminbox.valueChanged.connect(self.updateLineout)
#        self.ymaxbox.valueChanged.connect(self.updateLineout)
        self.loupdatebutton.clicked.connect(self.updateLineout)
        self.lolastshotradio.toggled.connect(self.updateLineout)

        exbtn = QtWidgets.QPushButton("Exit", self.main_widget)
        exbtn.clicked.connect(self.btnExit)

        runlbl = QtWidgets.QLabel("Run No:", self.main_widget)
        eventlbl = QtWidgets.QLabel("Event No:", self.main_widget)
        self.runbox = QtWidgets.QSpinBox(self.main_widget)
        self.runbox.setRange(1,5000)
#        self.runbox = QtWidgets.QLineEdit(str(self.runno), self.main_widget)
#        self.runbox.textChanged.connect(self.setRunno)
        self.runbox.valueChanged.connect(self.setRunno)

#        runbutton = QtWidgets.QPushButton("Next run", self.main_widget)
#        runbutton.clicked.connect(self.incrRun)

        self.eventnum = QtWidgets.QLCDNumber(self.main_widget)
        self.eventnum.display(self.eventno)
        self.eventnum.setDigitCount(4)
        self.eventnum.setSegmentStyle(2)

        self.overrideeventbutton = QtWidgets.QPushButton("Manual event number...",self.main_widget)
        self.overrideeventbutton.clicked.connect(self.eventDialog)

        srclbl = QtWidgets.QLabel("Source Dir:", self.main_widget)
        self.srcbox = QtWidgets.QLineEdit(self.srcdir, self.main_widget)
        self.srcbox.textChanged.connect(self.changeWatch)

        srcbutton = QtWidgets.QPushButton("Browse...", self.main_widget)
        srcbutton.clicked.connect(self.btnSrc)


        destlbl = QtWidgets.QLabel("Destination Dir:", self.main_widget)
        self.destbox = QtWidgets.QLineEdit(self.destdir, self.main_widget)
        self.destbox.textChanged.connect(self.changeDest)

        destbutton = QtWidgets.QPushButton("Browse...", self.main_widget)
        destbutton.clicked.connect(self.btnDest)

        self.watch_chk = QtWidgets.QCheckBox("Watch enabled", self.main_widget, checked= False)
        self.watch_chk.stateChanged.connect(self.toggleWatch)
        self.watch_chk.setDisabled(True)
        self.startbutton = QtWidgets.QPushButton("Start Run", self.main_widget)
        self.startbutton.clicked.connect(self.startRun)

        self.stopbutton = QtWidgets.QPushButton("Stop Run", self.main_widget)
        self.stopbutton.clicked.connect(self.stopRun)
        self.stopbutton.setDisabled(True)
        runhbl = QtWidgets.QHBoxLayout()
        runhbl.addWidget(runlbl)
        runhbl.addWidget(self.runbox)
#        runhbl.addWidget(runbutton)
        runhbl.addWidget(self.startbutton)
        runhbl.addWidget(self.stopbutton)
        runhbl.addWidget(eventlbl)
        runhbl.addWidget(self.eventnum)
        runhbl.addWidget(self.overrideeventbutton)

        runhbl.addWidget(srclbl)
        runhbl.addWidget(self.srcbox, stretch =1)
        runhbl.addWidget(srcbutton)
        runhbl.addWidget(destlbl)
        runhbl.addWidget(self.destbox, stretch =1)
        runhbl.addWidget(destbutton)
        runhbl.addWidget(self.watch_chk)
        #runhbl.addStretch(1)
        plotshbl = QtWidgets.QHBoxLayout()
        plotshbl.addWidget(self.qmc)
        plotshbl.addWidget(self.qmc2)

        ntbhbl = QtWidgets.QHBoxLayout()
        ntbhbl.addWidget(ntb)
        ntbhbl.addWidget(ntb2)

        vbl.addWidget(QtWidgets.QLabel("QRunManager - 2017 CRDB"))
        vbl.addLayout(plotshbl)
        vbl.addLayout(lineouthbl)
        vbl.addLayout(ntbhbl)
        vbl.addLayout(runhbl)
        self.log = logger.Logger(self.main_widget)
        vbl.addWidget(self.log)
        vbl.addWidget(exbtn)

    def initFileWatcher(self):
        self.filewatcher = QtCore.QFileSystemWatcher(self.main_widget)
        self.filewatcher.addPath(self.srcdir)
        self.filewatcher.directoryChanged.connect(self.fileadded)

    def toggleWatch(self, e):
        self.filewatcher.blockSignals(not e)

    def changeWatch(self, e):
        self.filewatcher.removePaths(self.filewatcher.directories())
        self.filewatcher.addPath(e)

    def changeDest(self, e):
        self.destdir = e

    def btnExit(self):
        self.close()

    def btnSrc(self):
        dirname = QtWidgets.QFileDialog.getExistingDirectory(self, "Choose source directory")
        print dirname
        if dirname:
            self.srcbox.setText(dirname)

    def btnDest(self):
        dirname = QtWidgets.QFileDialog.getExistingDirectory(self, "Choose destination directory")
        print dirname
        if dirname:
            self.destbox.setText(dirname)

    def setEventno(self, e):
        self.eventno = e
        self.eventnum.display(self.eventno)

    def eventDialog(self):
        newnum = QtWidgets.QInputDialog.getInt(self, "Enter event number", "Manual event number:")
        print newnum
        if newnum[1]:
            self.setEventno(newnum[0])

    def setRunno(self, e):
        self.runno = int(e)
#        if os.path.exists(self.destdir+"/run"+str(self.runno)+"/"):
#            self.lbl.setText("Run number is: "+str(e)+"  ****WARNING RUN ALREADY EXISTS****")
#        else:
#            self.lbl.setText("Run number is: "+str(e))
       # self.setEventno(1)

#    def incrRun(self):
#        self.runbox.setText(str(self.runno +1))

    def startRun(self, e):
        self.log.disablechk.setChecked(True)

        if os.path.exists(self.destdir+"/run"+str(self.runno)+"/"):
            try: reply = QtWidgets.QMessageBox.question(self, "Warning",
                                                        "Run already exists. Do you want to overwrite?",
                                                        QtWidgets.QMessageBox.Yes | 
                                                        QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
            except TypeError as e:
                print "Error:", e
            if reply == QtWidgets.QMessageBox.Yes:
                reply2 = QtWidgets.QMessageBox.question(self, "Warning",
                                                        "Really sure?",
                                                        QtWidgets.QMessageBox.Yes | 
                                                        QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
                if reply2 == QtWidgets.QMessageBox.No:
                    return
            if reply == QtWidgets.QMessageBox.No:
                return
           # print "Path exists"
        self.stopbutton.setDisabled(False)
        self.startbutton.setDisabled(True)
        self.watch_chk.setChecked(True)
        self.log.writeEntry("Starting Run: {0}".format(self.runno))

    def stopRun(self):
        self.stopbutton.setDisabled(True)
        self.startbutton.setDisabled(False)
        self.watch_chk.setChecked(False)
        self.log.writeEntry("Stopping Run: {0}".format(self.runno))
        self.log.disablechk.setChecked(False)
        self.setEventno(1)
        self.runbox.setValue(self.runno + 1)

    def fileadded(self, e):
        self.newevent = True
        dirconts_new = filter(os.path.isfile, glob.glob(e+"/*"))
        dirconts_new.sort(key=lambda x: os.path.getctime(x))
        self.dest_path = self.destdir+"/run"+str(self.runno)+"/event_"+str(self.eventno)+".tiff"
        self.dest_path = os.path.normpath(self.dest_path)
        print self.dest_path
        if not os.path.exists(self.destdir+"/run"+str(self.runno)+"/"):
            os.mkdir(self.destdir+"/run"+str(self.runno)+"/")
        newfile = os.path.normpath(dirconts_new[-1])
        print newfile
        oscmd = 'copy "{0}" "{1}"'.format(newfile, self.dest_path)
        print oscmd
        try:
            #shutil.copyfile(newfile, self.dest_path)
            os.system(oscmd)
        except IOError as e:
            print "IOError {0} in copyfile: {1}".format(e.errno, e.strerror)
        self.log.writeEntry(dirconts_new[-1]+" copied to: "+self.dest_path)

        #Grab image for plotting and lineouts
        self.lastimage = mplimage.imread(self.dest_path)
        if self.numevents == 0:
            self.cummimage = self.lastimage
        else:
            self.cummimage = (self.cummimage*(self.numevents - 1) + self.lastimage) / self.numevents
        self.numevents = self.numevents + 1
        self.setEventno(self.eventno + 1)
        self.updatePlots()
        self.newevent = False
    def updatePlots(self):


        self.xminbox.setRange(0, len(self.lastimage[0,:]) - 1)
        self.xmaxbox.setRange(0, len(self.lastimage[0,:]) - 1)
        self.yminbox.setRange(0, len(self.lastimage[:,0]) - 1)
        self.ymaxbox.setRange(0, len(self.lastimage[:,0]) - 1)
        self.qmc2.updateImage(self.lastimage, self.dest_path)
        self.updateLineout()

    def updateLineout(self):
        #self.loupdatebutton.setDisabled(True)
        xmin = self.xminbox.value()
        xmax = self.xmaxbox.value()
        ymin = self.yminbox.value()
        ymax = self.ymaxbox.value()
        #print xmin, xmax, ymin, ymax
        if self.lolastshotradio.isChecked() == True:
            try:
                lo = lineout(self.lastimage, xmin, xmax, ymin, ymax, "x")
                

               # self.qmc.updateLineout(lo[100:1900], self.dest_path)
                self.qmc.updateLineout(lo, self.dest_path)
            except AttributeError as e:
                print e
                
                error_dialog = QtWidgets.QErrorMessage()
                try: 
                    error_dialog.showMessage(str(e))
                except TypeError as e:
                    print "Error", e
                return
                
            #self.qmc.updateLineout(lo, self.dest_path)
        elif self.numevents > 0:
            cummlo = lineout(self.cummimage, xmin, xmax, ymin, ymax, "x")
            self.qmc.updateLineout(cummlo, "Accumulation of {0} events".format(self.numevents))
        
        lastlo = lineout(self.lastimage, xmin, xmax, ymin, ymax, "x")
        # TODO: Test some smooth action
            
        gauss = signal.gaussian(100, 5)
        smoolo = signal.convolve(lastlo, gauss, mode = "same")/sum(gauss)
        minlo = smoolo[100:-100].min()
        maxlo = smoolo[100:-100].max()
        halfval = (maxlo + minlo)*0.5
        #print minlo, maxlo
        #print halfval
        halfcross = np.where(smoolo > halfval)[0]
        #print halfcross[0]
        rotlo = rotate_array(lastlo, halfcross[0] - 500)
        
        if self.numevents < 2:
            self.aligncummlo = rotlo
        elif self.newevent == True:
            print "New event"
            self.aligncummlo = (self.aligncummlo*(self.numevents -1 ) + rotlo) / self.numevents
        if self.autochk.isChecked() == True and self.locumradio.isChecked() == True:
            self.qmc.updateLineout(self.aligncummlo, "Aligned accumulation of {0} events".format(self.numevents))
        elif self.autochk.isChecked() == True and self.locumradio.isChecked() == False:
            self.qmc.updateLineout(rotlo, "Aligned last shot".format(self.numevents))
        #self.loupdatebutton.setDisabled(False)  
        
    def closeEvent(self, event):
        
        reply = QtWidgets.QMessageBox.question(self, 'Message',
            "Are you sure to quit?", QtWidgets.QMessageBox.Yes | 
            QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)

        if reply == QtWidgets.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()        
if __name__ == "__main__":

    qApp = QtWidgets.QApplication(sys.argv)

    aw = ApplicationWindow()

    aw.show()

    sys.exit(qApp.exec_())