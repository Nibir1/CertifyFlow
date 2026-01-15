# CertifyFlow: AI-Assisted FAT Procedure Generator


![Status](https://img.shields.io/badge/Status-Pilot%20Ready-green)
![Coverage](https://img.shields.io/badge/Coverage-100%25-brightgreen)
![Tech](https://img.shields.io/badge/Stack-FastAPI%20%7C%20React%20%7C%20OpenAI-blue)

## The Diagnosis
**The Problem:** Vaisala engineers spend hundreds of hours manually translating Technical Specifications (Datasheets) into Factory Acceptance Test (FAT) procedures.
**The Trap:** Generic "Chat with PDF" tools produce conversational text that is legally unusable and prone to hallucinating sensor values (e.g., inventing a -50°C threshold for a -40°C sensor).
**The Solution:** **CertifyFlow**. A Structured Extraction Engine that uses Pydantic to force LLMs into rigid JSON schemas, backed by a deterministic Regex Validator to guarantee safety compliance.

---

## Architecture & Tech Stack

### 1. The Intelligence Layer (Backend)
- **Engine:** Python 3.11 + FastAPI
- **Orchestration:** `Instructor` + `OpenAI` (Forces JSON output, prevents "Chatty" responses).
- **Guardrails:** `ComplianceValidator` (Regex-based logic that auto-flags High Voltage steps if the AI misses them).
- **Artifacts:** `WeasyPrint` + `Jinja2` (Renders strictly formatted PDF reports).

### 2. The Interface Layer (Frontend)
- **Framework:** React 18 + TypeScript + Vite
- **State:** TanStack Query (Server state management).
- **Styling:** Tailwind CSS (Vaisala Blue theme).

### 3. Infrastructure
- **Containerization:** Docker Compose (Full stack isolation).
- **Testing:** Pytest (Backend) + Vitest (Frontend) with **100% Code Coverage**.

---

## Architect's Decision Record (ADR)

| Decision | Alternative Considered | Rationale |
| :--- | :--- | :--- |
| **Schema Enforcement** | Pure Prompt Engineering | Prompts fail at scale. `Instructor` patches the LLM to validate output against Python classes *before* returning, guaranteeing valid JSON every time. |
| **PDF Rendering** | Browser/Client-side PDF | Engineering docs require strict pagination (ISO headers on every page). Server-side `WeasyPrint` (CSS Paged Media) is the only robust way to achieve this. |
| **Monorepo** | Multi-repo | Simplified delivery for the Pilot phase. Easier for Vaisala IT to audit a single Docker Compose file. |

---

## FinOps: Cost Estimation

**Model:** GPT-3.5-Turbo (0125)
* **Average Input (Spec):** 500 Tokens ($0.00025)
* **Average Output (Procedure):** 300 Tokens ($0.00045)
* **Total Cost per Document:** **$0.0007 (less than 1/10th of a cent)**

*Comparison: Engineer time (1 hour) vs. CertifyFlow (5 seconds).*

---

## Safety & Compliance
**The "Hallucination" Guardrail:**
We do not trust the LLM blindly. The `ComplianceValidator` runs post-generation:
1.  **Regex Scan:** Scans for "VAC", "230V", "High Voltage".
2.  **Logic Check:** If found, checks `safety_critical` boolean.
3.  **Override:** If the AI marked it `False`, the code forces it to `True` and appends `[AUTO-FLAGGED]`.

---

## ⚡ Quick Start

### Prerequisites
* Docker & Docker Compose
* OpenAI API Key

### 1. Installation
```bash
git clone https://github.com/Nibir1/CertifyFlow.git
cd certifyflow
# Create .env file in backend/
echo "OPENAI_API_KEY=sk-..." > backend/.env

```

### 2. Run the Pilot

```bash
make build
# App will be live at http://localhost:5173

```

### 3. Run Tests (100% Verification)

```bash
make test

```