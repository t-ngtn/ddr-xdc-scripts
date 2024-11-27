import sys
from pprint import pprint

from parse import Property, parse_ddr_lines

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python check_diff.py input_file_1, input_file_2")
        sys.exit(1)

    input_file_1 = sys.argv[1]
    input_file_name_1 = input_file_1.split("/")[-1]
    with open(input_file_1, 'r') as f:
        input_text_1 = f.read()

    input_file_2 = sys.argv[2]
    input_file_name_2 = input_file_2.split("/")[-1]
    with open(input_file_2, 'r') as f:
        input_text_2 = f.read()

    p1 = parse_ddr_lines(input_text_1)
    pin_to_port_1 = {x.package_pin: x.net_name for x in p1}

    p2 = parse_ddr_lines(input_text_2)
    pin_to_port_2 = {x.package_pin: x.net_name for x in p2}


    for k, v in pin_to_port_1.items():
        if k in pin_to_port_2:
            if v != pin_to_port_2[k]:
                print(f"Pin {k} has different port name: {v} -> {pin_to_port_2[k]}")