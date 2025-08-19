import matplotlib.pyplot as plt


class LightCalculator():
    def __init__(self, input_output, red=None, green=None, blue=None, fr=None):

        ###############################################
        # INPUT = INPUT INTO SYSTEM.     OUTPUT = PPFD
        ###############################################
        if input_output not in ['input', 'output']:
            raise ValueError('Input_output must be either "input" or "output"')

        self.input_output = input_output

        # Intialising inputs/outputs
        self.red = red
        self.green = green
        self.blue = blue
        self.fr = fr

        # Slopes and Intercepts
        self.red_slope = 1.6050835691635004
        self.red_intercept = -1.597644104176652

        self.green_slope = 4.74224485
        self.green_intercept = -3.05396698

        self.blue_slope = 2.90036752
        self.blue_intercept = -2.5590344

        self.fr_slope = 4.16448387
        self.fr_intercept = -4.18764624

        self.fr_red_leak_slope = 75.6369857400261
        self.fr_red_leak_intercept = -6.186891349720568

        self.green_red_leak_slope = 12.770559424457426
        self.green_red_leak_intercept = -2.3123216648046423

        self.green_blue_leak_slope = 52.72278614
        self.green_blue_leak_intercept = -2.5590344

        #####################################################
        # OUTPUTS: WHAT WILL BE EMITED FROM A SPECIFIED INPUT
        #####################################################
        self.red_output = 0
        self.green_output = 0
        self.blue_output = 0
        self.fr_output = 0

        self.fr_red_leak_output = None
        self.green_red_leak_output = None
        self.green_blue_leak_output = None

        #####################################################
        # INPUTS: WHAT HEX TO INPUT TO GET SPECIFIED OUTPUT
        #####################################################
        self.red_input = 0
        self.green_input = 0
        self.blue_input = 0
        self.fr_input = 0

        self.figure, self.ax = plt.subplots(figsize=(5, 4))

        self.input_or_output()

    def input_or_output(self):
        if self.input_output == 'input':
            self.check_inputs()
        if self.input_output == 'output':
            self.check_outputs()

    ######################################
    # CALCULATE OUTPUTS FROM GIVEN INPUTS
    ######################################

    # CHANGING SO ALL ARE CALLED AT THE SAME TIME AND OUTPUTS ARE CALUCULATED ENTIRELY IN THEIR RESPECTIVE ZONE.
    def check_inputs(self):

        self.red_calc_output()

        self.green_calc_output()

        self.blue_calc_output()

        self.fr_calc_output()

        self.printing_outputs()
        self.plotting()

    ######################################
    # CALCULATE RED OUTPUT
    ######################################
    def red_calc_output(self):

        # MAIN RED CHANNEL
        if self.red is not None and self.red != 0:
            self.red_output = (self.red - self.red_intercept) / self.red_slope
        elif self.red is None or self.red == 0:
            self.red_output = 0

        # RED LEAKAGE FROM FAR RED CHANNEL
        if self.fr is not None and self.fr != 0:
            self.fr_red_leak_output = (self.fr - self.fr_red_leak_intercept) / self.fr_red_leak_slope
            self.red_output += self.fr_red_leak_output

        # RED LEAKAGE FROM GREEN CHANNEL
        if self.green is not None and self.green != 0:
            self.green_red_leak_output = (self.green - self.green_red_leak_intercept) / self.green_red_leak_slope
            self.red_output += self.green_red_leak_output

    ######################################
    # CALCULATE GREEN OUTPUT
    ######################################
    def green_calc_output(self):

        # MAIN CHANNEL
        if self.green is not None and self.green != 0:
            self.green_output = (self.green - self.green_intercept) / self.green_slope

        elif self.green is None or self.green == 0:
            self.green_output = 0

    ######################################
    # CALCULATE BLUE OUTPUT
    ######################################
    def blue_calc_output(self):

        # MAIN CHANNEL
        if self.blue is not None and self.blue != 0:
            self.blue_output = (self.blue - self.blue_intercept) / self.blue_slope
        elif self.blue is None or self.blue == 0:
            self.blue_output = 0

        # BLUE LEAKAGE FROM GREEN CHANNEL
        if self.green is not None and self.green != 0:
            self.green_blue_leak_output = (self.green - self.green_blue_leak_intercept) / self.green_blue_leak_slope
            self.blue_output = self.blue_output + self.green_blue_leak_output

    ######################################
    # CALCULATE FAR RED OUTPUT
    ######################################
    def fr_calc_output(self):

        # MAIN CHANNEL
        if self.fr is not None and self.fr != 0:
            self.fr_output = (self.fr - self.fr_intercept) / self.fr_slope
        if self.fr is None or self.fr == 0:
            self.fr_output = 0

    ######################################
    # PRINTING OUTPUTS
    ######################################
    def printing_outputs(self):

        # RED PRINT IF RED != 0
        if self.red is not None and self.red != 0:
            red_text = f'Red output (input: {self.red}): {round(self.red_output, 2)} umol/m2/s'

            if self.green is not None and self.green != 0:
                green_text = f', {round((self.green - self.green_red_leak_intercept) / self.green_red_leak_slope, 2)} umol/m2/s from Green leak'
                red_text += green_text

            if self.fr is not None and self.fr != 0:
                fr_text = f', {round((self.fr - self.fr_red_leak_intercept) / self.fr_red_leak_slope, 2)} umol/m2/s from Far Red leak'
                red_text += fr_text

            print(red_text)

        # RED PRINT IF RED == 0 THIS IS THE SAME AS ABOVE... COULD OPTIMISE THIS SOMEHOW BUT GONNA LEAVE IT FOR NOW
        if self.red is None or self.red == 0:

            red_text = f'Red output (input: {self.red}): {round(self.red_output, 2)} umol/m2/s'

            if self.green is not None and self.green != 0:
                green_text = f', {round((self.green - self.green_red_leak_intercept) / self.green_red_leak_slope, 2)} umol/m2/s from Green leak'
                red_text += green_text

            if self.fr is not None and self.fr != 0:
                fr_text = f', {round((self.fr - self.fr_red_leak_intercept) / self.fr_red_leak_slope, 2)} umol/m2/s from Far Red leak'
                red_text += fr_text

            print(red_text)

        # BLUE PRINT IF BLUE IS != 0
        if self.blue is not None and self.blue != 0:
            blue_text = f'Blue output (input: {self.blue}): {round(self.blue_output, 2)} umol/m2/s'

            if self.green is not None and self.green != 0:
                green_text = f', {round((self.green - self.green_blue_leak_intercept) / self.green_blue_leak_slope, 2)} umol/m2/s from Green leak'
                blue_text += green_text

        # BLUE PRINT IF BLUE IS == 0
        if self.blue is None or self.blue == 0:
            blue_text = f'Blue output (input: {self.blue}): {round(self.blue_output, 2)} umol/m2/s'

            if self.green is not None and self.green != 0:
                green_text = f', {round((self.green - self.green_blue_leak_intercept) / self.green_blue_leak_slope, 2)} umol/m2/s from Green leak'
                blue_text += green_text

            print(blue_text)

        print(f'Green output (input: {self.green}):', round(self.green_output, 2), 'umol/m2/s')
        print(f'Far Red out (input: {self.fr}):', round(self.fr_output, 2), 'umol/m2/s')

    #######################################################################################################
    #######################################################################################################

    ######################################
    # CALCULATE INPUTS FROM GIVEN OUTPUTS
    ######################################

    # Check output values and pass to input calculators
    def check_outputs(self):

        self.red_calc_input()

        self.green_calc_input()

        self.blue_calc_input()

        self.fr_calc_input()

        self.printing_inputs()

        self.plotting()

    ######################################
    # CALCULATE RED INPUT FROM RED OUTPUT
    ######################################

    # THIS IS FAR MORE DIFFICULT TO CALCULATE DUE TO LEAKAGES. HOW MUCH LEAKAGE SHOULD COME FROM WHAT CHANNEL. I THINK THE BEST WAY IS TO FIRST CHECK WHICH LEAKAGE CHANNELS ARE ON AND GO FROM THERE.

    def red_calc_input(self):

        red_output = self.red

        if self.green is not None and self.green != 0:
            # FIND THE INPUT REQUIRED FOR SPECIFIED GREEN OUTPUT
            green_input = round((self.green * self.green_slope) + self.green_intercept)

            # TAKE THE INPUT AND CALCULATE THE RED LEAKAGE
            green_red_leak_output = (green_input - self.green_red_leak_intercept) / self.green_red_leak_slope

            # TAKE THE RED LEAKAGE AND REMOVE IT FROM THE RED GOAL
            red_output -= green_red_leak_output

        if self.fr is not None and self.fr != 0:
            fr_input = round((self.fr * self.fr_slope) + self.fr_intercept)

            fr_red_leak_output = (fr_input - self.fr_red_leak_intercept) / self.fr_red_leak_slope

            red_output -= fr_red_leak_output

        if self.red is not None and self.red != 0:
            self.red_input = round((red_output * self.red_slope) + self.red_intercept)

        # IF SELF.RED IS = 0 IT MIGHT NOT BE 0 DUE TO THE LEAKAGE FROM GREEN. MIGHT HAVE TO HANDLE THIS WITH ERROR POPUPS
        # FOR NOW JUST MAKING IT 0

        if self.red is None or self.red == 0:
            self.red_input = 0

    ###########################################
    # CALCULATE GREEN INPUT FROM GREEN OUTPUT #
    ###########################################
    def green_calc_input(self):

        if self.green is not None and self.green != 0:
            self.green_input = round((self.green * self.green_slope) + self.green_intercept)

        elif self.green is None or self.green == 0:
            self.green_input = 0

        # WORK ON THIS###################################################
        if self.blue is None or self.blue == 0:
            self.blue_output = (self.green_input - self.green_blue_leak_intercept) / self.green_blue_leak_slope

        if self.red is None or self.red == 0:
            self.red_output += (self.green_input - self.green_red_leak_intercept) / self.green_red_leak_slope

    #########################################
    # CALCULATE BLUE INPUT FROM BLUE OUTPUT #
    #########################################
    def blue_calc_input(self):

        blue_output = self.blue

        # CHECKING IF GREEN IS ON
        if self.green is not None and self.green != 0:
            # FIND THE INPUT REQUIRED FOR SPECIFIED GREEN OUTPUT
            green_input = round((self.green * self.green_slope) + self.green_intercept)

            # TAKE THE INPUT AND CALCULATE THE BLUE LEAKAGE
            green_blue_leak_output = (green_input - self.green_blue_leak_intercept) / self.green_blue_leak_slope

            # TAKE THE BLUE LEAKAGE AND REMOVE IT FROM THE BLUE TOTAL
            blue_output -= green_blue_leak_output

        if self.blue is not None and self.blue != 0:
            self.blue_input = round((blue_output * self.blue_slope) + self.blue_intercept)

    #######################################
    # CALCULATE FAR RED INPUT FROM OUTPUT #
    #######################################
    def fr_calc_input(self):

        if self.fr is not None and self.fr != 0:
            self.fr_input = round((self.fr * self.fr_slope) + self.fr_intercept)

        elif self.fr is None or self.fr == 0:
            self.fr_input = 0

        if self.red is None or self.red == 0:
            self.red_output += (self.fr - self.fr_red_leak_intercept) / self.fr_red_leak_slope

    #######################################
    #            PRINTING INPUTS          #
    #######################################
    def printing_inputs(self):

        # GREEN PRINT OUT
        if self.green is not None and self.green != 0:
            green_text = f'Green input for specified value({self.green} umol/m2/s): {self.green_input}'

            print(green_text)

        # FAR RED PRINT OUT
        if self.fr is not None and self.fr != 0:
            fr_text = f'Far Red input for specified value ({self.fr} umol/m2/s): {self.fr_input}'

            print(fr_text)

        # RED PRINT OUT IF SELF.RED != 0
        if self.red is not None and self.red != 0:

            if self.red_input < 0:
                self.red_input = 0

            red_text = f'Red input for specified value ({self.red} umol/m2/s): {self.red_input}'

            if self.green is not None and self.green != 0:
                green_red_leak_text = f', {round((self.green_input - self.green_red_leak_intercept) / self.green_red_leak_slope, 2)} umol/m2/s from Green leak'
                red_text += green_red_leak_text

            if self.fr is not None and self.fr != 0:
                fr_red_leak_text = f', {round((self.fr_input - self.fr_red_leak_intercept) / self.fr_red_leak_slope, 2)} umol/m2/s from Far Red leak'
                red_text += fr_red_leak_text

            print(red_text)

        # RED PRINT OUT IF IT IS 0
        if self.red is None or self.red == 0:

            red_text = f'Red input for specified value ({self.red} umol/m2/s): {self.red_input}'

            if self.green is not None and self.green != 0:
                green_red_leak_text = f', {round((self.green_input - self.green_red_leak_intercept) / self.green_red_leak_slope, 2)} umol/m2/s from Green leak'
                red_text += green_red_leak_text

            if self.fr is not None and self.fr != 0:
                fr_red_leak_text = f', {round((self.fr_input - self.fr_red_leak_intercept) / self.fr_red_leak_slope, 2)} umol/m2/s from Far Red leak'
                red_text += fr_red_leak_text

            print(red_text)

        # BLUE PRINT OUT IF SELF.BLUE != 0
        if self.blue is not None and self.blue != 0:

            if self.blue_input < 0:
                self.blue_input = 0

            blue_text = f'Blue input for specified value ({self.blue} umol/m2/s): {self.blue_input}'

            if self.green is not None and self.green != 0:
                green_blue_leak_text = f', {round((self.green_input - self.green_blue_leak_intercept) / self.green_blue_leak_slope, 2)} umol/m2/s from Green leak'
                blue_text += green_blue_leak_text

            print(blue_text)

        if self.blue is None or self.blue == 0:

            blue_text = f'Blue input for specified value ({self.blue} umol/m2/s): {self.blue_input}'

            if self.green is not None and self.green != 0:
                green_blue_leak_text = f', {round((self.green_input - self.green_blue_leak_intercept) / self.green_blue_leak_slope, 2)} umol/m2/s from Green leak'
                blue_text += green_blue_leak_text

            print(blue_text)

    #######################################
    #             PLOTTING                #
    #######################################

    def plotting(self):

        # self.ax.clear()

        if self.input_output == 'input':
            light_output_list = []
            light_categories = []
            bar_colours = []
            if self.red_output is not None:
                light_output_list.append(self.red_output)
                light_categories.append('Red')
                bar_colours.append('red')

            if self.green_output is not None:
                light_output_list.append(self.green_output)
                light_categories.append('Green')
                bar_colours.append('green')

            if self.blue_output is not None:
                light_output_list.append(self.blue_output)
                light_categories.append('Blue')
                bar_colours.append('blue')

            if self.fr is not None:
                light_output_list.append(self.fr_output)
                light_categories.append('Far Red')
                bar_colours.append('purple')

            self.ax.bar(light_categories, light_output_list, color=bar_colours)
            self.ax.set_ylabel('umol/m2/s')


        if self.input_output == 'output':
            light_output_list = []
            light_categories = []
            bar_colours = []

            if self.red is not None and self.red != 0:
                light_output_list.append(self.red)
                light_categories.append('Red')
                bar_colours.append('red')

            if self.green is not None and self.green != 0:
                light_output_list.append(self.green)
                light_categories.append('Green')
                bar_colours.append('green')

                if self.blue is None or self.blue == 0:
                    light_output_list.append(self.blue_output)
                    light_categories.append('Blue')
                    bar_colours.append('blue')

                if self.red is None or self.red == 0:
                    light_output_list.append(self.red_output)
                    light_categories.append('Red')
                    bar_colours.append('red')
                    print(self.red_output)

            if self.blue is not None:
                light_output_list.append(self.blue)
                light_categories.append('Blue')
                bar_colours.append('blue')

            if self.fr is not None:
                light_output_list.append(self.fr)
                light_categories.append('Far Red')
                bar_colours.append('purple')

                if self.red is None and self.red == 0:
                    light_output_list.append(self.red_output)
                    light_categories.append('Red')
                    bar_colours.append('red')

            self.ax.bar(light_categories, light_output_list, color=bar_colours)
            self.ax.set_ylabel('umol/m2/s')
