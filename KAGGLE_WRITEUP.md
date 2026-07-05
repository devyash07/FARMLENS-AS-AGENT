# FarmLens AI

## Multi-Agent Crop Health Intelligence for Sustainable Agriculture

### Kaggle 5-Day AI Agents Capstone
### Track: Agents for Good

---

# Problem Statement

Agriculture remains one of the most critical sectors worldwide, yet many farmers still face challenges in identifying crop diseases at an early stage. Delayed diagnosis often leads to reduced yields, increased treatment costs, and significant economic losses.

Most existing disease detection systems provide only a classification result and do not offer actionable guidance regarding disease severity, environmental risks, or treatment planning.

FarmLens AI aims to bridge this gap by transforming disease detection into an intelligent agricultural decision-support system.

---

# Why Agents?

Crop disease management is a complex problem that involves more than simply identifying a disease.

Farmers require answers to questions such as:

- How severe is the infection?
- How quickly can the disease spread?
- What environmental conditions increase the risk?
- What actions should be taken immediately?
- How should interventions be scheduled?

A Multi-Agent architecture enables specialization, where each agent focuses on a particular task and collaborates to generate meaningful agricultural insights.

---

# Solution Overview

FarmLens AI employs a collaborative Multi-Agent system designed to assist farmers throughout the crop health assessment process.

The system consists of five specialized agents:

### Vision Agent
Responsible for:

- Crop Identification
- Disease Detection
- Heatmap Generation
- Diagnostic Prediction Pipeline

### Severity Agent

Determines infection progression by categorizing disease impact into:

- Healthy
- Mild
- Moderate
- Severe

### Weather Agent

Assesses environmental conditions associated with disease propagation and generates risk assessments.

Outputs include:

- Humidity analysis
- Temperature indicators
- Disease spread likelihood

### Planner Agent

Produces a structured 14-Day Intervention Calendar containing:

- Monitoring schedules
- Treatment recommendations
- Water management guidance
- Sanitation procedures

### Orchestrator Agent

Coordinates execution across all agents and aggregates their outputs into a unified response.

---

# Architecture

```text
Farmer Uploads Crop Image
            │
            ▼
      Vision Agent
            │
            ▼
     Severity Agent
            │
            ▼
      Weather Agent
            │
            ▼
      Planner Agent
            │
            ▼
   Orchestrator Agent
            │
            ▼
     FarmLens Dashboard
```

---

# Technical Implementation

Backend:
- FastAPI
- Python

Frontend:
- React
- TypeScript
- Vite

AI Components:
- Gemini Vision API
- PyTorch
- Heatmap Generation

Security:
- JWT Authentication
- File Type Validation
- Anonymous Access Mode

Supported Formats:

- JPEG
- PNG
- WEBP

---

# Antigravity Usage

Antigravity was used during development to transform an existing crop disease detection platform into an Agentic AI system.

It assisted with:

- Agent architecture planning
- Backend integration
- Orchestrator implementation
- Workflow validation
- Preservation of frontend compatibility

The resulting system evolved from a prediction engine into a collaborative agricultural assistant.

---

# Demonstrated Concepts

This submission demonstrates multiple concepts introduced during the Kaggle 5-Day AI Agents course.

Implemented concepts include:

✅ Multi-Agent Systems

✅ Agent Orchestration

✅ Deployability

✅ Security Features

✅ Agent Skills

✅ Antigravity Workflow

---

# Impact

FarmLens AI seeks to support sustainable agriculture through accessible crop intelligence.

Potential benefits include:

- Reduced crop losses
- Earlier disease intervention
- Increased farmer awareness
- Improved treatment planning
- Enhanced agricultural decision making

---

# Future Work

Planned extensions include:

- Weather API integration
- Region-specific treatment recommendations
- Satellite imagery analysis
- Mobile applications
- Voice-enabled farmer assistance

---

# Conclusion

FarmLens AI demonstrates how Agentic AI systems can move beyond prediction and provide actionable decision support for agriculture.

By combining disease diagnosis, severity assessment, environmental analysis, and intervention planning, FarmLens AI contributes toward a more sustainable and resilient agricultural ecosystem.
