import sys
from PySide6.QtWidgets import (QDialog, QSlider, QHBoxLayout, QVBoxLayout, QLabel, QApplication, QComboBox, QWidget,
                               QPushButton, QDoubleSpinBox, QListView)
from PySide6.QtGui import QIcon, QMovie
from PySide6.QtCore import Qt, QSize

class FansMainWindow(QDialog):
    def __init__(self, shell=None):
        super().__init__()

        self.setWindowTitle('Set Fans')

        self.setMinimumSize(500,500)

        self.shell = shell
        #######################################
        #           TOP ROW LAYOUT            #
        #######################################
        top_row_widget = QWidget()
        top_row_layout = QHBoxLayout()


        # COMBO BOX FOR FAN PERCENTAGE
        fan_percentage_combo_box = QComboBox()
        for i in range(0,100):
            fan_percentage_combo_box.addItem(f'{i}%')

        # COMBO BOX FOR CANAL SELECT
        canal_combo_box = QComboBox()
        canal_combo_box.addItem('1.1')
        canal_combo_box.addItem('1.2')
        canal_combo_box.addItem('1.3')
        canal_combo_box.addItem('1.4')
        canal_combo_box.addItem('1.5')
        canal_combo_box.addItem('2.1')
        canal_combo_box.addItem('2.2')
        canal_combo_box.addItem('2.3')
        canal_combo_box.addItem('2.4')
        canal_combo_box.addItem('2.5')
        canal_combo_box.addItem('*')

        # FAN BUTTON
        set_fan_button = QPushButton("")
        set_fan_button.setIcon(QIcon("images/fan.png"))
        set_fan_button.setFixedSize(100, 100)
        set_fan_button.setIconSize(QSize(100, 100))
        set_fan_button.clicked.connect(lambda: self.SetFans(shell=self.shell, fan_speed=fan_percentage_combo_box.currentText(),
                                                    canal=canal_combo_box.currentText()))

        top_row_layout.addWidget(set_fan_button)
        top_row_layout.addWidget(QLabel('Set Fan Percentage:'))
        top_row_layout.addWidget(fan_percentage_combo_box)
        top_row_layout.addWidget(QLabel('For Canal:'))
        top_row_layout.addWidget(canal_combo_box)

        top_row_layout.addStretch(1)
        top_row_widget.setLayout(top_row_layout)



        #######################################
        #             MAIN LAYOUT             #
        #######################################
        # ANIMATED FAN
        animated_fan_label = QLabel(self)
        animated_fan_label.setAlignment(Qt.AlignCenter)

        animated_fan = QMovie('images/rotating_fan.gif')
        animated_fan_label.setMovie(animated_fan)
        animated_fan.start()

        # SETTING LAYOUT
        main_layout = QVBoxLayout()
        main_layout.addWidget(top_row_widget)
        main_layout.addStretch(1)
        main_layout.addWidget(animated_fan_label)

        self.setLayout(main_layout)

    def SetFans(self,shell=None, fan_speed=None, canal=None):
        fan_speed = fan_speed.strip('%')
        canal=canal
        self.shell.send(f'fans set {canal} {canal}' + '\n')

        if self.shell.recv_ready():
            output = self.shell.recv(4096).decode()
            print(output)




# app = QApplication(sys.argv)
# window = FansMainWindow()
# window.show()
# sys.exit(app.exec())