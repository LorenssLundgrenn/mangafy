import argparse as argp
import time
import cv2
import os

import mangafy

parser = argp.ArgumentParser(description="convert image to manga style")
parser.add_argument(
    "-p", "--path", type=str,
    help="specify target file path", 
    required=True
)
parser.add_argument(
    "-o", "--output", type=str,
    help="specify output path", 
    required=False
)
parser.add_argument(
    "-d", "--distribute", type=float, default=1,
    help="set pixel distribution in decimal percentage", 
    required=False
)
parser.add_argument(
    "-l", "--level", type=float, default=2,
    help="set number of brightness levels", 
    required=False 
)
parser.add_argument(
    "-px", "--pixels", type=int, default=0,
    help="offset pixel brightness", 
    required=False 
)
parser.add_argument(
    "-s", "--stretch", action="store_true",
    help="stretch image pixel data from 0 to 255", 
    required=False
)
parser.add_argument(
    "-i", "--invert", action="store_true",
    help="invert pixel brightness", 
    required=False
)
parser.add_argument(
    "-v", "--video", action="store_true",
    help="specified path is treated as a video file", 
    required=False
)

args = parser.parse_args()
if not os.path.exists(args.path):
    raise ValueError(f"could not find path {args.path}")

path_ext = args.path.split('.')[-1]
out_path = "out" if not args.output else args.output
if '.' not in out_path: out_path = out_path + '.' + path_ext

timestamp = time.time()
if args.video:
    mangafy.normalize_video(path=args.path, 
        out=out_path,
        level=args.level, 
        distribute=args.distribute, 
        pixel_offset=args.pixels, 
        stretch=args.stretch, 
        invert=args.invert
    )   
else:
    image = cv2.imread(args.path, cv2.IMREAD_GRAYSCALE)
    image = mangafy.normalize_grayscale(image, 
        level=args.level, 
        distribute=args.distribute, 
        pixel_offset=args.pixels, 
        stretch=args.stretch, 
        invert=args.invert
    )
    cv2.imwrite(out_path, image)
print(f"elapsed processing time: {time.time() - timestamp}ms")