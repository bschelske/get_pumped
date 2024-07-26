from classes import MultifrequencyBoard
from routine import routine

# Parameters
voltage = 25  # Vpp
frequency = 90  # kHz

# Run the routine
# routine(voltage, frequency)

"""
TESTING ROUTINE PARTS
"""

# Initialize pumps
# outlet_pump = SyringePump(0, 'COM9')
# cell_pump = SyringePump(1, 'COM7')
# buffer_pump = SyringePump(2, 'COM7')
# waste_pump = SyringePump(0, 'COM9')


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
# waste_pump.get_syringe()
#
# waste_pump.input('wrate 1200 um')
# waste_pump.input('irate 1200 um')
# for i in range(3):
#     waste_pump.input('cvolume')
#     waste_pump.input('tvolume 20 u')
#     waste_pump.input('wrun')
#
#     waste_pump.input('tvolume 20 u')
#     waste_pump.input('irun')

# BOARD Testing
board = MultifrequencyBoard('COM10')
# board.amplitude(5)
# board.frequency(10)
# board.enable()
board.disable()
board.disable()



