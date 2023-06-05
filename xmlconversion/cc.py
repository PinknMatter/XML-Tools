import argparse
import re
import os

""""
Created By Noah Kornberg

.CC file conversion
This tool will convert .CC files into .CCC or .CDL file types 

"""

def parse_cc(input_file):
    with open(input_file, 'r') as file:
        cc_content = file.read()

    id_match = re.search(r'id="(.*?)"', cc_content)
    slope_match = re.search(r'<Slope>(.*?)</Slope>', cc_content)
    offset_match = re.search(r'<Offset>(.*?)</Offset>', cc_content)
    power_match = re.search(r'<Power>(.*?)</Power>', cc_content)
    saturation_match = re.search(r'<Saturation>(.*?)</Saturation>', cc_content)

    if not all([id_match, slope_match, offset_match, power_match, saturation_match]):
        raise ValueError("Unable to extract required elements from the input file.")

    id = id_match.group(1)
    slope = slope_match.group(1)
    offset = offset_match.group(1)
    power = power_match.group(1)
    saturation = saturation_match.group(1)

    return id, slope, offset, power, saturation


def write_cdl(output_path, id, slope, offset, power, saturation):
    try:
        filename = os.path.join(output_path, f"{id}.cdl")
        with open(filename, 'w') as file:
            file.write(f'<ColorDecisionList xmlns="urn:ASC:CDL:v1.01">\n')
            file.write(f'  <ColorDecision>\n')
            file.write(f'    <ColorCorrection>\n')
            file.write(f'      <SOPNode>\n')
            file.write(f'        <Description>{id}</Description>\n')
            file.write(f'        <Slope>{slope}</Slope>\n')
            file.write(f'        <Offset>{offset}</Offset>\n')
            file.write(f'        <Power>{power}</Power>\n')
            file.write(f'      </SOPNode>\n')
            file.write(f'      <SatNode>\n')
            file.write(f'        <Saturation>{saturation}</Saturation>\n')
            file.write(f'      </SatNode>\n')
            file.write(f'    </ColorCorrection>\n')
            file.write(f'  </ColorDecision>\n')
            file.write(f'</ColorDecisionList>\n')
        print(f"CDL file '{filename}' was successfully created.")
    except IOError:
        raise ValueError("Error writing the CDL file.")


def write_ccc(output_path, id, slope, offset, power, saturation):
    try:
        filename = os.path.join(output_path, f"{id}.ccc")
        with open(filename, 'w') as file:
            file.write('<ColorCorrectionCollection xmlns="urn:ASC:CDL:v1.01">\n')
            file.write('  <ColorCorrection id="{}">\n'.format(id))
            file.write('    <SOPNode>\n')
            file.write('      <Slope>{}</Slope>\n'.format(slope))
            file.write('      <Offset>{}</Offset>\n'.format(offset))
            file.write('      <Power>{}</Power>\n'.format(power))
            file.write('    </SOPNode>\n')
            file.write('    <SatNode>\n')
            file.write('      <Saturation>{}</Saturation>\n'.format(saturation))
            file.write('    </SatNode>\n')
            file.write('  </ColorCorrection>\n')
            file.write('</ColorCorrectionCollection>\n')
        print(f"CCC file '{filename}' was successfully created.")
    except IOError:
        raise ValueError("Error writing the CCC file.")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", help="Input CC file.")
    parser.add_argument("output_path", help="Output path for the files.")
    parser.add_argument("--output_type", help="Output type (CDL or CCC).", default="CDL")

    args = parser.parse_args()

    input_file = os.path.abspath(args.input_file)
    args.output_path = os.path.dirname(os.path.abspath(args.output_path))

    try:
        id, slope, offset, power, saturation = parse_cc(input_file)

        if args.output_type.lower() == "cdl":
            write_cdl(args.output_path, id, slope, offset, power, saturation)
        elif args.output_type.lower() == "ccc":
            write_ccc(args.output_path, id, slope, offset, power, saturation)
        else:
            raise ValueError(f"Invalid output type '{args.output_type}'. Only 'CDL' and 'CCC' are supported.")
    except ValueError as e:
        print(f"Error: {str(e)}")


if __name__ == "__main__":
    main()
