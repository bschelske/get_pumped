import tkinter as tk
from tkinter import filedialog


class InitializationInterface:
    def __init__(self, master):
        self.master = master

        self.outlet_COM = tk.StringVar(value='COM1')
        self.cell_COM = tk.StringVar(value='COM1')
        self.buffer_COM = tk.StringVar(value='COM1')
        self.waste_COM = tk.StringVar(value='COM1')
        self.mf_COM = tk.StringVar(value='COM1')

        self.outlet_ADDR = tk.StringVar(value='0')
        self.cell_ADDR = tk.StringVar(value='1')
        self.buffer_ADDR = tk.StringVar(value='2')
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

        # OK button
        self.OK_button = tk.Button(self.master, text="OK", command=self.press_ok, width=7)
        self.OK_button.grid(row=row+1, column=2, padx=1, pady=10)

        # Quit button
        self.quit_button = tk.Button(self.master, text="Quit", command=self.quit_ui, width=7)
        self.quit_button.grid(row=row+1, column=3, padx=1, pady=10)



    def quit_ui(self):
        self.master.destroy()
        quit(2)

    def press_ok(self):
        self.master.destroy()
        new_window = tk.Tk()
        new_window.title("Get Pumped!")
        PumpControlUserInterface(new_window, self)


class PumpControlUserInterface:
    def __init__(self, master, init_settings):
        self.init_settings = init_settings
        self.master = master
        self.placeholder_value = tk.IntVar(value=10)

        # Pump default flow rates
        self.inlet_flow_rate = tk.StringVar(value="1200 um")

        self.buffer_rate = self.inlet_flow_rate
        self.cell_rate = self.inlet_flow_rate
        self.waste_rate = self.inlet_flow_rate

        self.outlet_capture = tk.StringVar(value="100 nm")
        self.outlet_ff = tk.StringVar(value="1200 um")

        # Pump default target volumes
        self.inlet_target_volume = tk.StringVar(value="20 u")
        self.buffer_volume = self.inlet_target_volume
        self.cell_volume = self.inlet_target_volume
        self.waste_volume = self.inlet_target_volume

        # MF Board Parameters
        self.mf_amp = tk.StringVar(value='28')
        self.mf_frequency = tk.StringVar(value='90')

        self.create_toolbar()
        self.create_pump_controls()

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
        self.entry_value = tk.Entry(self.master, textvariable=self.outlet_capture, width=COM_width, justify='right')
        self.entry_value.grid(row=row, column=col + 1, padx=pad_x, pady=5)


        # Label and Entry 1: Outlet Pump
        row += row
        col = 0
        tk.Label(self.master, text="Outlet Pump FF", anchor=anchor, width=width).grid(row=row, column=col, padx=pad_x, pady=5)
        self.entry_value = tk.Entry(self.master, textvariable=self.outlet_ff, width=COM_width, justify='right')
        self.entry_value.grid(row=row, column=col + 1, padx=pad_x, pady=5)
        self.entry_value = tk.Entry(self.master, textvariable=self.outlet_ff, width=COM_width, justify='right')
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

        # Update button
        self.update_button = tk.Button(self.master, text="Update Settings", command=self.press_ok, width=14)
        self.update_button.grid(row=row + 1, column=1, padx=pad_x, pady=10)

        # Run/Restart button
        self.run_button = tk.Button(self.master, text="Run/Restart", command=self.press_ok, width=14)
        self.run_button.grid(row=row + 1, column=2, padx=pad_x, pady=10)

        # Quit button
        self.quit_button = tk.Button(self.master, text="Quit", command=self.quit_ui, width=7)
        self.quit_button.grid(row=row + 1, column=3, padx=pad_x, pady=10)

    def quit_ui(self):
        self.master.destroy()
        quit(2)

    def press_ok(self):
        self.master.destroy()
        # new_window = tk.Tk()
        # new_window.title("New Window")



def create_ui():
    root = tk.Tk()
    root.title("Initialization")
    app = InitializationInterface(root)
    root.mainloop()
    return app

    # window.iconbitmap(r'count.ico')


if __name__ == '__main__':
    create_ui()

# TODO: Add icon
# TODO: Print progress / progress bar?
# TODO: Access classes from ui
# TODO: update classes from ui during routine while loop
