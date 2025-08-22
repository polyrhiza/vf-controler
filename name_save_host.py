from PySide6.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QLabel, QPushButton, QApplication
import sys
from PySide6.QtCore import QSize

class HostNameSaveWindow(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Save')
        self.setFixedSize(QSize(350,100))

        main_layout = QVBoxLayout()

        enter_name_text = QLabel('Enter Name of Host to Save As:')

        self.name_enter = QLineEdit()

        save_button = QPushButton('Save')
        save_button.clicked.connect(self.accept)

        main_layout.addWidget(enter_name_text)
        main_layout.addWidget(self.name_enter)
        main_layout.addWidget(save_button)
        self.setLayout(main_layout)

    def GetText(self):
        return self.name_enter.text()


# app = QApplication(sys.argv)
# window = HostNameSaveWindow()
# window.show()
# sys.exit(app.exec())