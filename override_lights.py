import sys
from PySide6.QtWidgets import QDialog, QSlider, QHBoxLayout, QVBoxLayout, QLabel, QApplication, QComboBox, QWidget,\
    QLineEdit, QPushButton, QDoubleSpinBox, QSizePolicy
from light_calculator import LightCalculator
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
# import pyqtgraph as pg

class OverrideLights(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Set Override Lights')

        self.setMinimumSize(500,500)

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

        #######################
        # MAIN LAYOUT SETTING #
        #######################
        self.input_output_changeable_label = QLabel('Enter Inputs (Hex)')

        main_layout = QVBoxLayout()
        main_layout.addWidget(input_output_widget)
        main_layout.addWidget(self.input_output_changeable_label)
        main_layout.addWidget(light_channel_input_widget)
        main_layout.addWidget(self.plot_widget)
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

        canvas = FigureCanvas(light_calc.figure)
        self.plot_layout.addWidget(canvas)
        canvas.draw()

app = QApplication(sys.argv)
window = OverrideLights()
window.show()
sys.exit(app.exec())
