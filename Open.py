from PyQt6.QtWidgets import *
from pathlib import Path
import sys
from Mp3Tagger.Mp3_Tagger import MainWindow as Mp3TaggerWindow
script_dir = Path(__file__).resolve().parent

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("List app")
        self.setMinimumSize(250,150)
        self.resize(250, 300)
        
        self.Mp3tagger_B = QPushButton("Push")
        self.Mp3tagger_B.clicked.connect(self.Mp3tagger_open)
        
        self.Mp3TaggerSubwindow = None
        
        layout1 = QVBoxLayout()
        
        layout1.addWidget(self.Mp3tagger_B)
        
        container = QWidget()
        container.setLayout(layout1)
        
        self.setCentralWidget(container)
    def Mp3tagger_open(self):
        if self.Mp3TaggerSubwindow is None:
            self.Mp3TaggerSubwindow = Mp3TaggerWindow()
            self.Mp3TaggerSubwindow.show()
        else:
            self.Mp3TaggerSubwindow.raise_()
        
app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()