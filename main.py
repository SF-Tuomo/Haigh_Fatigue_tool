import sys
from start import Start
from haigh import Haigh
from PyQt5.QtWidgets import QApplication


def main():
    # creates instance of QApplication.
    global app
    app = QApplication(sys.argv)

    # run start menu first
    start = Start()
    app.exec()
    
    # get fatigue parameters
    parameters = start.apply()
    
    # run haigh with given parameters
    haigh = Haigh(parameters)
    
    # clean exit
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

