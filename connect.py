from PySide6.QtWidgets import QDialog, QVBoxLayout, QTextEdit, QLabel, QPushButton
from PySide6.QtCore import QSize


class Connect(QDialog):

    def __init__(self):
        super().__init__()

        self.setWindowTitle('Connect')
        self.setMinimumSize(QSize(500, 100))

        layout = QVBoxLayout()

        ssh_connect_text = QLabel('Connect to Secure Shell')
        host_connect_text = QLabel('Host:')
        self.host_enter = QTextEdit('')
        self.host_enter.setFixedSize(500,30)
        username_connect_text = QLabel('Username:')
        self.username_enter = QTextEdit('')
        self.username_enter.setFixedSize(500,30)
        password_connect_text = QLabel('Password:')
        self.password_enter = QTextEdit('')
        self.password_enter.setFixedSize(500,30)
        self.connect_button = QPushButton('Connect')
        self.connect_button.clicked.connect(self.send_connection_info)

        self.host = ''
        self.username = ''
        self.password = ''


        layout.addWidget(ssh_connect_text)
        layout.addWidget(host_connect_text)
        layout.addWidget(self.host_enter)
        layout.addWidget(username_connect_text)
        layout.addWidget(self.username_enter)
        layout.addWidget(password_connect_text)
        layout.addWidget(self.password_enter)
        layout.addWidget(self.connect_button)

        self.setLayout(layout)

    def send_connection_info(self):
        self.host = self.host_enter.toPlainText()
        self.username = self.username_enter.toPlainText()
        self.password = self.password_enter.toPlainText()

        self.accept()

