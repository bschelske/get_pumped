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

    time.sleep(10)  # Time to start script and switch window
    something = True
    while something:
        # 0. Ensure regular conditions
        outlet_pump.withdraw_rate(outlet_withdraw_rate)
        outlet_pump.run()

        # 1. Image blank
        autocapture_image()

        # 2. Withdraw buffer from inlet
        waste_pump.input('cvolume')
        waste_pump.input('tvolume 20 u')
        waste_pump.input('wrun')
        time.sleep(1.5)

        # 3. Infuse cells
        cell_pump.input('cvolume')
        cell_pump.input('tvolume 20 u')
        cell_pump.input('irun')
        time.sleep(1.5)

        # 4. FF withdraw outlet pump
        outlet_pump.withdraw_rate('200 n/m')
        outlet_pump.run()
        time.sleep(1)

        # 5. Turn on voltage
        board.enable()

        # 6. Wait 5 min withdraw outlet pump
        outlet_pump.withdraw_rate(outlet_withdraw_rate)
        outlet_pump.run()
        time.sleep(5 * 60)

        # 7. Withdraw cells from inlet
        waste_pump.input('cvolume')
        waste_pump.input('tvolume 20 u')
        waste_pump.input('wrun')
        time.sleep(1.5)

        # 8. Infuse buffer
        buffer_pump.input('cvolume')
        buffer_pump.input('tvolume 20 u')
        buffer_pump.input('irun')
        time.sleep(1.5)

        # 9. Wait ~2 min for channel to rinse
        outlet_pump.withdraw_rate(outlet_withdraw_rate)
        outlet_pump.run()
        time.sleep(2 * 60)

        # 10. Image tips
        autocapture_image()
        time.sleep(1.5)

        # 11. Turn off voltage
        board.disable()
        time.sleep(10)  # Cells transfer in

        # 12. Image transfer
        autocapture_image()
        time.sleep(1.5)

        # 12. FF withdraw flow pump
        outlet_pump.withdraw_rate('200 n/m')
        outlet_pump.run()
        time.sleep(1)


if __name__ == '__main__':
    routine(voltage=25, frequency=90, outlet_withdraw_rate='50 n/m')