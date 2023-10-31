import cv2
import numpy as np
import os
from PIL import Image

def load_image(image_path):
    """Loads image into numpy array

    Args:
        image_path(str)

    Returns:
        np.array
    
    """
    img = cv2.imread(image_path)   # reads an image in the BGR format
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)   # BGR -> RGB
    return img

def load_image_pil(image_path):

    """ loads image """
    img = Image.open(image_path)
    return img

def xywh_to_xyxy(coord,image_w,image_h):
    """"
    Bboxes from yolo format to standard [xmin,ymin,xmax,ymax]

    Args:
        coord(List[float]): [x_center,y_center,w,h]
        image_w(int)
        image_h(int)

    Returns:
        List[int]: [xmin,ymin,xmax,ymax] 
    """

    xmin = coord[0]*image_w - (coord[2]*image_w)/2
    xmax = coord[0]*image_w + (coord[2]*image_w)/2
    ymin = coord[1]*image_h - (coord[3]*image_h)/2
    ymax = coord[1]*image_h + (coord[3]*image_h)/2

    bbox = [int(xmin), int(ymin),int(xmax),int(ymax)]
    return bbox

def xyxy_to_xywh(bbox):
    w=bbox[2]-bbox[0]
    h=bbox[3]-bbox[1]
    x=bbox[0]+w/2
    y=bbox[1]+h/2
    xywh=[x,y,w,h]
    return xywh


def anotation_inside_slice(bbox,slice_coord):
    """
    Checks the bbox lies inside the slice

    Args:
        bbox(List[int]): [xmin,ymin,xmax,ymax]
        slice_coord(List[int]): [xmin,ymin,xmax,ymax]


    Returns:
        (bool): True if yes
    """

    if slice_coord[0] >= bbox[2]:
        return False
    
    elif slice_coord[2] <= bbox[0]:
        return False

    elif slice_coord[1] >= bbox[3]:
        return False
    
    elif slice_coord[3] <= bbox[1]:
        return False
    
    else:
        return True
    

def load_label(label):
    """
    Function for loading the labels in a numpy array. Returns none if the txt is empty

    Args:
        label(str): file path to the label txt

    Returns:
        np.array: shape(n,5) class x y w h

    """
    if not os.path.exists(label):
        l = None
        print(f'ETIQUETA NO ENCONTRADA PARA {os.path.basename(label)}')

    else:
        l = np.loadtxt(label)

        if not l.shape[0]:
            l = None

    return l

def array_xywh_xyxy(array,image_w,image_h):
    """
    Transforms numpy array from xywh to xmin ymin xmax ymax

    Args:
        array(np.array(n,5)): each row is class xcenter y center w h (normalized)

    Returns:
        array(np.array(n,5)): class xmin ymin xmax ymax (not normalized)
    
    """
    if array.ndim == 1:
        array = array.reshape(1,5)

    new_array = np.zeros(array.shape)
    new_array[:,0] = array[:,0]
    new_array[:,1] = array[:,1]*image_w - (image_w*(array[:,3]))/2 #xmin
    new_array[:,2] = array[:,2]*image_h - (image_h*(array[:,4]))/2 #ymin
    new_array[:,3] = array[:,1]*image_w + (image_w*(array[:,3]))/2 #xmax
    new_array[:,4] = array[:,2]*image_h + (image_h*(array[:,4]))/2 #ymax

    return new_array



def intersect_xyxy(bbox,slice_coord):
    """
    Calculate intersection between two boxes

    Returns:
        List[int]: [xmin,ymin,xmax,ymax]
    """

    x1 = max(bbox[0], slice_coord[0])
    y1 = max(bbox[1], slice_coord[1])
    x2 = min(bbox[2], slice_coord[2])
    y2 = min(bbox[3], slice_coord[3])

    #w = x2-x1
    #h = y2-y1
    #x = x1 + w/2
    #y = y1 + w/2


    intersection = [x1,y1,x2,y2]
    return intersection


def rel_coord_xywh(bbox, slice_coord):
    """
    Calculate relative coordinates to the slice

    Args: 
        bbox(List[int]): [xmin,ymin,xmax,ymax]
        slice_coord(List[int]): [xmin,ymin,xmax,ymax]

    Returns:
        coord(List[float]): [x,y,w,h]
    """
    xmin = bbox[0]-slice_coord[0]
    ymin = bbox[1]-slice_coord[1]
    xmax = bbox[2]-slice_coord[0]
    ymax = bbox[3]-slice_coord[1]

    w = xmax-xmin
    h = ymax-ymin
    x = xmin + w/2
    y = ymin + h/2

    coord = [x,y,w,h]
    return coord
    


def normalize_bbox(bbox, image_w,image_h):
    """
    Normalizes bbox

    Args:
        List[int]: [x,y,w,h]
    
    Returns:
        List[float]: [x,y,w,h]

    """

    new_bbox = [bbox[0]/image_w, bbox[1]/image_h, bbox[2]/image_w, bbox[3]/image_h]

    return new_bbox
