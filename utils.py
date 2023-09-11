import cv2

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