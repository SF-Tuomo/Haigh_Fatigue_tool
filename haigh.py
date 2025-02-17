import numpy as np
from sn import Sn
from calculation import Calculation
from reduction import Reduction
from PyQt5 import QtWidgets, QtGui
from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg


class Haigh(QtWidgets.QMainWindow):
    
    def __init__(self, parameters):
        super().__init__()
        self.main_widget = QtWidgets.QWidget()
        self.setCentralWidget(self.main_widget)
        # define variables
        self.parameters = parameters
        self.line = 0
        self.show_all_curves = 2
        self.dev = False
        self.surv = False
        self.red2 = False
        # create bold font
        self.Bold=QtGui.QFont()
        self.Bold.setBold(True)
        # get diagram curves
        self.get_curves()
        # making the window
        self.init_window()

    def init_window(self):
        # create window
        self.setGeometry(300, 300, 1200, 600)
        
        # create diagram
        self.fig = Figure(figsize=(7.5, 7.5))
        self.canvas = FigureCanvasQTAgg(self.fig)
        self.ax = self.fig.add_subplot()
        if self.parameters[3] == True:
            self.ax.plot(self.s_m, self.s_af, label="modified linear part")
        else:
            self.ax.plot(self.s_m, self.s_af, label="linear part")
        self.ax.plot(self.s_m2, self.s_af2, label="tensile parabola")
        self.ax.plot(self.s_m3, self.s_af3, label="negative mean stress curve")
        self.ax.plot(self.s_m4, self.s_af4, label="Morrow")
        self.ax.plot(self.s_m5, self.s_af5, label="Goodman")
        # format plot
        self.ax.set_xlabel("Mean stress [MPa]", fontsize=8)
        self.ax.set_ylabel("Stress amplitude [MPa]", fontsize=8)
        self.ax.grid(True)
        self.ax.set_ylim(bottom=0)
        self.ax.set_xlim(left=self.s_m3[0]-80)
        self.ax.legend(loc="upper right", fontsize=8)
        
        # Add menu
        self.box = QtWidgets.QCheckBox("Show all curves", self)
        self.box.setChecked(True)
        self.box.stateChanged.connect(self.show_curves)
        self.line_combobox = QtWidgets.QComboBox()
        self.line_combobox.addItem('C.Mourier')
        self.line_combobox.addItem('Morrow')
        self.line_combobox.addItem('Goodman')
        self.line_combobox.currentIndexChanged.connect(self.on_change_line)
        self.line_combobox.setFixedSize(200, 20)
        self.qLineEdit = QtWidgets.QLineEdit(self)
        self.qLineEdit.setFixedSize(200, 20)
        self.qLineEdit.textChanged[str].connect(self.on_change_mean)
        self.qLineEdit2 = QtWidgets.QLineEdit(self)
        self.qLineEdit2.setFixedSize(200, 20)
        self.qLineEdit2.textChanged[str].connect(self.on_change_amp)
        self.label = QtWidgets.QLabel()
        self.label.setText("Mean stress")
        self.label.setFont(self.Bold)
        self.label3 = QtWidgets.QLabel()
        self.label3.setText("Stress amplitude")
        self.label3.setFont(self.Bold)
        self.button1 = QtWidgets.QPushButton("Apply")
        self.button1.setFixedSize(200, 50)
        self.button1.clicked.connect(self.apply)
        self.button2 = QtWidgets.QPushButton("Draw S-N curve")
        self.button2.setFixedSize(200, 50)
        self.button2.clicked.connect(self.sn)
        self.label8 = QtWidgets.QLabel("Select mean stress correction")
        self.label8.setFont(self.Bold)
        # sn reduction parameters
        self.qLineEdit3 = QtWidgets.QLineEdit(self)
        self.qLineEdit3.setFixedSize(40, 20)
        self.qLineEdit3.textChanged[str].connect(self.on_change_surv)
        self.qLineEdit3.setText("99")
        self.qLineEdit4 = QtWidgets.QLineEdit(self)
        self.qLineEdit4.setFixedSize(40, 20)
        self.qLineEdit4.textChanged[str].connect(self.on_change_dev)
        self.qLineEdit4.setText("8")
        self.qLineEdit5 = QtWidgets.QLineEdit(self)
        self.qLineEdit5.setFixedSize(40, 20)
        self.qLineEdit5.textChanged[str].connect(self.on_change_red2)
        self.qLineEdit5.setText("1")
        self.label4 = QtWidgets.QLabel()
        self.label4.setText("survival probability %")
        self.label4.setFixedSize(150, 20)
        self.label5 = QtWidgets.QLabel()
        self.label5.setFixedSize(150, 20)
        self.label5.setText("relative standard deviation %")
        self.label6 = QtWidgets.QLabel()
        self.label6.setText("S-N Curve reduction parameters")
        self.label6.setFont(self.Bold)
        self.label7 = QtWidgets.QLabel()
        self.label7.setFixedSize(150, 20)
        self.label7.setText("additional reduction factor")
        
        # fat indicator
        self.label2 = QtWidgets.QLabel()
        
        # layout
        self.h_layout = QtWidgets.QHBoxLayout()
        self.h_layout.addWidget(self.canvas)
        self.v_layout = QtWidgets.QVBoxLayout()
        self.g_layout = QtWidgets.QGridLayout()
        self.v_layout.addWidget(self.label8)
        self.v_layout.addWidget(self.line_combobox)
        self.v_layout.addWidget(self.box)
        self.v_layout.insertSpacing(3, 20)
        self.v_layout.addWidget(self.label)
        self.v_layout.addWidget(self.qLineEdit)
        self.v_layout.addWidget(self.label3)
        self.v_layout.addWidget(self.qLineEdit2)
        self.v_layout.insertSpacing(9, 20)
        self.v_layout.addWidget(self.button1)
        self.v_layout.insertSpacing(11, 60)
        self.v_layout.addWidget(self.label6)
        self.g_layout.addWidget(self.qLineEdit3,0,1)
        self.g_layout.addWidget(self.qLineEdit4,1,1)
        self.g_layout.addWidget(self.qLineEdit5,2,1)
        self.g_layout.addWidget(self.label4,0,0)
        self.g_layout.addWidget(self.label5,1,0)
        self.g_layout.addWidget(self.label7,2,0)
        self.v_layout.addLayout(self.g_layout)
        self.v_layout.addWidget(self.button2)
        self.v_layout.addStretch(10)
        self.h_layout.addLayout(self.v_layout)
        
        # set main layout and show
        self.main_widget.setLayout(self.h_layout)
        self.show()
        
    def get_curves(self):
        calc = Calculation(self.parameters)
        curves = calc.get_curves()
        self.s_m, self.s_m2, self.s_m3, self.s_af, self.s_af2, self.s_af3, self.s_m4, self.s_m5, self.s_af4, self.s_af5 = curves[0], curves[1], curves[2], curves[3], curves[4], curves[5], curves[6], curves[7], curves[8], curves[9]
        
    def on_change_mean(self, text):
        self.mean = text
    
    def on_change_amp(self, text):
        self.amp = text
    
    def on_change_line(self, index):
        self.line = index
    
    def on_change_surv(self, text):
        self.surv = text
        
    def on_change_dev(self, text):
        self.dev = text
    
    def on_change_red2(self, text):
        self.red2 = text
    
    def show_curves(self, status):
        self.show_all_curves = status
    
    def apply(self):
        self.amp = float(self.amp)
        self.mean = float(self.mean)
        # get FAT
        if self.line == 0:
            if self.mean > self.s_m2[0]:
                self.FAT = np.interp(self.mean, self.s_m2, self.s_af2)
            elif self.mean < self.s_m[0] :
                self.FAT = np.interp(self.mean, self.s_m3, self.s_af3)
            else:
                self.FAT = np.interp(self.mean, self.s_m, self.s_af)
        elif self.line == 1:
            if self.mean > 0:
                self.FAT = np.interp(self.mean, self.s_m4, self.s_af4)
            elif self.mean < self.s_m[0] :
                self.FAT = np.interp(self.mean, self.s_m3, self.s_af3)
            else:
                self.FAT = np.interp(self.mean, self.s_m, self.s_af)
        else:
            if self.mean > 0:
                self.FAT = np.interp(self.mean, self.s_m5, self.s_af5)
            elif self.mean < self.s_m[0] :
                self.FAT = np.interp(self.mean, self.s_m3, self.s_af3)
            else:
                self.FAT = np.interp(self.mean, self.s_m, self.s_af)
            
        # draw plot
        self.redraw()
        self.ax.plot([self.mean, self.mean, self.mean, -10000], [0, self.amp, self.FAT, self.FAT], linestyle='--', marker='o', color='k')
        self.ax.annotate('FAT {}'.format(format(self.FAT, ".2f")), xy=(self.mean, self.FAT), xytext=(self.mean+5, self.FAT+5))
        self.ax.annotate('Mean stress'.format(format(self.mean, ".0f")), xy=(self.mean, self.mean), xytext=(self.mean+5, self.mean+5))
        self.canvas.draw()
    
    def redraw(self):
        # draw plot
        self.ax.clear()
        if self.show_all_curves == 2: #draw all curves if box cheked
            if self.parameters[3] == True:
                self.ax.plot(self.s_m, self.s_af, label="modified linear part")
            else:
                self.ax.plot(self.s_m, self.s_af, label="linear part")
            self.ax.plot(self.s_m2, self.s_af2, label="tensile parabola")
            self.ax.plot(self.s_m3, self.s_af3, label="negative mean stress curve")
            self.ax.plot(self.s_m4, self.s_af4, label="Morrow")
            self.ax.plot(self.s_m5, self.s_af5, label="Goodman")
        else:
            if self.line == 0: # draw only parabola
                if self.parameters[3] == True:
                    self.ax.plot(self.s_m, self.s_af, label="modified linear part")
                else:
                    self.ax.plot(self.s_m, self.s_af, label="linear part")
                self.ax.plot(self.s_m2, self.s_af2, label="tensile parabola")
                self.ax.plot(self.s_m3, self.s_af3, label="negative mean stress curve")
            elif self.line == 1: # draw only morrow
                if self.parameters[3] == True:
                    self.ax.plot(self.s_m, self.s_af, label="modified linear part")
                else:
                    self.ax.plot(self.s_m, self.s_af, label="linear part")
                self.ax.plot(self.s_m3, self.s_af3, label="negative mean stress curve")
                self.ax.plot(self.s_m4, self.s_af4, label="Morrow")
            else: # draw only goodman
                if self.parameters[3] == True:
                    self.ax.plot(self.s_m, self.s_af, label="modified linear part")
                else:
                    self.ax.plot(self.s_m, self.s_af, label="linear part")
                self.ax.plot(self.s_m3, self.s_af3, label="negative mean stress curve")
                self.ax.plot(self.s_m5, self.s_af5, label="Goodman")
                
        # format plot
        self.ax.set_xlabel("Mean stress [MPa]", fontsize=8)
        self.ax.set_ylabel("Stress amplitude [MPa]", fontsize=8)
        self.ax.grid(True)
        self.ax.set_ylim(bottom=0)
        self.ax.set_xlim(left=self.s_m3[0]-80)
        self.ax.legend(loc="upper right", fontsize=8)
        
        # FAT indicator text
        self.label2.setText("FAT Class:{}".format(self.FAT))
        self.v_layout.addWidget(self.label2, -1)

    def sn(self):
        reduction_factor = 1
        reduction_factor2 = 1
        if self.dev and self.surv:
            red = Reduction(self.FAT, float(self.dev)/100, float(self.surv)/100)
            reduction_factor = red.calculate()
        if self.red2:
            reduction_factor2 = float(self.red2)
        self.sn = Sn(self.FAT * reduction_factor * reduction_factor2, self.amp)
        self.sn.show()



























                              
    
    