#!/usr/bin/env python
import argparse


def main();
    pass


def get_args():
    parser = argparse.ArgumentParser(
        description='A script for optimizing pokecrystal music.')
    parser.add_argument('asm', help='script input file')
    parser.add_argument('output', help='optimized output file')
    return parser.parse_args()


if __name__ == '__main__':
    main()
