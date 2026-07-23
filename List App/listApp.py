from PyQt6.QtWidgets import *; from PyQt6.QtCore import *; from PyQt6.QtGui import *
import subprocess; from pathlib import Path
import datetime
import sys
import os

settings = {}
timeToggled = bool()
script_dir = Path(__file__).resolve().parent

config_dir = script_dir / "listAppConfig" / "config.txt"
list_dir = script_dir / "listAppConfig" / "list.log"
savedLists_dir = script_dir / "savedLists"

#make sure the files and folders actually exists
config_dir.parent.mkdir(parents=True, exist_ok=True)
savedLists_dir.mkdir(parents=True, exist_ok=True)

with open(list_dir, "a"):
    pass
with open(config_dir, "a"):
    pass

with open(config_dir, "r") as file:
    for line in file:
        if "=" in line:
            name, value = line.split("=", 1)
            settings[name.strip()] = value.strip()
if settings.get('dateToggle') == 'True':
    timeToggled = True

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("List app")
        self.setMinimumSize(250,150)
        self.resize(250, 300)

        #create the buttons, text box (label), ect.
        self.button = QPushButton("Add to list")
        self.clearbutton = QPushButton("Clear list")
        self.removeLineButton = QPushButton("Remove last item")
        self.toggleTimebutton = QPushButton("Incldue time")
        self.saveListButton = QPushButton("Save list")
        self.openFolderButton = QPushButton("Open folder")
        self.input = QLineEdit("")
        self.label = QLabel()
        self.scrollArea = QScrollArea()
        
        #giving the text box a scroll bar
        self.label.setWordWrap(True)
        self.label.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        
        self.scrollArea.setWidget(self.label)
        
        #what happens when the buttons are pressed
        self.button.clicked.connect(self.add_to_list)
        self.clearbutton.clicked.connect(self.clear_list)
        self.removeLineButton.clicked.connect(self.remove_last_line)
        self.toggleTimebutton.setCheckable(True)
        self.toggleTimebutton.setChecked(timeToggled)
        self.toggleTimebutton.clicked.connect(self.toggle_time)
        self.saveListButton.clicked.connect(self.save_list_to_file)
        self.openFolderButton.clicked.connect(self.open_folder)
        self.input.returnPressed.connect(self.add_to_list)
        

        layout1 = QVBoxLayout()
        layout2 = QGridLayout()
        layout3 = QHBoxLayout()
        
        #puts each of the buttons into a grid layout
        layout2.addWidget(self.button,0,0)
        layout2.addWidget(self.clearbutton,0,1)
        layout2.addWidget(self.removeLineButton,1,0)
        layout2.addWidget(self.toggleTimebutton,1,1)
        
        layout3.addWidget(self.saveListButton) 
        layout3.addWidget(self.openFolderButton)
        
        #adds the grid layout to the main vertical layout along with the text box and label
        layout1.addLayout(layout2)
        layout1.addWidget(self.input)
        layout1.addWidget(self.scrollArea) 
        layout1.addLayout(layout3)      
        
        container = QWidget()
        container.setLayout(layout1)
        
        self.setCentralWidget(container)
        
        #load the list from the list.log file
        self.update_list()

    def add_to_list(self):
        with open(list_dir, "a") as f:
            if timeToggled:
                f.write(f"> {self.input.text()}  |  {datetime.datetime.now().strftime("%X")}\n")
            else:
                f.write(f"> {self.input.text()}\n")
            self.input.setText("")
        
        self.update_list()
        
    def clear_list(self):
        with open(list_dir, "w") as f:
            f.write("")
            
        self.update_list()
        
    def remove_last_line(self):
        with open(list_dir, "r") as f:
            lines = f.readlines()
        with open(list_dir, "w") as f:
            f.writelines(lines[:-1])
            
        self.update_list()
        
    def toggle_time(self):
        global timeToggled
        timeToggled = not timeToggled

    def update_list(self):
        with open(list_dir, "r") as f:
            list = f.read()
        self.label.setText(list)
        
    def save_list_to_file(self):
        dlg = QInputDialog()
        dlg.setLabelText("Save file with name:")
        
        clickedButton = dlg.exec()
        if clickedButton == 1:            
            with open(list_dir, 'r') as f:
                file = f.read()
            with open(savedLists_dir / f"{dlg.textValue()}.txt", 'w') as f:
                f.write(file)
                
    def open_folder(self):
        try:
            os.startfile(savedLists_dir)
        except:
            subprocess.run(["xdg-open", savedLists_dir], check=True) 
                   

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()

settings.update({'dateToggle': str(timeToggled)})
with open(config_dir, "w") as f:
    f.write(f"dateToggle = {settings.get('dateToggle')}")
    
print("commit test")