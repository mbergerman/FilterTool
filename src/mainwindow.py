from src.ui.mainwindow import *
import numpy as np
from numpy import linspace, logspace, cos, sin, heaviside, log10, floor, zeros, ones, pi
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
from src.Aproximations import *
from src.FilterStage import *


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)

        # Init
        self.setFixedSize(1200, 675)
        self.stackedWidget.setCurrentIndex(0)
        self.tabPlots.setCurrentIndex(0)
        self.updateType()
        self.updateAprox()

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
        self.btn_plot.clicked.connect(lambda: self.plotAll(self.designconfig))
        self.combo_tipo.currentIndexChanged.connect(self.updateType)
        self.combo_aprox.currentIndexChanged.connect(self.updateAprox)
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

    def updateType(self):
        type = self.combo_tipo.currentText()
        w_band = type == 'Pasa Banda' or type == 'Rechaza Banda'
        self.label_wp_2.setEnabled(w_band)
        self.spin_wp_2.setEnabled(w_band)
        self.label_wa_2.setEnabled(w_band)
        self.spin_wa_2.setEnabled(w_band)

        self.label_wp.setText('Frecuencia ωp+' if w_band else 'Frecuencia ωp')
        self.label_wa.setText('Frecuencia ωa+' if w_band else 'Frecuencia ωa')
        return

    def updateAprox(self):
        #aprox = self.combo_aprox.currentText()
        return

    def plotAll(self, designconfig):
        type = self.combo_tipo.currentText()
        aprox = self.combo_aprox.currentText()
        denorm = self.spin_denorm.value()
        minord = self.spin_minord.value()
        maxord = self.spin_maxord.value()
        qmax =  self.spin_qmax.value()
        Ap = self.spin_Ap.value()
        Aa = self.spin_Aa.value()
        wp = self.spin_wp.value()
        wa = self.spin_wa.value()
        wp2 = self.spin_wp_2.value()
        wa2 = self.spin_wa_2.value()

        # Mensaje advertencia: Parametros invalidos
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle("Advertencia!")

        w_band = type == 'Pasa Banda' or type == 'Rechaza Banda'
        if (wp == 0 or wa == 0) or \
            (w_band and (wp2 == 0 or wa2 == 0 or wp2 >= wp or wa2 >= wa)) or \
            (type == 'Pasa Banda' and (wp >= wa or wp2 <= wa2)) or \
            (type == 'Rechaza Banda' and (wp <= wa or wp2 >= wa2)) or \
            (type == 'Pasa Bajos' and wa <= wp) or \
            (type == 'Pasa Altos' and wp <= wa):
                msg.setText("Los parametros para ωp y ωa no son válidos.")
                msg.exec_()
        elif Aa <= 0 or Ap <= 0:
            msg.setText("Los parametros para Ap y/o Aa no son válidos.\n Ambos deben ser mayores a 0.")
            msg.exec_()
        else:
            for x, ax in enumerate(self.axes):
                ax.clear()
                ax.grid()

            self.designconfig.setParameters(type, aprox, denorm, minord, maxord, qmax, Ap, Aa, wp, wa, wp2, wa2)
            wpn = 1
            dwa = wa - wa2
            dwp = wp - wp2
            if type == 'Pasa Bajos':
                won = wa/wp
            elif type == 'Pasa Altos':
                won = wp/wa
            elif type == 'Pasa Banda':
                won = dwa/dwp
            elif type == 'Rechaza Banda':
                won = dwp/dwa

            self.plotTemplate(type, Ap, Aa, wp, wa, wp2, wa2)

            # Calcular aproximación here
            if aprox == 'Butterworth':
                z, p, k = Butterworth(designconfig)

            try:
                lowerfreq = min(wa, wp, wa2, wp2) / 10
                higherfreq = max(wa, wp, wa2, wp2) * 10
                x = np.logspace((log10(lowerfreq)), (log10(higherfreq)), num=1000)
                Gain = signal.bode(signal.ZerosPolesGain(z, p, k), x)
                Attenuation = signal.bode(signal.ZerosPolesGain(p, z, 1 / k), x)
                self.axes[0].semilogx(Attenuation[0], Attenuation[1], 'k')
                self.axes[1].semilogx(Gain[0], Gain[2], 'k')
            except:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setWindowTitle("Error!")
                msg.setText("Error crítico intentando generar gráficos!")
                msg.exec_()

            for x, canv in enumerate(self.canvas):
                canv.draw()
        pass # TO-DO

    def plotTemplate(self, type, Ap, Aa, wp, wa, wp2, wa2):
        if type == 'Pasa Bajos':
            x = [wp / 10, wp, wp]
            y = [Ap, Ap, Aa + 10]
            self.axes[0].semilogx(x, y, 'b--', color='#28658a', linewidth=2)
            self.axes[0].fill_between(x, y, np.max(y), facecolor="none", edgecolor='#539ecd', hatch='X', linewidth=0)
            x = [wa, wa, wa * 10]
            y = [Ap - 10, Aa, Aa]
            self.axes[0].semilogx(x, y, 'b--', color='#28658a', linewidth=2)
            self.axes[0].fill_between(x, y, np.min(y), facecolor="none", edgecolor='#539ecd', hatch='X', linewidth=0)
        elif type == 'Pasa Altos':
            x = [wa / 10, wa, wa]
            y = [Aa, Aa, Ap - 10]
            self.axes[0].semilogx(x, y, 'b--', color='#28658a', linewidth=2)
            self.axes[0].fill_between(x, y, np.min(y), facecolor="none", edgecolor='#539ecd', hatch='X', linewidth=0)
            x = [wp, wp, wp * 10]
            y = [Aa + 10, Ap, Ap]
            self.axes[0].semilogx(x, y, 'b--', color='#28658a', linewidth=2)
            self.axes[0].fill_between(x, y, np.max(y), facecolor="none", edgecolor='#539ecd', hatch='X', linewidth=0)
        elif type == 'Pasa Banda':
            x = [wa2 / 10, wa2, wa2]
            y = [Aa, Aa, Ap - 10]
            self.axes[0].semilogx(x, y, 'b--', color='#28658a', linewidth=2)
            self.axes[0].fill_between(x, y, np.min(y), facecolor="none", edgecolor='#539ecd', hatch='X', linewidth=0)
            x = [wp2, wp2, wp, wp]
            y = [Aa + 10, Ap, Ap, Aa + 10]
            self.axes[0].semilogx(x, y, 'b--', color='#28658a', linewidth=2)
            self.axes[0].fill_between(x, y, np.max(y), facecolor="none", edgecolor='#539ecd', hatch='X', linewidth=0)
            x = [wa, wa, wa * 10]
            y = [Ap - 10, Aa, Aa]
            self.axes[0].semilogx(x, y, 'b--', color='#28658a', linewidth=2)
            self.axes[0].fill_between(x, y, np.min(y), facecolor="none", edgecolor='#539ecd', hatch='X', linewidth=0)
        elif type == 'Rechaza Banda':
            x = [wp2 / 10, wp2, wp2]
            y = [Ap, Ap, Aa + 10]
            self.axes[0].semilogx(x, y, 'b--', color='#28658a', linewidth=2)
            self.axes[0].fill_between(x, y, np.max(y), facecolor="none", edgecolor='#539ecd', hatch='X', linewidth=0)
            x = [wa2, wa2, wa, wa]
            y = [Ap - 10, Aa, Aa, Ap - 10]
            self.axes[0].semilogx(x, y, 'b--', color='#28658a', linewidth=2)
            self.axes[0].fill_between(x, y, np.min(y), facecolor="none", edgecolor='#539ecd', hatch='X', linewidth=0)
            x = [wp, wp, wp * 10]
            y = [Aa + 10, Ap, Ap]
            self.axes[0].semilogx(x, y, 'b--', color='#28658a', linewidth=2)
            self.axes[0].fill_between(x, y, np.max(y), facecolor="none", edgecolor='#539ecd', hatch='X', linewidth=0)

        return

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

