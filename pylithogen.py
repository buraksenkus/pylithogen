from generator import generate

import argparse


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog='Image to STL',
        description='Converts image to STL',
        epilog='Written by bsenkus')

    parser.add_argument('image_path')
    parser.add_argument('--min-height', default=0, help='Minimum pixel height, in mm', type=float)
    parser.add_argument('--max-height', default=10, help='Maximum pixel height, in mm', type=float)
    parser.add_argument('--scale', default=1, help='Scale', type=float)
    parser.add_argument('-m', '--method', default='emboss', help="STL creation method", choices=['emboss', 'column'])
    parser.add_argument('-v', '--verbose', action='store_true')

    args = parser.parse_args()

    generate(args)
