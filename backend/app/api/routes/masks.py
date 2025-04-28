from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any
import requests
from app.core.config import settings
from app.services.car_recolor_service import CarRecolorService

router = APIRouter()

def get_car_recolor_service():
    return CarRecolorService(
        base_dir="storage",
        api_url=settings.MASKING_API_URL
    )

@router.post("/proxy-mask/{image_uuid}")
async def proxy_mask_generation(
    image_uuid: str,
    service: CarRecolorService = Depends(get_car_recolor_service)
) -> Dict[str, Any]:
    """
    Proxy request to the external masking API and cache the result
    """
    try:
        # Check if mask already exists
        mask_filename = service.get_mask_filename(image_uuid)
        mask = service.check_existing_mask(mask_filename)
        
        if mask is not None:
            return {
                "success": True,
                "message": "Mask retrieved from cache",
                "cached": True
            }
        
        # Get mask from external API
        image_path = service.get_image_path(image_uuid)
        mask = service.get_mask_from_api(image_path)
        
        # Save the mask
        service.save_mask(mask, mask_filename)
        
        return {
            "success": True,
            "message": "Mask generated successfully",
            "cached": False
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating mask: {str(e)}")
