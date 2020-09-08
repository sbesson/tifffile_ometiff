import tifffile
import cv2  # for fast resizing
import sys

print("Reading %s" % sys.argv[1])
image = tifffile.imread(sys.argv[1])

print("Writing %s" % sys.argv[2])
with tifffile.TiffWriter(sys.argv[2], bigtiff=True) as tif:
  options = {'tile': (512, 512), 'compress': 6}
  tif.save(image, subifds=8, **options)
  for _ in range(8):
    image = cv2.resize(image, (image.shape[0] // 2, image.shape[1] // 2), interpolation=cv2.INTER_LINEAR)
    tif.save(image, **options)
