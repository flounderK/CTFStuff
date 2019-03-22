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
        if self.actions[name].get("Sub-Execution") is not None and self.actions[name]["Sub-Execution"]["Pre"] > 0:
            payload += self.sub_execute(self.actions[name]["Sub-Execution"]["Pre"],
                                        self.actions[name]["Sub-Execution"])

        for item in queue:
            payload += self.packer(item)

        if self.actions[name].get("Sub-Execution") is not None and self.actions[name]["Sub-Execution"]["Post"] > 0:
            payload += self.sub_execute(self.actions[name]["Sub-Execution"]["Post"],
                                        self.actions[name]["Sub-Execution"])

        return payload

    def sub_execute(self, iters, specs: dict):
        """This function will service as an easy way to perform other actions before or after this action is executed
        as well as make small modifications to the parameters of the """
        changing_param_ind = None

        if specs.get("actionable_param") is not None and specs["actionable_param"] != "":
            changing_param_ind = self.actions[specs["name"]]["Parameters"].index(specs["actionable_param"])

        args = specs["args"]
        payload = b''
        for iteration in range(0, iters):

            payload += self.execute(specs["name"], *args)
            if changing_param_ind is not None:
                args = list(args)
                action_on_iteration = specs["action_on_iteration"]
                args[changing_param_ind] = action_on_iteration(args[changing_param_ind])
                args = tuple(args)

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
                "Queue": list(),
                "Sub-Execution": {"name": "",
                                  "args": tuple(),
                                  "Pre": 0,
                                  "Post": 0,
                                  "action_on_iteration": lambda a: a + 1,
                                  "actionable_param": ""}}

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


def test_sub():
    gizmo_maker = GizmoMaker()
    basic_template = gizmo_maker.get_template_template()
    basic_template["name"] = "basic"
    basic_template["Parameters"] = ["1", "2"]
    basic_template["Queue"] = ["1", "2"]

    template = gizmo_maker.get_template_template()
    template["name"] = "adv"
    template["Parameters"] = ["Param1", "Param2"]
    template["Queue"] = ["Param1", "Param2"]
    template["Sub-Execution"]["name"] = "basic"
    template["Sub-Execution"]["Pre"] = 2
    template["Sub-Execution"]["actionable_param"] = "1"
    template["Sub-Execution"]["args"] = (0x1, 0x1)

    gizmo_maker.add_template(basic_template)
    gizmo_maker.add_template(template)

    print(gizmo_maker.execute("adv", 0x1, 0x1))


if __name__ == "__main__":
    test_sub()
