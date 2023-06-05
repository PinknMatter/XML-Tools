import re
import os
import argparse
import xml.etree.ElementTree as ET

def pretty_print(elem, level=0):
    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            pretty_print(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

def read_edl_file(edl_file):
    try:
        with open(edl_file, 'r') as file:
            data = file.readlines()
        return data
    except FileNotFoundError:
        print(f"Input file {edl_file} not found. Please enter a valid file path.")
        return None

def extract_color_data(edl_data):
    sop_values = [re.findall(r"\*ASC_SOP ((?:\(-?[\d.]+\s-?[\d.]+\s-?[\d.]+\)\s*)+)", line) for line in edl_data if "*ASC_SOP" in line]
    sop_values = [[float(val) for val in re.findall(r"(-?[\d.]+)", sop[0])] for sop in sop_values]
    sat_values = [re.findall(r"\*ASC_SAT (.*?) ", line) for line in edl_data if "*ASC_SAT" in line]
    source_file_names = [re.findall(r"\*SOURCE FILE: (.*?)$", line.strip()) for line in edl_data if "*SOURCE FILE:" in line]
    return sop_values, sat_values, source_file_names

def write_file(filename, element):
    pretty_print(element)
    ET.ElementTree(element).write(filename)
    print(f"Printed {filename} successfully.")

def create_cc_file(sop_values, sat_values, output_file, source_file_names):
    for i in range(len(sop_values)):
        name, _ = os.path.splitext(source_file_names[i][0])
        filename = os.path.join(output_file, f"{name}.cc")
        color_correction = ET.Element("ColorCorrection", id=source_file_names[i][0], xmlns="urn: ASC:CDL: v1.2")
        sop_node = ET.SubElement(color_correction, "SOPNode")
        slope = " ".join(map(str, sop_values[i][:3]))
        offset = " ".join(map(str, sop_values[i][3:6]))
        power = " ".join(map(str, sop_values[i][6:]))

        ET.SubElement(sop_node, "Slope").text = slope
        ET.SubElement(sop_node, "Offset").text = offset
        ET.SubElement(sop_node, "Power").text = power

        sat_node = ET.SubElement(color_correction, "SatNode")
        ET.SubElement(sat_node, "Saturation").text = str(sat_values[i][0])

        write_file(filename, color_correction)

def create_cdl_file(sop_values, sat_values, output_file, source_file_names):
    for i in range(len(sop_values)):
        name, _ = os.path.splitext(source_file_names[i][0])
        filename = os.path.join(output_file, f"{name}.cdl")
        color_decision_list = ET.Element("ColorDecisionList", xmlns="urn:ASC:CDL:v1.01")
        color_decision = ET.SubElement(color_decision_list, "ColorDecision")
        color_correction = ET.SubElement(color_decision, "ColorCorrection")
        sop_node = ET.SubElement(color_correction, "SOPNode")
        ET.SubElement(sop_node, "Description").text = source_file_names[i][0]
        slope = " ".join(map(str, sop_values[i][:3]))
        offset = " ".join(map(str, sop_values[i][3:6]))
        power = " ".join(map(str, sop_values[i][6:]))

        ET.SubElement(sop_node, "Slope").text = slope
        ET.SubElement(sop_node, "Offset").text = offset
        ET.SubElement(sop_node, "Power").text = power

        sat_node = ET.SubElement(color_correction, "SatNode")
        ET.SubElement(sat_node, "Saturation").text = str(sat_values[i][0])

        write_file(filename, color_decision_list)

def create_ccc_file(sop_values, sat_values, output_file, source_file_names):
    for i in range(len(sop_values)):
        name, _ = os.path.splitext(source_file_names[i][0])
        filename = os.path.join(output_file, f"{name}.ccc")
        color_correction_collection = ET.Element("ColorCorrectionCollection", xmlns="urn:ASC:CDL:v1.01")
        color_correction = ET.SubElement(color_correction_collection, "ColorCorrection", id=source_file_names[i][0])
        sop_node = ET.SubElement(color_correction, "SOPNode")
        slope = " ".join(map(str, sop_values[i][:3]))
        offset = " ".join(map(str, sop_values[i][3:6]))
        power = " ".join(map(str, sop_values[i][6:]))

        ET.SubElement(sop_node, "Slope").text = slope
        ET.SubElement(sop_node, "Offset").text = offset
        ET.SubElement(sop_node, "Power").text = power

        sat_node = ET.SubElement(color_correction, "SatNode")
        ET.SubElement(sat_node, "Saturation").text = str(sat_values[i][0])

        write_file(filename, color_correction_collection)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", help="EDL file to process.")
    parser.add_argument("output_file", help="Output directory.")
    parser.add_argument("--output_type", choices=['ccc', 'cdl', 'cc'], help="Output file format: ccc, cdl, or cc.")
    args = parser.parse_args()

    # If the output path includes a file name, remove it
    args.output_file = os.path.dirname(args.output_file)

    edl_data = read_edl_file(args.input_file)
    if edl_data is not None:
        sop_values, sat_values, source_file_names = extract_color_data(edl_data)

        if args.output_type == 'ccc':
            create_ccc_file(sop_values, sat_values, args.output_file, source_file_names)
        elif args.output_type == 'cdl':
            create_cdl_file(sop_values, sat_values, args.output_file, source_file_names)
        elif args.output_type == 'cc':
            create_cc_file(sop_values, sat_values, args.output_file, source_file_names)



if __name__ == "__main__":
    main()
