import RPIO as G
from time import sleep

class Sipo_reg(object):
    def __init__(self, control_pins, byte_count, freq = 1/10000, latched = False):
        """

        :param control_pins: Three for non-latched, Four for latched
                             Data, Clock, Reset, Latch
        :param byte_count: dependent on the number of registers (1 register = 8 bites)
        :param freq = frequency, default value 1kHz
        :param latched: False stands for direct shifting, reversed bits
                        True, latched, needs four pins

        """

        # Define input variables

        self.control_pins = control_pins
        self.latched = latched
        self.byte_count = byte_count
        self.freq = freq

        # Dealing with variable number of pins from RPi

        if latched and len(control_pins) != 4:
            raise Exception("Didn't you forget to provide fourth, latch pin?")

        # Dealing with possible errors within passing of list pins

        if len(control_pins) != 3:
            raise Exception("Number of pins insufficient, namely {}".format(len(control_pins)))

        # Define shift register control pins

        self.data = control_pins[0]
        self.clock = control_pins[1]
        self.reset = control_pins[2]

        # Define latch pin if present

        if latched:
            self.latch = control_pins[3]

        # RPi pins ready

        for pin in control_pins:
            G.setup(pin, G.OUT)

        # Enable

        G.output(self.reset, 1)


    def shift_out(self, num_list):

        # Dealing with possible errors within passing of list pins

        if len(num_list) > self.byte_count * 8:
            raise Exception("Expression would take up more space than available, length of expression = {}, available bites =  {}".format(len(num_list), self.byte_count * 8))

        # Reverse non-latched output

        num_list = num_list[::-1]

        # Loop vars

        i = 0
        length = len(num_list)

        while i < length:
            G.output(self.data, num_list[i])
            sleep(self.freq)
            G.output(self.clock, 1)
            sleep(self.freq)
            G.output(self.clock, 0)

            i += 1

    def clear(self):
        G.output(self.reset, 0)
        G.output(self.reset, 1)



class Piso_reg(object):
    pass

