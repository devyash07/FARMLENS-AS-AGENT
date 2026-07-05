# 🌾 FarmLens AI
## Multi-Agent Crop Health Intelligence for Sustainable Agriculture

<div align="center">

### Kaggle 5-Day AI Agents Capstone Project
### Agents for Good Track

Empowering farmers through Agentic AI for disease diagnosis, risk assessment and intervention planning.

</div>

---

# Problem Statement

Farmers often struggle to identify crop diseases early and determine effective intervention strategies.

Most disease detection systems only provide predictions and leave users without:

- Disease severity assessment
- Environmental risk analysis
- Structured treatment planning
- Actionable intervention timelines

FarmLens AI addresses this challenge through a collaborative Multi-Agent AI architecture.

---

# Solution

FarmLens AI transforms crop disease diagnosis into an intelligent decision-support system.

The platform combines specialized agents that work together to generate comprehensive agricultural insights.

The system provides:

- Crop Identification
- Disease Detection
- Heatmap Visualization
- Severity Assessment
- Environmental Risk Evaluation
- 14-Day Intervention Planning
- Treatment Recommendations

---

# 🤖 Multi-Agent Architecture

```text
Farmer Uploads Crop Image
            │
            ▼
      Vision Agent
(Crop & Disease Detection)
            │
            ▼
     Severity Agent
(Infection Assessment)
            │
            ▼
      Weather Agent
(Environmental Risk Analysis)
            │
            ▼
      Planner Agent
(14-Day Intervention Plan)
            │
            ▼
   Orchestrator Agent
(Response Aggregation)
            │
            ▼
      FarmLens Dashboard
```

---

# Agents

## Vision Agent

Responsible for:

- Crop Identification
- Disease Detection
- Diagnostic Pipeline
- Heatmap Generation

Uses the existing FarmLens prediction cascade.

---

## Severity Agent

Analyzes infection progression.

Categories:

- Healthy
- Mild
- Moderate
- Severe

Provides contextual explanations for farmers.

---

## Weather Agent

Estimates disease spread risk based on environmental conditions.

Produces:

- Temperature indicators
- Humidity estimates
- Disease propagation risks

Risk levels:

- Low
- Medium
- High

---

## Planner Agent

Generates a structured 14-Day Crop Care Plan.

Examples:

- Monitoring schedules
- Water management
- Follow-up inspections
- Treatment recommendations
- Sanitation procedures

---

## Orchestrator Agent

Coordinates all FarmLens agents.

Workflow:

```text
Vision
↓

Severity
↓

Weather
↓

Planner
```

Combines outputs while preserving compatibility with the original FarmLens API schema.

---

# Features

- Multi-Agent Architecture
- Crop Classification
- Disease Detection
- Explainable AI
- Heatmap Visualization
- Severity Analysis
- Environmental Risk Assessment
- 14-Day Intervention Planning
- Treatment Recommendations
- Multilingual Support
- Agricultural Chatbot

---

# Technology Stack

## Backend

- FastAPI
- Python
- Gemini Vision API
- PyTorch
- Supabase
- JWT Authentication

## Frontend

- React
- TypeScript
- Vite
- TailwindCSS
- shadcn/ui

---

# Security Features

FarmLens AI includes:

- JWT Authentication
- Anonymous Access Mode
- Input Validation
- Allowed File Type Verification
- Environment Variable Protection

Supported image formats:

```text
image/jpeg
image/png
image/webp
```

---

# Deployability

Backend

```bash
uvicorn main:app --reload
```

Frontend

```bash
npm install
npm run dev
```

Open:

```text
http://localhost:8080
```

---

# Running Locally

Backend

```bash
cd backend

source venv312/bin/activate

uvicorn main:app --reload
```

Frontend

```bash
npm install

npm run dev
```

---

# Competition Alignment

Kaggle 5-Day AI Agents Intensive Course

Track:

## Agents for Good

FarmLens AI supports sustainable agriculture by helping farmers reduce crop losses through intelligent diagnosis and intervention planning.

Demonstrated Concepts:

✅ Multi-Agent Systems

✅ Agent Orchestration

✅ Antigravity Workflow

✅ Deployability

✅ Security Features

✅ Agent Skills

---

# Project Impact

FarmLens AI aims to:

- Reduce crop losses
- Improve farmer decision making
- Support sustainable agriculture
- Increase accessibility to agricultural expertise
- Deliver actionable insights rather than predictions alone

---

# Future Work

Potential enhancements include:

- Real Weather API Integration
- Satellite Image Support
- Region-specific Treatment Knowledge
- Mobile Applications
- Voice Assistance for Farmers
- IoT Integration

---

# Authors

FarmLens AI

Kaggle 5-Day AI Agents Capstone

Agents for Good Track

2026

---

Made with ❤️ for farmers worldwide.