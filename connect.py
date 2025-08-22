from PySide6.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QLabel, QPushButton, QApplication, QWidget, QHBoxLayout
from PySide6.QtCore import QSize, Qt
import sys
from name_save_host import HostNameSaveWindow
import os


class Connect(QDialog):

    def __init__(self):
        super().__init__()

        self.setWindowTitle('Connect')
        self.setMinimumSize(QSize(500, 100))



        ssh_connect_text = QLabel('Connect to Secure Shell')
        host_connect_text = QLabel('Host:')
        self.host_enter = QLineEdit('')
        self.host_enter.setFixedSize(500,30)
        username_connect_text = QLabel('Username:')
        self.username_enter = QLineEdit('')
        self.username_enter.setFixedSize(500,30)
        password_connect_text = QLabel('Password:')
        self.password_enter = QLineEdit('')
        self.password_enter.setFixedSize(500,30)

        #######################################
        #      CONNECT AND SAV LAYOUT         #
        #######################################

        save_connect_widget = QWidget()
        save_connect_layout = QHBoxLayout()

        connect_button = QPushButton('Connect')
        connect_button.clicked.connect(self.send_connection_info)

        save_button = QPushButton('Save')
        save_button.clicked.connect(lambda: self.save_ssh(host=self.host_enter.text(),
                                                  usr=self.username_enter.text(),
                                                  pwd=self.password_enter.text()))

        save_connect_layout.addWidget(connect_button)
        save_connect_layout.addWidget(save_button)
        save_connect_widget.setLayout(save_connect_layout)


        ########################################
        #             SHH INFO                 #
        ########################################

        self.host = ''
        self.username = ''
        self.password = ''

        #######################################
        #            MAIN LAYOUT              #
        #######################################

        main_layout = QVBoxLayout()

        main_layout.addWidget(ssh_connect_text)
        main_layout.addWidget(host_connect_text)
        main_layout.addWidget(self.host_enter)
        main_layout.addWidget(username_connect_text)
        main_layout.addWidget(self.username_enter)
        main_layout.addWidget(password_connect_text)
        main_layout.addWidget(self.password_enter)
        main_layout.addWidget(save_connect_widget)

        self.setLayout(main_layout)

    def send_connection_info(self):
        self.host = self.host_enter.text()
        self.username = self.username_enter.text()
        self.password = self.password_enter.text()

        self.accept()

    def save_ssh(self, host=None, usr=None, pwd=None):
        save_name_dialog = HostNameSaveWindow()
        if save_name_dialog.exec() == QDialog.Accepted:
            save_text = save_name_dialog.GetText()

            save_dir = os.path.expanduser('~/vf-ssh-saves')
            file_path = os.path.join(save_dir, save_text)

            os.makedirs(save_dir, exist_ok=True)

            with open(file_path, "w") as f:
                f.write(host + '\n')
                f.write(usr + '\n')
                f.write(pwd + '\n')








# app = QApplication(sys.argv)
# window = Connect()
# window.show()
# sys.exit(app.exec())