#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Md5 hash generator tools

author: Alexander Fedorov
"""

import sys
from PyQt4.QtGui import *
#from PyQt4.QtCore import *


class AppWindow(QMainWindow):
    
    def __init__(self):
        super(AppWindow, self).__init__()
        self.initUI()
        self.HashFilePath = '/home/alexander/EFI/Hash.dat'
        self.hashes = []
        self.readHashFile()
        
    def initUI(self):      

        self.filesViewer = QTableWidget()
        self.filesViewer.setColumnCount(2)
        self.filesViewer.setRowCount(2)
        self.filesViewer.setHorizontalHeaderLabels(['Path', 'Hash'])
        self.filesViewer.verticalHeader().hide()
        self.filesViewer.horizontalHeader().setStretchLastSection(True)
        self.setCentralWidget(self.filesViewer)

        statusbar = self.statusBar()
        statusbar.showMessage('Status bar')

        openFile = QAction(QIcon('open.png'), 'Open', self)
        openFile.setShortcut('Ctrl+O')
        openFile.setStatusTip('Open new File')
        openFile.triggered.connect(self.showDialog)

        updateHash = QAction(QIcon('update.png'), 'Update', self)
        updateHash.setShortcut('F5')
        updateHash.setStatusTip('Update hash file')
        updateHash.triggered.connect(self.updateHashFile)

        toolbar = self.addToolBar('Tools')
        toolbar.addAction(openFile)       
        toolbar.addAction(updateHash)
        
        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle('File dialog')
        self.show()
    
    def readHashFile(self):
        count = 0
        for line in open(self.HashFilePath).readlines():
            params = line.split(':')
            self.hashes.insert(count, params)
            count += 1

        self.filesViewer.setRowCount(count)
        count = 0
        for params in self.hashes:
            print (params)
            self.filesViewer.setItem(count, 0, QTableWidgetItem(params[0])) 
            self.filesViewer.setItem(count, 1, QTableWidgetItem(params[1])) 
            count += 1


    def updateHashFile(self):
        self.statusBar().showMessage('Update manual')
        
    def showDialog(self):

        fname = QFileDialog.getOpenFileName(self, 'Open file', 
                '/home')
       
        #f = open(fname, 'r')
        
        #with f:        
        #    data = f.read()
        #    self.textEdit.setText(data) 
                                
        
def main():
    
    app = QApplication(sys.argv)
    ex = AppWindow()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
