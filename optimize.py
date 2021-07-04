#!/usr/bin/env python
import argparse


def main():
    args = get_args()
    input_file = read_file(args.asm)


def get_args():
    parser = argparse.ArgumentParser(description='A script for optimizing pokecrystal music.')
    parser.add_argument('asm', help='script input file')
    parser.add_argument('output', help='optimized output file')
    return parser.parse_args()


def read_file(filename):
    try:
        with open(filename, 'r') as input_file:
            file_contents = tuple(input_file.readlines())
        return file_contents
    except FileNotFoundError:
        print(f'Input file {filename} does not exist.')
    except PermissionError:
        print(f'No permission to read file {filename}.')
    
    return ()


if __name__ == '__main__':
    main()
