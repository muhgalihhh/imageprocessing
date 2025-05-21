import cv2
import numpy as np


def resize(image, width=None, height=None, percentage=None):
    """
    Resize an image
    
    Args:
        image: Input image
        width: Target width (if not None)
        height: Target height (if not None)
        percentage: Scale percentage (if width and height are None)
        
    Returns:
        Resized image
    """
    if percentage is not None:
        scale = percentage / 100.0
        width = int(image.shape[1] * scale)
        height = int(image.shape[0] * scale)
    elif width is None and height is not None:
        aspect_ratio = width / float(image.shape[1])
        height = int(image.shape[0] * aspect_ratio)
    elif height is None and width is not None:
        aspect_ratio = height / float(image.shape[0])
        width = int(image.shape[1] * aspect_ratio)
    
    return cv2.resize(image, (width, height), interpolation=cv2.INTER_AREA)

def rotate(image, angle, center=None, scale=1.0):
    """
    Rotate an image
    
    Args:
        image: Input image
        angle: Rotation angle in degrees
        center: Center of rotation (if None, image center is used)
        scale: Isotropic scale factor
        
    Returns:
        Rotated image
    """
    (h, w) = image.shape[:2]
    
    if center is None:
        center = (w // 2, h // 2)
        
    M = cv2.getRotationMatrix2D(center, angle, scale)
    rotated = cv2.warpAffine(image, M, (w, h))
    
    return rotated

def flip(image, flip_code):
    """
    Flip an image
    
    Args:
        image: Input image
        flip_code: Flip code
                  0: flip vertically (around x-axis)
                  1: flip horizontally (around y-axis)
                  -1: flip both vertically and horizontally
                  
    Returns:
        Flipped image
    """
    return cv2.flip(image, flip_code)

def crop(image, x, y, width, height):
    """
    Crop an image
    
    Args:
        image: Input image
        x: Start x-coordinate
        y: Start y-coordinate
        width: Width of the crop
        height: Height of the crop
        
    Returns:
        Cropped image
    """
    # Ensure coordinates are within image boundaries
    h, w = image.shape[:2]
    x = max(0, min(x, w - 1))
    y = max(0, min(y, h - 1))
    width = max(1, min(width, w - x))
    height = max(1, min(height, h - y))
    
    return image[y:y+height, x:x+width]

def perspective_transform(image, pts1, pts2):
    """
    Apply perspective transformation to an image
    
    Args:
        image: Input image
        pts1: Four points in the input image
        pts2: Corresponding four points in the output image
        
    Returns:
        Perspective transformed image
    """
    M = cv2.getPerspectiveTransform(pts1, pts2)
    h, w = image.shape[:2]
    return cv2.warpPerspective(image, M, (w, h))

def affine_transform(image, pts1, pts2):
    """
    Apply affine transformation to an image
    
    Args:
        image: Input image
        pts1: Three points in the input image
        pts2: Corresponding three points in the output image
        
    Returns:
        Affine transformed image
    """
    M = cv2.getAffineTransform(pts1, pts2)
    h, w = image.shape[:2]
    return cv2.warpAffine(image, M, (w, h))
