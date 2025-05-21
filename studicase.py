import cv2
import numpy as np


def detect_faces(image):
    # Load the face cascade
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Detect faces
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    
    # Make a copy of the input image
    output = image.copy()
    
    face_list = []
    # Draw rectangle around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(output, (x, y), (x+w, y+h), (255, 0, 0), 2)
        face_list.append((x, y, w, h))
    
    return output, face_list

def detect_eyes(image):
    """
    Detect eyes in an image using Haar cascades
    
    Args:
        image: Input image (BGR format)
        
    Returns:
        Image with detected eyes marked and list of eye coordinates
    """
    # Load the eye cascade
    eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
    
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Detect eyes
    eyes = eye_cascade.detectMultiScale(gray, 1.3, 5)
    
    # Make a copy of the input image
    output = image.copy()
    
    eye_list = []
    # Draw rectangle around the eyes
    for (x, y, w, h) in eyes:
        cv2.rectangle(output, (x, y), (x+w, y+h), (0, 255, 0), 2)
        eye_list.append((x, y, w, h))
    
    return output, eye_list

def detect_contours(image, threshold1=50, threshold2=150):
    """
    Detect contours in an image
    
    Args:
        image: Input image
        threshold1: First threshold for the Canny edge detector
        threshold2: Second threshold for the Canny edge detector
        
    Returns:
        Image with contours drawn and list of contours
    """
    # Convert to grayscale
    if len(image.shape) > 2:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image
        
    # Apply Canny edge detection
    edges = cv2.Canny(gray, threshold1, threshold2)
    
    # Find contours
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Make a copy of the input image for drawing
    if len(image.shape) > 2:
        output = image.copy()
    else:
        # Convert grayscale to BGR for drawing colored contours
        output = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
    
    # Draw contours
    cv2.drawContours(output, contours, -1, (0, 255, 0), 2)
    
    return output, contours

def histogram_equalization(image):
    """
    Perform histogram equalization
    
    Args:
        image: Input image
        
    Returns:
        Equalized image and histogram data
    """
    # If the image is colored, equalize each channel
    if len(image.shape) > 2:
        # Split the image into channels
        b, g, r = cv2.split(image)
        
        # Apply histogram equalization to each channel
        b_eq = cv2.equalizeHist(b)
        g_eq = cv2.equalizeHist(g)
        r_eq = cv2.equalizeHist(r)
        
        # Merge the equalized channels
        equalized = cv2.merge((b_eq, g_eq, r_eq))
        
        # Calculate histograms for the original and equalized images
        hist_orig = [cv2.calcHist([b], [0], None, [256], [0, 256]),
                    cv2.calcHist([g], [0], None, [256], [0, 256]),
                    cv2.calcHist([r], [0], None, [256], [0, 256])]
        
        hist_eq = [cv2.calcHist([b_eq], [0], None, [256], [0, 256]),
                  cv2.calcHist([g_eq], [0], None, [256], [0, 256]),
                  cv2.calcHist([r_eq], [0], None, [256], [0, 256])]
    else:
        # Apply histogram equalization
        equalized = cv2.equalizeHist(image)
        
        # Calculate histograms
        hist_orig = cv2.calcHist([image], [0], None, [256], [0, 256])
        hist_eq = cv2.calcHist([equalized], [0], None, [256], [0, 256])
    
    return equalized, (hist_orig, hist_eq)

def template_matching(image, template):
    """
    Perform template matching to find a template in an image
    
    Args:
        image: Input image
        template: Template to find in the image
        
    Returns:
        Image with matched template marked and coordinates of best match
    """
    # Make a copy of the input image
    output = image.copy()
    
    # Get template dimensions
    h, w = template.shape[:2]
    
    # Apply template matching
    result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
    
    # Find the location with highest correlation
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    
    # Get the top-left corner of the matched area
    top_left = max_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)
    
    # Draw a rectangle around the matched region
    cv2.rectangle(output, top_left, bottom_right, (0, 255, 0), 2)
    
    return output, (top_left, bottom_right)

def optical_flow(prev_frame, current_frame, prev_points):
    """
    Calculate optical flow between two frames
    
    Args:
        prev_frame: Previous grayscale frame
        current_frame: Current grayscale frame
        prev_points: Points to track from the previous frame
        
    Returns:
        Current frame with optical flow vectors drawn and new tracked points
    """
    # Parameters for lucas kanade optical flow
    lk_params = dict(winSize=(15, 15),
                    maxLevel=2,
                    criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))
    
    # Calculate optical flow
    next_points, status, error = cv2.calcOpticalFlowPyrLK(prev_frame, current_frame, prev_points, None, **lk_params)
    
    # Select good points
    good_new = next_points[status == 1]
    good_old = prev_points[status == 1]
    
    # Make a copy of the current frame
    output = cv2.cvtColor(current_frame, cv2.COLOR_GRAY2BGR) if len(current_frame.shape) == 2 else current_frame.copy()
    
    # Draw the optical flow tracks
    for i, (new, old) in enumerate(zip(good_new, good_old)):
        a, b = new.ravel()
        c, d = old.ravel()
        output = cv2.line(output, (int(a), int(b)), (int(c), int(d)), (0, 255, 0), 2)
        output = cv2.circle(output, (int(a), int(b)), 5, (0, 0, 255), -1)
    
    return output, good_new
