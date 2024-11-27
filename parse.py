import sys
import re
import csv

class Property:
    def __init__(self, package_pin, iostandard, port_name, bank, vcco, slot, net_name, io_info):
        self.package_pin = package_pin
        self.iostandard = iostandard
        self.port_name = port_name
        self.bank = bank
        self.vcco = vcco
        self.slot = slot
        self.net_name = net_name
        self.io_info = io_info

    def __repr__(self):
        return (f"Property(package_pin={self.package_pin}, iostandard={self.iostandard}, "
                f"port_name={self.port_name}, bank={self.bank}, vcco={self.vcco}, "
                f"slot={self.slot}, net_name={self.net_name}, io_info={self.io_info})")

    def to_dict(self):
        return {
            "PACKAGE_PIN": self.package_pin,
            "IOSTANDARD": self.iostandard,
            "PORT_NAME": self.port_name,
            "BANK": self.bank,
            "VCCO": self.vcco,
            "SLOT": self.slot,
            "NET_NAME": self.net_name,
            "IO_INFO": self.io_info,
        }

def parse_lines(xdc_text: str) -> list[Property]:
    properties = []
    pattern = re.compile(
        r'set_property -dict \{\s*PACKAGE_PIN\s+(\S+)\s+IOSTANDARD\s+(\S+)\s*\} '
        r'\[get_ports\s+(\S+)\s*\];\s+#\s+Bank\s+(\S+)\s+VCCO\s+-\s+(\S+)\s+Net\s+"DDR4_(\S+?)_(\S+?)"\s+-\s+(.+)'
    )

    for line in xdc_text.strip().splitlines():
        match = pattern.match(line)
        if match:
            properties.append(Property(
                package_pin=match.group(1),
                iostandard=match.group(2),
                port_name=match.group(3),
                bank=match.group(4),
                vcco=match.group(5),
                slot=match.group(6),
                net_name=match.group(7),
                io_info=match.group(8)
            ))
    return properties

def parse_ddr_lines(xdc_text: str) -> list[Property]:
    properties = parse_lines(xdc_text)
    ddr_properties = [x for x in properties if "DDR" in x.net_name or "ddr" in x.port_name]
    return ddr_properties

def to_csv(properties: Property, input_file_name:str):
    file_name = input_file_name.split(".")[0]
    with open(f"out/{file_name}.csv", "w") as f:
        writer = csv.DictWriter(f, fieldnames=properties[0].to_dict().keys())
        writer.writeheader()
        for prop in properties:
            writer.writerow(prop.to_dict())
    print(f"output success!\nOutput file: out/{file_name}.csv")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python parse.py input_file")
        sys.exit(1)

    input_file = sys.argv[1]
    input_file_name = input_file.split("/")[-1]
    with open(input_file, 'r') as f:
        input_text = f.read()
    print(input_text)
    properties = parse_lines(input_text)
    print(properties)
    to_csv(properties, input_file_name)
