from PyQt6.QtWidgets import *
from pathlib import Path
import sys
from mutagen.easyid3 import EasyID3

script_dir = Path(__file__).resolve().parent
repeat = 0

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Mp3 tagger")
        self.setMinimumSize(150,100)
        self.resize(210, 150)
        
        self.Open_button = QPushButton("Open file(s)")
        self.New_property_input = QLineEdit()
        self.New_property_input.setPlaceholderText("e.g. I Wish")
        self.Log_hint = QLabel()
        self.Log_hint.setWordWrap(True)
        self.Update_propertys_button = QPushButton("Update propertys")
        self.label = QLabel("Update:")
        self.Type_selection = QComboBox()
        self.Type_selection.addItems(["Album", "Artist", "Year", "Genre"])
        self.Type_selection.currentIndexChanged.connect(self.Input_hint)
        
        self.Open_button.clicked.connect(self.pressed)
        self.Update_propertys_button.clicked.connect(self.Update_file)
        
        layout1 = QVBoxLayout()
        layout2 = QHBoxLayout()
        
        layout2.addWidget(self.label)
        layout2.addWidget(self.Type_selection)
        
        layout1.addWidget(self.Open_button)
        layout1.addLayout(layout2)
        layout1.addWidget(self.New_property_input)
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
                global repeat
                audio = file_path[i]
                audiofile = EasyID3(audio)
                repeat += 1
                choices = ['album', 'artist', 'date', 'genre']
                
                print(repeat)
                print(self.Type_selection.currentIndex())
                
                audiofile[choices[self.Type_selection.currentIndex()]] = self.New_property_input.text()
                self.Log_hint.setText(f"({repeat}) Upated {choices[self.Type_selection.currentIndex()]} for {len(file_path)} song(s)")
                
                audiofile.save()
        except Exception as e:
            self.Log_hint.setText(f"Error: {e}")
    
    def Input_hint(self, i):
        global repeat
        repeat = 0
        
        if i == 0:
            self.New_property_input.setPlaceholderText("e.g. I Wish")
        elif i == 1:
            self.New_property_input.setPlaceholderText("e.g. Skee-Lo")
        elif i == 2:
            self.New_property_input.setPlaceholderText("e.g. 1995")
        elif i == 3:
            self.New_property_input.setPlaceholderText("e.g. Hip-Hop")

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()