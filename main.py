import sys
from PyQt5 import QtGui, QtWidgets
__all__ = [QtGui, QtWidgets]


def window():
    app = QtWidgets.QApplication(sys.argv)
    w = QtWidgets.QWidget()
    b = QtWidgets.QLabel(w)
    b.setText("Hello World!")
    w.setGeometry(100, 100, 400, 200)
    b.move(50, 20)
    w.setWindowTitle('PyQt')
    w.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    window()
