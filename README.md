# XML-Tools
These are Tools for XML conversion and Editting EDL files

## XML Conversion
This tool is used to convert EDLs to XML file types as well as convert XMl file types (CC, CDL, CCC) with each other. 
To run simply use this command:
python [script location]/(File to convert type) (path to file) (output path) (type to convert to)
python edl.py desktop/test.edl desktop/ cc

## Edit EDL
This tool is used to edit EDL files to include cut names below each entry, it will skip entries that include MOV as well as entries that already have a cut name. It will add *CUTNAME under every entry
to run simply use this command

python [script location]/editedl.py (path to edl file)
python editedl.py dektop/test.edl


These scripts are open source and free to use to anyone under no copyright.
