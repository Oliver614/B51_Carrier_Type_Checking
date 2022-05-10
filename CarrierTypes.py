
import enum


class CarrierTypes(enum):
    """
    Carrier types used for classification.
    """
    CARRIER_TYPE_UNKNOWN: bytearray = 0
    BY631: bytearray = 1
    BY634_635: bytearray = 2
    BY636: bytearray = 3
    by631_EWB: bytearray = 4


def to_big_endian(_byte: bytearray):
    """
    Use when sending bytes to the plc.
    :param _byte: the byte to convert
    :return: the byte with the bit order reversed.
    """
    return _byte.reverse()
