#!/usr/bin/python3

from check import is_xml_correct
from convert import convert_file
import argparse

def convert_and_check(input_file : str):
    output_file = f"{input_file}.converted"
    convert_file(input_file, output_file)
    good = is_xml_correct(output_file)
    if good == None:
        print("Nie można sprawdzić poprawności pliku!")
    else:
        print("XML poprawny!" if good else "XML niepoprawny:(")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Plots for benchmark results')
    parser.add_argument('--path', type=str, required=True, nargs="+")
    args = parser.parse_args()

    for file in args.path:
        if file.endswith("xml"):
            print("Przetwarzam", file)
            convert_and_check(file)