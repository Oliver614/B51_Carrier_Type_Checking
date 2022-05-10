"""
Logging functions, will write to file info, warnings and errors

Use as:
Logger.log_info / warning / error('Class Name', 'Intended Message')
"""

from datetime import datetime


def colored(r, g, b, text):
    """
    Set the RGB colour for text to the console. Good Visual aid.
    """
    return "\033[38;2;{};{};{}m{} \033[38;2;255;255;255m".format(r, g, b, text)


class Logger:
    """
    Static Logger class does not need to be instantiated for use.
    """
    error_file = open('LogFiles/error_log.txt', 'a+')
    warning_file = open('LogFiles/warning_log.txt', 'a+')
    info_file = open('LogFiles/info_log.txt', 'a+')

    @staticmethod
    def log_info(area, message):
        """
        Logs info to console and saves it to log file.
        :param area: The class or program area the info is coming from, use self.name if in a class.
        :param message: The message to be displayed
        :return: nothing.
        """
        now = datetime.now()
        info = '[INFO]: {} [FROM]: {} [MESSAGE]: {}'.format(now.strftime("%Y/%m/%d, %H:%M:%S"), area, message)
        print(colored(0, 255, 0, info))
        Logger.info_file.write(info)
        Logger.info_file.write('\n')

    @staticmethod
    def log_warning(area, message):
        """
        Logs warning to console and saves it to log file.
        :param area: The class or program area the info is coming from, use self.name if in a class.
        :param message: The message to be displayed
        :return: nothing.
        """
        now = datetime.now()
        info = '[WARNING]: {} [FROM]: {} [MESSAGE]: {}'.format(now.strftime("%Y/%m/%d, %H:%M:%S"), area, message)
        print(colored(255, 255, 0, info))
        Logger.warning_file.write(info)
        Logger.warning_file.write('\n')

    @staticmethod
    def log_error(area, message):
        """
        Logs error to console and saves it to log file.
        :param area: The class or program area the info is coming from, use self.name if in a class.
        :param message: The message to be displayed
        :return: nothing.
        """
        now = datetime.now()
        info = '[ERROR]: {} [FROM]: {} [MESSAGE]: {}'.format(now.strftime("%Y/%m/%d, %H:%M:%S"), area, message)
        print(colored(255, 0, 0, info))
        Logger.error_file.write(info)
        Logger.error_file.write('\n')
