"""

Python + QT timer
@author: robert van duursen

"""
from PyQt5 import QtWidgets, uic, QtCore, QtGui
import sys, os, time, math

app = QtWidgets.QApplication(sys.argv)
app.setStyle('Fusion')


# QtWidgets.QMainWindow
class PythonTimer(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()

        ui_path = os.path.join(os.path.join(os.path.dirname(__file__), 'standalone_QT_timer.ui'))
        q_file = QtCore.QFile(ui_path)
        q_file.open(QtCore.QFile.ReadOnly)

        self.ui_content = uic.loadUi(q_file, None)
        self.__dict__.update(self.ui_content.__dict__)
        q_file.close()

        self.ui_content.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.ui_content.show()
        self.makeConnections()

        self.reset()

        self._timer = QtCore.QTimer()
        self._timer.timeout.connect(self.setTime)
        self._timer.setInterval(1000)
        self._timer.start()

    def makeConnections(self):
        self.reset_btn.pressed.connect(self.reset)

    def reset(self):
        self.start = time.time()
        self.setTime()


    def setTime(self):
        delta = time.time() - self.start

        sec = int(delta)
        min = math.floor(sec / 60.0)
        hour = math.floor(min / 60.0)

        self.statusText.setText("{:02d}h:{:02d}m:{:02d}s".format(hour , min % 60, sec % 60))


test = PythonTimer()
sys.exit(app.exec_())
