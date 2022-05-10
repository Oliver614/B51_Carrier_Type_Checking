# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import time
from PLC_Interface import PlcInterface
from VisionInterface import VisionInterface
from Log import Logger
from Window import *
import HistoryLog


def init():
    Logger.log_info("main_init", "Started Initialisation")
    plc_interface_ = PlcInterface("", 0)
    if not plc_interface_.hand_shake():
        Logger.log_error("main_init", "Failed to connect to PLC!")
    vision_interface_ = VisionInterface()
    if not vision_interface_.init_cameras():
        Logger.log_error("min_init", "Failed to initialise cameras!")
    # Todo: initialise neural net
    return plc_interface_, vision_interface_


def main():
    window_ = make_window()
    while True:
        window_.update()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
