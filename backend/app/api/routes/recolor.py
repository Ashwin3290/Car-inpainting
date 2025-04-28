from fastapi import APIRouter, HTTPException, Depends, Body
from fastapi.responses import FileResponse
from typing import Dict, List, Any, Tuple
from pydantic import BaseModel
import os
from app.services.car_recolor_service import CarRecolorService
from app.core.config import settings

router = APIRouter()

def get_car_recolor_service():
    return CarRecolorService(
        base_dir="storage",
        api_url=settings.MASKING_API_URL
    )

class ColorRequest(BaseModel):
    color: Tuple[int, int, int]  # RGB color

@router.post("/analyze/{image_uuid}")
async def analyze_car_image(
    image_uuid: str,
    service: CarRecolorService = Depends(get_car_recolor_service)
) -> Dict[str, Any]:
    """
    Analyze car colors and prepare for recoloring
    """
    try:
        # Check if analysis already exists
        analysis_filename = service.get_analysis_filename(image_uuid)
        analysis = service.load_analysis(analysis_filename)
        
        if analysis is not None:
            return {
                "success": True,
                "message": "Analysis retrieved from cache",
                "cached": True
            }
        
        # Perform analysis
        image_path = service.get_image_path(image_uuid)
        mask_filename = service.get_mask_filename(image_uuid)
        mask = service.check_existing_mask(mask_filename)
        
        if mask is None:
            raise HTTPException(status_code=400, detail="Mask not found. Generate mask first.")
        
        # Analyze car colors
        analysis_results = service.analyze_car_image(image_path, mask)
        service.save_analysis(analysis_results, analysis_filename)
        
        return {
            "success": True,
            "message": "Car analyzed successfully",
            "cached": False
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing car: {str(e)}")

@router.post("/recolor/{image_uuid}")
async def recolor_car_image(
    image_uuid: str,
    color_request: ColorRequest,
    service: CarRecolorService = Depends(get_car_recolor_service)
) -> Dict[str, Any]:
    """
    Recolor the car with the specified color
    """
    try:
        result = service.recolor_current_image(
            target_color=color_request.color,
            image_uuid=image_uuid
        )
        
        if not result['success']:
            raise HTTPException(status_code=500, detail=result['message'])
        
        return {
            "success": True,
            "message": "Car recolored successfully",
            "image_path": result["image_path"]
        }
    except Exception as e:
        import traceback
        stack_trace = traceback.format_exc()
        print(f"Exception in /recolor/{image_uuid} endpoint: {str(e)}")
        print(f"Stack trace: {stack_trace}")
        raise HTTPException(status_code=500, detail=f"Error recoloring car: {str(e)}")

@router.get("/recolored/{image_uuid}")
async def get_recolored_image(
    image_uuid: str,
    service: CarRecolorService = Depends(get_car_recolor_service)
):
    """
    Get the recolored image
    """
    output_path = os.path.join("storage", settings.OUTPUT_DIR, f"recolored_{image_uuid}")
    if not os.path.exists(output_path):
        raise HTTPException(status_code=404, detail="Recolored image not found")
    
    return FileResponse(output_path)
