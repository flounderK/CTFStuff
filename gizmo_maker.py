from ropper import RopperService
import argparse
import itertools

parser = argparse.ArgumentParser()
parser.add_argument("filepath", help="File to get gadgets from")
args = parser.parse_args()

options = {'color': False,
           'badbytes': '00',
           'all': False,
           'inst_count': 6,
           'type': 'all',
           'detailed': False}


def find_useful_pop_rets(rs, filename):
    gadgets = rs.getFileFor(filename).gadgets
    pop_rets = [i for i in gadgets if re.search(r"^( *pop [^;]+;)+ ret;", i.simpleInstructionString())]
    return pop_rets


def find_arbitrary_write_gizmos(rs, filename, pop_source=None):
    """Finds simple arbitrary writes"""
    if pop_source is None:
        pop_source = rs.searchPopPopRet()[filename]

    related_gadgets = list()
    for pop_pop_ret_gad in pop_source:
        for l_reg, r_reg in itertools.permutations(pop_pop_ret_gad.affected_regs, 2):
            for gad in rs.search(search=f"mov [{l_reg}], {r_reg}"):
                related_gadgets.append({"popper": pop_pop_ret_gad, "mover": gad[1]})
    return related_gadgets


filename = args.filepath
rs = RopperService(options)
rs.addFile(filename)
rs.loadGadgetsFor()


print(f"{filename}\n")
arbitrary_write_gizmos = find_arbitrary_write_gizmos(rs, filename)
if len(arbitrary_write_gizmos) > 0:
    print("Basic arbitrary write gizmos:\n")
    for i in arbitrary_write_gizmos:
        print(f"{i['popper']}\n{i['mover']}\n\n")


