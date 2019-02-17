"""This is a quick class to help deal with a challenge where the input string is run through 
memfrob before the vulnerable function is reached"""

import struct
class memfrob_lookup_table:
    def __init__(self):
        self.__generate_lookup_table()

    def __generate_lookup_table(self):
        self.lookup_map = dict()
        for i in range(0,256):
            key = hex(i ^ 42)[2:]
            value = hex(i)[2:]
            if len(key) == 1:
                key = "0" + key
            if len(value) == 1:
                value = "0" + value
            self.lookup_map[key] = value
    
    def __get_bytes(self, hex):
        l = len(hex)
        for i in range(0, l, 2):
            yield hex[i:min(i + 2, l)]

    def lookup_word(self, value, printable=False):
        hex = struct.pack("I", value).hex()
        result = list()
        for i in self.__get_bytes(hex):
            result.append(self.lookup_map[i])
        if printable:
            print("{:s}{:s}".format("\\x", "\\x".join(result)))
        return result

    def lookup_single_byte(self, byte_value, printable=False):
        """This is necessary because some part of lookup defaults to 4 bytes
        and the first 3 are just assumed to be 00."""
        result = self.lookup_word(byte_value)[0]
        if printable:
            print("{:s}{:s}".format("\\x", result))
        return result
