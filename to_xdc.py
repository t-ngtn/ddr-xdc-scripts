import sys

from parse import Property, parse_lines, to_csv
from fix_xdc import prop_to_xdc

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python main.py correct_file master_file")
        sys.exit(1)

    correct_file = sys.argv[1]
    with open(correct_file, 'r') as f:
        correct_text = f.read()

    correct_props = parse_lines(correct_text)

    master_file = sys.argv[2]
    with open(master_file, 'r') as f:
        master_text = f.read()

    master_props = parse_lines(master_text)

    target_slot = "C2"
    master_target_props = [x for x in master_props if x.slot == target_slot]

    for prop in correct_props:
        for master_target_prop in master_target_props:
            if prop.net_name == master_target_prop.net_name:
                prop.bank = master_target_prop.bank
                prop.io_info = master_target_prop.io_info
                prop.package_pin = master_target_prop.package_pin
                prop.slot = master_target_prop.slot

    prop_to_xdc(correct_props, target_slot)