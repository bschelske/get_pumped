import tkinter as tk
import threading
import queue

import routine
from classes import SyringePump, MultifrequencyBoard


class InitializationInterface:
    def __init__(self, master):
        self.master = master
        # Default COM values
        self.outlet_COM = tk.StringVar(value='COM15')
        self.cell_COM = tk.StringVar(value='COM12')
        self.buffer_COM = tk.StringVar(value='COM9')
        self.waste_COM = tk.StringVar(value='COM16')
        self.mf_COM = tk.StringVar(value='COM8')
        # Default address values
        self.outlet_ADDR = tk.StringVar(value='0')
        self.cell_ADDR = tk.StringVar(value='2')
        self.buffer_ADDR = tk.StringVar(value='1')
        self.waste_ADDR = tk.StringVar(value='3')

        self.create_toolbar()
        self.create_initialization_window()

    def create_toolbar(self):
        menu = tk.Menu(self.master)
        self.master.config(menu=menu)

        file_ = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label='File', menu=file_)
        file_.add_command(label='New')
        file_.add_command(label='Open...')
        file_.add_command(label='Exit', command=self.master.quit)

        help_ = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label='Help', menu=help_)
        help_.add_command(label='Help', command=None)
        help_.add_separator()
        help_.add_command(label='About', command=None)

    def create_initialization_window(self):
        anchor = "e"
        width = 10
        COM_width = 9

        row = 1
        tk.Label(self.master, text='Enter COM (windows device manager) and\nAddress (pump settings) for each device', anchor='c', width=35).grid(row=row, column=0, columnspan=4, padx=15, pady=5)
        row += row
        tk.Label(self.master, text='"COM#"', anchor='c', width=5).grid(row=row, column=1,  padx=15, pady=0)
        tk.Label(self.master, text='ADDR', anchor='c', width=5).grid(row=row, column=2,  padx=15, pady=0)

        # Label and Entry 1: Outlet Pump
        row += row
        col = 0
        tk.Label(self.master, text="Outlet Pump", anchor=anchor, width=width).grid(row=row, column=col, padx=5, pady=5)
        self.entry_value = tk.Entry(self.master, textvariable=self.outlet_COM, width=COM_width, justify='center')
        self.entry_value.grid(row=row, column=col + 1, padx=5, pady=5)
        self.entry_value = tk.Entry(self.master, textvariable=self.outlet_ADDR, width=COM_width, justify='center')
        self.entry_value.grid(row=row, column=col + 2, padx=5, pady=5)


        # Label and Entry 2: Cell Pump
        row += row
        col = 0
        tk.Label(self.master, text="Cell Pump",  anchor=anchor, width=width).grid(row=row, column=col, padx=5, pady=5)
        self.entry_value = tk.Entry(self.master, textvariable=self.cell_COM, width=COM_width, justify='center')
        self.entry_value.grid(row=row, column=col + 1, padx=5, pady=5)
        self.entry_value = tk.Entry(self.master, textvariable=self.cell_ADDR, width=COM_width, justify='center')
        self.entry_value.grid(row=row, column=col + 2, padx=5, pady=5)
        # Label and Entry 3: Buffer Pump
        row += row
        col = 0
        tk.Label(self.master, text="Buffer Pump", anchor=anchor, width=width).grid(row=row, column=col, padx=5, pady=5)
        self.entry_value = tk.Entry(self.master, textvariable=self.buffer_COM, width=COM_width, justify='center')
        self.entry_value.grid(row=row, column=col + 1, padx=5, pady=5)
        self.entry_value = tk.Entry(self.master, textvariable=self.buffer_ADDR, width=COM_width, justify='center')
        self.entry_value.grid(row=row, column=col + 2, padx=5, pady=5)
        # Label and Entry 4: Waste Pump
        row += row
        col = 0
        tk.Label(self.master, text="Waste Pump", anchor=anchor, width=width).grid(row=row, column=col, padx=5, pady=5)
        self.entry_value = tk.Entry(self.master, textvariable=self.waste_COM, width=COM_width, justify='center')
        self.entry_value.grid(row=row, column=col + 1, padx=5, pady=5)
        self.entry_value = tk.Entry(self.master, textvariable=self.waste_ADDR, width=COM_width, justify='center')
        self.entry_value.grid(row=row, column=col + 2, padx=5, pady=5)
        # Label and Entry 5: MF Board
        row += row
        col = 0
        tk.Label(self.master, text="MF Board", anchor=anchor, width=width).grid(row=row, column=col, padx=5, pady=5)
        self.entry_value = tk.Entry(self.master, textvariable=self.mf_COM, width=COM_width, justify='center')
        self.entry_value.grid(row=row, column=col + 1, padx=5, pady=5)

        # Test button
        self.test_button = tk.Button(self.master, text="Test", command=self.press_test, width=7)
        self.test_button.grid(row=row + 1, column=1, padx=1, pady=10)

        # OK button
        self.OK_button = tk.Button(self.master, text="OK", command=self.press_ok, width=7)
        self.OK_button.grid(row=row+1, column=2, padx=1, pady=10)

        # Quit button
        self.quit_button = tk.Button(self.master, text="Quit", command=self.quit_ui, width=7)
        self.quit_button.grid(row=row+1, column=3, padx=1, pady=10)

    def quit_ui(self):
        self.master.destroy()
        quit(2)

    def press_test(self):
        self.master.destroy()

    def press_ok(self):
        self.press_connect()
        self.master.destroy()

    def press_connect(self):
        # Create Pump instances
        self.outlet_pump = SyringePump(self.outlet_ADDR.get(), self.outlet_COM.get(), 'Outlet pump')
        self.cell_pump = SyringePump(self.cell_ADDR.get(), self.cell_COM.get(), 'Cell pump')
        self.buffer_pump = SyringePump(self.buffer_ADDR.get(), self.buffer_COM.get(), 'Buffer pump')
        self.waste_pump = SyringePump(self.waste_ADDR.get(), self.waste_COM.get(), 'Waste pump')

        # Create MF instance
        self.mf_board = MultifrequencyBoard(self.mf_COM.get())


