import time

import serial


class SyringePump:
    """Class defining a syringe pump.

    Pump addresses must start at 0 and increase with each pump.
    The pump address must be set on the pump

    com needs to be str in format 'COM#'
    """

    def __init__(self, address, com):
        self.address = address
        self.com = com
        self.ser = serial.Serial(
            port=self.com,
            baudrate=9600,
            parity=serial.PARITY_ODD,
            stopbits=serial.STOPBITS_TWO,
            bytesize=serial.SEVENBITS
            )
        self.state = ''
        self.connection()

    def connection(self):
        if self.ser.isOpen():
            print('Connected')
        else:
            print('Failed to connect')

    def input(self, input_message: str) -> str:
        output = ''
        print('IN:', input_message)
        formatted_input = input_message + '\r\n'
        self.ser.write(formatted_input.encode('ascii'))

        # Wait 1 sec before reading output
        time.sleep(1)
        while self.ser.inWaiting() > 0:
            output += self.ser.read(1).decode("utf-8")

        if output != '':
            print('OUT:', output)
            self.state = output
        return output

    def get_address(self):
        response = self.input('address')
        return response

    def get_syringe(self):
        response = self.input('syrm')
        return response

    def run(self):
        response = self.input('run')
        return response

    def stop(self):
        response = self.input('stop')
        return response

    def withdraw_rate(self, rate=''):
        if rate:
            rate = ' ' + rate
        response = self.input('wrate' + rate)
        return response

    def clear_target_volume(self):
        response = self.input('ctvolume')
        return response

    def set_target_volume(self, volume=''):
        if volume:
            volume = ' ' + volume
        response = self.input('tvolume' + volume)
        return response

    def trigger_status(self):
        response = self.input('input')
        return response

    def set_output(self):
        response = self.input('output')
        return response

    def get_metrics(self):
        response = self.input('metrics')
        return response

    def poll(self, value=''):
        if value:
            value = ' ' + value
        response = self.input('poll' + value)
        return response


class MultifrequencyBoard:
    """Class defining the multifreqeuncy board.

    Only designed with one channel in mind (HAHAHA)
    From appendix A of the MFG documentation, I suspect it can be controlled through serial com.

    com needs to be str in format 'COM#'
    baudrate=115200 for boards. Will not work otherwise
    """

    def __init__(self, com):
        self.com = com
        self.ser = serial.Serial(
            baudrate=115200,
            port=self.com)
        self.channel = 1
        self.connection()

    def connection(self):
        if self.ser.isOpen():
            print('Connected')
        else:
            print('Failed to connect')

    def input(self, input_message: str) -> str:
        output = ''
        formatted_input = '<' + input_message + '\n'
        print('IN:', formatted_input)
        self.ser.write(formatted_input.encode('ascii'))

        # Wait 1 sec before reading output
        time.sleep(1)
        while self.ser.inWaiting() > 0:
            output += self.ser.read(1).decode("utf-8")

        if output != '':
            print('OUT:', output)
        return output

    def enable(self):
        s = 'enable ' + str(self.channel) + ' ' + str(1)
        self.input(s)

    def disable(self):
        s = 'enable ' + str(self.channel) + ' ' + str(0)
        self.input(s)

    def amplitude(self, amp=''):
        if amp != '':
            # Set amplitude to new value
            s = 'amp ' + str(self.channel) + ' ' + str(amp)
        else:
            # Get current amplitude
            s = 'amp ' + str(self.channel)
        self.input(s)

    def frequency(self, freq=''):
        if freq != '':
            # Set amplitude to new value
            s = 'freq ' + str(self.channel) + ' ' + str(freq)
        else:
            # Get current amplitude
            s = 'freq ' + str(self.channel)
        self.input(s)


class Microscope:
    """class representing the SMZ18"""
    def __init__(self):
        self.path = ''
        self.current_trial = 1

    def image(self, filename):
        # Take an image with the microscope
        image_path = self.path + filename + '.tif'
        pass

    def connect(self):
        # Connect to microscope
        pass
