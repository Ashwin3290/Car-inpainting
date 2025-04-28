from typing import Union, Optional, Tuple, Dict, Any, List
import os
import cv2
import numpy as np
import shutil
import requests
import uuid
import base64
from pathlib import Path
from io import BytesIO
import pickle
from sklearn.cluster import KMeans

class CarRecolorError(Exception):
    """Custom exception for car recoloring errors"""
    pass

def generate_uuid_filename() -> str:
    """Generate a UUID filename while preserving the original extension."""
    return str(uuid.uuid4())

def get_mask_filename(image_path: str) -> str:
    """Generate the mask filename for a given image UUID."""
    base_uuid = os.path.splitext(image_path)[0]
    return f"{base_uuid}_mask.png"

def get_analysis_filename(image_path: str) -> str:
    """Generate the analysis filename for a given image UUID."""
    base_uuid = os.path.splitext(image_path)[0]
    return f"{base_uuid}_analysis.pkl"

def check_existing_mask(base_dir: str, mask_filename: str) -> Optional[np.ndarray]:
    """Check if a mask file exists and load it if it does."""
    mask_path = os.path.join(base_dir, 'masks', mask_filename)
    if os.path.exists(mask_path):
        mask = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)
        return mask
    return None

def save_mask(mask: np.ndarray, base_dir: str, mask_filename: str) -> bool:
    """Save a mask to the masks directory."""
    try:
        masks_dir = os.path.join(base_dir, 'masks')
        os.makedirs(masks_dir, exist_ok=True)
        
        mask_path = os.path.join(masks_dir, mask_filename)
        return cv2.imwrite(mask_path, mask)
    except Exception as e:
        print(f"Error saving mask: {str(e)}")
        return False

def get_mask_from_api(image_path: str, api_url: str) -> np.ndarray:
    """Get mask from the API for a given image."""
    try:
        with open(image_path, 'rb') as image_file:
            files = {'file': ('image.jpg', image_file, 'image/jpeg')}
            
            full_url = f"{api_url}/generate_mask"
            response = requests.post(full_url, files=files)
            
            if response.status_code == 404:
                raise Exception(f"API endpoint not found: {full_url}")
            elif response.status_code != 200:
                raise Exception(f"API request failed with status {response.status_code}")
            
            mask_base64 = response.json()['mask']
            mask_bytes = base64.b64decode(mask_base64)
            mask_array = np.frombuffer(mask_bytes, dtype=np.uint8)
            mask = cv2.imdecode(mask_array, cv2.IMREAD_GRAYSCALE)
            
            return mask
            
    except Exception as e:
        raise Exception(f"Error getting mask from API: {str(e)}")

