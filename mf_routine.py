import time

from mf_ui import MultifrequencyBoardInterface


def routine(mf_control: MultifrequencyBoardInterface):
    # Set parameters
    mf_control.device.mf_board.amplitude = mf_control.mf_amp
    mf_control.device.mf_board.frequency = mf_control.mf_frequency

    # Turn on board and wait
    mf_control.device.mf_board.enable()
    time.sleep(mf_control.mf_time_ON.get())

    # Turn off board and wait
    mf_control.device.mf_board.disable()
    time.sleep(mf_control.mf_time_OFF.get())
