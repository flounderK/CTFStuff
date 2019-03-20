import struct
import json


class GizmoMaker:
    """This class is meant to store templates for ROP-Chain gizmos so that gizmos can easily be
    created, stored, and used automatically in a structured manner"""
    def __init__(self, packer=lambda a: struct.pack("<I", a), bytes_per_pack=4):

        self.packer = packer
        self.bytes_per_pack = bytes_per_pack
        self.templates = dict()
        self.actions = dict()

    def add_template(self, template: dict):
        """Add a template to the gizmo maker. For a template for your template,
        use get_template_template()"""
        self.templates[template["name"]] = template
        # adding this so that if someone wants to make a template with constants already in place they can
        self.actions[template["name"]] = template

    def execute(self, name, *args):
        """Returns the packed and encoded gizmo, ready for integration into your rop chain"""
        parameters = self.actions[name]["Parameters"]
        queue = self.actions[name]["Queue"]
        for arg_ind in range(0, len(args)):
            queue = [i if i != parameters[arg_ind] else args[arg_ind] for i in queue]

        payload = b''
        for item in queue:
            payload += self.packer(item)
        return payload

    def init_template(self, name, *args):
        """Initialize or re-initialize constants in your template and make the initialized version available to
        the execute function"""
        self.actions[name] = self.templates[name]
        constants = self.templates[name]["Constants"]
        queue = self.templates[name]["Queue"]
        for arg_ind in range(0, len(args)):
            queue = [i if i != constants[arg_ind] else args[arg_ind] for i in queue]

        self.actions[name]["Queue"] = queue

    def get_template_template(self):
        """Provides a blank template that can be used"""
        return {"name": "",
                "Constants": list(),
                "Parameters": list(),
                "Queue": list()}

    def load_templates(self, json_path):
        """Load templates from a json file. Structure of json should be [template, template, etc...]"""
        with open(json_path, "r") as f:
            json_content = json.load(f)
        for template in json_content:
            self.add_template(template)


def example_usage():
    gizmo_maker = GizmoMaker()
    template = gizmo_maker.get_template_template()
    template["name"] = "test_action"
    template["Constants"] = ["popper", "mover"]
    template["Parameters"] = ["Parameter1", "Parameter2"]
    template["Queue"] = ["popper", "Parameter1", "Parameter2", "mover"]
    gizmo_maker.add_template(template)
    gizmo_maker.init_template("test_action", 0xcafebabe, 0xdeadbeef)
    print(gizmo_maker.execute("test_action", 0x4a4a4a4a, 0x4b4b4b4b))




