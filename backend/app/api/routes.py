from fastapi import APIRouter, HTTPException, Response
from app.models.schemas import TechSpec, FATProcedure
from app.core.generator import generate_fat_from_spec
from app.services.pdf_renderer import render_fat_pdf
from app.core.validator import ComplianceValidator  # <--- NEW: Import the Safety Guardrail

router = APIRouter()

@router.post("/generate", response_model=FATProcedure)
async def generate_procedure(spec: TechSpec):
    """
    Generate a standard FAT Procedure from a raw technical specification.
    Includes a post-processing validation step to enforce safety rules.
    """
    try:
        # 1. Generate via AI (The "Creative" Step)
        raw_result = generate_fat_from_spec(spec.raw_text)
        
        # 2. Validate via Rule Engine (The "Safety" Guardrail)
        # This checks for missing High Voltage warnings that the AI might have missed
        validated_result = ComplianceValidator.validate(raw_result)
        
        return validated_result
    except Exception as e:
        # In a real enterprise app, we would log this to Splunk/Datadog
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/generate-pdf")
async def generate_pdf(procedure: FATProcedure):
    """
    Converts a FATProcedure object (JSON) into a downloadable PDF file.
    """
    try:
        # Render the PDF bytes
        pdf_content = render_fat_pdf(procedure)
        
        # Return as a binary stream with correct MIME type
        return Response(
            content=pdf_content,
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename=FAT_{procedure.device_model}.pdf"}
        )
    except Exception as e:
        print(f"PDF Error: {e}") # Log for debugging
        raise HTTPException(status_code=500, detail="Failed to generate PDF document.")