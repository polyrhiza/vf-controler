import sys
from PySide6.QtWidgets import (QDialog, QHBoxLayout, QVBoxLayout, QLabel, QApplication, QComboBox, QWidget,
                               QPushButton, QTextEdit)
from PySide6.QtGui import QFont
import time
import re
import string


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
        # what_to_show_combo_box.addItem('Command History')

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
        show_output_font = QFont('Courier')
        show_output_font.setStyleHint(QFont.Monospace)
        self.show_output.setFont(show_output_font)

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
            show_item = "history"

        print(show_item)
        print(f'{show_item} show' + '\n')

        while self.shell.recv_ready():
            self.shell.recv(4096)

        self.shell.send(f'{show_item} show' + '\n')

        output = ''
        marker = '>'
        start_time = time.time()
        timeout = 15
        quiet_period = 0.1
        last_recv_time = time.time()
        full_command = f'{show_item} show'

        while True:
            while self.shell.recv_ready():
                output += self.shell.recv(4096).decode(errors='ignore')
                last_recv_time = time.time()

            if time.time() - last_recv_time > quiet_period:
                print('No more data to recieve.')
                break

            if time.time() - start_time > timeout:
                print('Timeout waiting for shell')
                print('Timeout output:\n', output)
                break

            time.sleep(0.1)

        print("Raw Output:\n", output)
        print('End Raw Output')

        # CLEAN THE OUTPUT

        # STRIP ANSI CODES
        ansi_codes = re.compile(r'(?:\x1B[@-_][0-?]*[ -/]*[@-~])')
        stripped_output = ansi_codes.sub('', output)
        print(f'Stripped output:\n {stripped_output}')

        stripped_output_lines = []
        for line in stripped_output.splitlines():
            stripped_line = line.rstrip()
            stripped_output_lines.append(stripped_line)


        # for line in stripped_output.splitlines():
        #     cleaned_line = ''
        #     for c in line:
        #         if c in string.printable:
        #             cleaned_line += c
        #         else:
        #             pass
        #     cleaned_line = cleaned_line.rstrip()
        #     stripped_output_lines.append(cleaned_line)

        last_seen_command_idx = 0
        for i, line in enumerate(stripped_output_lines):
            if full_command in line:
                last_seen_command_idx = i + 1

        stripped_output = stripped_output_lines[last_seen_command_idx:]

        last_seen_marker = 0
        for i, line in enumerate(stripped_output):
            if marker in line:
                last_seen_marker = i

        stripped_output = stripped_output[:last_seen_marker]


        # if stripped_output and marker in stripped_output_lines:
        #     stripped_output_lines.pop()

        # stripped_output = stripped_output_lines[last_seen_command_idx:]
        final_output = "\n".join(stripped_output)

        print(f'Final output:\n {final_output}')

        # SET SHOW_OUTPUT AS THE OUTPUT OF THE SHELL
        self.show_output.setText(final_output)

        while self.shell.recv_ready():
            self.shell.recv(4096)

# app = QApplication(sys.argv)
# window = ShowMainWindow()
# window.show()
# sys.exit(app.exec())
