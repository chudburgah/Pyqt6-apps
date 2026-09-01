from PyQt6.QtWidgets import *; from PyQt6.QtCore import *
import json
import datetime
from pathlib import Path
import sys
script_dir = Path(__file__).resolve().parent

#attempts to open the file. If it is empty or doesn't exsist it creates the formatted json
with open(script_dir/"sleepHours.json", "a"):
    pass
with open(script_dir/"sleepHours.json", "r") as f:
    if f.read() == "":
        with open(script_dir/"sleepHours.json", "a") as f:
                f.write('''{
    "Current_week": {
        "0": null,
        "1": null,
        "2": null,
        "3": null,
        "4": null,
        "5": null,
        "6": null,
        "week_number": null
    },
    "Previous_week": {
        "0": null,
        "1": null,
        "2": null,
        "3": null,
        "4": null,
        "5": null,
        "6": null,
        "week_number": null
    },
    "Total_hours": 0
}''')

#initialize the window 
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        #Set the window title and the size of the window
        self.setWindowTitle("Sleep Tracker")
        self.resize(200,300)
        
        #Creates the buttons, label, and table
        self.addSleep_b = QPushButton("Add sleep")
        self.totalSeep_b = QPushButton("Total hours slept")
        self.table = QTableWidget(7, 2)
        self.dateLabel = QLabel()
        
        #Update contents and alingment of the 'hours slept this week' label
        self.hours_slept()
        self.dateLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        #Set flags (no scroll bar, max height, etc.)
        self.table.setHorizontalHeaderLabels(["Day", "Hours"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setFixedWidth(150)
        self.table.setMaximumHeight(230)
        self.table.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        
        #Make the buttons do stuff when you press them 
        self.addSleep_b.clicked.connect(self.Add_Sleep)
        self.totalSeep_b.clicked.connect(self.Total_Sleep)
        
        #Updates vars so the program can read and edit the json file
        self.Update_JSON(1), self.Update_JSON(2)
        
        days = ["Sun", "Mon", "Tus", "Wed", "Thu", "Fri", "Sat"]
        
        #Populate the table with json data
        for i in range(7):
            index_val = self.json_data["Current_week"][str(i)]
            self.table.setItem(i, 0, QTableWidgetItem(days[i]))
            self.table.setItem(i, 1, QTableWidgetItem(str(index_val)))
        
        #Layouts to structure the visual elements  
        layout1 = QVBoxLayout()
        layout2 = QHBoxLayout()
        layout3 = QVBoxLayout()
        
        layout3.addWidget(self.dateLabel)
        layout3.addWidget(self.addSleep_b)
        
        layout2.addWidget(self.table)
        layout2.addLayout(layout3)
        
        layout1.addLayout(layout2)
        layout1.addWidget(self.totalSeep_b)
        
        #Create a widget with all the nested layouts inside and make it the central widget so we can see it
        contianer = QWidget()
        contianer.setLayout(layout1)
        self.setCentralWidget(contianer)

    #Calculates the total hours slept by comparing the difference 
    def hours_slept(self):
        self.Update_JSON(1)
        numb = 0
        for i in range(7):
            try:
                self.json_data["Current_week"][str(i)] >= 0
                numb += self.json_data["Current_week"][str(i)]
            except:
                pass
        self.dateLabel.setText(f'''
        Today is {datetime.datetime.now().strftime("%A")}
        Total hours slept this week {numb}''')
    
    def Update_JSON(self, new_old):
        if new_old == 1:
            with open(script_dir/"sleepHours.json", 'r') as json_file:
                self.json_data = json.load(json_file)
            return(self.json_data) 
        elif new_old == 2:
            with open(script_dir/"sleepHours.json", 'r') as json_file:
                    self.json_old = json.load(json_file)
            return(self.json_old)    
    
    def Add_Sleep(self):
        dlg = QInputDialog()
        dlg.setLabelText("How many hours did you sleep:")
        
        if dlg.exec():
            try:
                self.table.setItem(int(datetime.datetime.now().strftime("%w")), 1, QTableWidgetItem(str(int(dlg.textValue()))))
                
                self.json_data["Current_week"][datetime.datetime.now().strftime("%w")] = int(dlg.textValue())
                with open(script_dir/"sleepHours.json", 'w') as json_file:
                    json.dump(self.json_data, json_file, indent=4)
            except:
                print("Invalid input")
        self.hours_slept()
    
    def Total_Sleep(self):
        dlg = QMessageBox()
        self.Update_JSON(1)
        
        for i in range(7):
            if self.json_old["Current_week"][str(i)] != self.json_data["Current_week"][str(i)]:
                try:
                    old = int(self.json_old["Current_week"][str(i)])
                except:
                    old = 0
                new = int(self.json_data["Current_week"][str(i)])
                self.Update_JSON(2)
                self.json_data["Total_hours"] += new-old
                with open(script_dir/"sleepHours.json", 'w') as json_file:
                    json.dump(self.json_data, json_file, indent=4)
        self.Update_JSON(1)
        
        dlg.setText(f"Total hours slept {self.json_data["Total_hours"]}")
        dlg.exec()        
            
app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()

with open(script_dir/"sleepHours.json", "r") as json_file:
    json_data = json.load(json_file)
    if json_data["Current_week"]["week_number"] != int(datetime.datetime.now().strftime("%U")):
        for i in range(7):
            try:
                json_data["Current_week"][str(i)] >= 0
                numb += json_data["Current_week"][str(i)]
            except:
                pass
        with open(script_dir/"sleepHours.json", "w") as json_file0:
            json_data["Current_week"]["week_number"] = int(datetime.datetime.now().strftime("%U"))
            json.dump(json_data, json_file0, indent=4)
        print("changed week")