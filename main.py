import serial
import time


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


# Initialize pumps
outlet_pump = SyringePump(0, 'COM9')
# cell_pump = SyringePump(1, 'COM7')
# buffer_pump = SyringePump(2, 'COM7')
# waste_pump = SyringePump(3, 'COM7')

# Apply settings to each pump

# Check for incorrect settings
# assert outlet_pump.get_address() == '\nPump address is 0\r\n:'
# assert cell_pump.get_address() == 1
# assert buffer_pump.get_address() == 2
# assert waste_pump.get_address() == 3

# assert outlet_pump.get_syringe() == 0
# assert cell_pump.get_syringe() == 1
# assert buffer_pump.get_syringe() == 2
# assert waste_pump.get_syringe() == 3

# Testing
outlet_pump.poll()
outlet_pump.poll('off')
outlet_pump.get_syringe()
outlet_pump.get_metrics()
outlet_pump.run()
outlet_pump.stop()
outlet_pump.trigger_status()
outlet_pump.withdraw_rate()

