
import base64
import os
import uuid

import cv2
import numpy as np
from flask import Flask, jsonify, render_template, request, send_from_directory
from werkzeug.utils import secure_filename

# Import image processing modules
import filter
import segmentasi
import studicase
import transform

app = Flask(__name__, static_folder='static')
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['PROCESSED_FOLDER'] = 'processed'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

# Create directories if they don't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['PROCESSED_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def save_image(image_data):
    """Save an image from base64 data or a file upload"""
    if isinstance(image_data, str) and image_data.startswith('data:image'):
        # Handle base64 image data
        format_info, imgstr = image_data.split(';base64,')
        ext = format_info.split('/')[-1]
        filename = f"{uuid.uuid4().hex}.{ext}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        with open(filepath, 'wb') as f:
            f.write(base64.b64decode(imgstr))
        return filepath
    else:
        # Handle file upload
        filename = secure_filename(image_data.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        image_data.save(filepath)
        return filepath

def process_image(filepath, method, params=None):
    """Process the image with the specified method and parameters"""
    if params is None:
        params = {}
    
    # Read the image
    image = cv2.imread(filepath)
    if image is None:
        return None, "Failed to read image"
    
    # Create unique filename for processed image
    filename = os.path.basename(filepath)
    base_name, ext = os.path.splitext(filename)
    output_filename = f"{base_name}_processed{ext}"
    output_path = os.path.join(app.config['PROCESSED_FOLDER'], output_filename)
    
    # Process the image based on the method
    try:
        # Filter methods
        if method == "grayscale":
            result = filter.grayscale(image)
        elif method == "gaussian_blur":
            kernel_size = int(params.get("kernel_size", 5))
            result = filter.gaussian_blur(image, kernel_size)
        elif method == "median_blur":
            kernel_size = int(params.get("kernel_size", 5))
            result = filter.median_blur(image, kernel_size)
        elif method == "bilateral_filter":
            d = int(params.get("d", 9))
            sigma_color = int(params.get("sigma_color", 75))
            sigma_space = int(params.get("sigma_space", 75))
            result = filter.bilateral_filter(image, d, sigma_color, sigma_space)
        elif method == "sobel_edge":
            dx = int(params.get("dx", 1))
            dy = int(params.get("dy", 1))
            ksize = int(params.get("ksize", 3))
            result = filter.sobel_edge_detection(image, dx, dy, ksize)
        elif method == "canny_edge":
            threshold1 = int(params.get("threshold1", 100))
            threshold2 = int(params.get("threshold2", 200))
            result = filter.canny_edge_detection(image, threshold1, threshold2)
        elif method == "sharpen":
            result = filter.sharpen(image)
        elif method == "emboss":
            result = filter.emboss(image)
        
        # Segmentation methods
        elif method == "threshold":
            thresh = int(params.get("thresh", 127))
            max_val = int(params.get("max_val", 255))
            type_threshold = int(params.get("type_threshold", cv2.THRESH_BINARY))
            result = segmentasi.threshold(image, thresh, max_val, type_threshold)
        elif method == "adaptive_threshold":
            max_val = int(params.get("max_val", 255))
            adaptive_method = int(params.get("adaptive_method", cv2.ADAPTIVE_THRESH_GAUSSIAN_C))
            threshold_type = int(params.get("threshold_type", cv2.THRESH_BINARY))
            block_size = int(params.get("block_size", 11))
            C = int(params.get("C", 2))
            result = segmentasi.adaptive_threshold(image, max_val, adaptive_method, threshold_type, block_size, C)
        elif method == "otsu_threshold":
            result, _ = segmentasi.otsu_threshold(image)
        elif method == "watershed":
            result, _ = segmentasi.watershed_segmentation(image)
        elif method == "kmeans":
            k = int(params.get("k", 3))
            attempts = int(params.get("attempts", 10))
            result, _ = segmentasi.k_means_segmentation(image, k, attempts)
        elif method == "color_segmentation":
            lower_bound = np.array(params.get("lower_bound", [0, 0, 0]))
            upper_bound = np.array(params.get("upper_bound", [255, 255, 255]))
            result, _ = segmentasi.color_segmentation(image, lower_bound, upper_bound)
        
        # Study case methods
        elif method == "face_detection":
            result, _ = studicase.detect_faces(image)
        elif method == "eye_detection":
            result, _ = studicase.detect_eyes(image)
        elif method == "contour_detection":
            threshold1 = int(params.get("threshold1", 50))
            threshold2 = int(params.get("threshold2", 150))
            result, _ = studicase.detect_contours(image, threshold1, threshold2)
        elif method == "histogram_equalization":
            result, _ = studicase.histogram_equalization(image)
        
        # Transform methods
        elif method == "resize":
            width = params.get("width", None)
            height = params.get("height", None)
            percentage = params.get("percentage", None)
            if width is not None:
                width = int(width)
            if height is not None:
                height = int(height)
            if percentage is not None:
                percentage = float(percentage)
            result = transform.resize(image, width, height, percentage)
        elif method == "rotate":
            angle = float(params.get("angle", 0))
            center = params.get("center", None)
            scale = float(params.get("scale", 1.0))
            result = transform.rotate(image, angle, center, scale)
        elif method == "flip":
            flip_code = int(params.get("flip_code", 1))
            result = transform.flip(image, flip_code)
        elif method == "crop":
            x = int(params.get("x", 0))
            y = int(params.get("y", 0))
            width = int(params.get("width", image.shape[1]))
            height = int(params.get("height", image.shape[0]))
            result = transform.crop(image, x, y, width, height)
        else:
            return None, f"Unknown method: {method}"
        
        # Save the processed image
        cv2.imwrite(output_path, result)
        return output_path, None
    except Exception as e:
        return None, str(e)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    # Check if the post request has the file part
    if 'file' not in request.files and 'image_data' not in request.form:
        return jsonify({"error": "No file or image data provided"}), 400
    
    try:
        if 'file' in request.files:
            file = request.files['file']
            if file.filename == '':
                return jsonify({"error": "No selected file"}), 400
            if file and allowed_file(file.filename):
                filepath = save_image(file)
            else:
                return jsonify({"error": "File type not allowed"}), 400
        else:
            # Handle image data from camera
            image_data = request.form['image_data']
            filepath = save_image(image_data)
        
        return jsonify({
            "success": True,
            "filepath": filepath,
            "filename": os.path.basename(filepath)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/process', methods=['POST'])
def process_request():
    data = request.json
    
    if 'filepath' not in data or 'method' not in data:
        return jsonify({"error": "Missing filepath or method"}), 400
    
    filepath = data['filepath']
    method = data['method']
    params = data.get('params', {})
    
    output_path, error = process_image(filepath, method, params)
    
    if error:
        return jsonify({"error": error}), 500
    
    return jsonify({
        "success": True,
        "processed_image": f"/processed/{os.path.basename(output_path)}"
    })

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/processed/<filename>')
def processed_file(filename):
    return send_from_directory(app.config['PROCESSED_FOLDER'], filename)

@app.route('/methods')
def get_methods():
    """Return available processing methods"""
    methods = {
        "filter": [
            {"name": "grayscale", "display": "Grayscale", "params": {}},
            {"name": "gaussian_blur", "display": "Gaussian Blur", "params": {"kernel_size": 5}},
            {"name": "median_blur", "display": "Median Blur", "params": {"kernel_size": 5}},
            {"name": "bilateral_filter", "display": "Bilateral Filter", "params": {"d": 9, "sigma_color": 75, "sigma_space": 75}},
            {"name": "sobel_edge", "display": "Sobel Edge Detection", "params": {"dx": 1, "dy": 1, "ksize": 3}},
            {"name": "canny_edge", "display": "Canny Edge Detection", "params": {"threshold1": 100, "threshold2": 200}},
            {"name": "sharpen", "display": "Sharpen", "params": {}},
            {"name": "emboss", "display": "Emboss", "params": {}}
        ],
        "segmentation": [
            {"name": "threshold", "display": "Basic Threshold", "params": {"thresh": 127, "max_val": 255}},
            {"name": "adaptive_threshold", "display": "Adaptive Threshold", "params": {"max_val": 255, "block_size": 11, "C": 2}},
            {"name": "otsu_threshold", "display": "Otsu Threshold", "params": {}},
            {"name": "watershed", "display": "Watershed Segmentation", "params": {}},
            {"name": "kmeans", "display": "K-Means Segmentation", "params": {"k": 3, "attempts": 10}},
            {"name": "color_segmentation", "display": "Color Segmentation", "params": {"lower_bound": [0, 0, 0], "upper_bound": [255, 255, 255]}}
        ],
        "studicase": [
            {"name": "face_detection", "display": "Face Detection", "params": {}},
            {"name": "eye_detection", "display": "Eye Detection", "params": {}},
            {"name": "contour_detection", "display": "Contour Detection", "params": {"threshold1": 50, "threshold2": 150}},
            {"name": "histogram_equalization", "display": "Histogram Equalization", "params": {}}
        ],
        "transform": [
            {"name": "resize", "display": "Resize", "params": {"width": 300, "height": 300, "percentage": 50}},
            {"name": "rotate", "display": "Rotate", "params": {"angle": 45, "scale": 1.0}},
            {"name": "flip", "display": "Flip", "params": {"flip_code": 1}},
            {"name": "crop", "display": "Crop", "params": {"x": 0, "y": 0, "width": 200, "height": 200}}
        ]
    }
    
    return jsonify(methods)

if __name__ == '__main__':
    app.run(debug=True)
