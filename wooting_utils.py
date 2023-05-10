from os import path
import ctypes
import sys
import time

dylib_dir = 'dylibs'

SCAN_CODE_ESC = 0x00
HID_CODE_SPACE = 44
SLEEP_TIME = 0.0001
HID_CODE_ENTER = 40
HID_CODE_LEFT_ARROW = 80
HID_CODE_RIGHT_ARROW = 79


class WootingPython(object):

    def __init__(self, dylib_dir='dylibs'):
        try:
            self._sdk = ctypes.CDLL(path.join(
                dylib_dir, 'libwooting_analog_wrapper.dylib'))
            self._rgb = ctypes.CDLL(path.join(
                dylib_dir, 'libwooting-rgb-sdk.dylib'))
        except OSError as e:
            sys.exit('Failed to load dll from "{}" ({})'.format(dylib_dir, e))
        self._excluded = []

    def set_excluded_keys(self, excluded):
        self._excluded = excluded

    def initialise(self):
        """
        Initialises a Wooting One/Two keyboard
        """
        self._sdk.wooting_analog_initialise()

    def is_initialised(self):
        """
        Returns True if a Wooting One/Two is initialised, False if not
        """
        return bool(self._sdk.wooting_analog_is_initialised())

    def is_connected(self):
        """
        Returns True if a Wooting One/Two is connected, False if not
        """
        return bool(self._rgb.wooting_rgb_kbd_connected())

    def get_info(self, buffer_len=4):
        """
        Returns a device description using the buffer_len.
        Values >=0 indicate the number of items filled into the buffer,
        with `<0` being of type WootingAnalogResult
        """
        # number of keypresses that can be retrieved in one operation
        # (range must be 1-16)
        items = min(max(1, buffer_len), 8)
        # buffer is items x 2 bytes to allow for (keycode, analog value)
        #  pairs to be returned
        buffer = ctypes.cast(ctypes.create_string_buffer(items * 2),
                             ctypes.POINTER(ctypes.c_uint8))

        return self._sdk.wooting_analog_get_connected_devices_info(
            buffer, ctypes.c_uint32(items))

    def read_full_buffer(self, items=4):
        """
        Reads a full buffer from the keyboard. See wooting_read_full_buffer
        description at:
        https://dev.wooting.io/wooting-analog-sdk-guide/analog-api-description/
        """

        # number of keypresses that can be retrieved in one operation
        # (range must be 1-32)
        items = min(max(1, items), 8)

        # buffer is items x 2 bytes to allow for (keycode, analog value)
        # pairs to be returned
        code_buffer = (ctypes.c_uint8 * items)(*(0 for i in range(items)))
        analog_buffer = (ctypes.c_float * items)(*(0 for i in range(items)))
        # call the C function, which returns the number of keys
        # written into the buffer.
        # the values are interleaved, i.e.
        # scancode1, analogvalue1, scancode2, analogvalue2, ...
        items_read = self._sdk.wooting_analog_read_full_buffer(
            code_buffer, analog_buffer, ctypes.c_uint32(items))

        return ([code_buffer[i] for i in range(items_read)],
                [analog_buffer[i] for i in range(items_read)],
                items_read)

    def read_analog(self, keycode):
        return self._sdk.wooting_analog_read_analog(keycode)

    def wait_for_key(self, scan_code):
        """
        Blocks until a specific scan code is received
        """
        while True:
            scan_codes, _, _ = self.read_full_buffer()
            if scan_code in scan_codes:
                return
            time.sleep(SLEEP_TIME)


def get_log_name(prefix='wooting_log_'):
    for i in range(10000):
        fname = path.join('{}{:04d}.csv'.format(prefix, i))
        if not path.exists(path.join(fname)):
            return fname

    return None
