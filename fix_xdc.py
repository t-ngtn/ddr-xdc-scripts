import sys
from pprint import pprint
from parse import Property, parse_lines

def prop_to_xdc(props: list[Property], file_name) -> None:
    with open(f"out/{file_name}.xdc", "w") as f:
        for p in props:
            f.write(f"set_property -dict {{PACKAGE_PIN {p.package_pin} IOSTANDARD {p.iostandard} }} [get_ports {p.port_name}]; # Bank {p.bank} VCCO - {p.vcco} Net \"DDR4_{p.slot}_{p.net_name}\" - {p.io_info}\n")

    print(f"output success!\nOutput file: out/{file_name}.xdc")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python main.py input_file correct_file")
        sys.exit(1)

    input_file = sys.argv[1]
    input_file_name = input_file.split("/")[-1]
    with open(input_file, 'r') as f:
        input_text = f.read()

    props = parse_lines(input_text)

    correct_file = sys.argv[2]
    correct_file_name = correct_file.split("/")[-1]
    with open(correct_file, 'r') as f:
        correct_text = f.read()

    correct_props = parse_lines(correct_text)

    pin2net = {}
    for p in correct_props:
        pin2net[p.package_pin] = p.net_name

    for p in props:
        if p.package_pin in pin2net and p.net_name != pin2net[p.package_pin]:
            p.net_name = pin2net[p.package_pin]
            print(f"Pin {p.package_pin} has different net name: {p.net_name} -> {pin2net[p.package_pin]}")

    prop_to_xdc(props, "corrrect_" + input_file_name.split(".")[0])