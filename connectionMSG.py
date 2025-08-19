from PySide6.QtWidgets import QDialog, QPushButton, QVBoxLayout, QLabel
from PySide6.QtCore import Qt, QSize

class connectionFailed(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('ERROR')
        self.setFixedSize(QSize(350, 100))

        self.error_text = QLabel('Failed to Connect! Retry Login.')
        self.close_button = QPushButton('Close')
        self.close_button.clicked.connect(self.close_this)

        layout = QVBoxLayout()
        layout.addWidget(self.error_text, alignment=Qt.AlignCenter)
        layout.addWidget(self.close_button, alignment=Qt.AlignCenter)

        self.setLayout(layout)

    def close_this(self):
        self.accept()

class connectionSecured(QDialog):
    def __init__(self):
        super().__init__()

        self.setFixedSize(QSize(350,100))
        self.setWindowTitle('Connected')

        self.front_text = QLabel('Connection Secured!')
        self.close_button = QPushButton('Close')
        self.close_button.clicked.connect(self.close_this)

        layout = QVBoxLayout()
        layout.addWidget(self.front_text, alignment=Qt.AlignCenter)
        layout.addWidget(self.close_button, alignment=Qt.AlignCenter)

        self.setLayout(layout)


    def close_this(self):
        self.accept()
