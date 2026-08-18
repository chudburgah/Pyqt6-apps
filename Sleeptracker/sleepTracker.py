from PyQt6.QtWidgets import *
import json
import datetime
from pathlib import Path
script_dir = Path(__file__).resolve().parent

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Sleep tracker")
        self.setMinimumSize(200,150)