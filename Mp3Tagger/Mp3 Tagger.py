from PyQt6.QtWidgets import *
from pathlib import Path
import sys
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3

script_dir = Path(__file__).resolve().parent

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Mp3 tagger")
        self.setMinimumSize(150,100)
        self.resize(210, 150)
        
        self.Open_button = QPushButton("Open file(s)")
        self.New_album_input = QLineEdit()
        self.New_album_input.setPlaceholderText("e.g. I Wish")
        self.Log_hint = QLabel()
        self.Log_hint.setWordWrap(True)
        self.Update_propertys_button = QPushButton("Update propertys")
        self.label = QLabel("Update:")
        self.Type_selection = QComboBox()
        self.Type_selection.addItems(["Album", "Artist", "Year"])
        
        self.Open_button.clicked.connect(self.pressed)
        self.Update_propertys_button.clicked.connect(self.Update_file)
        
        layout1 = QVBoxLayout()
        layout2 = QHBoxLayout()
        
        layout2.addWidget(self.label)
        layout2.addWidget(self.Type_selection)
        
        layout1.addWidget(self.Open_button)
        layout1.addLayout(layout2)
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
                audio = file_path[i]
                audiofile = EasyID3(audio)
                tags = ID3(audio)
                    
                print(self.Type_selection.currentIndex())
                if self.Type_selection.currentIndex() == 0:
                    audiofile['album'] = self.New_album_input.text()
                elif self.Type_selection.currentIndex() == 1:
                    audiofile['artist'] = self.New_album_input.text()
                elif self.Type_selection.currentIndex() == 2:
                    audiofile['date'] = self.New_album_input.text()         
                
                tags.save()
                audiofile.save()
                self.Log_hint.setText(f"Upated properties for {len(file_path)} song(s)")
        except Exception as e:
            self.Log_hint.setText(f"Error: {e}")
  
app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()