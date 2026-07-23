from PyQt6.QtWidgets import *; from PyQt6.QtCore import *; from PyQt6.QtGui import *
import subprocess; from pathlib import Path
import datetime
import sys
import os


#make sure the files and folders actually exists
if not os.path.exists("listAppConfig"):
    os.mkdir("listAppConfig")
if not os.path.exists("savedLists"):
    os.mkdir("savedLists")

with open(Path("listAppConfig") / "list.log", "a"):
    pass
with open(Path("listAppConfig") / "config.txt", "a"):
    pass

settings = {}
timeToggled = bool()

with open(Path("listAppConfig") / "config.txt", "r") as file:
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

        # 1. Get the directory where this script lives
        basedir = Path(__file__).resolve().parent
        
        # 2. Construct the path to the icon in the subfolder
        icon_path = basedir / "listAppConfig" / "thomasfolk.jpg"
        
        # 3. Set the icon
        self.setWindowIcon(QIcon(str(icon_path)))

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
        with open(Path("listAppConfig") / "list.log", "a") as f:
            if timeToggled:
                f.write(f"> {self.input.text()}  |  {datetime.datetime.now().strftime("%X")}\n")
            else:
                f.write(f"> {self.input.text()}\n")
            self.input.setText("")
        
        self.update_list()
        
    def clear_list(self):
        with open(Path("listAppConfig") / "list.log", "w") as f:
            f.write("")
            
        self.update_list()
        
    def remove_last_line(self):
        with open(Path("listAppConfig") / "list.log", "r") as f:
            lines = f.readlines()
        with open(Path("listAppConfig") / "list.log", "w") as f:
            f.writelines(lines[:-1])
            
        self.update_list()
        
    def toggle_time(self):
        global timeToggled
        timeToggled = not timeToggled

    def update_list(self):
        with open(Path("listAppConfig") / "list.log", "r") as f:
            list = f.read()
        self.label.setText(list)
        
    def save_list_to_file(self):
        dlg = QInputDialog()
        dlg.setLabelText("Save file with name:")
        
        clickedButton = dlg.exec()
        if clickedButton == 1:            
            with open(Path("listAppConfig") / "list.log", 'r') as f:
                file = f.read()
            with open(Path("savedLists") / f"{dlg.textValue()}.txt", 'w') as f:
                f.write(file)
                
    def open_folder(self):
        dir = Path("savedLists")
        try:
            os.startfile(dir)
        except:
            subprocess.run(["xdg-open", dir], check=True) 
                   

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()

settings.update({'dateToggle': str(timeToggled)})
with open(Path("listAppConfig") / "config.txt", "w") as f:
    f.write(f"dateToggle = {settings.get('dateToggle')}")
