from classes import MultifrequencyBoard, SyringePump
import win32api
import win32con
import time


def autocapture_image():
    # Press down the Ctrl key
    win32api.keybd_event(win32con.VK_CONTROL, 0, 0, 0)
    # Press down the Spacebar
    win32api.keybd_event(win32con.VK_SPACE, 0, 0, 0)

    # Release the Spacebar
    win32api.keybd_event(win32con.VK_SPACE, 0, win32con.KEYEVENTF_KEYUP, 0)
    # Release the Ctrl key
    win32api.keybd_event(win32con.VK_CONTROL, 0, win32con.KEYEVENTF_KEYUP, 0)
    time.sleep(5)


def routine(voltage=25, frequency=90, outlet_withdraw_rate = '50 n/m'):
    # Initialize Pumps, Board
    outlet_pump = SyringePump(0, 'COM9')
    cell_pump = SyringePump(2, 'COM7')
    buffer_pump = SyringePump(1, 'COM7')
    waste_pump = SyringePump(3, 'COM9')

    board = MultifrequencyBoard('COM10')
    board.amplitude(voltage)
    board.frequency(frequency)
    print('Connected:', + board.ser.isOpen())

    # Set inlet rates
    waste_pump.input('wrate 1200 um')
    cell_pump.input('irate 1200 um')
    buffer_pump.input('irate 1200 um')
    outlet_fast_rate = 'wrate 1200 um'

    time.sleep(5)  # Time to start script and switch window
    something = True
    while something:
        # 0. Ensure regular conditions
        print('0. Ensure regular conditions')
        board.disable()
        waste_pump.input('cvolume')
        waste_pump.input('tvolume 20 u')
        waste_pump.input('wrun')

        buffer_pump.input('cvolume')
        buffer_pump.input('tvolume 15 u')
        buffer_pump.input('irun')

        outlet_pump.input('cvolume')
        outlet_pump.input(outlet_fast_rate)
        outlet_pump.input('tvolume 15 u')
        outlet_pump.input('wrun')
        time.sleep(3)

        outlet_pump.withdraw_rate(outlet_withdraw_rate)
        outlet_pump.run()
        time.sleep(10)

        # 1. Image blank
        print('1. Image blank')
        autocapture_image()
        time.sleep(1.5)

        # 2. Remove waste from inlet
        print('2. Remove waste from inlet')
        waste_pump.input('cvolume')
        waste_pump.input('tvolume 30 u')
        waste_pump.input('wrun')
        time.sleep(1.5)

        # 3. Infuse cells
        print('3. Infuse cells')
        cell_pump.input('cvolume')
        cell_pump.input('tvolume 30 u')
        cell_pump.input('irun')
        time.sleep(1.5)

        # 4. FF withdraw outlet pump
        print('4. FF withdraw outlet pump')
        outlet_pump.input('cvolume')
        outlet_pump.input(outlet_fast_rate)
        outlet_pump.input('tvolume 15 u')
        outlet_pump.input('wrun')
        time.sleep(1.5)
        outlet_pump.input('cvolume')
        outlet_pump.withdraw_rate(outlet_withdraw_rate)
        outlet_pump.run()
        time.sleep(1)

        # 5. Turn on voltage
        print('5. Turn on voltage')
        board.enable()

        # 6. Wait 5 min withdraw outlet pump
        print('6. Wait 5 min withdraw outlet pump')
        outlet_pump.withdraw_rate(outlet_withdraw_rate)
        outlet_pump.run()
        time.sleep(5 * 60)

        # 7. Withdraw cells from inlet
        print('7. Withdraw cells from inlet')
        waste_pump.input('cvolume')
        waste_pump.input('wrate 1200 um')
        waste_pump.input('tvolume 30 u')
        waste_pump.input('wrun')
        time.sleep(1.5)

        # 8. Infuse buffer
        print('8. Infuse buffer')
        buffer_pump.input('cvolume')
        buffer_pump.input('tvolume 15 u')
        buffer_pump.input('irun')
        time.sleep(1.5)

        # 9. Wait ~2 min for channel to rinse
        print('9. Wait ~2 min for channel to rinse')
        outlet_pump.withdraw_rate(outlet_withdraw_rate)
        outlet_pump.run()
        time.sleep(2 * 60)

        # 10. Image tips
        print('10. Image tips')
        autocapture_image()
        time.sleep(1.5)

        # 11. Turn off voltage
        print('11. Turn off voltage')
        board.disable()
        time.sleep(10)  # Cells transfer in

        # 12. Image transfer
        print('12. Image transfer')
        autocapture_image()
        time.sleep(1.5)

        # 12. FF withdraw flow pump
        print('13. FF withdraw flow pump')
        outlet_pump.input('cvolume')
        outlet_pump.input(outlet_fast_rate)
        outlet_pump.input('tvolume 15 u')
        outlet_pump.input('wrun')
        time.sleep(1.5)
        outlet_pump.input('cvolume')
        outlet_pump.withdraw_rate(outlet_withdraw_rate)
        outlet_pump.run()
        time.sleep(1)


if __name__ == '__main__':
    routine(voltage=25, frequency=90, outlet_withdraw_rate='100 n/m')