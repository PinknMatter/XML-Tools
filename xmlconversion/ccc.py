import argparse
import re
import os
""""
Created By Noah Kornberg

.CCC file conversion
This tool will convert .CCC files into .CC or .CDL file types 


"""

def parse_ccc(input_file):
    with open(input_file, 'r') as file:
        ccc_content = file.read()

    id_match = re.search(r'<ColorCorrection id="(.*?)"', ccc_content)
    slope_match = re.search(r'<Slope>(.*?)</Slope>', ccc_content)
    offset_match = re.search(r'<Offset>(.*?)</Offset>', ccc_content)
    power_match = re.search(r'<Power>(.*?)</Power>', ccc_content)
    saturation_match = re.search(r'<Saturation>(.*?)</Saturation>', ccc_content)

    if not all([id_match, slope_match, offset_match, power_match, saturation_match]):
        raise ValueError("Unable to extract required elements from the input file.")

    id = id_match.group(1)
    slope = slope_match.group(1)
    offset = offset_match.group(1)
    power = power_match.group(1)
    saturation = saturation_match.group(1)

    return id, slope, offset, power, saturation


def write_cc(output_path, id, slope, offset, power, saturation):
    try:
        filename = os.path.join(output_path, f"{id}.cc")
        with open(filename, 'w') as file:
            file.write(f'<ColorCorrection id="{id}" xmlns="urn:ASC:CDL:v1.2">\n')
            file.write(f'  <SOPNode>\n')
            file.write(f'    <Slope>{slope}</Slope>\n')
            file.write(f'    <Offset>{offset}</Offset>\n')
            file.write(f'    <Power>{power}</Power>\n')
            file.write(f'  </SOPNode>\n')
            file.write(f'  <SatNode>\n')
            file.write(f'    <Saturation>{saturation}</Saturation>\n')
            file.write(f'  </SatNode>\n')
            file.write(f'</ColorCorrection>\n')
        print(f"CC file '{filename}' was successfully created.")
    except IOError:
        raise ValueError("Error writing the CC file.")


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


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", help="Input CCC file.")
    parser.add_argument("output_path", help="Output path for the files.")
    parser.add_argument("--output_type", help="Output type (CDL or CC).", default="CDL")

    args = parser.parse_args()

     # If the output path includes a file name, remove it
    args.output_path = os.path.dirname(args.output_path)

    try:
        id, slope, offset, power, saturation = parse_ccc(args.input_file)

        if args.output_type.lower() == "cdl":
            write_cdl(args.output_path, id, slope, offset, power, saturation)
        elif args.output_type.lower() == "cc":
            write_cc(args.output_path, id, slope, offset, power, saturation)
        else:
            raise ValueError(f"Invalid output type '{args.output_type}'. Only 'CDL' and 'CC' are supported.")
    except ValueError as e:
        print(f"Error: {str(e)}")


if __name__ == "__main__":
    main()
