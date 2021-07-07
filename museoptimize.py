#!/usr/bin/env python
import argparse
from functools import reduce
from ast import Index


def main():
    args = get_args()
    input_file = read_file(args.asm)
    if input_file == ():
        return
    pre_optimized_size = calc_song_size(input_file)
    print(pre_optimized_size)


def get_args():
    parser = argparse.ArgumentParser(
        description='A script for optimizing pokecrystal compatible '
                    'music scripts.')
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


def calc_song_size(song):
    scrubbed_song = tuple(filter(filter_non_command, song))
    command_bytes = multi_map(scrubbed_song, get_root_command, get_command_size)
    accumulator = lambda a, b: a + b
    song_size = reduce(accumulator, command_bytes)
    return song_size


def multi_map(iterable, *functions):
    mapped = iterable
    for function in functions:
        mapped = tuple(map(function, mapped))
    return mapped


def filter_non_command(line):
    clean_line = line.strip()
    # Check if line is blank
    if clean_line == '':
        return False
    # Skip commented out lines
    # Inline comments still work for non-labels
    elif clean_line[0] == ';':
        return False
    # Check for labels
    elif clean_line[-1] == ':':
        return False
    # Check for inline comments
    elif ';' in clean_line and clean_line.split(';')[0].strip()[-1] == ':':
        return False

    return True


def get_root_command(raw_command):
    command = raw_command.split(' ')[0].strip()
    if command == 'notetype':
        if len(raw_command.split(' ')) > 2:
            return 'notetype_1'
        else:
            return 'notetype_2'

    return command


def get_command_size(root_command):
    """
    Get a byte size (int) for an associated music command.
    Size map is ordered by most to least common commands.
    """
    # notetype can vary in size
    size_map_names = ('note', 'octave', 'notetype_1', 'notetype_2',
                      'dutycycle', 'intensity', 'tempo', 'tone',
                      'stereopanning', 'vibrato', 'slidepitchto', 'transpose',
                      'jumpchannel', 'callchannel', 'loopchannel',
                      'endchannel', 'jumpif', 'setcondition', 'togglenoise',
                      'volume', 'musicheader')
    size_map_bytes = (1, 1, 2, 3,
                      2, 2, 3, 2,
                      2, 3, 3, 2,
                      3, 3, 4,
                      1, 4, 2, 2,
                      2, 3)
    try:
        bytesize = size_map_bytes[size_map_names.index(root_command)]
    except IndexError:
        print(f'Unknown music command {root_command}, assuming size 1')
        bytesize = 1

    return bytesize


if __name__ == '__main__':
    main()
