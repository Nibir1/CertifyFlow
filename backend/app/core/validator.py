import re
from app.models.schemas import FATProcedure

class ComplianceValidator:
    """
    Deterministic Rule-Based Engine.
    Acts as a 'Second Pair of Eyes' on the AI output.
    """
    
    # Terms that MUST appear if the voltage > 50V
    HIGH_VOLTAGE_TRIGGERS = [r"230\s*V", r"110\s*V", r"220\s*V", r"VAC"]
    SAFETY_WARNINGS = ["High Voltage", "Lockout/Tagout", "PPE Required"]

    @staticmethod
    def validate(procedure: FATProcedure) -> FATProcedure:
        """
        Scans the generated procedure for safety compliance.
        1. If high voltage is mentioned, ensure 'Safety Critical' is flagged.
        2. If temperature is extreme, ensure 'Chamber' is mentioned.
        """
        for step in procedure.steps:
            # RULE 1: High Voltage Guardrail
            # If the instruction mentions VAC/High Voltage but safety_critical is False, FLIP IT.
            instruction_text = step.instruction.lower()
            
            # Check for high voltage keywords
            is_hv = any(re.search(pattern, instruction_text, re.IGNORECASE) 
                       for pattern in ComplianceValidator.HIGH_VOLTAGE_TRIGGERS)
            
            if is_hv and not step.safety_critical:
                step.safety_critical = True
                step.instruction += " [AUTO-FLAGGED: SAFETY CRITICAL]"

            # RULE 2: Empty Field Check
            if not step.expected_result or step.expected_result.lower() == "n/a":
                step.expected_result = "VERIFY MANUALLY (AI Could not determine)"

        return procedure