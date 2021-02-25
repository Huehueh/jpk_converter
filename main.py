#!/usr/bin/python3

from check import is_xml_correct
from convert import convert_file
import argparse, os

def convert_and_check_xml(input_file : str):
    output_file = f"{input_file}.converted"
    convert_file(input_file, output_file)
    good = is_xml_correct(output_file)
    if good == None:
        print("Nie można sprawdzić poprawności pliku!")
    else:
        print("XML poprawny!" if good else "XML niepoprawny:(")
    print("===================================================")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Plots for benchmark results')
    parser.add_argument('--path', type=str, required=True, nargs="+")
    args = parser.parse_args()

    for path in args.path:
        files = [os.path.join(path, file) for file in os.listdir(path)] if os.path.isdir(path) else [path]
        for file in files:
            if file.endswith("xml") or file.endswith("XML"):
                print("Przetwarzam", file)
                convert_and_check_xml(file)