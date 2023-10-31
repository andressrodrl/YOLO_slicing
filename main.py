import argparse
from slicing import *
from utils import *
import os
from pathlib import Path



"""
Script for slicing object detection dataset in YOLO format

python main.py --folder_in <input folder> --folder_out <output folder> 
--w <slice width> --h <slice height> --w_o <overlap width ratio> --h_o <height overlap ratio>
"""

def main(args):
    print('ejecutando main')
    folder_in = args.folder_in
    folder_out = args.folder_out
    slice_w = args.w
    slice_h = args.h
    overlap_w = args.w_o
    overlap_h = args.h_o


    for file in os.listdir(folder_in):
        if file.endswith('.jpg'):
            image_path = os.path.join(folder_in,file)
            label_path = os.path.join(folder_in,file.split('.')[0]+'.txt')
            print(image_path, label_path, folder_out, slice_w, slice_h, overlap_w, overlap_h)
            slice_image(image_path, label_path, folder_out, slice_w, slice_h, overlap_w, overlap_h)


def get_args(): # define args
    parser = argparse.ArgumentParser("Calculate metrics from YOLO format")
    parser.add_argument(
        "--folder_in",
        type=str,
        help="Path to images and labels folder",
    )
    parser.add_argument(
        "--folder_out",
        type=str,
        help="Path to folder where crops and labels will be saved",
    )
    parser.add_argument(
        "--w",
        type=int,
        help="slice width",
    )
    parser.add_argument(
        "--h",
        type=int,
        help="slice height",
    )
    parser.add_argument(
        "--w_o",
        type=float,
        help="width overlap ratio",
    )
    parser.add_argument(
        "--h_o",
        type=float,
        help="height overlap ratio",
    )
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    paths = get_args() # define args
    main(paths)











