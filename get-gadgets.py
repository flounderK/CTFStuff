from ropper import RopperService
import argparse
"""The regular Ropper.py was throwing an error, so im doing this"""

parser = argparse.ArgumentParser()
parser.add_argument("filepath", help="File to get gadgets from")
args = parser.parse_args()

options = {'color' : False,
            'badbytes': '00',
            'all' : False,
            'inst_count' : 6,
            'type' : 'all',
            'detailed' : False}

filename = args.filepath

rs = RopperService(options)
rs.addFile(filename)
rs.loadGadgetsFor()
gadgets = rs.getFileFor(filename).gadgets 
for i in gadgets:
    print(f"{hex(i.address)}:  {i.simpleInstructionString()}")
