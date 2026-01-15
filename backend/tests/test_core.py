import pytest
from unittest.mock import patch, MagicMock
from app.core.generator import generate_fat_from_spec
from app.services.pdf_renderer import render_fat_pdf
from app.models.schemas import FATProcedure, TestStep

mock_data = FATProcedure(
    project_name="Unit Test",
    device_model="Unit-1",
    standard_reference=None,
    steps=[TestStep(step_id="1", instruction="Do", expected_result="Done", safety_critical=True)]
)

# Test the AI Generator Logic
@patch("app.core.generator.client.chat.completions.create")
def test_core_generator(mock_openai):
    # Mock the complicated OpenAI response structure
    mock_openai.return_value = mock_data
    
    result = generate_fat_from_spec("some text")
    
    assert result.project_name == "Unit Test"
    assert result.steps[0].safety_critical is True
    mock_openai.assert_called_once()

# Test the PDF Renderer Logic
def test_pdf_renderer_logic():
    # We allow WeasyPrint to actually run (it's fast enough for unit tests usually),
    # OR we can mock the HTML class if we don't want to rely on libs.
    # Let's run it for real to prove the template works.
    
    pdf_bytes = render_fat_pdf(mock_data)
    
    # PDF files start with %PDF-
    assert pdf_bytes.startswith(b"%PDF-")
    assert len(pdf_bytes) > 0