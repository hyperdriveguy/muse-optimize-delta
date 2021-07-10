#!/usr/bin/env python
import argparse
import concurrent.futures
from ast import Index

from callchannel import optimize_callchannel
from util_funcs import calc_song_size, filter_comments_space,\
    remove_inline_comment


def main():
    # args = get_args()
    # input_file = read_file(args.asm)
    input_file = read_file('paradise.asm')
    if input_file == ():
        return
    scrubbed_song = scrub_song(input_file)
    pre_optimized_size = calc_song_size(scrubbed_song)
    print('BEFORE:',pre_optimized_size)
    callchannel_optimized = optimize_callchannel(scrubbed_song)
    post_optimized_size = calc_song_size(callchannel_optimized)
    print('AFTER:', post_optimized_size)
    percent_saved_new = (post_optimized_size / pre_optimized_size) * 100
    print(f'{percent_saved_new:.2f}% of previous size')
    old_optimized = read_file('paradise_optimized_v1.asm')
    old_song_size = calc_song_size(old_optimized)
    print('OLD:', old_song_size)
    percent_saved_old = (old_song_size / pre_optimized_size) * 100
    print(f'{percent_saved_old:.2f}% of previous size')
    percent_diff = percent_saved_old - percent_saved_new
    print(f'\n{percent_diff:.2f}% smaller than old optimizations')


def scrub_song(song):
    scrubbed_song = tuple(filter(filter_comments_space, song))
    scrubbed_song = tuple(map(remove_inline_comment, scrubbed_song))
    return scrubbed_song


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
        print(f'Input file "{filename}" does not exist.')
    except PermissionError:
        print(f'No permission to read file "{filename}".')

    return ()


if __name__ == '__main__':
    main()
