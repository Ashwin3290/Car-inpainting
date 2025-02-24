import os
import threading
import cv2
from typing import Optional, Dict, Any, Tuple
from recolor import (
    generate_uuid_filename,
    get_mask_filename,
    get_analysis_filename,
    check_existing_mask,
    get_mask_from_api,
    analyze_car,
    save_analysis,
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
    
    def recolor_current_image(
        self,
        target_color: Tuple[int, int, int],
        wait_timeout: int = 30
    ) -> Dict[str, Any]:
        """
        Recolor the current image with the specified target color.
        Returns the result dictionary with success status and image path.
        """
        if not self.current_uuid:
            return {
                'success': False,
                'message': 'No image currently loaded'
            }
        
        # Wait for processing to complete
        if not self.processing_complete.wait(timeout=wait_timeout):
            return {
                'success': False,
                'message': 'Processing timeout'
            }
        
        # Perform recoloring
        image_path = os.path.join(self.base_dir, 'processed', self.current_uuid)
        output_path = os.path.join(self.base_dir, 'output', f"recolored_{self.current_uuid}")
        
        result = recolor_car(
            image_uuid=self.current_uuid,
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