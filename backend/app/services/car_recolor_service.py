import os
import threading
import cv2
import numpy as np
from typing import Optional, Dict, Any, Tuple, List
import requests
import base64
import uuid
import pickle
from pathlib import Path

# Importing the recolor functions
from app.services.color_analysis import (
    generate_uuid_filename,
    get_mask_filename,
    get_analysis_filename,
    check_existing_mask,
    get_mask_from_api,
    analyze_car,
    save_analysis,
    load_analysis,
    recolor_car
)

class CarRecolorService:
    def __init__(self, base_dir: str, api_url: str):
        """Initialize the car recolor service with base directory and API URL."""
        self.base_dir = base_dir
        self.api_url = api_url
        self.current_uuid = None
        self.processing_lock = threading.Lock()
        self.processing_thread = None
        self.processing_complete = threading.Event()
        self.mask_complete = threading.Event()
        self._setup_directories()
        print("CarRecolorService initialized.")
        
    def _setup_directories(self):
        """Create necessary directories if they don't exist."""
        for dir_name in ['processed', 'masks', 'analyses', 'output']:
            os.makedirs(os.path.join(self.base_dir, dir_name), exist_ok=True)
        
        # Ensure history.json exists
        history_path = os.path.join(self.base_dir, "history.json")
        if not os.path.exists(history_path):
            with open(history_path, "w") as f:
                f.write("[]")
    
    def _process_image_async(self, image_path: str):
        """Background processing of mask and analysis."""
        try:
            # Generate mask
            mask_filename = get_mask_filename(self.current_uuid)
            mask = check_existing_mask(self.base_dir, mask_filename)
            
            if mask is None:
                mask = get_mask_from_api(image_path, self.api_url)
                cv2.imwrite(os.path.join(self.base_dir, 'masks', mask_filename), mask)
            
            self.mask_complete.set()
            
            # Perform analysis
            original = cv2.imread(image_path)
            mask = cv2.resize(mask, (original.shape[1], original.shape[0]))
            _, mask = cv2.threshold(mask, 127, 255, cv2.THRESH_BINARY)
            
            masked_car = cv2.bitwise_and(original, original, mask=mask)
            analysis_results = analyze_car(cv2.cvtColor(masked_car, cv2.COLOR_BGR2RGB))
            
            analysis_filename = get_analysis_filename(self.current_uuid)
            save_analysis(analysis_results, self.base_dir, analysis_filename)
            
            self.processing_complete.set()
            
        except Exception as e:
            print(f"Error in background processing: {str(e)}")
            # Reset events in case of error
            self.mask_complete.set()
            self.processing_complete.set()
    
    def process_new_image(self, image_data: bytes, file_name: str) -> str:
        """
        Process a new image upload.
        Returns the UUID for the processed image.
        """
        with self.processing_lock:
            # Reset processing flags
            self.mask_complete.clear()
            self.processing_complete.clear()
            
            # Generate new UUID and save image
            file_extension = os.path.splitext(file_name)[1]
            self.current_uuid = generate_uuid_filename() + file_extension
            new_image_path = os.path.join(self.base_dir, 'processed', self.current_uuid)
            
            with open(new_image_path, 'wb') as f:
                f.write(image_data)
            
            # Start background processing
            self.processing_thread = threading.Thread(
                target=self._process_image_async,
                args=(new_image_path,)
            )
            self.processing_thread.start()
            
            return self.current_uuid
    
    def get_image_path(self, image_uuid: str) -> str:
        """Get the path to an image by UUID."""
        return os.path.join(self.base_dir, 'processed', image_uuid)
    
    def get_mask_filename(self, image_uuid: str) -> str:
        """Get the mask filename for an image UUID."""
        return get_mask_filename(image_uuid)
    
    def get_analysis_filename(self, image_uuid: str) -> str:
        """Get the analysis filename for an image UUID."""
        return get_analysis_filename(image_uuid)
    
    def check_existing_mask(self, mask_filename: str) -> Optional[np.ndarray]:
        """Check if a mask exists and load it."""
        return check_existing_mask(self.base_dir, mask_filename)
    
    def save_mask(self, mask: np.ndarray, mask_filename: str) -> bool:
        """Save a mask to disk."""
        mask_path = os.path.join(self.base_dir, 'masks', mask_filename)
        return cv2.imwrite(mask_path, mask)
    
    def get_mask_from_api(self, image_path: str) -> np.ndarray:
        """Get mask from external API."""
        return get_mask_from_api(image_path, self.api_url)
    
    def analyze_car_image(self, image_path: str, mask: np.ndarray) -> Dict[str, Any]:
        """Analyze car colors in an image."""
        original = cv2.imread(image_path)
        mask = cv2.resize(mask, (original.shape[1], original.shape[0]))
        _, mask = cv2.threshold(mask, 127, 255, cv2.THRESH_BINARY)
        
        masked_car = cv2.bitwise_and(original, original, mask=mask)
        return analyze_car(cv2.cvtColor(masked_car, cv2.COLOR_BGR2RGB))
    
    def load_analysis(self, analysis_filename: str) -> Optional[Dict[str, Any]]:
        """Load analysis results."""
        return load_analysis(self.base_dir, analysis_filename)
    
    def save_analysis(self, analysis_results: Dict[str, Any], analysis_filename: str) -> bool:
        """Save analysis results."""
        return save_analysis(analysis_results, self.base_dir, analysis_filename)
    
    def recolor_current_image(
        self,
        target_color: Tuple[int, int, int],
        image_uuid: Optional[str] = None,
        wait_timeout: int = 30
    ) -> Dict[str, Any]:
        """
        Recolor the image with the specified target color.
        If image_uuid is provided, it will be used. Otherwise, falls back to current_uuid.
        Returns the result dictionary with success status and image path.
        """
        # Determine which UUID to use
        uuid_to_use = image_uuid if image_uuid else self.current_uuid
        
        if not uuid_to_use:
            return {
                'success': False,
                'message': 'No image UUID provided or currently loaded'
            }
        
        # If using current_uuid, wait for processing to complete
        if not image_uuid and not self.processing_complete.wait(timeout=wait_timeout):
            return {
                'success': False,
                'message': 'Processing timeout'
            }
        
        # Perform recoloring
        image_path = os.path.join(self.base_dir, 'processed', uuid_to_use)
        output_path = os.path.join(self.base_dir, 'output', f"recolored_{uuid_to_use}")
        print(f"Recoloring image: {image_path} to {output_path}")
        print(f"Target color: {target_color}")
        
        # Validate that image exists
        if not os.path.exists(image_path):
            return {
                'success': False,
                'message': f'Image not found: {image_path}'
            }
            
        # Validate that analysis exists
        analysis_filename = get_analysis_filename(uuid_to_use)
        analysis_path = os.path.join(self.base_dir, 'analyses', analysis_filename)
        if not os.path.exists(analysis_path):
            print(f"Analysis not found: {analysis_path}")
            # Try to generate analysis on-the-fly
            try:
                # Get or generate mask
                mask_filename = get_mask_filename(uuid_to_use)
                mask = check_existing_mask(self.base_dir, mask_filename)
                if mask is None:
                    mask = get_mask_from_api(image_path, self.api_url)
                    save_mask(mask, self.base_dir, mask_filename)
                
                # Generate analysis
                original = cv2.imread(image_path)
                mask = cv2.resize(mask, (original.shape[1], original.shape[0]))
                _, mask = cv2.threshold(mask, 127, 255, cv2.THRESH_BINARY)
                
                masked_car = cv2.bitwise_and(original, original, mask=mask)
                analysis_results = analyze_car(cv2.cvtColor(masked_car, cv2.COLOR_BGR2RGB))
                
                save_analysis(analysis_results, self.base_dir, analysis_filename)
                print(f"Generated analysis on-the-fly for {uuid_to_use}")
            except Exception as e:
                print(f"Failed to generate analysis: {str(e)}")
                return {
                    'success': False,
                    'message': f'Analysis not found and could not be generated: {str(e)}'
                }
        result = recolor_car(
            image_uuid=uuid_to_use,
            target_color=target_color,
            base_dir=self.base_dir,
            api_url=self.api_url,
            output_path=output_path
        )
        
        return result
    
    def get_processing_status(self) -> Dict[str, bool]:
        """Get the current processing status."""
        return {
            'mask_complete': self.mask_complete.is_set(),
            'analysis_complete': self.processing_complete.is_set()
        }
    
    def get_current_uuid(self) -> Optional[str]:
        """Get the current image UUID."""
        return self.current_uuid
