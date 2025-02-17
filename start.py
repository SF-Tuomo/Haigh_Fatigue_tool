from read_materials import Read_materials
from PyQt5 import QtWidgets, QtCore


class Start(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.main_widget = QtWidgets.QWidget()
        self.setCentralWidget(self.main_widget)
        # reading materials
        self.materials = Read_materials()
        self.materials = self.materials.return_materials()
        # making the window
        self.init_window()
        # set opt to false
        self.opt = False

    def init_window(self):
        # create game window
        self.setGeometry(300, 300, 800, 500)
        self.show()
        # text boxes
        self.qLineEdit = QtWidgets.QLineEdit(self)
        self.qLineEdit.setFixedSize(200, 20)
        self.qLineEdit.textChanged[str].connect(self.on_change_Rm)
        self.qLineEdit2 = QtWidgets.QLineEdit(self)
        self.qLineEdit2.setFixedSize(200, 20)
        self.qLineEdit2.textChanged[str].connect(self.on_change_Rp)
        self.qLineEdit3 = QtWidgets.QLineEdit(self)
        self.qLineEdit3.setFixedSize(200, 20)
        self.qLineEdit3.textChanged[str].connect(self.on_change_E)
        # button
        self.button1 = QtWidgets.QPushButton("Apply")
        self.button1.setFixedSize(200, 50)
        self.button1.clicked.connect(self.apply_and_close)
        # Comboboxes
        self.material_combobox = QtWidgets.QComboBox()
        self.material_combobox.addItem('Custom')
        for material in self.materials:
            self.material_combobox.addItem(material[0])
        self.material_combobox.currentIndexChanged.connect(self.select_material)
        self.option = QtWidgets.QComboBox()
        self.option.addItem("default")
        self.option.addItem("1.3*Rm (recommended for low strength steels)")
        self.option.currentIndexChanged.connect(self.on_change_option)
        # label
        self.label = QtWidgets.QLabel()
        self.label.setText("Ultimate tensile strength")
        self.label.setFixedSize(150, 40)
        self.label2 = QtWidgets.QLabel()
        self.label2.setText("Yield strength")
        self.label2.setFixedSize(150, 40)
        self.label3 = QtWidgets.QLabel()
        self.label3.setText("MPa")
        self.label3.setFixedSize(200, 40)
        self.label4 = QtWidgets.QLabel()
        self.label4.setText("MPa")
        self.label4.setFixedSize(200, 40)
        self.label5 = QtWidgets.QLabel()
        self.label5.setText("GPa")
        self.label5.setFixedSize(200, 40)
        self.label6 = QtWidgets.QLabel()
        self.label6.setText("Youngs modulus")
        self.label6.setFixedSize(150, 40)
        self.label7 = QtWidgets.QLabel()
        self.label7.setText("Fict. ult. strength definition")
        self.label7.setFixedSize(150, 40)
        self.label8 = QtWidgets.QLabel()
        self.label8.setText("Select material")
        self.label8.setFixedSize(150, 40)
        # box_layout
        self.box_layout = QtWidgets.QGridLayout()
        self.box_layout.addWidget(self.material_combobox,1,2)
        self.box_layout.addWidget(self.option,0,2)
        self.box_layout.addWidget(self.qLineEdit,2,2)
        self.box_layout.addWidget(self.qLineEdit2,3,2)
        self.box_layout.addWidget(self.qLineEdit3,4,2)
        self.box_layout.addWidget(self.button1,5,3)
        self.box_layout.addWidget(self.label7,0,1, alignment=QtCore.Qt.AlignmentFlag.AlignRight)
        self.box_layout.addWidget(self.label8,1,1, alignment=QtCore.Qt.AlignmentFlag.AlignRight)
        self.box_layout.addWidget(self.label,2,1, alignment=QtCore.Qt.AlignmentFlag.AlignRight)
        self.box_layout.addWidget(self.label2,3,1, alignment=QtCore.Qt.AlignmentFlag.AlignRight)
        self.box_layout.addWidget(self.label3,2,3)
        self.box_layout.addWidget(self.label4,3,3)
        self.box_layout.addWidget(self.label5,4,3)
        self.box_layout.addWidget(self.label6,4,1, alignment=QtCore.Qt.AlignmentFlag.AlignRight)
        
        # set main layout and show
        self.main_widget.setLayout(self.box_layout)
        self.show()

    def on_change_Rm(self, text):
        self.Rm = text
    
    def on_change_Rp(self, text):
        self.Rp = text
    
    def on_change_E(self, text):
        self.E = text
    
    def on_change_option(self, index): # select method for defining ficticious tensile strength
        if index == 1:
            self.opt = True
        else:
            self.opt = False
        
    def select_material(self, index):
        self.qLineEdit.setText(str(self.materials[index - 1][1]))
        self.qLineEdit2.setText(str(self.materials[index - 1][2]))
        self.qLineEdit3.setText(str(self.materials[index - 1][3]))
    
    def apply(self):
        self.E = 0
        self.parameters = [float(self.Rm), float(self.Rp), float(self.E), self.opt]
        return self.parameters
    
    def apply_and_close(self):
        self.apply()
        self.close()
    
    