import os
import sys


def normalize_line_endings(text):
    return text.replace("\r\n", "\n").replace("\r", "\n")


def edit_edl(edl_file_path):
    # Convert the file path to the appropriate format
    edl_file_path = os.path.normpath(edl_file_path)

    # Read the contents of the EDL file
    with open(edl_file_path, "r") as file:
        edl_contents = file.read()

    # Normalize line endings in the EDL contents
    edl_contents = normalize_line_endings(edl_contents)

    # Modify the specific entries in the EDL
    modified_edl = []
    lines = edl_contents.split("\n")
    for i, line in enumerate(lines):
        if "* FROM CLIP NAME:" in line:
            clipname = line.split(":")[1].strip()
            # Check if it's a MOV file or if the next line is already a clipname, we skip appending
            next_line = lines[i+1] if i+1 < len(lines) else None
            if ".mov" in line or (next_line and next_line.strip().startswith("*")):
                modified_edl.append(line)
            else:
                modified_edl.append(line)
                modified_edl.append("* " + clipname)
        else:
            modified_edl.append(line)

    # Write the modified contents back to the EDL file
    with open(edl_file_path, "w") as file:
        file.write("\n".join(modified_edl))

    print("EDL file modification complete!")


if __name__ == "__main__":
    # Get the EDL file path from command-line argument
    if len(sys.argv) < 2:
        print("Please provide the EDL file path as a command-line argument.")
        sys.exit(1)

    edl_file_path = sys.argv[1]
    edit_edl(edl_file_path)
