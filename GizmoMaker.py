import struct


class GizmoMaker:
    def __init__(self, packer=lambda a: struct.pack("<I", a), bytes_per_pack=4):
        self.packer = packer
        self.bytes_per_pack = bytes_per_pack
        self.templates = dict()

    def add_template(self, template: dict):
        self.templates[template["name"]] = template

    def execute(self, name, *args):
        parameters = self.templates[name]["Parameters"]
        queue = self.templates[name]["Queue"]
        for param_ind in range(0, len(parameters)):
            queue = [i if i != parameters[param_ind] else args[param_ind] for i in queue]

        payload = b''
        for item in queue:
            payload += self.packer(item)
        return payload

    def get_template_template(self):
        return {"name": "",
                "Parameters": list(),
                "Queue": list()}


def example_usage():
    gizmo_maker = GizmoMaker()
    template = gizmo_maker.get_template_template()
    template["name"] = "test_action"
    template["Parameters"] = ["Parameter1", "Parameter2"]
    template["Queue"] = [0xb0bbAD, "Parameter1", "Parameter2", 0x44444444]
    gizmo_maker.add_template(template)
    print(gizmo_maker.execute("test_action", 0x4a4a4a4a, 0x4b4b4b4b))




