"""
Pydantic Schemas (Data Models)
------------------------------
Defines the strict structure for Input (Technical Specs) and Output (FAT Procedures).
These models are used by Instructor to guide the LLM's generation.
"""

from pydantic import BaseModel, Field
from typing import List, Optional

class TechSpec(BaseModel):
    """
    The raw input data representing a Vaisala Weather Sensor specification.
    """
    raw_text: str = Field(
        ..., 
        description="The full raw text of the technical specification or datasheet."
    )

class TestStep(BaseModel):
    """
    A single atomic step in a Factory Acceptance Test (FAT).
    """
    step_id: str = Field(
        ..., 
        description="Sequential ID (e.g., '1.1', '1.2')."
    )
    instruction: str = Field(
        ..., 
        description="Clear, imperative action for the technician (e.g., 'Apply 24V DC power')."
    )
    expected_result: str = Field(
        ..., 
        description="The precise expected outcome or observable reading (e.g., 'LED turns Green', 'Output reads 4-20mA')."
    )
    safety_critical: bool = Field(
        default=False, 
        description="True if this step involves high voltage, extreme temperatures, or hazardous materials."
    )

class FATProcedure(BaseModel):
    """
    The complete structured Factory Acceptance Test document.
    """
    project_name: str = Field(
        ..., 
        description="Name of the project or customer derived from context (or 'Generic' if unknown)."
    )
    device_model: str = Field(
        ..., 
        description="The specific Vaisala model number being tested (e.g., 'WXT530', 'HMP155')."
    )
    standard_reference: Optional[str] = Field(
        None, 
        description="ISO or IEC standards mentioned in the text."
    )
    steps: List[TestStep] = Field(
        ..., 
        description="A chronological list of validation steps extracted from the specs."
    )