import sys
from PySide6.QtWidgets import (QDialog, QHBoxLayout, QVBoxLayout, QLabel, QApplication, QComboBox, QWidget,
                               QPushButton, QTextEdit)

class ShowMainWindow(QDialog):
    def __init__(self, shell=None):
        super().__init__()

        self.setWindowTitle('Show/Remove')

        self.setMinimumSize(500, 500)

        self.shell = shell

        #######################################
        #             FIRST ROW               #
        #######################################

        first_row_widget = QWidget()
        first_row_layout = QHBoxLayout()

        what_to_show_text = QLabel('What do you want to show?')

        what_to_show_combo_box = QComboBox()
        what_to_show_combo_box.addItem('Light Schedules')
        what_to_show_combo_box.addItem('Lights')
        what_to_show_combo_box.addItem('Fans')
        what_to_show_combo_box.addItem('Nozzles')
        what_to_show_combo_box.addItem('Command History')

        show_button = QPushButton('Show')
        show_button.clicked.connect(lambda: self.Show(show_item=what_to_show_combo_box.currentText()))

        first_row_layout.addWidget(what_to_show_text)
        first_row_layout.addWidget(what_to_show_combo_box)
        first_row_layout.addWidget(show_button)
        first_row_layout.addStretch(1)
        first_row_widget.setLayout(first_row_layout)

        #######################################
        #             THIRD ROW               #
        #######################################

        # SECOND ROW IS IN MAIN LAYOUT AND IS THE TEXT OUTPUT


        #######################################
        #            MAIN LAYOUT              #
        #######################################

        self.show_output = QTextEdit()
        self.show_output.setReadOnly(True)

        main_layout = QVBoxLayout()
        main_layout.addWidget(first_row_widget)
        main_layout.addWidget(self.show_output)
        main_layout.addStretch(1)

        self.setLayout(main_layout)

    def Show(self, show_item=None):

        show_item = show_item.lower()

        if show_item == "light schedules":
            show_item = "scheduler lights"

        if show_item == "command history":
            show_item = "history show"

        self.shell.send(f'{show_item} show' + '\n')

        if self.shell.recv_ready():
            output = self.shell.recv(4096).decode()
            print(output)

        # SET SHOW_OUTPUT AS THE OUTPUT OF THE SHELL
        self.show_output.setText(output)


# app = QApplication(sys.argv)
# window = ShowMainWindow()
# window.show()
# sys.exit(app.exec())