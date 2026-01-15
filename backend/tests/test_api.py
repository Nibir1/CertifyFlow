import pytest
from unittest.mock import patch, Mock
from app.models.schemas import FATProcedure, TestStep

# Shared Mock Data
mock_procedure = FATProcedure(
    project_name="Test Project",
    device_model="TestModel-100",
    standard_reference="ISO-123",
    steps=[
        TestStep(
            step_id="1.1",
            instruction="Turn it on",
            expected_result="It turns on",
            safety_critical=False
        )
    ]
)

def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200

# --- HAPPY PATHS ---

@patch("app.api.routes.generate_fat_from_spec")
def test_generate_procedure(mock_gen, client):
    mock_gen.return_value = mock_procedure
    response = client.post("/api/v1/generate", json={"raw_text": "test"})
    assert response.status_code == 200
    assert response.json()["device_model"] == "TestModel-100"

@patch("app.api.routes.render_fat_pdf") # <--- PATCHING WHERE IT IS USED
def test_generate_pdf(mock_render, client):
    mock_render.return_value = b"%PDF-Fake"
    response = client.post("/api/v1/generate-pdf", json=mock_procedure.model_dump())
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"

# --- SAD PATHS (Error Handling) ---

@patch("app.api.routes.generate_fat_from_spec")
def test_generate_procedure_error(mock_gen, client):
    """Simulate a crash in the AI engine to test the 500 handler"""
    mock_gen.side_effect = Exception("AI Overload")
    response = client.post("/api/v1/generate", json={"raw_text": "crash me"})
    assert response.status_code == 500
    assert "AI Overload" in response.json()["detail"]

@patch("app.api.routes.render_fat_pdf") # <--- PATCHING WHERE IT IS USED
def test_generate_pdf_error(mock_render, client):
    """Simulate a crash in PDF rendering to test the 500 handler"""
    mock_render.side_effect = Exception("Font missing")
    response = client.post("/api/v1/generate-pdf", json=mock_procedure.model_dump())
    
    # Now this assertion will pass because the mock is correctly wired
    assert response.status_code == 500
    assert "Failed to generate PDF" in response.json()["detail"]