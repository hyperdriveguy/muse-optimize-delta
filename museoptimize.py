#!/usr/bin/env python
import argparse

from optimization_passes import run_optimization_passes
from util_funcs import scrub_song


def main():
    args = get_args()
    input_file = read_file(args.asm)
    if input_file == ():
        return
    scrubbed_song = scrub_song(input_file)
    optimized_song, orignal_size, optimum_size = run_optimization_passes(scrubbed_song, no_panning=args.mono, agress=args.agressive)
    print(format_size_diff(orignal_size, optimum_size))
    write_file(args.output, optimized_song)


def get_args():
    parser = argparse.ArgumentParser(
        description='A script for optimizing pokecrystal compatible '
                    'music scripts.')
    parser.add_argument('asm', help='script input file')
    parser.add_argument('output', help='optimized output file')
    parser.add_argument('-m', '--mono', type=bool, help='remove stereopanning')
    parser.add_argument('-a', '--agressive', type=bool, help='Use more agressive optimization (takes longer)')
    return parser.parse_args()


def read_file(filename):
    try:
        with open(filename, 'r') as input_file:
            file_contents = tuple(input_file.readlines())
        return file_contents
    except FileNotFoundError:
        print(f'Input file "{filename}" does not exist.')
    except PermissionError:
        print(f'No permission to read file "{filename}".')

    return ()


def write_file(filename, file_contents):
    try:
        with open(filename, 'w') as input_file:
            for line in file_contents:
                input_file.write(line)
    except PermissionError:
        print(f'No permission to write file "{filename}".')


def format_size_diff(old_size, new_size):
    old_size_format = f'Before optimization: {old_size}\n'
    new_size_format = f'After optimization: {new_size}\n'
    percent_diff = (new_size / old_size) * 100
    percent_diff_format = f'{percent_diff:.2f}% of original size'
    return old_size_format + new_size_format + percent_diff_format


if __name__ == '__main__':
    main()
