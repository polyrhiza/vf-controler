##########################################
#              GIT HUB TOKEN     #
# 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
###########################################

import paramiko
from PySide6.QtWidgets import QApplication, QPushButton, QMessageBox, QWidget, QMainWindow, QVBoxLayout, QGridLayout
from PySide6.QtCore import QSize, Qt
import sys
from connect import Connect
from connectionMSG import connectionFailed, connectionSecured
import ipaddress
from override_lights import OverrideLights
from fans import FansMainWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("VF Controller")

        # FOR STORING SSH HOST AND LOGIN INFO
        self.host = ''
        self.username = ''
        self.password = ''

        # FOR STORING THE SSH CLIENT AND VIRTUAL SHELL
        self.client = None
        self.shell = None

        self.setMinimumSize(500,500)

        # INITIALISING INITIAL LAYOUT
        self.set_connect_layout()


    def set_connect_layout(self):
        self.connect_layout = ConnectLayout(self.open_connect)
        self.setCentralWidget(self.connect_layout)

    def set_options_layout(self):
        self.main_options_layout = MainOptionsLayout()
        self.setCentralWidget(self.main_options_layout)
        self.resize(self.main_options_layout.sizeHint())


    def open_connect(self):
        connectDialog = Connect()

        if connectDialog.exec():
            self.host = connectDialog.host
            self.username = connectDialog.username
            self.password = connectDialog.password

            self.ssh_connect()

    # THIS IS HERE BECAUSE IF AN IMPROPER HOST IS GIVEN AND PARAMIKO TRIES TO CONNECT IT CRASHES THE PROGRAM (AND MAYBE PYTHON?)
    def validate_host(self, ip):
        try:
            ipaddress.IPv4Address(ip)
            return True
        except ipaddress.AddressValueError:
            return False

    # CONNECT TO SSH
    def ssh_connect(self):

        # CALL VALIDATE_HOST BEFORE PASSING TO PARAMIKO
        if self.validate_host(ip = self.host):
            self.client = paramiko.client.SSHClient()
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            try:
                self.client.connect(hostname=self.host, username=self.username, password=self.password)
                self.shell = self.client.invoke_shell()

                print('Connection Secured')

                connect_success = connectionSecured()
                connect_success.exec()

                self.set_options_layout()

            except Exception as e:
                print('Connection Failed!')

                connect_fail = connectionFailed()
                connect_fail.exec()

        else:

            connect_fail2 = connectionFailed()
            connect_fail2.exec()

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
#                           EDITING LAYOUTS                               #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

# MAIN VF OPTIONS LAYOUT
class MainOptionsLayout(QWidget):
    def __init__(self):
        super().__init__()

        layout = QGridLayout()

        # OVERRIDE LIGHTS BUTTON AND CONNECT
        override_lights_button = QPushButton('Override Lights')
        override_lights_button.setMinimumSize(150,150)

        override_lights_button.clicked.connect(lambda: OverrideLights(shell=main_window.shell).exec())

        scheduler_button = QPushButton('Scheduler')
        scheduler_button.setMinimumSize(150,150)

        # FANS
        fans_button = QPushButton('Fans')
        fans_button.setMinimumSize(150,150)

        fans_button.clicked.connect(lambda: FansMainWindow(shell=main_window.shell).exec())

        # SHOW ALL CONFIGS
        show_button = QPushButton('Show')
        show_button.setMinimumSize(150,150)

        layout.addWidget(override_lights_button, 1,1)
        layout.addWidget(scheduler_button, 1,2)
        layout.addWidget(fans_button, 2,1)
        layout.addWidget(show_button, 2,2)


        self.setLayout(layout)


# STARTING LAYOUT FOR CONNECTING TO VF
class ConnectLayout(QWidget):
    def __init__(self, open_connect):
        super().__init__()

        open_connect = open_connect
        layout = QVBoxLayout()

        connect_button = QPushButton('Connect to VF')
        connect_button.setMinimumSize(200,200)
        connect_button.clicked.connect(open_connect)

        layout.addWidget(connect_button, alignment=Qt.AlignCenter)
        self.setLayout(layout)

app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
sys.exit(app.exec())





