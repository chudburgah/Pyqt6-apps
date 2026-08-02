from PyQt6.QtWidgets import *; from PyQt6.QtCore import *; from PyQt6.QtGui import *
from pathlib import Path
import sys
import eyed3
import logging

script_dir = Path(__file__).resolve().parent

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Mp3 tagger")
        self.setMinimumSize(150,100)
        self.resize(210, 150)
        
        self.Open_button = QPushButton("Open file(s)")
        self.New_album_input = QLineEdit()
        self.New_album_input.setPlaceholderText("Album Name:")
        self.Log_hint = QLabel()
        self.Log_hint.setWordWrap(True)
        self.Update_propertys_button = QPushButton("Update propertys")
        
        self.Open_button.clicked.connect(self.pressed)
        self.Update_propertys_button.clicked.connect(self.Update_file)
        
        layout1 = QVBoxLayout()
        layout1.addWidget(self.Open_button)
        layout1.addWidget(self.New_album_input)
        layout1.addWidget(self.Log_hint)
        layout1.addWidget(self.Update_propertys_button)
        
        container = QWidget()
        container.setLayout(layout1)
        
        self.setCentralWidget(container)
    def pressed(self):
        global file_path
        file_path, _ = QFileDialog.getOpenFileNames(None, "Choose Files", "","Mp3 Files (*.mp3)")
        if file_path:
            for i in range(len(file_path)):
                print(file_path[int(i)])
    def Update_file(self):
        try:
            for i in range(len(file_path)):
                audiofile = eyed3.load(file_path[i])
                if audiofile.tag is None:
                    audiofile.initTag()
                
                audiofile.tag.album = self.New_album_input.text()
                
                audiofile.tag.save()
                self.Log_hint.setText(f"Upated album name for {len(file_path)} song(s)")
        except:
            self.Log_hint.setText("failed to update propertys")

        
app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()