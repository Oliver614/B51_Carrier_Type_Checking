"""
Implementation to talk to the siemens PLC on the buffer.
Some things to take into consideration is:
Siemens is BIG ENDIAN whereas most computers are LITTLE ENDIAN,
take this into consideration when writing bits on the PLC.

An example:                                                                     BIT:   01234567
To set bit one of a byte in siemens for example DB01_DBX0.1 start from left to right 0b10000000
"""

import snap7
import time
from snap7 import util

from Log import Logger

PLC_ADDRESS = ''
INTERFACE_DB_ON_PLC = 0


class PlcInterface:
    """
    Interface class for talking to the PLC
    """
    def __init__(self, plc_address: str, interface_db: int):
        self.name = 'PLC Interface'
        self._plc_address = plc_address
        self._interface_db = interface_db
        self._buffer_plc = snap7.client.Client()
        self._buffer_plc.connect(self._plc_address, 0, 3)

    def hand_shake(self):
        """
        handshakes with the PLC to ensure a connection.
        Send 0b10101010:
        Retrieve 0b01010101 from the same row in the DB
        Send | Retrieve == 255
        :param db: the db the interface is made with.
        :return: boolean if the handshake was successful or not
        """
        write_value: bytearray = 0b10101010
        # Write a byte to the PLC DB in the first row.
        self._buffer_plc.db_write(self._interface_db, 0, 1, write_value)

        # Give the plc time to set the bit to 0.
        time.sleep(1)

        # Read a byte from the byte in the db.
        read_value: bytearray = self._buffer_plc.db_read(self._interface_db, 0, 1)

        # sum_: bytearray = write_value | read_value # maybe use this...maybe

        if read_value == 85:
            Logger.log_info(self.name, "Hand shake with PLC successful")
            return True
        Logger.log_error(self.name, "Hand shake with PLC NOT successful")
        return False

    def set_db_row(self, db, start, size, _bytearray):
        """
        Here we replace a piece of data in a db block with new data
        Args:
           db (int): The db to use
           start(int): The start within the db
           size(int): The size of the data in bytes
           _bytearray (enumerable): The data to put in the db
        """
        self._buffer_plc.db_write(db, start, size, _bytearray)

    def get_db_row(self, start: int, size: int):
        """
        Gets data from the interface DB in the PLC and returns a raw byte array.
        :param start: (int) the starting row
        :param size: (int) the amount of data in bytes to capture float = 4 bytes etc...
        :return:
        """
        type_ = snap7.types.wordlen_to_ctypes[snap7.types.S7WLByte]
        data: bytearray = self._buffer_plc.db_read(self._interface_db, start, size)
        return bytearray


