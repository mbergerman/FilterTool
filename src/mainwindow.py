from src.ui.mainwindow import *
import numpy as np
import sys
import os
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QApplication, QWidget, QPushButton, QAction, QLineEdit, QMessageBox, QRadioButton, QInputDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot

import scipy.signal as signal

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

from src.DesignConfig import *
from src.FilterStage import *


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)
        self.setFixedSize(1200, 675)
        self.stackedWidget.setCurrentIndex(0)
        self.tabPlots.setCurrentIndex(0)

        # Variables
        self.page = 0
        self.max_page = 1
        self.designconfig = DesignConfig()
        self.num_plots = self.tabPlots.count()
        self.plot_layouts = [self.plotlayout_1, self.plotlayout_2, self.plotlayout_3, self.plotlayout_4, self.plotlayout_5, self.plotlayout_6, self.plotlayout_7]

        # Signals/Slots
            # General
        self.btn_next.clicked.connect(self.nextPage)
        self.btn_prev.clicked.connect(self.prevPage)
        self.btn_save.clicked.connect(self.saveFile)
        self.btn_open.clicked.connect(self.openFile)
            # Etapa 1
        self.btn_plot.clicked.connect(self.plotAll)
            # Etapa 2
        self.btn_new_stage.clicked.connect(self.newStage)
        self.btn_delete_stage.clicked.connect(self.deleteStage)
        self.stage_list.itemClicked.connect(self.updateStageView)

        # Plots
        self.figure = [Figure() for x in range(self.num_plots)]
        self.canvas = [FigureCanvas(self.figure[x]) for x in range(self.num_plots)]
        self.axes = [self.figure[x].subplots() for x in range(self.num_plots)]
        for x, layout in enumerate(self.plot_layouts):
            layout.addWidget(NavigationToolbar(self.canvas[x], self))
            layout.addWidget(self.canvas[x])
            self.figure[x].tight_layout()
            self.axes[x].grid()
        self.axes[0].set_xscale('log')
        self.axes[1].set_xscale('log')
        self.axes[2].set_xscale('log')

        # Polos y ceros Etapa 2
        self.figure2 = Figure()
        self.canvas2 = FigureCanvas(self.figure2)
        self.axes2 = self.figure2.subplots()
        self.plotlayout_poles.addWidget(NavigationToolbar(self.canvas2, self))
        self.plotlayout_poles.addWidget(self.canvas2)
        self.figure2.tight_layout()
        self.axes2.grid()

    def nextPage(self):
        self.page = min(self.page+1, self.max_page)
        self.stackedWidget.setCurrentIndex(self.page)
        return

    def prevPage(self):
        self.page = max(self.page-1, 0)
        self.stackedWidget.setCurrentIndex(self.page)
        return

    def saveFile(self):
        pass # TO-DO

    def openFile(self):
        pass # TO-DO

    def plotAll(self):
        pass # TO-DO

    def newStage(self):
        polo1 = self.combo_polo1.currentText()
        polo2 = self.combo_polo2.currentText()
        self.stage_list.addItem(' {} , {}'.format(polo1, polo2))
        return

    def deleteStage(self):
        selection = self.stage_list.selectedItems()
        if len(selection) > 0:
            index = self.stage_list.row(selection[0])
            self.stage_list.takeItem(index)
        return

    def updateStageView(self):
        pass # TO-DO

