import serial
import time


class SyringePump:
    """Class defining a syringe pump.

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

# Create class instance
pump_0 = SyringePump(0, 'COM6')
pump_1 = SyringePump(1,'COM7')

pumps = [pump_0, pump_1]
for pump in pumps:
    print('\nPump:', pump.address)
    # Configure serial connection
    pump.ser.isOpen()

    input = 'stp'
    print('IN:', input)
    out = ''

    # Send the input to the device
    # Note the carriage return and line feed characters \r\n will depend on the device
    message = input + '\r\n'
    pump.ser.write(message.encode('ascii'))

    # Wait 1 sec before reading output
    # time.sleep(1)
    while pump.ser.inWaiting() > 0:
        out += pump.ser.read(1).decode("utf-8")

    if out != '':
        print('OUT:', out)

    out = out.strip('\r\n')
    out = out.split('\n')

    # Print the response
    if out != '':
        for line in out:
            line = line.strip('\r')
            if line == ':':
                print('The pump is idle')
            if line == '<':
                print('The pump is withdrawing')
            if line == '>':
                print('The pump is infusing')
            if line == '*':
                print('The pump stalled')
            if line == 'T*':
                print('The target was reached')

