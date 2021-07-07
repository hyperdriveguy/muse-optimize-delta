#!/usr/bin/env python
import argparse


def main():
    args = get_args()
    input_file = read_file(args.asm)


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
    pass


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
                      2, 2, 2, 2,
                      2, 3, 3, 2,
                      3, 3, 4,
                      1, 4, 2, 2,
                      2, 3)
    
    bytesize = size_map_bytes[size_map_names.index(root_command)]

    return bytesize


if __name__ == '__main__':
    main()
