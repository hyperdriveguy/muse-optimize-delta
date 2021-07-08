#!/usr/bin/env python
import argparse
from functools import reduce
import concurrent.futures
from ast import Index


def main():
    args = get_args()
    input_file = read_file(args.asm)
    if input_file == ():
        return
    pre_optimized_size = calc_song_size(input_file)
    optimize_callchannel(input_file)


def optimize_callchannel(song):
    """
    Makes different reusable song branches to be called.

    This is the most common and generally most space saving
    optimization in practice. It imitates a dictionary based
    compression algorithm and takes hints from LZ77. The biggest
    drawback is that called channels cannot be nested.
    Since callchannel + endchannel takes 4 bytes, the minimum
    branch size with no space savings is 4 bytes with 2 matches.
    """

    scrubbed_song = tuple(filter(filter_comments_space, song))
    scrubbed_song = tuple(map(remove_inline_comment, scrubbed_song))

    build_zipper = lambda x: True
    song_zipper = tuple(map(build_zipper, scrubbed_song))

    index_blacklist = make_blacklist_indexes(song)


    # A while loop accounts for a mutating file size
    file_index = 0
    while file_index < len(scrubbed_song):
        lookahead = build_ideal_lookahead(scrubbed_song, file_index, index_blacklist)
        if lookahead == 0:
            file_index += 1
            continue


def build_ideal_lookahead(song, start_index, blacklist):
    lookahead = 0
    found_ideal_lookahead = False
    ideal_lookahead = 0
    prev_size_savings = 0
    while not found_ideal_lookahead:
        if not range_in_blacklist(start_index, lookahead, blacklist):
            window = song[start_index:lookahead + 1]
            num_matches = 1
            for cur_index in range(start_index + len(window), len(song) - lookahead):
                if(window[0] == song[cur_index] and
                        window == song[cur_index:lookahead + 1] and
                        not range_in_blacklist(cur_index, lookahead, blacklist)):

                    num_matches += 1
            cur_savings = calc_song_size(window) * num_matches - 4
            if cur_savings > prev_size_savings:
                prev_size_savings = cur_savings
                ideal_lookahead = lookahead
                lookahead += 1
            else:
                found_ideal_lookahead = True
    return ideal_lookahead


def parse_matches():
    pass


def range_in_blacklist(start, lookahead, blacklist):
    for index in range(start, start + lookahead + 1):
        if index in blacklist:
            return True
    return False


def make_blacklist_indexes(song):

    def build_callchannel_range(label):
        start_bad = None
        end_bad = None
        for index in range(len(song)):
            if song[index] == label:
                start_bad = index
            elif start_bad is not None and song[index] == 'endchannel':
                end_bad = index
        return tuple(range(start_bad, end_bad + 1))

    def filter_callchannel(line):
        if get_root_command(line) == 'callchannel':
            return True
        return False

    def filter_other_unoptimizable(line):
        unoptimizable = ('musicheader', 'endchannel', 'volume', 'togglenoise')
        if get_root_command(line) in unoptimizable:
            return True
        return False

    def other_unoptimizable_indexes(line):
        for index in range(len(song)):
            if song[index] == line:
                return index

    format_channel_label = lambda line: line.split(' ')[1].strip() + ':\n'

    called_channels = tuple(filter(filter_callchannel, song))
    filtered_other_unoptimizable = tuple(filter(filter_other_unoptimizable, song))
    other_unoptimizable = tuple(map(other_unoptimizable_indexes, filtered_other_unoptimizable))
    blacklisted_indexes = sum(multi_map(called_channels, format_channel_label, build_callchannel_range), other_unoptimizable)

    return blacklisted_indexes




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
    scrubbed_song = multi_filter(song, filter_label, filter_comments_space)
    command_bytes = multi_map(scrubbed_song, get_root_command, get_command_size)
    accumulator = lambda a, b: a + b
    song_size = reduce(accumulator, command_bytes)
    return song_size


def multi_map(iterable, *functions):
    mapped = iterable
    for function in functions:
        mapped = tuple(map(function, mapped))
    return mapped


def multi_filter(iterable, *filters):
    mapped = iterable
    for function in filters:
        mapped = tuple(filter(function, mapped))
    return mapped


def filter_label(line):
    clean_line = line.strip()
    try:
        # Check for labels
        if clean_line[-1] == ':':
            return False
        # Check for labels with inline comments
        elif ';' in clean_line and clean_line.split(';')[0].strip()[-1] == ':':
            return False
    except IndexError:
        # Found a blank line, fallthrough below
        pass

    return True


def filter_comments_space(line):
    clean_line = line.strip()
    # Check if line is blank
    if clean_line == '':
        return False
    # Skip commented out lines
    # Inline comments still work for non-labels
    elif clean_line[0] == ';':
        return False

    return True


def remove_inline_comment(line):
    if ';' in line:
        return line.split(';')[0].strip(' ') + '\n'
    
    return line
        


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
