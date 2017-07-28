#-*- coding:utf8 -*-  
  
from PyQt4.QtCore import *  
from PyQt4.QtGui import *  
import math  
  
QTextCodec.setCodecForTr(QTextCodec.codecForName("utf-8"))  
  
if __name__ == '__main__':  
    import sys  
    app = QApplication(sys.argv)  
    model = QDirModel()  
    selModel =QItemSelectionModel(model);   
      
    list = QListView()  
    tree = QTreeView()  
    table = QTableView()  
      
    tree.setModel(model)  
    list.setModel(model)  
    table.setModel(model)  
      
    tree.setSelectionModel(selModel)  
    list.setSelectionModel(tree.selectionModel())  
    table.setSelectionModel(tree.selectionModel())  
      
    QObject.connect(tree,SIGNAL("doubleClicked(QModelIndex)"),list.setRootIndex)  
    QObject.connect(tree,SIGNAL("doubleClicked(QModelIndex)"),table.setRootIndex)  
      
    splitter = QSplitter()  
    splitter.addWidget(tree)  
    splitter.addWidget(list)  
    splitter.addWidget(table)  
    splitter.setWindowTitle(splitter.tr("Model/View"))  
    splitter.show()  
      
    sys.exit(app.exec_())  