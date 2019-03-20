import pwn
from GizmoMaker import GizmoMaker


def write_string(popper: int, mover: int, start_addr: int, string: str):
    gizmo_maker = GizmoMaker(packer=pwn.p32, bytes_per_pack=4)
    template = gizmo_maker.get_template_template()
    template["name"] = "arbitrary_write"
    template["Parameters"] = ["to_addr", "value"]
    template["Queue"] = [popper, "to_addr", "value", mover]
    gizmo_maker.add_template(template)
    n = 4
    length = len(string)
    payload = b''
    for word in range(0, length, n):
        hexed = string[word:min(word + n, length)]
        to_addr = start_addr + word
        value = int("0x" + "".join([hex(ord(character))[2:] for character in hexed[::-1]]), 0)
        payload += gizmo_maker.execute("arbitrary_write", to_addr, value)
    return payload

