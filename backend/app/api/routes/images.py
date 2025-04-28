from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.responses import JSONResponse
from typing import List
import uuid
import os
from pathlib import Path
from app.core.config import settings
from app.services.car_recolor_service import CarRecolorService

router = APIRouter()

def get_car_recolor_service():
    return CarRecolorService(
        base_dir="storage",
        api_url=settings.MASKING_API_URL
    )

@router.post("/images")
async def upload_image(
    file: UploadFile = File(...),
    service: CarRecolorService = Depends(get_car_recolor_service)
):
    """
    Upload a car image for processing
    """
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    # Generate unique identifier for the image
    file_extension = os.path.splitext(file.filename)[1] if file.filename else ".jpg"
    unique_id = str(uuid.uuid4()) + file_extension
    
    # Read file content
    file_content = await file.read()
    
    # Process the image
    try:
        current_uuid = service.process_new_image(file_content, unique_id)
        
        return {
            "success": True,
            "uuid": current_uuid,
            "message": "Image uploaded successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")

@router.get("/images/{image_uuid}")
async def get_image_status(
    image_uuid: str,
    service: CarRecolorService = Depends(get_car_recolor_service)
):
    """
    Get the processing status of an image
    """
    status = service.get_processing_status()
    return status
