from fastapi import APIRouter, HTTPException, Depends, Body
from typing import Dict, List, Any
from pydantic import BaseModel
import os
import json
from datetime import datetime
from app.core.config import settings
from app.services.car_recolor_service import CarRecolorService

router = APIRouter()

def get_car_recolor_service():
    return CarRecolorService(
        base_dir="storage",
        api_url=settings.MASKING_API_URL
    )

class HistoryEntry(BaseModel):
    timestamp: str
    original_image: str
    recolored_image: str
    color: List[int]
    settings: Dict[str, Any]
    uuid: str

@router.get("/history")
async def get_history() -> List[Dict[str, Any]]:
    """
    Get processing history
    """
    history_path = os.path.join("storage", "history.json")
    
    if not os.path.exists(history_path):
        # Create empty history file
        os.makedirs(os.path.dirname(history_path), exist_ok=True)
        with open(history_path, "w") as f:
            f.write("[]")
        return []
    
    try:
        with open(history_path, "r") as f:
            history = json.load(f)
        return history
    except Exception as e:
        import traceback
        stack_trace = traceback.format_exc()
        print(f"Error loading history: {str(e)}")
        print(f"Stack trace: {stack_trace}")
        raise HTTPException(status_code=500, detail=f"Error loading history: {str(e)}")

@router.post("/history")
async def save_history_entry(
    entry: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Save a new history entry
    """
    history_path = os.path.join("storage", "history.json")
    
    try:
        # Load existing history
        if os.path.exists(history_path):
            with open(history_path, "r") as f:
                history = json.load(f)
        else:
            # Create directory and file if they don't exist
            os.makedirs(os.path.dirname(history_path), exist_ok=True)
            history = []
        
        # Add entry with timestamp
        entry["timestamp"] = datetime.now().isoformat()
        history.append(entry)
        
        # Save history
        with open(history_path, "w") as f:
            json.dump(history, f)
        
        print(f"Saved history entry: {entry}")
        
        return {
            "success": True,
            "message": "History entry saved successfully"
        }
    except Exception as e:
        import traceback
        stack_trace = traceback.format_exc()
        print(f"Error saving history: {str(e)}")
        print(f"Stack trace: {stack_trace}")
        raise HTTPException(status_code=500, detail=f"Error saving history: {str(e)}")

@router.delete("/history/{entry_id}")
async def delete_history_entry(
    entry_id: str
) -> Dict[str, Any]:
    """
    Delete a history entry
    """
    history_path = os.path.join("storage", "history.json")
    
    if not os.path.exists(history_path):
        raise HTTPException(status_code=404, detail="History not found")
    
    try:
        # Load existing history
        with open(history_path, "r") as f:
            history = json.load(f)
        
        # Filter out the entry to delete
        filtered_history = [entry for entry in history if entry.get("uuid") != entry_id]
        
        if len(history) == len(filtered_history):
            raise HTTPException(status_code=404, detail="History entry not found")
        
        # Save history
        with open(history_path, "w") as f:
            json.dump(filtered_history, f)
        
        return {
            "success": True,
            "message": "History entry deleted successfully"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting history entry: {str(e)}")
