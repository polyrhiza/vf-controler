import sys
from PySide6.QtWidgets import (QDialog, QHBoxLayout, QVBoxLayout, QLabel, QApplication, QComboBox, QWidget,
                               QPushButton, QTextEdit)
from PySide6.QtGui import QFont
import time
import re


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

        # SECOND ROW IS IN MAIN LAYOUT AND IS THE TEXT OUTPUT - I DONT KNOW WHY I DID THIS

        third_row_widget = QWidget()
        third_row_layout = QHBoxLayout()

        self.remove_schedule_text = QLabel('To Remove a Light Schedule Select a Job:')
        self.remove_schedule_text.setVisible(False)

        self.job_select_combo_box = QComboBox()
        self.job_select_combo_box.setVisible(False)

        third_row_layout.addWidget(self.remove_schedule_text)
        third_row_layout.addWidget(self.job_select_combo_box)
        third_row_widget.setLayout(third_row_layout)

        #######################################
        #             FOURTH ROW               #
        #######################################

        fourth_row_widget = QWidget()
        fourth_row_layout = QHBoxLayout()

        self.remove_job_button = QPushButton()
        self.remove_job_button.setVisible(False)

        fourth_row_layout.addWidget(self.remove_job_button)
        fourth_row_widget.setLayout(fourth_row_layout)

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
        main_layout.addWidget(third_row_widget)
        main_layout.addWidget(fourth_row_widget)
        main_layout.addStretch(1)

        self.setLayout(main_layout)

    def Show(self, show_item=None):

        show_item = show_item.lower()

        if show_item == "light schedules":
            show_item = "scheduler lights"

        if show_item == "command history":
            show_item = "history"

        # DUMP PREVIOUS RETRIEVALS STILL SITTING IN LIMBO
        while self.shell.recv_ready():
            self.shell.recv(4096)

        # SEND COMMAND
        self.shell.send(f'{show_item} show' + '\n')

        output = ''
        marker = '>'
        start_time = time.time()
        timeout = 15
        quiet_period = 0.1
        last_recv_time = time.time()
        full_command = f'{show_item} show'

        # LOOP FOR RETRIEVING OUTPUT
        while True:
            # CONTINUE TO LOOP WHILE THE SHELL IS READY
            while self.shell.recv_ready():
                output += self.shell.recv(4096).decode(errors='ignore')
                last_recv_time = time.time()

            # IF RECV_READY IS SHOWING FALSE FOR A SHORT PERIOD THE LOOP IS BROKEN I.E. NO MORE DATA TO RETRIEVE
            if time.time() - last_recv_time > quiet_period:
                print('No more data to recieve.')
                break

            # IF AN ERROR OCCURS AND RECV_READY IS STUCK IN TRUE TIMES OUT AFTER 15 SECONDS
            if time.time() - start_time > timeout:
                print('Timeout waiting for shell')
                print('Timeout output:\n', output)
                break

            time.sleep(0.1)


        # STRIP ANSI CODES
        ansi_codes = re.compile(r'(?:\x1B[@-_][0-?]*[ -/]*[@-~])')
        stripped_output = ansi_codes.sub('', output)
        print(f'Stripped output:\n {stripped_output}')

        # STRIPPING UNECESSARY SPACES AT END OF LINES
        stripped_output_lines = []
        for line in stripped_output.splitlines():
            stripped_line = line.rstrip()
            stripped_output_lines.append(stripped_line)

        # THE SENT COMMAND SEES THE INITIAL SHELL PROMPT AND SENT COMMAND. THIS FINDS ITS INDEX
        last_seen_command_idx = 0
        for i, line in enumerate(stripped_output_lines):
            if full_command in line:
                last_seen_command_idx = i + 1

        # THIS REMOVES THE INITIAL SHELL PROMPT FORM THE OUTPUT
        stripped_output = stripped_output_lines[last_seen_command_idx:]

        # THE OUTPUT ALSO CONTAINS THE SHELL PROMPT THAT APPEARS AFTER THE OUTPUT. THIS FINDS ITS INDEX
        last_seen_marker = 0
        for i, line in enumerate(stripped_output):
            if marker in line:
                last_seen_marker = i

        # THIS REMOVES ITS INDEX
        stripped_output = stripped_output[:last_seen_marker]

        # JOINS BACK TOGETHER LINES
        final_output = "\n".join(stripped_output)

        print(f'Final output:\n {final_output}')

        # SET SHOW_OUTPUT AS THE OUTPUT OF THE SHELL
        self.show_output.setText(final_output)

        # ANOTHING DUMPING OF WAITING DATA. JUST INCASE.
        while self.shell.recv_ready():
            self.shell.recv(4096)

        # SEND TO THE FUNCTION THAT REMOVES A JOB.
        if show_item == 'scheduler lights':
            self.CaptureJobs(output=final_output)

    def CaptureJobs(self, output=None):

        # SETTING OPTIONS AS VISIBLE
        self.remove_schedule_text.setVisible(True)
        self.job_select_combo_box.setVisible(True)
        self.remove_job_button.setVisible(True)

        lines = output.splitlines()

        jobs = []
        for line in lines:
            match = re.match(r'^(Job \d+)', line)
            if match:
                jobs.append(match.group(1))

        for i in jobs:
            self.job_select_combo_box.addItem(i)

        self.remove_job_button.clicked.connect(self.RemoveLightSchedule)

    def RemoveLightSchedule(self):

        job = self.job_select_combo_box.currentText()

        job_match = re.match(r'^Job (\d+)', job)

        if job_match:
            job_id = job_match.group(1)

        self.shell.send(f'scheduler lights remove {job_id}' + '\n')



# app = QApplication(sys.argv)
# window = ShowMainWindow()
# window.show()
# sys.exit(app.exec())
