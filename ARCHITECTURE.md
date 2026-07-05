# FarmLens AI Architecture

## Multi-Agent System Overview

```text
                    FarmLens AI

            Farmer Uploads Crop Image
                        │
                        ▼

              ┌──────────────────┐
              │   Vision Agent   │
              │ Disease Detection│
              │ Heatmap Creation │
              └──────────────────┘
                        │

        ┌───────────────┼───────────────┐
        ▼                               ▼

┌──────────────────┐        ┌──────────────────┐
│ Severity Agent   │        │ Weather Agent    │
│ Infection Stage  │        │ Risk Assessment  │
│ Healthy–Severe   │        │ Humidity Analysis│
└──────────────────┘        └──────────────────┘
        │                               │
        └───────────────┬───────────────┘
                        ▼

              ┌──────────────────┐
              │ Planner Agent    │
              │ 14-Day Strategy  │
              │ Treatment Plan   │
              └──────────────────┘
                        │
                        ▼

              ┌──────────────────┐
              │ Orchestrator     │
              │ Aggregation      │
              │ Response Builder │
              └──────────────────┘
                        │
                        ▼

              ┌──────────────────┐
              │ FarmLens UI      │
              │ Dashboard        │
              └──────────────────┘
```

---

## Agent Responsibilities

### Vision Agent
- Crop Identification
- Disease Detection
- Heatmap Generation
- Diagnostic Prediction Pipeline

### Severity Agent
- Infection Categorization
- Healthy
- Mild
- Moderate
- Severe

### Weather Agent
- Environmental Analysis
- Disease Propagation Risk
- Humidity Assessment

### Planner Agent
- Intervention Scheduling
- Treatment Recommendations
- Monitoring Suggestions
- Crop Care Planning

### Orchestrator Agent
Coordinates all FarmLens agents and produces a unified response for the frontend.

---

## Competition Alignment

Track:
**Agents for Good**

Concepts Demonstrated:

✅ Multi-Agent Systems

✅ Agent Orchestration

✅ Antigravity Workflow

✅ Security Features

✅ Deployability

✅ Agent Skills