class PumpControlUserInterface:
    def __init__(self, master, InitializationInstance):
        self.device = InitializationInstance
        self.master = master

        self.set_ui_default_values()
        self.create_toolbar()
        self.create_pump_controls()

        self.routine_running = False
        self.thread = None
        # self.queue = queue.Queue()
        #
        # self.master.after(100, self.process_queue)

    def set_ui_default_values(self):
        # Pump default flow rates
        #   Add default values to UI
        self.inlet_flow_rate = tk.StringVar(value="1200 um")
        self.buffer_rate = tk.StringVar(value="1200 um")
        self.cell_rate = tk.StringVar(value="1200 um")
        self.waste_rate = tk.StringVar(value="1200 um")

        self.outlet_capture_rate = tk.StringVar(value="100 nm")
        self.outlet_ff_rate = tk.StringVar(value="1200 um")

        # Pump default target volumes
        self.inlet_target_volume = tk.StringVar(value="15 u")
        self.buffer_volume = tk.StringVar(value=self.inlet_target_volume.get())
        self.cell_volume = tk.StringVar(value=self.inlet_target_volume.get())
        self.waste_volume = tk.StringVar(value="30 u")
        self.outlet_ff_volume = tk.StringVar(value="100 u")

        # MF Board Parameters
        self.mf_amp = tk.StringVar(value='28')
        self.mf_frequency = tk.StringVar(value='90')

    def set_hardware_values(self):
        print("Setting values...")
        # Inlet Pump flow rates
        self.device.buffer_pump.input('irate ' + self.buffer_rate.get())
        self.device.cell_pump.input('irate ' + self.cell_rate.get())
        self.device.waste_pump.input('wrate ' + self.waste_rate.get())

        # Outlet pump flow rates
        self.device.outlet_pump.input('wrate ' + self.outlet_capture_rate.get())

        # Pump default target volumes
        # Clear volumes
        self.device.buffer_pump.input('cvolume')
        self.device.cell_pump.input('cvolume')
        self.device.waste_pump.input('cvolume')

        # Set target values
        self.device.buffer_pump.input('tvolume ' + self.buffer_volume.get())
        self.device.cell_pump.input('tvolume ' + self.cell_volume.get())
        self.device.waste_pump.input('tvolume ' + self.waste_volume.get())

        # Set MF Board Parameters
        self.device.mf_board.amplitude = self.mf_amp.get()
        self.device.mf_board.frequency = self.mf_frequency.get()
        print("Values set!")

    def create_toolbar(self):
        menu = tk.Menu(self.master)
        self.master.config(menu=menu)

        file_ = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label='File', menu=file_)
        file_.add_command(label='New')
        file_.add_command(label='Open...')
        file_.add_command(label='Exit', command=self.master.quit)

        help_ = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label='Help', menu=help_)
        help_.add_command(label='Help', command=None)
        help_.add_separator()
        help_.add_command(label='About', command=None)

    def create_pump_controls(self):
        anchor = "e"
        width = 15
        COM_width = 9
        pad_x = 1

        row = 1
        # tk.Label(self.master, text='Control parameters:',
        #          anchor='c', width=30).grid(row=row, column=0, columnspan=1, padx=0, pady=5)
        row += row
        tk.Label(self.master, text='Rate', anchor='c', width=width).grid(row=row, column=1, padx=pad_x, pady=0)
        tk.Label(self.master, text='tvolume', anchor='c', width=width).grid(row=row, column=2, padx=pad_x, pady=0)

        # Label and Entry Outlet Pump Capture conditions
        row += row
        col = 0
        tk.Label(self.master, text="Outlet Pump Capture", anchor=anchor, width=20).grid(row=row, column=col, padx=pad_x, pady=5)
        self.entry_value = tk.Entry(self.master, textvariable=self.outlet_capture_rate, width=COM_width, justify='right')
        self.entry_value.grid(row=row, column=col + 1, padx=pad_x, pady=5)


        # Label and Entry 1: Outlet Pump
        row += row
        col = 0
        tk.Label(self.master, text="Outlet Pump FF", anchor=anchor, width=width).grid(row=row, column=col, padx=pad_x, pady=5)
        self.entry_value = tk.Entry(self.master, textvariable=self.outlet_ff_rate, width=COM_width, justify='right')
        self.entry_value.grid(row=row, column=col + 1, padx=pad_x, pady=5)
        self.entry_value = tk.Entry(self.master, textvariable=self.outlet_ff_volume, width=COM_width, justify='right')
        self.entry_value.grid(row=row, column=col + 2, padx=pad_x, pady=5)

        # Label and Entry 2: Cell Pump
        row += row
        col = 0
        tk.Label(self.master, text="Cell Pump", anchor=anchor, width=width).grid(row=row, column=col, padx=pad_x, pady=5)
        self.entry_value = tk.Entry(self.master, textvariable=self.cell_rate, width=COM_width, justify='right')
        self.entry_value.grid(row=row, column=col + 1, padx=pad_x, pady=5)
        self.entry_value = tk.Entry(self.master, textvariable=self.cell_volume, width=COM_width, justify='right')
        self.entry_value.grid(row=row, column=col + 2, padx=pad_x, pady=5)
        # Label and Entry 3: Buffer Pump
        row += row
        col = 0
        tk.Label(self.master, text="Buffer Pump", anchor=anchor, width=width).grid(row=row, column=col, padx=pad_x, pady=5)
        self.entry_value = tk.Entry(self.master, textvariable=self.buffer_rate, width=COM_width, justify='right')
        self.entry_value.grid(row=row, column=col + 1, padx=pad_x, pady=5)
        self.entry_value = tk.Entry(self.master, textvariable=self.buffer_volume, width=COM_width, justify='right')
        self.entry_value.grid(row=row, column=col + 2, padx=pad_x, pady=5)
        # Label and Entry 4: Waste Pump
        row += row
        col = 0
        tk.Label(self.master, text="Waste Pump", anchor=anchor, width=width).grid(row=row, column=col, padx=pad_x, pady=5)
        self.entry_value = tk.Entry(self.master, textvariable=self.waste_rate, width=COM_width, justify='right')
        self.entry_value.grid(row=row, column=col + 1, padx=pad_x, pady=5)
        self.entry_value = tk.Entry(self.master, textvariable=self.waste_volume, width=COM_width, justify='right')
        self.entry_value.grid(row=row, column=col + 2, padx=pad_x, pady=5)

        # Label and Entry 5: MF Board
        row += row
        col = 0
        tk.Label(self.master, text='Amplitude (Vpp)', anchor='c', width=width).grid(row=row, column=1, padx=0, pady=0, columnspan=1)
        tk.Label(self.master, text='Frequency (kHz)', anchor='c', width=width).grid(row=row, column=2, padx=0, pady=0, columnspan=1)
        row += row
        tk.Label(self.master, text="MF Board", anchor=anchor, width=width).grid(row=row, column=col, padx=pad_x, pady=5)
        self.entry_value = tk.Entry(self.master, textvariable=self.mf_amp, width=COM_width, justify='right')
        self.entry_value.grid(row=row, column=col + 1, padx=pad_x, pady=5)
        self.entry_value = tk.Entry(self.master, textvariable=self.mf_frequency, width=COM_width, justify='right')
        self.entry_value.grid(row=row, column=col + 2, padx=pad_x, pady=5)

        # Run/Restart button
        self.run_button = tk.Button(self.master, text="Run/Restart", command=self.press_run, width=14)
        self.run_button.grid(row=row + 1, column=2, padx=pad_x, pady=10)

        # Quit button
        self.quit_button = tk.Button(self.master, text="Quit", command=self.quit_ui, width=7)
        self.quit_button.grid(row=row + 1, column=3, padx=pad_x, pady=10)

    def quit_ui(self):
        self.routine_running = False
        if self.thread:
            self.thread.join()
        self.master.destroy()

    def press_run(self):
        if not self.routine_running:
            self.routine_running = True
            self.thread = threading.Thread(target=self.worker_loop)
            self.set_hardware_values()
            self.thread.start()

    # def process_queue(self):
    #     try:
    #         while True:
    #             msg = self.queue.get_nowait()
    #             print(msg)
    #     except queue.Empty:
    #         pass
    #     self.master.after(100, self.process_queue)

    def worker_loop(self):
        while self.routine_running:
            routine.ui_routine(self)
        print("Worker_loop ended")


def create_ui():
    root = tk.Tk()
    root.title("Initialization")
    app = InitializationInterface(root)
    root.mainloop()

    new_window = tk.Tk()
    new_window.title("Get Pumped!")
    PumpControlUserInterface(new_window, app)
    new_window.mainloop()

    # window.iconbitmap(r'count.ico')


if __name__ == '__main__':
    create_ui()

# TODO: Add icon
# TODO: Print progress / progress bar?

# TODO: How to quit without crashing
# TODO: Quit safely ^ turn off voltage and all pumps
