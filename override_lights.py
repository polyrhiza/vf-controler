import sys
from PySide6.QtWidgets import QDialog, QSlider, QHBoxLayout, QVBoxLayout, QLabel, QApplication, QComboBox, QWidget,\
    QLineEdit, QPushButton, QDoubleSpinBox, QSizePolicy
from PySide6.QtCore import Qt
from light_calculator import LightCalculator
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import paramiko
# import pyqtgraph as pg

class OverrideLights(QDialog):
    def __init__(self, shell=None):
        super().__init__()

        self.setWindowTitle('Set Override Lights')

        self.setMinimumSize(500,500)

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

        self.shell = shell

        # SETTING LAYOUT

        ################################
        # TOP ROW LAYOUT FOR COMBO BOX #
        ################################
        input_output_widget = QWidget()

        self.input_output_combo_box = QComboBox()
        self.input_output_combo_box.addItem('Output')
        self.input_output_combo_box.addItem('Input')
        self.input_output_combo_box.currentTextChanged.connect(self.update_spinbox_limits)

        input_output_layout = QHBoxLayout()
        input_output_layout.addWidget(QLabel('Calculate Input or Output'))
        input_output_layout.addWidget(self.input_output_combo_box)
        input_output_layout.addStretch(1)

        input_output_widget.setLayout(input_output_layout)

        #######################################
        # BLUE GREEN RED FAR RED INPUT WIDGET #
        #######################################
        light_channel_input_widget = QWidget()

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
        set_button.clicked.connect(self.calculate)

        light_channel_input_layout = QHBoxLayout()
        light_channel_input_layout.addWidget(QLabel('Blue:'))
        light_channel_input_layout.addWidget(self.blue_input)
        light_channel_input_layout.addWidget(QLabel('Green:'))
        light_channel_input_layout.addWidget(self.green_input)
        light_channel_input_layout.addWidget(QLabel('Red:'))
        light_channel_input_layout.addWidget(self.red_input)
        light_channel_input_layout.addWidget(QLabel('Far Red:'))
        light_channel_input_layout.addWidget(self.fr_input)
        light_channel_input_layout.addWidget(set_button)

        light_channel_input_widget.setLayout(light_channel_input_layout)

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
        #        SET OVERRIDE BUTTON          #
        #######################################
        self.set_override_button =  QPushButton('Override')
        self.set_override_button.clicked.connect(lambda: self.override(self.shell, self.blue, self.green, self.red, self.fr))
        self.set_override_button.setVisible(False)

        #######################
        # MAIN LAYOUT SETTING #
        #######################
        self.input_output_changeable_label = QLabel('Enter Inputs (Hex)')

        main_layout = QVBoxLayout()
        main_layout.addWidget(input_output_widget)
        main_layout.addWidget(self.input_output_changeable_label)
        main_layout.addWidget(light_channel_input_widget)
        main_layout.addWidget(self.plot_widget)
        main_layout.addWidget(self.blue_text)
        main_layout.addWidget(self.green_text)
        main_layout.addWidget(self.red_text)
        main_layout.addWidget(self.fr_text)
        main_layout.addWidget(self.set_override_button)
        main_layout.addStretch(1)
        self.setLayout(main_layout)

    def update_spinbox_limits(self, text):

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


    def calculate(self):
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
        self.set_override_button.setVisible(True)

        # STORING VALUES
        # THIS IS AS PER THE STARTING IF STATEMENT SO IF == INPUT THEN WE ARE CALCULATING OUTPUT
        if input_output == 'input':
            self.blue = blue
            self.green = green
            self.red = red
            self.fr = fr

        if input_output== 'output':
            self.blue = light_calc.blue_input
            self.green = light_calc.green_input
            self.red = light_calc.red_input
            self.fr = light_calc.fr

    def override(self,shell, blue, green, red, fr):
        self.shell.send(f'lights override-set 2.2 [{int(red)},{int(green)},{int(blue)},{int(fr)}, 0]' + '\n')
        print(f'lights override-set 2.2 [{red},{green},{blue},{fr}, 0]' + '\n')
        if self.shell.recv_ready():
            output = self.shell.recv(4096).decode()
            print(output)


# app = QApplication(sys.argv)
# window = OverrideLights()
# window.show()
# sys.exit(app.exec())