def analyze_car(masked_car_rgb: np.ndarray, k: int = 200) -> Dict[str, Any]:
    """
    Analyze car colors using both LAB and HSV color spaces.
    Automatically adjusts number of clusters based on available pixels.
    """
    # Convert to LAB space for brightness analysis
    lab_image = cv2.cvtColor(masked_car_rgb[:, :, ::-1], cv2.COLOR_BGR2LAB)
    
    # Also get HSV for color analysis
    hsv_image = cv2.cvtColor(masked_car_rgb[:, :, ::-1], cv2.COLOR_BGR2HSV)
    
    # Get valid pixels
    pixels_lab = lab_image.reshape(-1, 3)
    pixels_hsv = hsv_image.reshape(-1, 3)
    mask = np.any(masked_car_rgb.reshape(-1, 3) > 0, axis=1)
    valid_pixels_lab = pixels_lab[mask]
    valid_pixels_hsv = pixels_hsv[mask]
    
    # Adjust number of clusters based on available pixels
    n_pixels = len(valid_pixels_lab)
    adjusted_k = min(k, n_pixels - 1)  # Ensure k is less than number of samples
    adjusted_k = max(adjusted_k, 5)     # Ensure at least 5 clusters for meaningful analysis
    
    # Perform k-means clustering in LAB space
    kmeans = KMeans(n_clusters=adjusted_k, random_state=42)
    labels = kmeans.fit_predict(valid_pixels_lab)
    
    # Get cluster centers and convert to different color spaces
    centers_lab = kmeans.cluster_centers_
    centers_bgr = np.array([
        cv2.cvtColor(center.reshape(1, 1, 3).astype(np.uint8), 
                    cv2.COLOR_LAB2BGR).reshape(3) 
        for center in centers_lab
    ])
    centers_hsv = cv2.cvtColor(centers_bgr.reshape(-1, 1, 3), cv2.COLOR_BGR2HSV).reshape(-1, 3)
    
    # Calculate percentages and find dominant color
    unique_labels, counts = np.unique(labels, return_counts=True)
    percentages = counts / len(labels) * 100
    dominant_idx = np.argmax(percentages)
    
    # Get brightness information
    l_channel = lab_image[..., 0].astype(float)
    valid_l = l_channel[l_channel > 0]
    
    brightness_mean = np.mean(valid_l)
    brightness_std = np.std(valid_l)

    dark_measure = centers_hsv[dominant_idx][2]
    # Create brightness mask relative to dominant color
    base_brightness = centers_lab[dominant_idx][0]
    relative_brightness = np.zeros_like(l_channel, dtype=float)
    relative_brightness[l_channel > 0] = l_channel[l_channel > 0] / base_brightness
    
    # Create full labels array
    full_labels = np.zeros(pixels_lab.shape[0], dtype=int)
    full_labels[mask] = labels
    full_labels = full_labels.reshape(masked_car_rgb.shape[:2])
    
    return {
        'centers_lab': centers_lab,
        'centers_hsv': centers_hsv,
        'labels': full_labels,
        'percentages': percentages,
        'dominant_idx': dominant_idx,
        'relative_brightness': relative_brightness,
        'brightness_stats': {
            'mean': brightness_mean,
            'std': brightness_std,
            'is_dark_car': dark_measure < 40,
            'is_bright_car': dark_measure > 160,
        },
        'valid_mask': mask.reshape(masked_car_rgb.shape[:2])
    }

def save_analysis(results: Dict[str, Any], base_dir: str, analysis_filename: str) -> bool:
    """Save analysis results to a pickle file."""
    try:
        analyses_dir = os.path.join(base_dir, 'analyses')
        os.makedirs(analyses_dir, exist_ok=True)
        
        analysis_path = os.path.join(analyses_dir, analysis_filename)
        with open(analysis_path, 'wb') as f:
            pickle.dump(results, f)
        return True
    except Exception as e:
        print(f"Error saving analysis: {str(e)}")
        return False

def load_analysis(base_dir: str, analysis_filename: str) -> Optional[Dict[str, Any]]:
    """Load analysis results from a pickle file."""
    try:
        analysis_path = os.path.join(base_dir, 'analyses', analysis_filename)
        if os.path.exists(analysis_path):
            with open(analysis_path, 'rb') as f:
                return pickle.load(f)
        
        return None
    except Exception as e:
        print(f"Error loading analysis: {str(e)}")
        return None

