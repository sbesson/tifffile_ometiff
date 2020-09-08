#! /usr/bin/env python

import argparse
import logging
import tifffile
import cv2  # for fast resizing
import sys

log = logging.getLogger()


def convert(inputfile, outputfile):
    log.info("Reading %s" % inputfile)
    image = tifffile.imread(inputfile)

    print("Writing %s" % outputfile)
    with tifffile.TiffWriter(outputfile], bigtiff=True) as tif:
      options = {'tile': (512, 512), 'compress': 6}
      tif.save(image, subifds=8, **options)
      for _ in range(8):
        image = cv2.resize(
            image,
            (image.shape[0] // 2, image.shape[1] // 2),
            interpolation=cv2.INTER_LINEAR)
        tif.save(image, **options)


def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('inputfile', help='The file to convert')
    parser.add_argument('outputfile',help='The destination file')
    parser.add_argument(
        '--verbose', '-v', action='count', default=0,
        help='Increase the command verbosity')
    parser.add_argument(
        '--quiet', '-q', action='count', default=0,
        help='Decrease the command verbosity')
    args = parser.parse_args(argv)

    logging.basicConfig(
            level=logging.INFO - 10 * args.verbose + 10 * args.quiet)
    convert(args.inputfile, args.outputfile)


if __name__ == "__main__":
    main(sys.argv[1:])
