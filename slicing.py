from PIL import Image
import cv2
from utils import *
import os
import numpy as np
from pathlib import Path


def calculate_slices_xyxy(image_h,image_w,slice_h,slice_w,overlap_h,overlap_w):
    """
    Calculates the coordinates of the slices

    Args:
        image_h(int): image height
        image_w(int): image width
        slice_h(int): slice height
        slice_w(int): slice width
        overlap_h(float): overlap height ratio
        overlap_w(float): overlap width ratio

    Returns:
    List[List[int]]: list of slices coordinates [[xmin1,ymin1,xmax1,ymax1],...,[xminn,yminn,xmaxn,ymaxn]]
    """
    coords = []

    y_overlap = int(overlap_h * slice_h)
    x_overlap = int(overlap_w * slice_w)

    y_min=0
    y_max=0
    while y_max < image_h:
            x_min = x_max = 0
            y_max = y_min + slice_h
            while x_max < image_w:
                x_max = x_min + slice_w
                if y_max > image_h or x_max > image_w:
                    xmax = min(image_w, x_max)
                    ymax = min(image_h, y_max)
                    xmin = max(0, xmax - slice_w)
                    ymin = max(0, ymax - slice_h)
                    coords.append([xmin, ymin, xmax, ymax])
                else:
                    coords.append([x_min, y_min, x_max, y_max])
                x_min = x_max - x_overlap
            y_min = y_max - y_overlap

    return coords




def slice_image(image, label, out_dir, slice_w, slice_h, overlap_w, overlap_h):
    """
    Slice image into cuts, save crops and labels

    Args:
    image(str): file path to the image
    label(str): file path to the label txt
    out_dir(str): output folder path
    slice_h(int): slice height
    slice_w(int): slice width
    overlap_h(float): overlap height ratio
    overlap_w(float): overlap width ratio

    Return:

    """

    if out_dir is not None:
        Path(out_dir).mkdir(parents=True, exist_ok=True)

    filename_without_extension = Path(image).stem 

    img = load_image_pil(image)

    img_w,img_h = img.size

    #get list of slices coordinates
    slice_coords = calculate_slices_xyxy(img_h,img_w,slice_h,slice_w,overlap_h,overlap_w)

    #load labels as numpy array
    label_array = load_label(label,img_w,img_h)
    label_array_xyxy =  array_xywh_xyxy(label_array,img_w,img_h)

    #main loop, check if label is inside the slice, if it is,calculate intersection and add row to txt label
    for slice in slice_coords:

        #filename of the slice is like  image_filename_{xmin}_{ymin}_{xmax}_{ymax}
        slice_filename = filename_without_extension + f'_{slice[0]}_{slice[1]}_{slice[2]}_{slice[3]}' 

        #save slice:
        img_slice = img.crop((slice[0],slice[1],slice[2],slice[3]))
        img_slice.save(os.path.join(out_dir,slice_filename)+'.jpg')        

        #path to save the txt file
        txt_path = os.path.join(out_dir,slice_filename+'.txt')

        #make txt file, after we can delete empty txt
        with open(txt_path, 'w') as f:

            for label in label_array_xyxy:
                if label is None:
                    continue

                #check if the label is inside the box
                if anotation_inside_slice(label[1:],slice) == True:

                    #calculate intersection
                    intersection = intersect_xywh(label[1:],slice)
                    #normalize xywh
                    intersection = normalize_bbox(intersection)

                    #TODO:  calculate intersection area, if it is too small, dont save the annotation

                    #writes line
                    f.write(f'{int(label[0])} {intersection[0]} {intersection[1]} {intersection[2]} {intersection[3]}')
            f.close()




                
         
