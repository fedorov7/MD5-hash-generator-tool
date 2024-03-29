#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Md5 hash generator tools

author: Alexander Fedorov
"""

import sys
import md5
from PyQt4.QtGui import *

class HashFile:
    def __init__(self, path = None):
        self.filePath = path 
        self.Clean()

    def Read(self):
        self.Clean()
        for line in open(self.filePath).readlines():
            #print ('Read line:{0}'.format(line))
            params = line.split(':')
            if (len(params) is 2):
                params[0] = params[0].replace('/', '\\')
                params[1] = params[1].replace('\n', '')
                self.files.append(params)
            
    def Write(self):    
        f = open(self.filePath, 'w')
        for params in self.files:
            if (len(params) is 2):
                line = '{0}:{1}\n'.format(params[0], params[1])
                #print ('Write line:{0}'.format(line))
                f.write(line)
        f.close()

    def Clean(self):
        self.files = []

    def Insert(self, params):
        self.files.append(params)
        self.files.sort()

    def Remove(self, index):
        self.files.remove(self.files[index])

    def Length(self):  
        return len(self.files)

    def SetPath(self, path):
        self.filePath = path

    def Open(self, path):
        self.SetPath(path)
        self.Read()
        

class AppWindow(QMainWindow):
    
    def __init__(self):
        super(AppWindow, self).__init__()
        self.initUI()
        self.Hashes = HashFile() #'/home/alexander/EFI/Hash.dat'
        #self.ReadHashes()
        
    def initUI(self):      
        self.filesViewer = QTableWidget()
        self.filesViewer.setColumnCount(2)
        self.filesViewer.setColumnWidth(0, 350)
        self.filesViewer.setHorizontalHeaderLabels(['Path', 'Hash'])
        self.filesViewer.verticalHeader().hide()
        self.filesViewer.horizontalHeader().setStretchLastSection(True)
        self.setCentralWidget(self.filesViewer)

        statusbar = self.statusBar()
        statusbar.showMessage('Status bar')

        openFile = QAction(QIcon('open.png'), 'Open', self)
        openFile.setShortcut('ctrl+o')
        openFile.setStatusTip('Open file with hash table')
        openFile.triggered.connect(self.OpenConfigFile)

        newFile = QAction(QIcon('new.png'), 'New', self)
        newFile.setShortcut('ctrl+n')
        newFile.setStatusTip('Create new hash table')
        newFile.triggered.connect(self.CreateConfigFile)

        saveFile = QAction(QIcon('save.png'), 'Save', self)
        saveFile.setShortcut('ctrl+s')
        saveFile.setStatusTip('Write table on disk')
        saveFile.triggered.connect(self.SaveConfigFile)

        updateHash = QAction(QIcon('update.png'), 'Update', self)
        updateHash.setShortcut('F5')
        updateHash.setStatusTip('Update hash table')
        updateHash.triggered.connect(self.UpdateHashFile)

        insertHash = QAction(QIcon('insert.png'), 'Insert', self)
        insertHash.setShortcut('Insert')
        insertHash.setStatusTip('Insert hash to table')
        insertHash.triggered.connect(self.showDialog)

        removeHash = QAction(QIcon('remove.png'), 'Remove', self)
        removeHash.setShortcut('Delete')
        removeHash.setStatusTip('Remove hash from table')
        removeHash.triggered.connect(self.removeFile)

        appInfo = QAction(QIcon('info.png'), 'About', self)
        appInfo.setShortcut('F1')
        appInfo.setStatusTip('About this application')
        appInfo.triggered.connect(self.infoWindow)

        toolbar = self.addToolBar('Tools')
        toolbar.addAction(openFile)       
        toolbar.addAction(newFile)
        toolbar.addAction(saveFile)
        toolbar.addAction(updateHash)
        toolbar.addAction(insertHash)
        toolbar.addAction(removeHash)
        toolbar.addAction(appInfo)
        
        self.setGeometry(0, 0, 640, 480)
        self.setWindowTitle('MD5 Hash tools')
        self.show()
    
    def ReadHashes(self):
        self.Hashes.Read()
        self.UpdateHashes()
    
    def UpdateHashes(self):
        self.filesViewer.setRowCount(self.Hashes.Length())
        count = 0 
        for params in self.Hashes.files:
            self.filesViewer.setItem(count, 0, QTableWidgetItem(params[0])) 
            self.filesViewer.setItem(count, 1, QTableWidgetItem(params[1])) 
            count += 1

    def removeFile(self):
        self.Hashes.Remove(self.filesViewer.currentRow())
        self.UpdateHashes()

    def WriteHashes(self):
        self.Hashes.Write()

    def OpenConfigFile(self):
        fileName = QFileDialog.getOpenFileName(self, 'Open hash config', '/')
        self.Hashes.Open(fileName)
        self.UpdateHashes()

    def SaveConfigFile(self):
        self.WriteHashes()
        self.statusBar().showMessage('Hash table was saved')

    def CreateConfigFile(self):
        fileName = QFileDialog.getSaveFileName(self, 'Create file', '/')
        self.Hashes.SetPath(fileName)
        self.Hashes.Clean()
        self.UpdateHashes()

    def UpdateHashFile(self):
        for params in self.Hashes.files:
            f = open(params[0].replace('\\', '/'), 'r')
            m = md5.new()
            with f:
                data = f.read()
                m.update(data)
            params[1] = m.hexdigest()
            f.close()
            self.UpdateHashes()
        self.statusBar().showMessage('Hash table was updated')
        
    def showDialog(self):
        fileName = QFileDialog.getOpenFileName(self, 'Open file', '/')
        while (fileName.contains(':')):
            QMessageBox.warning(self, 'Warning', 'Please don\'t use files with \':\' in filename')
            fileName = QFileDialog.getOpenFileName(self, 'Open file', '/home')

        f = open(fileName, 'r')
        m = md5.new()
        with f:        
            data = f.read()
            m.update(data)
        params = [fileName, m.hexdigest()]
        params[0] = params[0].replace('/', '\\')
        f.close()
        self.Hashes.Insert(params)
        self.UpdateHashes()

    def infoWindow(self):
       QMessageBox.about(self, 'Hash Generator', 'MD5 Hash generator tools\n\nBy Alexander Fedorov\nCopyright (c) Kraftway Inc')
                                
        
def main():
    app = QApplication(sys.argv)
    ex = AppWindow()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
