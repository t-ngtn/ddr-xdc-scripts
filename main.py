import sys
import re
import csv
from enum import Enum

class Property:
    def __init__(self, package_pin, iostandard, port_name, bank, vcco, net_name, io_info):
        self.package_pin = package_pin
        self.iostandard = iostandard
        self.port_name = port_name
        self.bank = bank
        self.vcco = vcco
        self.net_name = net_name
        self.io_info = io_info

    def __repr__(self):
        return (f"Property(package_pin={self.package_pin}, iostandard={self.iostandard}, "
                f"port_name={self.port_name}, bank={self.bank}, vcco={self.vcco}, "
                f"net_name={self.net_name}, io_info={self.io_info})")

    def to_dict(self):
        return {
            "PACKAGE_PIN": self.package_pin,
            "IOSTANDARD": self.iostandard,
            "PORT_NAME": self.port_name,
            "BANK": self.bank,
            "VCCO": self.vcco,
            "NET_NAME": self.net_name,
            "IO_INFO": self.io_info,
        }

def parse_lines(tcl_text: str) -> list[Property]:
    properties = []
    pattern = re.compile(
        r'set_property -dict \{PACKAGE_PIN (\S+)\s+IOSTANDARD (\S+)\s+\} '
        r'\[get_ports (\S+)\s+\]; # Bank (\S+)\s+VCCO - (\S+)\s+Net "(.*?)"\s+- (.+)'
    )

    for line in tcl_text.strip().splitlines():
        match = pattern.match(line)
        if match:
            properties.append(Property(
                package_pin=match.group(1),
                iostandard=match.group(2),
                port_name=match.group(3),
                bank=match.group(4),
                vcco=match.group(5),
                net_name=match.group(6),
                io_info=match.group(7),
            ))
    return properties

def to_csv(properties: Property, input_file_name:str):
    with open(f"out/{input_file_name}.csv", "w") as f:
        writer = csv.DictWriter(f, fieldnames=properties[0].to_dict().keys())
        writer.writeheader()
        for prop in properties:
            writer.writerow(prop.to_dict())

    print(f"output success!\nOutput file: out/{input_file_name}.csv")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py input_file output_type\n output_type: csv or xdc")
        sys.exit(1)

    input_file = sys.argv[1]
    input_file_name = input_file.split("/")[-1]
    with open(input_file, 'r') as f:
        input_text = f.read()

    properties = parse_lines(input_text)
    to_csv(properties, input_file_name)
