# CertifyFlow: AI-Assisted FAT Procedure Generator

> **An Agentic Document Generation Engine for Automated Engineering Compliance**

[![CertifyFlow Demo](https://img.youtube.com/vi/kNP9shczafM/maxresdefault.jpg)](https://youtu.be/kNP9shczafM)

> 📺 **[Watch the System Demo](https://youtu.be/kNP9shczafM)** featuring Structured JSON Extraction and Deterministic Safety Guardrails.


![Status](https://img.shields.io/badge/Status-Pilot%20Ready-green)
![Coverage](https://img.shields.io/badge/Coverage-100%25-brightgreen)
![Tech](https://img.shields.io/badge/Stack-FastAPI%20%7C%20React%20%7C%20OpenAI-blue)

## The Diagnosis
- **The Problem:** Industrial engineers spend hundreds of hours manually translating Technical Specifications (Datasheets) into Factory Acceptance Test (FAT) procedures.
- **The Trap:** Generic "Chat with PDF" tools produce conversational text that is legally unusable and prone to hallucinating sensor values (e.g., inventing a -50°C threshold for a -40°C sensor).
- **The Solution:** **CertifyFlow**. A Structured Extraction Engine that uses Pydantic to force LLMs into rigid JSON schemas, backed by a deterministic Regex Validator to guarantee safety compliance.

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
- **Styling:** Tailwind CSS (Blue theme).

### 3. Infrastructure
- **Containerization:** Docker Compose (Full stack isolation).
- **Testing:** Pytest (Backend) + Vitest (Frontend) with **100% Code Coverage**.

---

## Architect's Decision Record (ADR)

| Decision | Alternative Considered | Rationale |
| :--- | :--- | :--- |
| **Schema Enforcement** | Pure Prompt Engineering | Prompts fail at scale. `Instructor` patches the LLM to validate output against Python classes *before* returning, guaranteeing valid JSON every time. |
| **PDF Rendering** | Browser/Client-side PDF | Engineering docs require strict pagination (ISO headers on every page). Server-side `WeasyPrint` (CSS Paged Media) is the only robust way to achieve this. |
| **Monorepo** | Multi-repo | Simplified delivery for the Pilot phase. Easier for IT to audit a single Docker Compose file. |

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

## Quick Start

### Prerequisites
* Docker & Docker Compose
* OpenAI API Key

### 1. Installation
```bash
git clone https://github.com/Nibir1/CertifyFlow.git
cd CertifyFlow
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

## Live Demo Scenarios

To verify the system's "Enterprise Readiness," run the following test cases in the UI to see the difference between a Chatbot and an Engineering Tool.

### 1. The Precision Test (Structured Extraction)

**Input:**

> *Technical Spec:* "Vaisala Indigo520 Transmitter. Power Input: 15...35 VDC. Analog Output 1: 4...20 mA. Operating Temperature: -40 to +60°C. Touchscreen display must be responsive."

* **Why this matters:** A generic LLM would write a paragraph. CertifyFlow uses **Instructor (Pydantic)** to force specific atomic steps.
* **Success Indicator:** The system generates a rigid list of steps. It correctly separates *"Apply 15...35 VDC"* as an Instruction and *"Device powers on"* as the Expected Result. The PDF export matches the ISO-standard template.

### 2. The Safety Guardrail (Deterministic Validation)

**Input:**

> *Technical Spec:* "Relay Output: Max load 250 VAC. Connection via screw terminals."
> *(Note: Do not explicitly ask for safety warnings in the input)*

* **Why this matters:** LLMs can "forget" safety context. This tests the **ComplianceValidator** (the regex engine).
* **Success Indicator:** Even if the AI fails to mark this as dangerous, the Backend Validator detects "250 VAC", forces the step to **Safety Critical**, and appends `[AUTO-FLAGGED]` to the instruction. The UI displays a **Red Safety Badge**.

---

## Developer Commands (Makefile)

We utilize a `Makefile` to standardize the development lifecycle across the engineering team.

| Command | Description |
| --- | --- |
| `make build` | Rebuilds all containers from scratch (Backend + Frontend) |
| `make up` | Starts the full system at `http://localhost:5173` |
| `make logs` | Streams live logs from the FastAPI backend and React frontend |
| `make test` | Runs the **100% Coverage** suite (Pytest + Vitest) |
| `make clean` | Nuclear option: Removes containers, volumes, and cache artifacts |

---

## Project Structure

A clean "Monorepo" architecture designed for easy auditing by Vaisala IT.

```text
certifyflow/
├── backend/
│   ├── app/
│   │   ├── core/
│   │   │   ├── generator.py   # AI Logic (Instructor + OpenAI)
│   │   │   └── validator.py   # Compliance Guardrails (Regex)
│   │   ├── models/            # Pydantic Schemas (The "Brain")
│   │   ├── services/          # WeasyPrint PDF Renderer
│   │   └── api/               # FastAPI Routes
│   ├── tests/                 # Pytest Suite (100% Coverage)
│   └── templates/             # Jinja2 Engineering Templates
├── frontend/
│   ├── src/
│   │   ├── components/        # InputForm, ProcedureView
│   │   ├── api/               # Axios Client & Endpoints
│   │   └── types/             # TypeScript Interfaces (Mirroring Pydantic)
│   └── vite.config.ts         # Build Configuration
├── docker-compose.yml         # Container Orchestration
└── Makefile                   # Automation Scripts

```
---
Architected by **Nahasat Nibir**