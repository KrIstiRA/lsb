#!/usr/bin/env python
# coding: UTF-8

import argparse
from PIL import Image

def hideByte(pixels, i, byte):
    for j in range(8):
        pixels[i + j] &= 0b11111110 | byte & 1
        byte >>= 1
    

def extractByte(pixels, i):
    byte = 0
    for j in range(8):
        byte |= (pixels[i + j] & 1) << j
    return byte


def lsb_in(picture, data):
    if len(data) > 255:
        return False

    pic = Image.open(picture)
    pixString = pic.tobytes()
    pixels = [ord(x) for x in pixString]

    data = [len(data)] + [ord(x) for x in data]

    for i, byte in enumerate(data):
        hideByte(pixels, i * 8, byte)

    pixString = ''.join([chr(x) for x in pixels])
    pic.frombytes(pixString)
    newName = picture[:-4] + 'x' + '.bmp'
    pic.save(newName, "BMP")
    return True


def lsb_out(picture):
    pic = Image.open(picture)
    pixString = pic.tobytes()
    pixels = [ord(x) for x in pixString]

    size = extractByte(pixels, 0)
    data = [0] * size
    for i in range(size):
        data[i] = extractByte(pixels, (i+1) * 8)

    result = [chr(x) for x in data]
    return ''.join(result)
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('picture')
    parser.add_argument('-i', '--input_data', nargs='?', help="File with data for hiding")
    parser.add_argument('-o', '--output_data', nargs='?', help="File for extracted data")
    args = parser.parse_args()

    if args.input_data:
        datafile = open(args.input_data, 'rb')
        data = datafile.read()
        datafile.close()

        if not lsb_in(args.picture, data):
            print "Can't hide this file to this picture"
    elif args.output_data:
        extracted = lsb_out(args.picture)

        outfile = open(args.output_data, 'wb')
        outfile.write(extracted)
        outfile.close()
    else:
        print "specify input_data for hiding or output_data for extracting"