import json
import re
import sys

DEBUG = True
COMMENTS = False
ASS_FILE = sys.argv[1]
if len(sys.argv) > 2:
    if sys.argv[2] == "-c":
        COMMENTS = True

if "Test" in ASS_FILE:
    DEBUG = True

with open(ASS_FILE) as f:
    max_ins = f.read().splitlines()

CLEANED = []
for m in max_ins:
    idx = -1
    instance = re.search("/", m)
    if instance:
        idx = instance.span()[0]
    if idx != -1:
        m = m[0:idx]
    curr_line = m.split(" ")
    if curr_line == [""]:
        continue
    cleaned_line = filter(None, curr_line)
    # if len(cleaned_line) == 1:
    # continue
    CLEANED.append(cleaned_line)


mask_map = {
    0: 0x01,
    1: 0x80,
    2: 0xFF,
    3: 0x20
}


def handle_line(line, outfile):
    """
            return a 9 bit machine code line given a line
            of assembly
    """
    sep = "\n"
    if COMMENTS:
        sep = "\t\t//" + " ".join(line) + "\n"
    # print "Handling line ", line
    if len(line) >= 1:
        # skip labels
        if ":" in line[0]:
            return
        inst_type = MASTER_LOOKUP[line[0]]["type"]
        # print inst_type
        # print line

        if inst_type == "J":
            # print line
            # handle J type
            opcode = MASTER_LOOKUP[line[0]]["opcode"]
            func = MASTER_LOOKUP[line[0]]["func"]
            rs = line[1]
            rs = reg_to_num(rs)
            rs = as_binary(rs)
                
            outfile.write(str(opcode + rs + func) + sep)

        elif inst_type == "G":
            # handle G type
            # print line
            if line[0] != "flip":

                opcode = MASTER_LOOKUP[line[0]]["opcode"]
                func = MASTER_LOOKUP[line[0]]["func"]
                rs = reg_to_num(line[1])
                rs = as_binary(rs)
                mask_selector = int(line[2])
                mask_selector = bin(mask_selector)[2:].zfill(2)
                outfile.write(str(opcode + rs + mask_selector + func + sep))
            else:
                opcode = MASTER_LOOKUP[line[0]]["opcode"]
                func = MASTER_LOOKUP[line[0]]["func"]
                rs = reg_to_num(line[1])
                rs = as_binary(rs)
                mask_selector = "10"
                outfile.write(str(opcode + rs + mask_selector + func + sep))

        elif inst_type == "H":
            # handle H type
            # print line
            opcode = MASTER_LOOKUP[line[0]]["opcode"]
            func = MASTER_LOOKUP[line[0]]["func"]
            if len(line) > 1:
                immediate = int(line[1])
                # print "immediate value: ", immediate
                if immediate > 0:
                    immediate = bin(immediate)[2:].zfill(4)
                # if immediate < 0, use 2s comp repr of immediate
                elif immediate < 0:
                    immediate = bin(immediate % (1<<4))[2:]
                else:
                    immediate = "0000"
            # print immediate
            # print "immediate value in binary: ", immediate
                if len(immediate) > 4:
                    immediate = "1111"
                outfile.write(str(opcode + immediate + func) + sep)
            elif len(line) == 1 and line[0] == "halt":
                immediate = "0000"
                outfile.write(str(opcode + immediate + func) + sep)
            elif len(line) == 1 and line[0] == "movc":
                immediate = "1111"
                outfile.write(str(opcode + immediate + func) + sep)

        elif inst_type == "B":
            # print line
            opcode = MASTER_LOOKUP[line[0]]["opcode"]
            func = MASTER_LOOKUP[line[0]]["func"]
            rs = reg_to_num(line[1])
            rs = as_binary(rs)
            rt = "0"
            # print line, rs
            outfile.write(str(opcode + rs + rt + func) + sep)
            # handle B type
    return 0


def as_binary(reg):
    if isinstance(reg, int):
        return bin(reg)[2:].zfill(4)
    else:
        return bin(15)

# print as_binary(6)


def reg_to_num(r):
    """
    TODO: regex on s register
    """
    # print "incoming r: ", r
    patt = re.search("(\$r)|(\$s)|(\$rCarry)", r)
    if patt:
        kind = r[1]
        # print "kind:", kind
        # print "found match ", patt
        idcs = patt.span()
        # print idcs
        r = r[idcs[1]:]
        # print "gonna return ", r
        if r == "Carry":
            return 15
        elif kind == "r":
            r = int(r)
            return r + 2
        elif kind == "s":
            r = int(r)
            return r
    else:
        return int(r)


if __name__ == '__main__':

    with open("parse_isa.txt") as f:
        INSTRUCTIONS = f.readlines()

    """
	items in master map follow the following format:
	(name, type, opcode, function_code)
	where:
		name is the name of the instruction
		type is either G, J, H, or B
		opcode is opcode
		func code is func code
	"""
    MASTER_MAP = []
    for inst in INSTRUCTIONS:
        inst = inst.replace("\n", "")
        MASTER_MAP.append(tuple(inst.split(" ")))

    # for m in master_map:
    # 	print m

    MASTER_LOOKUP = dict()

    for inst in MASTER_MAP:
        name = inst[0]
        cat = inst[1]
        opcode = inst[2]
        func = inst[3]
        MASTER_LOOKUP[name] = dict(type=cat, opcode=opcode, func=func)
    # print json.dumps(master_lookup, indent=4)

    if not DEBUG:
        with open("machineCode/"+ASS_FILE.replace(".ass", "")+".txt", "w") as outfile:
            for clean in CLEANED:
                mach_code = handle_line(clean, outfile)
    else:
        with open(ASS_FILE.replace(".ass", "")+".txt", "w") as outfile:
            for clean in CLEANED:
                mach_code = handle_line(clean, outfile)
