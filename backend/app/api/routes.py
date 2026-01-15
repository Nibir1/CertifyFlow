from fastapi import APIRouter, HTTPException
from app.models.schemas import TechSpec, FATProcedure
from app.core.generator import generate_fat_from_spec

router = APIRouter()

@router.post("/generate", response_model=FATProcedure)
async def generate_procedure(spec: TechSpec):
    """
    Generate a standard FAT Procedure from a raw technical specification.
    """
    try:
        # Call the AI logic
        result = generate_fat_from_spec(spec.raw_text)
        return result
    except Exception as e:
        # In a real app, we would log the error details here
        raise HTTPException(status_code=500, detail=str(e))