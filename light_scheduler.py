import sys
from PySide6.QtWidgets import (QDialog, QHBoxLayout, QVBoxLayout, QLabel, QApplication, QComboBox, QWidget,
                               QPushButton, QDoubleSpinBox)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PySide6.QtCore import Qt
from light_calculator import LightCalculator

class SchedulerMainWindow(QDialog):
    def __init__(self, shell=None):
        super().__init__()

        self.setWindowTitle('Scheduler')

        self.setMinimumSize(500, 825)

        #######################################
        #  INPUT OUTPUT VALUES FOR PARAMIKO   #
        #######################################

        self.blue = None
        self.green = None
        self.red = None
        self.fr = None

        #######################################
        #          PARAMIKO CLIENT            #
        #######################################

        shell = shell

        #######################################
        #             FIRST ROW               #
        #######################################

        first_row_widget = QWidget()
        first_row_layout = QHBoxLayout()

        select_canal_text = QLabel('Select Canal:')

        select_canal_combo_box = QComboBox()
        select_canal_combo_box.addItem('1.1')
        select_canal_combo_box.addItem('1.2')
        select_canal_combo_box.addItem('1.3')
        select_canal_combo_box.addItem('1.4')
        select_canal_combo_box.addItem('1.5')
        select_canal_combo_box.addItem('2.1')
        select_canal_combo_box.addItem('2.2')
        select_canal_combo_box.addItem('2.3')
        select_canal_combo_box.addItem('2.4')
        select_canal_combo_box.addItem('2.5')

        first_row_layout.addWidget(select_canal_text)
        first_row_layout.addWidget(select_canal_combo_box)
        first_row_layout.addStretch(1)
        first_row_widget.setLayout(first_row_layout)

        #######################################
        #             SECOND ROW              #
        #######################################

        second_row_widget = QWidget()
        second_row_layout = QHBoxLayout()

        select_time_text = QLabel('Set Time:')

        select_hours_combo_box = QComboBox()
        for i in range(1,13):
            if i < 10:
                select_hours_combo_box.addItem('0' + str(i))
            if i >= 10:
                select_hours_combo_box.addItem(str(i))

        hh_text = QLabel('hh :')

        select_minutes_combo_box = QComboBox()
        for i in range(0, 61):
            if i < 10:
                select_minutes_combo_box.addItem('0' + str(i))
            if i >= 10:
                select_minutes_combo_box.addItem(str(i))

        mm_text = QLabel('mm')

        second_row_layout.addWidget(select_time_text)
        second_row_layout.addWidget(select_hours_combo_box)
        second_row_layout.addWidget(hh_text)
        second_row_layout.addWidget(select_minutes_combo_box)
        second_row_layout.addWidget(mm_text)
        second_row_layout.addStretch(1)
        second_row_widget.setLayout(second_row_layout)

        #######################################
        #             THIRD ROW               #
        #######################################

        third_row_widget = QWidget()
        third_row_layout = QHBoxLayout()


        # INPUT OUTPUT COMBO BOX
        self.input_output_combo_box = QComboBox()
        self.input_output_combo_box.addItem('Output')
        self.input_output_combo_box.addItem('Input')
        self.input_output_combo_box.currentTextChanged.connect(self.UpdateSpinboxText)

        third_row_layout.addWidget(self.input_output_combo_box)
        third_row_layout.addWidget(QLabel('Calculate Input or Output:'))
        third_row_layout.addStretch(1)
        third_row_widget.setLayout(third_row_layout)

        #######################################
        #             FOURTH ROW              #
        #######################################

        fourth_row_widget = QWidget()
        fourth_row_layout = QHBoxLayout()

        self.input_output_changeable_label = QLabel('Enter Inputs (Hex):')

        fourth_row_layout.addWidget(self.input_output_changeable_label)
        fourth_row_widget.setLayout(fourth_row_layout)

        #######################################
        #             FIFTH ROW               #
        #######################################

        fifth_row_widget = QWidget()
        fifth_row_layout = QHBoxLayout()

        lights_label = QLabel('Set Lights:')

        # SPIN BOXES FOR INPUTS
        self.blue_input = QDoubleSpinBox()
        self.blue_input.setSingleStep(1.0)
        self.blue_input.setMaximum(255.0)

        self.green_input = QDoubleSpinBox()
        self.green_input.setSingleStep(1.0)
        self.green_input.setMaximum(255.0)

        self.red_input = QDoubleSpinBox()
        self.red_input.setSingleStep(1.0)
        self.red_input.setMaximum(255.0)

        self.fr_input = QDoubleSpinBox()
        self.fr_input.setSingleStep(1.0)
        self.fr_input.setMaximum(255.0)

        set_button = QPushButton('Set')
        set_button.clicked.connect(self.Calculate)

        fifth_row_layout = QHBoxLayout()
        fifth_row_layout.addWidget(QLabel('Blue:'))
        fifth_row_layout.addWidget(self.blue_input)
        fifth_row_layout.addWidget(QLabel('Green:'))
        fifth_row_layout.addWidget(self.green_input)
        fifth_row_layout.addWidget(QLabel('Red:'))
        fifth_row_layout.addWidget(self.red_input)
        fifth_row_layout.addWidget(QLabel('Far Red:'))
        fifth_row_layout.addWidget(self.fr_input)
        fifth_row_layout.addWidget(set_button)
        fifth_row_layout.addStretch(1)
        fifth_row_widget.setLayout(fifth_row_layout)

        #######################################
        #           FIGURE WIDGET             #
        #######################################

        self.plot_widget = QWidget()
        self.plot_layout = QVBoxLayout()
        self.plot_widget.setLayout(self.plot_layout)

        #######################################
        #           TEXT WIDGETS              #
        #######################################
        self.blue_text = QLabel()
        self.green_text = QLabel()
        self.red_text = QLabel()
        self.fr_text = QLabel()

        #######################################
        #         APPLY BUTTON WIDGET         #
        #######################################
        apply_button_widget = QWidget()
        apply_button_layout = QHBoxLayout()

        # SET OVERRIDE LIGHTS BUTTON
        self.apply_button = QPushButton('Set')
        self.apply_button.clicked.connect(lambda: self.Apply(shell=shell, blue=self.blue,
                                                                green=self.green, red=self.red, fr=self.fr,
                                                                canal=select_canal_combo_box.currentText(),
                                                             hh=select_hours_combo_box.currentText(),
                                                             mm=select_minutes_combo_box.currentText()))
        self.apply_button.setVisible(False)


        apply_button_layout.addWidget(self.apply_button)
        apply_button_widget.setLayout(apply_button_layout)

        #######################################
        #            MAIN LAYOUT              #
        #######################################

        main_layout = QVBoxLayout()

        main_layout.addWidget(first_row_widget)
        main_layout.addWidget(second_row_widget)
        main_layout.addWidget(third_row_widget)
        main_layout.addWidget(fourth_row_widget)
        main_layout.addWidget(fifth_row_widget)
        main_layout.addWidget(self.plot_widget)
        main_layout.addWidget(self.blue_text)
        main_layout.addWidget(self.green_text)
        main_layout.addWidget(self.red_text)
        main_layout.addWidget(self.fr_text)
        main_layout.addWidget(apply_button_widget)
        main_layout.addStretch(1)
        self.setLayout(main_layout)

    def UpdateSpinboxText(self, text):

        if text == 'Output':
            self.input_output_changeable_label.setText('Enter Inputs (Hex):')
            self.blue_input.setMaximum(255.0)
            self.green_input.setMaximum(255.0)
            self.red_input.setMaximum(255.0)
            self.fr_input.setMaximum(255.0)

        # HAVE TO FIGURE OUT A WAY TO RETRIEVE THE MAX POSSIBLE LIGHT.
        # DEPENDS ON LIGHT LEAKAGE. SETTING TO 200 FOR NOW.
        if text == 'Input':
            self.input_output_changeable_label.setText('Enter Outputs (PFD):')
            self.blue_input.setMaximum(200.0)
            self.green_input.setMaximum(200.0)
            self.red_input.setMaximum(200.0)
            self.fr_input.setMaximum(200.0)

    def Calculate(self):
        input_output = self.input_output_combo_box.currentText().lower()
        # NEED TO SWITCH IT AROUND BECAUSE OF THE WAY I'VE FRAMED IT HERE. IS BETTER THAN IN THE LIGHT CALC.
        if input_output == 'output':
            input_output = 'input'
        elif input_output == 'input':
            input_output = 'output'

        blue = self.blue_input.value()
        green = self.green_input.value()
        red = self.red_input.value()
        fr = self.fr_input.value()

        light_calc = LightCalculator(input_output=input_output, blue=blue, green=green, red=red, fr=fr)

        for i in reversed(range(self.plot_layout.count())):
            self.plot_layout.itemAt(i).widget().setParent(None)

        # SETTING UP FIGURE CANVAS AND MAKING IT WHITE
        canvas = FigureCanvas(light_calc.figure)
        canvas.setStyleSheet("background:transparent;")
        canvas.setAttribute(Qt.WA_TranslucentBackground, True)
        canvas.figure.patch.set_alpha(0)
        canvas.figure.axes[0].patch.set_alpha(0)
        canvas.figure.axes[0].title.set_color("white")
        canvas.figure.axes[0].xaxis.label.set_color("white")
        canvas.figure.axes[0].yaxis.label.set_color("white")
        canvas.figure.axes[0].tick_params(colors="white")
        ax = canvas.figure.axes[0]
        for spine in ax.spines.values():  # axis borders
            spine.set_edgecolor("white")

        canvas.draw()
        self.plot_layout.addWidget(canvas)

        # UPDATING TEXT QLABEL WIDGETS
        self.blue_text.setText(light_calc.blue_text)
        self.green_text.setText(light_calc.green_text)
        self.red_text.setText(light_calc.red_text)
        self.fr_text.setText(light_calc.fr_text)

        # SET OVERRIDE BUTTON VISIBLE
        self.apply_button.setVisible(True)
        self.apply_button.setVisible(True)

        # STORING VALUES
        # THIS IS AS PER THE STARTING IF STATEMENT SO IF == INPUT THEN WE ARE CALCULATING OUTPUT
        if input_output == 'input':
            self.blue = blue
            self.green = green
            self.red = red
            self.fr = fr

        if input_output == 'output':
            blue = light_calc.blue_input
            green = light_calc.green_input
            red = light_calc.red_input
            fr = light_calc.fr

    def Apply(self, shell=None, blue=None, green=None, red=None, fr=None, canal=None, hh=None, mm=None):

        shell = shell
        shell.send(f'scheduler lights add {hh} {mm} {canal} [{int(red)},{int(green)},{int(blue)},{int(fr)}, 0]' + '\n')

        if shell.recv_ready():
            output = shell.recv(4096).decode()
            print(output)


# app = QApplication(sys.argv)
# window = SchedulerMainWindow()
# window.show()
# sys.exit(app.exec())