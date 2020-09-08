#! /usr/bin/env python

import argparse
import logging
import tifffile
import cv2  # for fast resizing
import sys

log = logging.getLogger()


def convert(inputfile, outputfile, tilesize=256, compression=6, resolutions=8):
    log.info("Reading %s" % inputfile)
    image = tifffile.imread(inputfile)

    print("Writing %s" % outputfile)
    with tifffile.TiffWriter(outputfile, bigtiff=True) as tif:
      options = {'tile': (tilesize, tilesize), 'compress': compression}
      tif.save(image, subifds=resolutions, **options)
      for _ in range(resolutions):
        image = cv2.resize(
            image,
            (image.shape[0] // 2, image.shape[1] // 2),
            interpolation=cv2.INTER_LINEAR)
        tif.save(image, **options)


def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('inputfile', help='The file to convert')
    parser.add_argument('outputfile',help='The destination file')
    parser.add_argument('--tilesize', default=256, type=int, help='Tile size')
    parser.add_argument(
        '--compression', default=6, type=int, help='Compression')
    parser.add_argument(
        '--resolutions', default=8, type=int, help='Number of sub-resolutions')
    parser.add_argument(
        '--verbose', '-v', action='count', default=0,
        help='Increase the command verbosity')
    parser.add_argument(
        '--quiet', '-q', action='count', default=0,
        help='Decrease the command verbosity')
    args = parser.parse_args(argv)

    logging.basicConfig(
            level=logging.INFO - 10 * args.verbose + 10 * args.quiet)
    convert(args.inputfile, args.outputfile, tilesize=args.tilesize,
            compression=args.compression, resolutions=args.resolutions)


if __name__ == "__main__":
    main(sys.argv[1:])
