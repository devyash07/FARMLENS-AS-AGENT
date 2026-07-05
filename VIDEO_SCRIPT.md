t# FarmLens AI Video Script

## Duration: 5 Minutes

---

# 0:00 – 0:30 | Introduction

Hello everyone.

This is FarmLens AI, a Multi-Agent Crop Health Intelligence platform developed as part of the Kaggle 5-Day AI Agents Capstone under the Agents for Good track.

FarmLens AI helps farmers detect crop diseases, assess infection severity, understand environmental risks, and receive actionable intervention plans for sustainable agriculture.

---

# 0:30 – 1:15 | Problem Statement

Agriculture is one of the most important sectors globally, yet farmers still face significant challenges in identifying crop diseases at an early stage.

Most existing disease detection systems only provide a disease label and confidence score.

However, farmers also need answers to questions such as:

- How severe is the infection?
- How quickly can the disease spread?
- What environmental factors increase the risk?
- What actions should be taken immediately?
- How should treatment be planned?

FarmLens AI aims to bridge this gap by transforming disease prediction into an intelligent agricultural decision-support system.

---

# 1:15 – 2:00 | Why Agents?

Crop disease management is not a single-task problem.

It requires multiple specialized processes working together.

Therefore, FarmLens AI was redesigned as a Multi-Agent System.

Each agent focuses on a dedicated responsibility.

Vision Agent:
Responsible for crop identification and disease detection.

Severity Agent:
Evaluates infection progression and categorizes disease severity.

Weather Agent:
Assesses environmental conditions and estimates disease spread risk.

Planner Agent:
Creates a structured fourteen-day intervention plan.

Orchestrator Agent:
Coordinates all agents and combines their outputs into a unified response.

This architecture enables FarmLens AI to provide actionable insights instead of simple predictions.

---

# 2:00 – 2:45 | Architecture

The workflow begins when a farmer uploads a crop image.

The image is processed by the Vision Agent.

The Severity Agent then evaluates infection intensity.

The Weather Agent estimates environmental risk factors.

The Planner Agent generates a fourteen-day crop care strategy.

Finally, the Orchestrator Agent aggregates all results and presents them through the FarmLens dashboard.

Display Architecture Diagram Here

Farmer Upload
↓

Vision Agent
↓

Severity Agent
↓

Weather Agent
↓

Planner Agent
↓

Orchestrator Agent
↓

FarmLens Dashboard

---

# 2:45 – 4:00 | Live Demo

Now let's look at FarmLens AI in action.

Upload a crop image.

The Vision Agent identifies the crop and disease.

A heatmap is generated to explain the model's focus regions.

The Severity Agent estimates infection stage.

The Weather Agent evaluates potential disease propagation risks.

The Planner Agent creates a structured fourteen-day intervention timeline.

The farmer receives:

- Disease Identification
- Confidence Score
- Severity Assessment
- Environmental Risk Analysis
- Treatment Recommendations
- Fourteen-Day Intervention Calendar

This provides practical agricultural guidance rather than just prediction outputs.

---

# 4:00 – 4:30 | Antigravity Usage

Antigravity was used during development to transform an existing disease detection platform into an Agentic AI system.

It assisted in:

- Multi-agent architecture planning
- Agent orchestration
- Backend integration
- Workflow validation
- Competition-oriented development

FarmLens evolved from a prediction engine into a collaborative agricultural assistant.

---

# 4:30 – 5:00 | Impact and Future Work

FarmLens AI belongs to the Agents for Good track because it addresses real-world agricultural challenges.

Potential impact includes:

- Reduced crop losses
- Early disease intervention
- Improved farmer decision making
- Better treatment planning
- Sustainable agricultural practices

Future improvements include:

- Weather API integration
- Satellite imagery analysis
- Regional treatment databases
- Mobile applications
- Voice assistance for farmers

Thank you for watching.

FarmLens AI demonstrates how Agentic AI can move beyond prediction and provide meaningful support for sustainable agriculture.
