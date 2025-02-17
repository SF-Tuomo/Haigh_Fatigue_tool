import numpy as np
from PyQt5 import QtWidgets
from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg



class Sn(QtWidgets.QMainWindow):
    
    def __init__(self, FAT, amp):
        super().__init__()
        self.FAT = FAT
        self.amp = amp
        self.main_widget = QtWidgets.QWidget()
        self.setCentralWidget(self.main_widget)
        self.init_window()
        
    def init_window(self):
        # create window
        self.setGeometry(300, 300, 1200, 600)
        
        # data
        self.x1 = np.array([1,10,100,500,1000,2000,3000,4000,5000,6000,7000,8000])
        self.x1 = np.append(self.x1, np.linspace(1e4,1e7,1000))
        self.x2 = np.array([1e7,1.5e7,2e7,2.5e7,3e7,4e7,5e7,7e7])
        self.x2 = np.append(self.x2, np.linspace(1e8,1e10))
        m1 = 5
        m2 = m1*2-1
        self.y1 = self.FAT*(2000000/self.x1)**(1/m1)
        self.y2 = self.y1[-1]*(10000000/self.x2)**(1/m2)
        # create diagram
        self.fig = Figure(figsize=(7.5, 7.5))
        self.canvas = FigureCanvasQTAgg(self.fig)
        self.ax = self.fig.add_subplot()
        self.ax.plot(self.x1, self.y1)
        self.ax.plot(self.x2, self.y2)
        self.ax.set_xscale('log')
        self.ax.set_yscale('log')
        self.ax.set_xlabel("Number of cycles")
        self.ax.set_ylabel("Stress amplitude [MPa]")
        self.ax.set_ylim(bottom=1)
        self.ax.set_xlim(right=1e10, left=10)
        self.ax.grid(True)
        # plot fat
        self.ax.plot(2000000, self.FAT, 'bo')
        self.ax.annotate('FAT {}'.format(format(self.FAT, ".2f")), xy=(2000000, self.FAT), xytext=(2000000+1000, self.FAT+5))
        # find fatigue life
        if self.amp < self.y1[-1]:
            y_data = self.y2
            x_data = self.x2
            self.cycles = np.interp(-self.amp, -y_data, x_data)
        else:
            order = self.y1
            y_data = self.y1
            x_data = self.x1
            self.cycles = np.interp(-self.amp, -y_data, x_data)
        # plot cycles
        self.ax.plot([0, self.cycles, self.cycles], [self.amp, self.amp, 0], linestyle='--', marker='o', color='k')
        self.ax.annotate('Fatigue life {}'.format(format(self.cycles, ".0f")), xy=(self.cycles, self.amp), xytext=(15, 5))
        
        # layout
        self.h_layout = QtWidgets.QHBoxLayout()
        self.h_layout.addWidget(self.canvas)
        
        # set main layout and show
        self.main_widget.setLayout(self.h_layout)
        
        