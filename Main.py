#coding: utf-8
'''
Created on 2017年7月25日

@author: happy
'''
from PyQt4 import QtCore, QtGui
#从 ui.py 文件里 import ui类
from ui import Ui_Dialog
import sys
import time

#新建自己的窗口类，继承 QDialog 和 ui类
class MyDialog(QtGui.QDialog,Ui_Dialog):
    global url
    def __init__(self, parent=None):
        super(MyDialog, self).__init__(parent)
        #调用内部的 setupUi() ，本身对象作为参数
        self.setupUi(self)
        #连接 QPushButton 的点击信号到槽 BigWork()
        self.pushButton_2.clicked.connect(self.BigWork)
        #测试set值
        self.textEdit.setPlainText("http://sabrinacarpenterbr.com/galeria/thumbnails.php?album=1107")
        self.textEdit_2.setPlainText(r"D:\Users\happy\Desktop\sab\0507 - Chegando Ao Aeroporto De Vancouver, Canada")
        
        
    def BigWork(self):
        #import 自己的进程类
        url = self.textEdit.toPlainText()
        addr = self.textEdit_2.toPlainText()
        print url
        print addr
        from Thread2 import BigWorkThread
        #新建对象
        self.bwThread = BigWorkThread(url,addr)
        #连接子进程的信号和槽函数
        self.bwThread.finishSignal.connect(self.BigWorkEnd)
        #更新进度信号
        self.bwThread.progress.connect(self.progress)
        #开始执行run()函数里的内容
        self.pushButton_2.setDisabled(True)
        self.label_3.setText("Running")

        self.bwThread.start()

        #增加形参准备接受返回值 ls
    def BigWorkEnd(self,ls):
        print 'get!'
        #使用传回的返回值
        for word in ls:
            print word,
        #按钮回复
        self.pushButton_2.setDisabled(False)
        #搞定提示
        self.label_3.setText("   Done!")
    
    #更新进度
    def progress(self,ls):
        #print "更新进度"
        self.label_3.setText(str(ls[0])+" / "+str(ls[1])+"  Page"+str(ls[2]))
        
    
    
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    #新建类对象
    Dialog = MyDialog()
    #显示类对象
    Dialog.show()
    #测试set值
    
    
    sys.exit(app.exec_())