def remap_colors(masked_car_rgb, target_color_rgb, analysis_results):
    """
    Remap colors using hybrid approach with special handling for extreme colors
    """
    # Convert target color to both LAB and HSV
    target_color_bgr = target_color_rgb[::-1].reshape(1, 1, 3).astype(np.uint8)
    target_color_lab = cv2.cvtColor(target_color_bgr, cv2.COLOR_BGR2LAB)[0, 0]
    target_color_hsv = cv2.cvtColor(target_color_bgr, cv2.COLOR_BGR2HSV)[0, 0]

    # Get dominant color information
    dominant_idx = analysis_results['dominant_idx']
    dominant_color_hsv = analysis_results['centers_hsv'][dominant_idx]
    
    # Determine target color characteristics
    is_white = np.all(target_color_rgb >= 250)
    is_black = np.all(target_color_rgb <= 5)
    is_dark_car = analysis_results['brightness_stats']['is_dark_car']
    
    # Calculate target brightness (grayscale)
    target_brightness = np.mean(target_color_rgb)
    is_extreme_color = target_brightness > 240 or target_brightness < 30

    # Create new colors using HSV
    centers_hsv = analysis_results['centers_hsv'].copy()

    if is_white:
        # Special handling for white target
        for i in range(len(centers_hsv)):
            value_ratio = centers_hsv[i, 2] / 255.0
            centers_hsv[i, 0] = 0  # Hue doesn't matter
            centers_hsv[i, 1] = 0  # No saturation for white
            centers_hsv[i, 2] = np.clip(170 + (value_ratio * 10), 0, 255)  # High value with variation
    
    elif is_black:
        # Special handling for black target
        for i in range(len(centers_hsv)):
            value_ratio = centers_hsv[i, 2] / 255.0
            centers_hsv[i, 0] = 0  # Hue doesn't matter
            centers_hsv[i, 1] = 0  # No saturation for black
            centers_hsv[i, 2] = np.clip(value_ratio * 50, 0, 255)  # Keep low value with variation
    
    elif is_dark_car:
        dark_value_min, dark_value_max = 0, 100  # Original range for dark car value
        target_value_min, target_value_max = 50, target_color_hsv[2]  # Target range for normalization
        
        for i in range(len(centers_hsv)):
            # Normalize Value (V) - Map from dark_value range to target_value range
            current_value = centers_hsv[i, 2]
            normalized_value = ((current_value - dark_value_min) / (dark_value_max - dark_value_min + 1e-6)) * \
                            (target_value_max - target_value_min) + target_value_min
            centers_hsv[i, 2] = np.clip(normalized_value, 0, 255)
    
            # Weighted Saturation Adjustment - Blend original and target saturation
            original_saturation = centers_hsv[i, 1]
            target_saturation = target_color_hsv[1]
            blend_ratio = 0.6 if current_value < 50 else 0.3
            adjusted_saturation = (1 - blend_ratio) * original_saturation + blend_ratio * target_saturation
            centers_hsv[i, 1] = np.clip(adjusted_saturation, 100, 255)
    
            # Optionally adjust hue to match the target
            centers_hsv[i, 0] = target_color_hsv[0]

    else:
        print("Normal car detected")
        for i in range(len(centers_hsv)):
            dark_value_min, dark_value_max = 0, 100  # Original range for dark car value
            target_value_min, target_value_max = 50, target_color_hsv[2]  # Target range for normalization
            centers_hsv[i, 0] = target_color_hsv[0]
            current_value = centers_hsv[i, 2]
            # Adjust saturation while preserving relative differences
            original_saturation = centers_hsv[i, 1]
            target_saturation = target_color_hsv[1]
            blend_ratio = 0.6 if current_value < 50 else 0.3
            adjusted_saturation = (1 - blend_ratio) * original_saturation + blend_ratio * target_saturation
            centers_hsv[i, 1] = np.clip(adjusted_saturation, 110, 255)
    
    # Convert to RGB and create remapped image
    new_colors_bgr = cv2.cvtColor(centers_hsv.reshape(-1, 1, 3).astype(np.uint8), 
                                 cv2.COLOR_HSV2BGR).reshape(-1, 3)
    new_colors_rgb = new_colors_bgr[:, ::-1]

    remapped = np.zeros_like(masked_car_rgb)
    labels = analysis_results['labels']

    # Apply colors
    for i in range(len(new_colors_rgb)):
        color_mask = labels == i
        remapped[color_mask] = new_colors_rgb[i]
    
    # Apply brightness modulation
    relative_brightness = analysis_results['relative_brightness']
    brightness_factor = np.stack([relative_brightness] * 3, axis=2)
    
    if is_extreme_color:
        # For extreme colors, adjust brightness factor power
        if target_brightness > 240:  # Very bright
            brightness_factor = brightness_factor ** 0.7
        else:  # Very dark
            brightness_factor = brightness_factor ** 1.2
    if is_dark_car:
        brightness_factor = brightness_factor ** 0.1
    
    remapped = np.clip(remapped * brightness_factor, 0, 255).astype(np.uint8)
    remapped[~analysis_results['valid_mask']] = 0

    return remapped

