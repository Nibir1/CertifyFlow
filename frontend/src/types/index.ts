/**
 * Global Type Definitions
 * -----------------------
 * These interfaces mirror the Pydantic models defined in the Backend.
 * They ensure type safety for API responses.
 */

export interface TestStep {
    step_id: string;
    instruction: string;
    expected_result: string;
    safety_critical: boolean;
}

export interface FATProcedure {
    project_name: string;
    device_model: string;
    standard_reference: string | null;
    steps: TestStep[];
}

// Request payload for the generation endpoint
export interface TechSpecPayload {
    raw_text: string;
}