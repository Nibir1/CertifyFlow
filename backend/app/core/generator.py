"""
AI Generator Logic
------------------
Handles the interaction with OpenAI via the Instructor library to enforce
structured output generation.
"""

import os
import instructor
from openai import OpenAI
from app.models.schemas import FATProcedure

# Initialize the OpenAI client and patch it with Instructor
# This adds the `response_model` capability to the client
client = instructor.patch(OpenAI(api_key=os.environ.get("OPENAI_API_KEY")))

def generate_fat_from_spec(spec_text: str) -> FATProcedure:
    """
    Accepts raw technical specification text and returns a structured FATProcedure object.
    
    Args:
        spec_text (str): The raw text from the datasheet or engineering spec.
        
    Returns:
        FATProcedure: A validated Pydantic object containing the test steps.
    """
    
    system_prompt = """
    You are a Senior QA Automation Engineer at Vaisala. 
    Your job is to read technical specifications for industrial weather instruments 
    and generate a rigorous Factory Acceptance Test (FAT) procedure.
    
    RULES:
    1. Be specific. Do not say "Check the sensor." Say "Verify sensor output is within 0.5% accuracy."
    2. Identify Safety Critical steps (High Voltage, Lasers, Heat).
    3. Structure the output strictly according to the schema provided.
    4. If a specific value (e.g., "24V") is in the text, use it. Do not hallucinate numbers.
    """

    # The 'response_model' parameter is where Instructor works its magic.
    # It forces the LLM to output JSON that strictly matches our Pydantic class.
    procedure = client.chat.completions.create(
        model="gpt-3.5-turbo", # Can swap for gpt-4-turbo for higher precision
        response_model=FATProcedure,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Create a FAT Procedure for this spec: {spec_text}"}
        ],
        temperature=0.1, # Low temperature for deterministic, factual outputs
    )
    
    return procedure