def verify_color_format(color: tuple) -> bool:
    """Verify if the color format is valid (BGR tuple with values between 0-255)."""
    if not isinstance(color, tuple) or len(color) != 3:
        return False
    return all(isinstance(v, int) and 0 <= v <= 255 for v in color)

def recolor_car(
    image_uuid: str,
    target_color: Tuple[int, int, int],
    base_dir: str,
    api_url: str,
    output_path: Optional[str] = None,
    preserve_luminance: bool = True,
    reflection_threshold: int = 200
) -> Dict[str, Union[bool, str]]:
    """Main function to recolor a car image using the mask generation API."""
    try:
        if not verify_color_format(target_color):
            raise CarRecolorError("Invalid color format. Must be BGR tuple with values 0-255")
        
        # Create UUID filename and copy image to processing directory
        processed_dir = os.path.join(base_dir, 'processed')
        os.makedirs(processed_dir, exist_ok=True)
        
        new_image_path = os.path.join(processed_dir, image_uuid)
        
        # Check for existing mask or generate new one
        mask_filename = get_mask_filename(image_uuid)
        mask = check_existing_mask(base_dir, mask_filename)
        
        if mask is None:
            try:
                mask = get_mask_from_api(new_image_path, api_url)
                save_mask(mask, base_dir, mask_filename)
            except Exception as e:
                raise CarRecolorError(f"Failed to generate/save mask: {str(e)}")
        
        # Create masked car and perform analysis
        original = cv2.imread(new_image_path)
        if original is None:
            raise CarRecolorError("Failed to load image")
        
        # Ensure mask is proper size and binary
        mask = cv2.resize(mask, (original.shape[1], original.shape[0]))
        _, mask = cv2.threshold(mask, 127, 255, cv2.THRESH_BINARY)
        
        # Create masked car
        masked_car = cv2.bitwise_and(original, original, mask=mask)
        
        # Perform and save analysis
        analysis_filename = get_analysis_filename(image_uuid)
        analysis_results = analyze_car(cv2.cvtColor(masked_car, cv2.COLOR_BGR2RGB))
        save_analysis(analysis_results, base_dir, analysis_filename)
        
        # Perform recoloring
        # Note: target_color comes in as RGB from frontend, but OpenCV uses BGR
        # So we need to reverse the order for internal processing
        target_rgb = np.array(target_color)
        remapped = remap_colors(
            masked_car,
            target_rgb,
            analysis_results
        )
        
        # Convert back to BGR and create final image
        remapped_bgr = cv2.cvtColor(remapped, cv2.COLOR_RGB2BGR)
        result = cv2.bitwise_and(original, original, mask=cv2.bitwise_not(mask))
        result = cv2.add(result, remapped_bgr)
        
        # Save the result
        if output_path is None:
            output_filename = f"{image_uuid}"
            output_path = os.path.join(base_dir, 'output', f"recolored_{output_filename}")
        
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        cv2.imwrite(output_path, result)
        
        return {
            'success': True,
            'image_path': output_path,
            'message': 'Image successfully recolored'
        }
            
    except CarRecolorError as e:
        return {
            'success': False,
            'image_path': None,
            'message': str(e)
        }
    except Exception as e:
        import traceback
        stack_trace = traceback.format_exc()
        print(f"Exception in recolor_car: {str(e)}")
        print(f"Stack trace: {stack_trace}")
        return {
            'success': False,
            'image_path': None,
            'message': f"Unexpected error: {str(e)}"
        }
