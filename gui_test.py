import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QInputDialog, QPushButton
from PyQt5.QtCore import Qt

class TestApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Test')
        self.resize(400,400)

        label1 = QLabel('안녕하세요',self)
        label1.setAlignment(Qt.AlignCenter)

        button = QPushButton('test')


        layout = QVBoxLayout()
        layout.addWidget(label1)
        layout.addWidget(button)


        self.setLayout(layout)

        self.show()


if  __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = TestApp()
    sys.exit(app.exec_())



