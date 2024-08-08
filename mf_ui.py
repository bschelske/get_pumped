import tkinter as tk

import mf_routine
from classes import MultifrequencyBoard


class MultifrequencyInitializationInterface:
    def __init__(self, master):
        self.master = master
        # Default COM values
        self.mf_COM = tk.StringVar(value='COM8')
        # Default address values
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
        tk.Label(self.master, text='Enter COM (windows device manager)\nfor the board', anchor='c', width=35).grid(row=row, column=0, columnspan=4, padx=15, pady=5)
        row += row
        tk.Label(self.master, text='"COM#"', anchor='c', width=5).grid(row=row, column=1, columnspan=4,  padx=15, pady=0)

        row += row
        col = 0
        # tk.Label(self.master, text="Multifrequency Board:", anchor=anchor, width=width).grid(row=row, column=col, padx=5, pady=5)
        self.entry_value = tk.Entry(self.master, textvariable=self.mf_COM, width=COM_width, justify='center')
        self.entry_value.grid(row=row, column=col + 1, columnspan=4, padx=5, pady=5)

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
        self.mf_board = MultifrequencyBoard(self.mf_COM.get())
        self.master.destroy()


class MultifrequencyBoardInterface:
    def __init__(self, master, MultifrequencyInitializationInterface):
        self.device = MultifrequencyInitializationInterface
        self.master = master
        self.running = False

        self.set_ui_default_values()
        self.create_toolbar()
        self.create_widget()

    def set_ui_default_values(self):
        # MF Board Parameters
        self.mf_amp = tk.StringVar(value='1')
        self.mf_frequency = tk.StringVar(value='90')
        self.mf_time_ON = tk.IntVar(value=1)
        self.mf_time_OFF = tk.IntVar(value=1)

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

    def create_widget(self):
        anchor = "e"
        width = 15
        COM_width = 9
        pad_x = 1
        row = 1
        col = 2
        # Amplitude
        tk.Label(self.master, text='Amplitude (Vpp)', anchor='e', width=width).grid(row=1, column=col, padx=0, pady=0, columnspan=1)
        self.entry_value = tk.Entry(self.master, textvariable=self.mf_amp, width=COM_width, justify='right')
        self.entry_value.grid(row=1, column=col+1, padx=pad_x, pady=5)

        # Frequency
        row += row
        tk.Label(self.master, text='Frequency (kHz)', anchor='e', width=width).grid(row=row, column=col, padx=0, pady=0, columnspan=1)
        self.entry_value = tk.Entry(self.master, textvariable=self.mf_frequency, width=COM_width, justify='right')
        self.entry_value.grid(row=row, column=col+1, padx=pad_x, pady=5)

        # Time ON
        row += row
        tk.Label(self.master, text='Time ON (sec)', anchor='e', width=width).grid(row=row, column=col, padx=0, pady=0,
                                                                                    columnspan=1)
        self.entry_value = tk.Entry(self.master, textvariable=self.mf_time_ON, width=COM_width, justify='right')
        self.entry_value.grid(row=row, column=col + 1, padx=pad_x, pady=5)

        # Time OFF
        row += row
        tk.Label(self.master, text='Time OFF (sec)', anchor='e', width=width).grid(row=row, column=col, padx=0, pady=0,
                                                                                    columnspan=1)
        self.entry_value = tk.Entry(self.master, textvariable=self.mf_time_OFF, width=COM_width, justify='right')
        self.entry_value.grid(row=row, column=col + 1, padx=pad_x, pady=5)

        # Start button
        self.start = tk.Button(self.master, text="Start", command=self.start_loop, width=14)
        self.start.grid(row=row + 1, column=2, padx=pad_x, pady=10)

        # Stop button
        self.start = tk.Button(self.master, text="Stop", command=self.stop_loop, width=14)
        self.start.grid(row=row + 1, column=3, padx=pad_x, pady=10)

        # Quit button
        self.quit_button = tk.Button(self.master, text="Quit", command=self.quit_ui, width=7)
        self.quit_button.grid(row=row + 1, column=4, padx=pad_x, pady=10)

    def quit_ui(self):
        self.stop_loop()
        self.device.mf_board.disable()
        self.master.destroy()

    def start_loop(self):
        if not self.running:
            self.running = True
            self.loop()

    def stop_loop(self):
        print("Stopping")
        self.running = False

    def loop(self):
        if self.running:
            mf_routine.routine(self)
            # Schedule the next execution of this loop
            self.master.after(1000, self.loop)


def create_ui():
    root = tk.Tk()
    root.title("Initialization")
    app = MultifrequencyInitializationInterface(root)
    root.mainloop()

    new_window = tk.Tk()
    new_window.title("Control that MF board")
    MultifrequencyBoardInterface(new_window, app)
    new_window.mainloop()

    # window.iconbitmap(r'count.ico')


if __name__ == '__main__':
    create_ui()

# TODO: Add icon
