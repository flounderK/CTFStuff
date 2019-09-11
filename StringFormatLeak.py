import re
import argparse


def batch(it, siz):
    l = len(it)
    for i in range(0, l, siz):
        yield it[i:i+siz]


def gen_format_strings(start, end,  batchsize):
    fmt = ".%{0}$08X"
    octet_fmt_strings = [fmt.format(i).encode() for i in range(start, end)]
    for format_string_list in batch(octet_fmt_strings, batchsize):
        payload = b"".join(format_string_list)
        yield payload


def decode_output(string):
    if isinstance(string, str):
        string = string.encode()
    hex_vals = re.findall(b'[0-9A-F]+', string)
    decoded_strings = [bytes.fromhex(i.decode()).decode('ISO-8859-1')[::-1] for
                       i in hex_vals]
    decoded_string = ''.join(decoded_strings)
    return decoded_string


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()
    gen = subparsers.add_parser('gen', aliases=['g'])
    gen.set_defaults(func=gen_format_strings)
    gen.add_argument("--start", "-s", help="integer to start at",
                     type=int, required=True)
    gen.add_argument("--end", "-e", help="integer to end at", 
                     type=int, required=True)
    gen.add_argument("--batchsize", "-b", 
                     help="number of octets to print per formatstring",
                     type=int, required=True)
    dec = subparsers.add_parser("decode", aliases=["d"])
    dec.set_defaults(func=decode_output)

    dec.add_argument("--string", "-s", 
                     help="string to decode, little endian is assumed",
                     type=str, required=True)
    args = parser.parse_args()

    if args.__contains__('func'):
        kwargs = {k: v for k, v in args._get_kwargs() if k != 'func'}
        for i in args.func(**kwargs):
            if isinstance(i, bytes):
                print(i.decode())
            else:
                print(i, end="")
        print("")

