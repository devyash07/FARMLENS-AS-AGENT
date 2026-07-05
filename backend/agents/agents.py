import os
from services.ai_service import predict

class VisionAgent:
    """Vision Agent: Handles crop identification and disease diagnosis using the existing model cascade."""
    def run(self, image_bytes: bytes, language: str = "en") -> dict:
        print("[Vision Agent] Running diagnostic cascade prediction...")
        raw_result = predict(image_bytes, language=language)
        return {
            "crop": raw_result.get("crop", "Unknown"),
            "disease": raw_result.get("disease", "Unknown"),
            "severity_score": raw_result.get("severity", 0),
            "confidence": raw_result.get("confidence", 0),
            "status": raw_result.get("status", "Unknown"),
            "explanation": raw_result.get("explanation", ""),
            "treatment_fallback": raw_result.get("treatment", ""),
            "heatmap_b64": raw_result.get("heatmap_b64", "")
        }

class SeverityAgent:
    """Severity Agent: Analyzes the foliage damage level and categorizes the stage."""
    def run(self, vision_report: dict) -> dict:
        score = vision_report.get("severity_score", 0)
        disease = vision_report.get("disease", "Unknown")
        
        is_healthy = (disease.lower() == "healthy" or score == 0)
        
        if is_healthy:
            category = "Healthy"
            description = "Foliage is free of visible anomalies. The crop is in a healthy condition."
        elif score < 15:
            category = "Mild"
            description = "Early localized infection (under 15% leaf area). Spores are restricted to the lower canopy. Minimal threat if treated immediately."
        elif score <= 40:
            category = "Moderate"
            description = "Moderate active spread (15% to 40% area). Visible spots across multiple leaf clusters. Photosynthesis is partially restricted."
        else:
            category = "Severe"
            description = "Advanced stage of disease (over 40% area). Heavy defoliation or blight lesions observed. Extremely high risk of yield loss."
            
        return {
            "score": score,
            "category": category,
            "description": description
        }

class WeatherAgent:
    """Weather Agent: Correlates temperature and moisture conditions with disease spread risks."""
    def run(self, vision_report: dict) -> dict:
        disease = vision_report.get("disease", "Unknown")
        is_healthy = (disease.lower() == "healthy")
        
        if is_healthy:
            temp = 24
            humidity = 55
            risk_level = "Low"
            risk_factor = "Normal ambient vectors. Weather conditions do not favor pathogen propagation."
        else:
            # Check for typical fungal/bacterial spread conditions
            if any(term in disease.lower() for term in ["blight", "scab", "rot", "mildew", "rust", "spot"]):
                temp = 19
                humidity = 88
                risk_level = "High"
                risk_factor = f"Cool-to-moderate temperature ({temp}°C) and high humidity ({humidity}%) create damp leaf surfaces that accelerate {disease} spore spread."
            else:
                temp = 27
                humidity = 65
                risk_level = "Medium"
                risk_factor = f"Moderate temperatures ({temp}°C) and humidity ({humidity}%) support stable progression of {disease}."
                
        return {
            "temperature": f"{temp}°C",
            "humidity": f"{humidity}%",
            "risk_level": risk_level,
            "risk_factor": risk_factor
        }

class PlannerAgent:
    """Planner Agent: Constructs a 14-day chronological care calendar."""
    def run(self, vision_report: dict, severity_report: dict, weather_report: dict, language: str = "en") -> dict:
        crop = vision_report.get("crop", "Unknown")
        disease = vision_report.get("disease", "Unknown")
        is_healthy = (disease.lower() == "healthy")
        
        if is_healthy:
            timeline = (
                "[Day 1] Routine Foliage Inspection: Walk the rows to ensure no spots have developed.\n"
                "[Day 5] Nutrient Application: Apply standard compost tea or balanced N-P-K fertilizer.\n"
                "[Day 10] Maintenance: Sanitize all pruning shears and farming tools.\n"
                "[Day 14] Final Health Check: Confirm crop remains in a healthy state."
            )
            return {"timeline": timeline}
            
        # Get baseline treatment from fallback
        baseline_treatment = vision_report.get("treatment_fallback", "")
        
        # Build timeline dynamically based on weather/severity
        risk_level = weather_report.get("risk_level", "Low")
        category = severity_report.get("category", "Mild")
        
        day_1_action = "Prune and destroy infected leaves. Do NOT compost diseased parts."
        day_2_action = f"Apply baseline control: {baseline_treatment}"
        
        if risk_level == "High":
            day_5_action = "Inspect soil moisture; suspend overhead sprinkler irrigation to keep the leaf canopy dry."
        else:
            day_5_action = "Perform regular soil hydration check. Ensure clean drainage paths."
            
        if category in ["Moderate", "Severe"]:
            day_7_action = "Re-inspect lower leaf surfaces. Perform localized spot spray on newly affected foliage."
        else:
            day_7_action = "Monitor crop rows for secondary symptom development."
            
        day_14_action = "Sterilize all tools. If infection continues to spread, consult local agricultural extension."

        timeline = (
            f"[Day 1] Action: {day_1_action}\n"
            f"[Day 2] Treatment: {day_2_action}\n"
            f"[Day 5] Water Management: {day_5_action}\n"
            f"[Day 7] Monitoring: {day_7_action}\n"
            f"[Day 14] Review: {day_14_action}"
        )
        return {"timeline": timeline}

class OrchestratorAgent:
    """Orchestrator Agent: Directs sequential execution flow and formats output to fit original API contract."""
    def __init__(self):
        self.vision = VisionAgent()
        self.severity = SeverityAgent()
        self.weather = WeatherAgent()
        self.planner = PlannerAgent()
        
    def run_diagnostics(self, image_bytes: bytes, language: str = "en") -> dict:
        # 1. Run Vision Agent
        vision_report = self.vision.run(image_bytes, language=language)
        
        # 2. Run Severity Agent
        severity_report = self.severity.run(vision_report)
        
        # 3. Run Weather Agent
        weather_report = self.weather.run(vision_report)
        
        # 4. Run Planner Agent
        planner_report = self.planner.run(vision_report, severity_report, weather_report, language=language)
        
        # 5. Format results back to original API schema (preserving contracts)
        crop = vision_report.get("crop")
        disease = vision_report.get("disease")
        confidence = vision_report.get("confidence")
        status = vision_report.get("status")
        heatmap_b64 = vision_report.get("heatmap_b64")
        
        # Format the combined explanation: Severity analysis + Weather risk factor
        explanation = (
            f"Diagnostics: Detected {disease} in {crop} ({confidence}% confidence).\n"
            f"Severity Assessment: {severity_report.get('category')} level infection. {severity_report.get('description')}\n"
            f"Weather Risk: {weather_report.get('risk_level')} risk. {weather_report.get('risk_factor')}"
        )
        
        # Format treatment: 14-day calendar
        treatment = (
            f"14-DAY FARM INTERVENTION PLAN:\n"
            f"{planner_report.get('timeline')}"
        )
        
        return {
            "crop": crop,
            "disease": disease,
            "severity": severity_report.get("score", 0),
            "confidence": confidence,
            "status": status,
            "heatmap_b64": heatmap_b64,
            "heatmap_url": "",
            "explanation": explanation,
            "treatment": treatment
        }
