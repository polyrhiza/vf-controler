import sys
from PySide6.QtWidgets import (QDialog, QSlider, QHBoxLayout, QVBoxLayout, QLabel, QApplication, QComboBox, QWidget,
                               QPushButton, QDoubleSpinBox)
from PySide6.QtCore import Qt

class SchedulerMainWindow(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Scheduler')

        self.setMinimumSize(500, 500)

        