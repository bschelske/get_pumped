from classes import MultifrequencyBoard, SyringePump
import win32api
import win32con
import time
import datetime

from ui import PumpControlUserInterface


def left_click():
    # Oh brother
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time.sleep(.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
    print(f'{datetime.datetime.now().strftime('%H:%M:%S')} click')


def autocapture_image():
    # Press down the Ctrl key
    win32api.keybd_event(win32con.VK_CONTROL, 0, 0, 0)
    # Press down the spacebar
    win32api.keybd_event(win32con.VK_SPACE, 0, 0, 0)

    # Release the Spacebar
    win32api.keybd_event(win32con.VK_SPACE, 0, win32con.KEYEVENTF_KEYUP, 0)
    # Release the Ctrl key
    win32api.keybd_event(win32con.VK_CONTROL, 0, win32con.KEYEVENTF_KEYUP, 0)
    time.sleep(5)


def run_ben_macro(type, ui_control):
    # It takes about 36 seconds to capture 101 images.
    delay = 40
    # Macro Types (Used for file naming):
    # 1	0x31: Blanks
    # 2	0x32: DEP Trajectories
    # 3	0x33: Electrode Tips
    # 4	0x34: Transfer
    print(f'\t{datetime.datetime.now().strftime('%H:%M:%S')} The prison guard is on patrol!')
    # Press CTRL + ALT + 1
    win32api.keybd_event(win32con.VK_CONTROL, 0, 0, 0)
    win32api.keybd_event(win32con.VK_MENU, 0, 0, 0)
    win32api.keybd_event(type, 0, 0, 0)

    # Release CTRL + ALT + 1
    win32api.keybd_event(win32con.VK_CONTROL, 0, win32con.KEYEVENTF_KEYUP, 0)
    win32api.keybd_event(win32con.VK_MENU, 0, win32con.KEYEVENTF_KEYUP, 0)
    win32api.keybd_event(type, 0, win32con.KEYEVENTF_KEYUP, 0)
    print(f'\t{datetime.datetime.now().strftime('%H:%M:%S')} Wait {delay} s for microscope to image array...')
    for _ in range(delay):
        if not ui_control.running:
            break
        time.sleep(1)



def ui_routine(ui_control: PumpControlUserInterface):
    delay = 1.5
    # 0. Ensure regular conditions
    # Replace inlet solution with buffer
    print(f'{datetime.datetime.now().strftime('%H:%M:%S')} 0. Ensure regular conditions')
    ui_control.device.mf_board.disable()
    remove_waste(ui_control)
    infuse_buffer(ui_control)
    ff_outlet(ui_control)
    time.sleep(3)

    ui_control.device.outlet_pump.withdraw_rate(ui_control.outlet_capture_rate.get())
    ui_control.device.outlet_pump.run()
    time.sleep(10)

    # 1. Image blank
    print(f'{datetime.datetime.now().strftime('%H:%M:%S')} 1. Image blank')
    # autocapture_image()
    # left_click()
    run_ben_macro(0x31, ui_control)
    time.sleep(delay)

    # 2. Remove waste from inlet
    print(f'{datetime.datetime.now().strftime('%H:%M:%S')} 2. Remove waste from inlet')
    remove_waste(ui_control)
    time.sleep(2)

    # 3. Infuse cells
    print(f'{datetime.datetime.now().strftime('%H:%M:%S')} 3. Infuse cells')
    infuse_cells(ui_control)
    time.sleep(1.5)

    # 4. FF withdraw outlet pump
    print(f'{datetime.datetime.now().strftime('%H:%M:%S')} 4. FF withdraw outlet pump')
    ff_outlet(ui_control)
    time.sleep(1.5)
    outlet_capture_withdraw(ui_control)
    time.sleep(1)

    # 5. Turn on voltage
    print(f'{datetime.datetime.now().strftime('%H:%M:%S')} 5. Turn on voltage')
    ui_control.device.mf_board.enable()

    # 6. Wait 5 min withdraw outlet pump
    print(f'{datetime.datetime.now().strftime('%H:%M:%S')} 6. Capture Cells for 5 min and record cell trajectories')
    outlet_capture_withdraw(ui_control)

    print(f'{datetime.datetime.now().strftime('%H:%M:%S')} Capturing Cell Trajectory')
    run_ben_macro(0x32, ui_control)
    time.sleep(5 * 60)

    # 7. Withdraw cells from inlet
    print(f'{datetime.datetime.now().strftime('%H:%M:%S')} 7. Withdraw cells from inlet (1.5 s)')
    remove_waste(ui_control)
    time.sleep(1.5)

    # 8. Infuse buffer
    print(f'{datetime.datetime.now().strftime('%H:%M:%S')} 8. Infuse buffer (1.5 s)')
    infuse_buffer(ui_control)
    time.sleep(1.5)

    # 9. Wait ~2 min for channel to rinse
    print(f'{datetime.datetime.now().strftime('%H:%M:%S')} 9. Wait ~2 min for channel to rinse')
    outlet_capture_withdraw(ui_control)
    time.sleep(2 * 60)

    # 10. Image tips
    print(f'{datetime.datetime.now().strftime('%H:%M:%S')} 10. Image tips')
    # autocapture_image()
    # left_click()
    run_ben_macro(0x33, ui_control)
    time.sleep(delay)

    # 11. Turn off voltage
    print(f'{datetime.datetime.now().strftime('%H:%M:%S')} 11. Turn off voltage')
    ui_control.device.mf_board.disable()
    time.sleep(10)  # Cells transfer in

    # 12. Image transfer
    print(f'{datetime.datetime.now().strftime('%H:%M:%S')} 12. Image transfer')
    # autocapture_image()
    left_click()
    time.sleep(delay)

    # 12. FF withdraw flow pump
    print(f'{datetime.datetime.now().strftime('%H:%M:%S')} 13. FF withdraw flow pump')
    ff_outlet(ui_control)
    time.sleep(1.5)
    outlet_capture_withdraw(ui_control)
    time.sleep(1)

def threaded_routine(ui_control: PumpControlUserInterface):
    while ui_control.running:
        # 0. Ensure regular conditions
        # Replace inlet solution with buffer
        print(f'\n{datetime.datetime.now().strftime('%H:%M:%S')} 0. Ensure regular conditions')
        ui_control.device.mf_board.disable()
        remove_waste(ui_control)
        infuse_buffer(ui_control)
        ff_outlet(ui_control)
        print(f'\t{datetime.datetime.now().strftime('%H:%M:%S')} Wait 3 s for outlet pump to fast reverse...')
        sleep_w_status(3, ui_control)
        if not ui_control.running:
            break

        ui_control.device.outlet_pump.withdraw_rate(ui_control.outlet_capture_rate.get())
        ui_control.device.outlet_pump.run()
        print(f'\t{datetime.datetime.now().strftime('%H:%M:%S')} Wait 10 seconds for cells to slow down...')
        sleep_w_status(10, ui_control)
        print(f'\t{datetime.datetime.now().strftime('%H:%M:%S')} ...Done')
        if not ui_control.running:
            break


        # 1. Image blank
        print(f'\n{datetime.datetime.now().strftime('%H:%M:%S')} 1. Image blank (40 s)')
        # autocapture_image()
        # left_click()
        run_ben_macro(0x31, ui_control)
        print(f'\t{datetime.datetime.now().strftime('%H:%M:%S')} .tif saved to "E:\\BS\\TRAC\\Macro Save Path\\Blank"!')

        if not ui_control.running:
            break

        # 2. Remove waste from inlet
        print(f'\n{datetime.datetime.now().strftime('%H:%M:%S')} 2. Remove waste from inlet (2 s)')
        remove_waste(ui_control)
        sleep_w_status(2, ui_control)
        if not ui_control.running:
            break

        # 3. Infuse cells
        print(f'\n{datetime.datetime.now().strftime('%H:%M:%S')} 3. Infuse cells (1.5 s)')
        infuse_cells(ui_control)
        sleep_w_status(1.5, ui_control)
        if not ui_control.running:
            break

        # 4. FF withdraw outlet pump
        print(f'\n{datetime.datetime.now().strftime('%H:%M:%S')} 4. FF withdraw outlet pump (2 s)')
        ff_outlet(ui_control)
        sleep_w_status(1.5, ui_control)
        outlet_capture_withdraw(ui_control)
        sleep_w_status(1, ui_control)
        if not ui_control.running:
            break

        # 5. Turn on voltage
        print(f'\n{datetime.datetime.now().strftime('%H:%M:%S')} 5. Turn on voltage')
        ui_control.device.mf_board.enable()

        # 6. Wait 5 min withdraw outlet pump
        # This step is going to require careful timing to work correctly
        # On the macro with 101 images, it takes about 37 seconds from start to finish
        # 5 min / 37 s is 8.1 cycles... round up to 9 means a total waiting period of 333 sec
        # For safety, lets run the loop for 333 seconds, imaging 8 times.

        print(f'\n{datetime.datetime.now().strftime('%H:%M:%S')} 6. Capture Cells and record cell trajectories (5 min)')
        outlet_capture_withdraw(ui_control)
        for _ in range(8):
            if not ui_control.running:
                break
            print(f'\n{datetime.datetime.now().strftime('%H:%M:%S')} Capturing Cell Trajectories! ========================')
            run_ben_macro(0x32, ui_control)
        if not ui_control.running:
            break

        # 7. Withdraw cells from inlet
        print(f'\n{datetime.datetime.now().strftime('%H:%M:%S')} 7. Withdraw cells from inlet (1.5 s)')
        remove_waste(ui_control)
        sleep_w_status(1.5, ui_control)
        if not ui_control.running:
            break

        # 8. Infuse buffer
        print(f'\n{datetime.datetime.now().strftime('%H:%M:%S')} 8. Infuse buffer (1.5 s)')
        infuse_buffer(ui_control)
        sleep_w_status(1.5, ui_control)
        if not ui_control.running:
            break

        # 9. Wait ~2 min for channel to rinse
        print(f'\n{datetime.datetime.now().strftime('%H:%M:%S')} 9. Rinse channels of cells (2 min)')
        outlet_capture_withdraw(ui_control)
        for _ in range(60):
            if not ui_control.running:
                break
            time.sleep(2)
        if not ui_control.running:
            break

        # 10. Image tips
        print(f'\n{datetime.datetime.now().strftime('%H:%M:%S')} 10. Image tips')
        # autocapture_image()
        # left_click()
        run_ben_macro(0x33, ui_control)
        print(f'\t{datetime.datetime.now().strftime('%H:%M:%S')} .tif saved to "E:\\BS\\TRAC\\Macro Save Path\\Cells Captured on Electrode Tips"!')
        if not ui_control.running:
            break

        # 11. Turn off voltage
        print(f'\n{datetime.datetime.now().strftime('%H:%M:%S')} 11. Turn off voltage')
        ui_control.device.mf_board.disable()
        print(f'\t{datetime.datetime.now().strftime('%H:%M:%S')} Transfer cells to chambers... (10 s)')
        sleep_w_status(10, ui_control)  # Cells transfer in
        if not ui_control.running:
            break

        # 12. Image transfer
        print(f'\n{datetime.datetime.now().strftime('%H:%M:%S')} 12. Image transfer')
        # autocapture_image()
        # left_click()
        run_ben_macro(0x33, ui_control)
        print(f'\t{datetime.datetime.now().strftime('%H:%M:%S')} .tif saved to "E:\\BS\\TRAC\\Macro Save Path\\Cells Transferred into Chambers"!')
        if not ui_control.running:
            break

        # 12. FF withdraw flow pump
        print(f'\n{datetime.datetime.now().strftime('%H:%M:%S')} 13. FF withdraw flow pump (2 s)')
        ff_outlet(ui_control)
        sleep_w_status(1.5, ui_control)
        outlet_capture_withdraw(ui_control)
        sleep_w_status(1, ui_control)
        if not ui_control.running:
            break


def sleep_w_status(time_in_s, ui_control):
    ui_control.status_label.config(text=f"Status: Busy")
    time.sleep(time_in_s)
    ui_control.status_label.config(text=f"Status: Responsive")


def remove_waste(control: PumpControlUserInterface):
    control.device.waste_pump.clear_volume()
    control.device.waste_pump.set_target_volume(control.waste_volume.get())
    control.device.waste_pump.input('wrun')


def infuse_buffer(control: PumpControlUserInterface):
    control.device.buffer_pump.clear_volume()
    control.device.buffer_pump.set_target_volume(control.buffer_volume.get())
    control.device.buffer_pump.input('irun')


def infuse_cells(control: PumpControlUserInterface):
    control.device.cell_pump.clear_volume()
    control.device.cell_pump.set_target_volume(control.cell_volume.get())
    control.device.cell_pump.input('irun')


def ff_outlet(control: PumpControlUserInterface):
    control.device.outlet_pump.clear_volume()
    control.device.outlet_pump.withdraw_rate(control.outlet_ff_rate.get())
    control.device.outlet_pump.set_target_volume(control.outlet_ff_volume.get())
    control.device.outlet_pump.input('wrun')


def outlet_capture_withdraw(control: PumpControlUserInterface):
    control.device.outlet_pump.clear_volume()
    control.device.outlet_pump.withdraw_rate(control.outlet_capture_rate.get())
    control.device.outlet_pump.run()


def routine(voltage=25, frequency=90, outlet_withdraw_rate='50 n/m'):
    # deprecated
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
        print(f'{datetime.datetime.now().strftime('%H:%M:%S')} 0. Ensure regular conditions')
        board.disable()
        waste_pump.clear_volume()
        waste_pump.input('tvolume 20 u')
        waste_pump.input('wrun')

        buffer_pump.clear_volume()
        buffer_pump.input('tvolume 15 u')
        buffer_pump.input('irun')

        outlet_pump.clear_volume()
        outlet_pump.input(outlet_fast_rate)
        outlet_pump.input('tvolume 15 u')
        outlet_pump.input('wrun')
        time.sleep(3)

        outlet_pump.withdraw_rate(outlet_withdraw_rate)
        outlet_pump.run()
        time.sleep(10)

        # 1. Image blank
        print(f'{datetime.datetime.now().strftime('%H:%M:%S')} 1. Image blank')
        autocapture_image()
        time.sleep(1.5)

        # 2. Remove waste from inlet
        print(f'{datetime.datetime.now().strftime('%H:%M:%S')} 2. Remove waste from inlet')
        waste_pump.clear_volume()
        waste_pump.input('tvolume 30 u')
        waste_pump.input('wrun')
        time.sleep(1.5)

        # 3. Infuse cells
        print(f'{datetime.datetime.now().strftime('%H:%M:%S')} 3. Infuse cells')
        cell_pump.clear_volume()
        cell_pump.input('tvolume 30 u')
        cell_pump.input('irun')
        time.sleep(1.5)

        # 4. FF withdraw outlet pump
        print(f'{datetime.datetime.now().strftime('%H:%M:%S')} 4. FF withdraw outlet pump')
        outlet_pump.clear_volume()
        outlet_pump.input(outlet_fast_rate)
        outlet_pump.input('tvolume 15 u')
        outlet_pump.input('wrun')
        time.sleep(1.5)
        outlet_pump.clear_volume()
        outlet_pump.withdraw_rate(outlet_withdraw_rate)
        outlet_pump.run()
        time.sleep(1)

        # 5. Turn on voltage
        print(f'{datetime.datetime.now().strftime('%H:%M:%S')} 5. Turn on voltage')
        board.enable()

        # 6. Wait 5 min withdraw outlet pump
        print(f'{datetime.datetime.now().strftime('%H:%M:%S')} 6. Wait 5 min withdraw outlet pump')
        outlet_pump.withdraw_rate(outlet_withdraw_rate)
        outlet_pump.run()
        # time.sleep(5 * 60)
        time.sleep(1)

        # 7. Withdraw cells from inlet
        print(f'{datetime.datetime.now().strftime('%H:%M:%S')} 7. Withdraw cells from inlet')
        waste_pump.clear_volume()
        waste_pump.input('wrate 1200 um')
        waste_pump.input('tvolume 30 u')
        waste_pump.input('wrun')
        time.sleep(1.5)

        # 8. Infuse buffer
        print(f'{datetime.datetime.now().strftime('%H:%M:%S')} 8. Infuse buffer')
        buffer_pump.clear_volume()
        buffer_pump.input('tvolume 15 u')
        buffer_pump.input('irun')
        time.sleep(1.5)

        # 9. Wait ~2 min for channel to rinse
        print(f'{datetime.datetime.now().strftime('%H:%M:%S')} 9. Wait ~2 min for channel to rinse')
        outlet_pump.withdraw_rate(outlet_withdraw_rate)
        outlet_pump.run()
        time.sleep(2 * 60)

        # 10. Image tips
        print(f'{datetime.datetime.now().strftime('%H:%M:%S')} 10. Image tips')
        autocapture_image()
        time.sleep(1.5)

        # 11. Turn off voltage
        print(f'{datetime.datetime.now().strftime('%H:%M:%S')} 11. Turn off voltage')
        board.disable()
        time.sleep(10)  # Cells transfer in

        # 12. Image transfer
        print(f'{datetime.datetime.now().strftime('%H:%M:%S')} 12. Image transfer')
        autocapture_image()
        time.sleep(1.5)

        # 12. FF withdraw flow pump
        print(f'{datetime.datetime.now().strftime('%H:%M:%S')} 13. FF withdraw flow pump')
        outlet_pump.clear_volume()
        outlet_pump.input(outlet_fast_rate)
        outlet_pump.input('tvolume 15 u')
        outlet_pump.input('wrun')
        time.sleep(1.5)
        outlet_pump.clear_volume()
        outlet_pump.withdraw_rate(outlet_withdraw_rate)
        outlet_pump.run()
        time.sleep(1)


if __name__ == '__main__':
    # routine(voltage=25, frequency=90, outlet_withdraw_rate='100 n/m')
    time.sleep(2)
    run_ben_macro()