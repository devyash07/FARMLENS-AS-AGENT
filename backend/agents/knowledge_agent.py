import os
from agents.base_agent import BaseAgent

KNOWLEDGE_SYSTEM_PROMPT = """You are the Knowledge Agent of FarmLens. Your task is to retrieve detailed, expert-level agricultural treatments and safety regulations for plant diseases. For any given disease, you must provide:
1. Chemical Treatments (fungicides, bactericides, or pesticides with application rates).
2. Organic/Biological Controls (neem oil, copper soaps, beneficial microbes).
3. Cultural Prevention (spacing, pruning, drainage, crop rotation).
4. Safety & Environmental Warnings (pollinator protection, pre-harvest intervals)."""

LOCAL_DB = {
    "tomato___late_blight": {
        "chemical": "Apply copper-based fungicides or Chlorothalonil at 7-10 day intervals. Use systemic options like Metalaxyl under high disease pressure.",
        "organic": "Use Bacillus subtilis sprays (e.g., Serenade) or organic copper octanoate soaps. Prune lower foliage to keep leaves dry.",
        "cultural": "Destroy volunteer potato/tomato plants. Avoid overhead watering. Maintain 60-90cm plant spacing for high airflow.",
        "safety": "Copper products can be toxic to aquatic life; avoid runoff. Respect the 1-day pre-harvest interval (PHI) for fruit picking."
    },
    "corn_(maize)___common_rust_": {
        "chemical": "Foliar fungicides like Pyraclostrobin or Tebuconazole if pustules appear on more than 10% of leaves before silking.",
        "organic": "Apply sulfur dusts or potassium bicarbonate sprays early in the morning when wind is low.",
        "cultural": "Plant rust-resistant hybrids. Till under infected residue in fall to reduce overwintering spores.",
        "safety": "Ensure proper protective equipment (PPE) is worn during fungicide spraying. Protect local water runoffs."
    },
    "apple___apple_scab": {
        "chemical": "Use protectant fungicides (Mancozeb, Captan) from green tip stage through petal fall. Use Myclobutanil for curative action.",
        "organic": "Apply liquid lime-sulfur or copper sprays during dormant season. Use compost tea to boost foliage health.",
        "cultural": "Rake and destroy fallen leaves in autumn. Prune the canopy to allow rapid drying of leaves and fruit.",
        "safety": "Fungicides Captan and Mancozeb are highly toxic to fish. Do not apply near honeybee foraging hours."
    }
}

class KnowledgeAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="KnowledgeAgent", system_prompt=KNOWLEDGE_SYSTEM_PROMPT)

    async def run(self, context: dict) -> dict:
        """Retrieves treatments and regulations based on target crop and disease classification."""
        vision_report = context.get("vision_report", {})
        crop = vision_report.get("crop", "Unknown")
        disease = vision_report.get("disease", "Unknown")
        language = context.get("language", "en")
        
        is_healthy = (disease == "Healthy" or disease == "healthy")
        if is_healthy:
            return {
                "chemical": "None needed.",
                "organic": "Standard compost and nutrient supplements.",
                "cultural": "Regular crop monitoring and balanced irrigation.",
                "safety": "Keep tools clean between operations."
            }

        # Lookup in local DB
        db_key = f"{crop.lower()}___{disease.lower()}".replace(" ", "_").replace(",", "").replace("(", "").replace(")", "")
        entry = None
        for key, val in LOCAL_DB.items():
            if db_key in key or key in db_key:
                entry = val
                break
                
        if entry:
            chemical = entry["chemical"]
            organic = entry["organic"]
            cultural = entry["cultural"]
            safety = entry["safety"]
        else:
            # Query Gemini to dynamically construct expert knowledge
            try:
                prompt = f"Retrieve expert agricultural recommendations for Crop: {crop}, Disease: {disease}."
                if language != "en":
                    prompt += f" Respond in {language}."
                
                text = self.generate_with_system_instruction(
                    prompt=f"{prompt}\nProvide responses formatted exactly as: \nChemical: <chemical>\nOrganic: <organic>\nCultural: <cultural>\nSafety: <safety>"
                )
                
                # Parse output
                chemical, organic, cultural, safety = "Consult expert", "Consult organic extension", "Maintain good crop hygiene", "Follow label rules"
                lines = text.split("\n")
                for line in lines:
                    if line.lower().startswith("chemical:"):
                        chemical = line.split(":", 1)[1].strip()
                    elif line.lower().startswith("organic:"):
                        organic = line.split(":", 1)[1].strip()
                    elif line.lower().startswith("cultural:"):
                        cultural = line.split(":", 1)[1].strip()
                    elif line.lower().startswith("safety:"):
                        safety = line.split(":", 1)[1].strip()
            except Exception as e:
                print(f"[KnowledgeAgent] LLM retrieval failed: {e}")
                chemical = f"Apply labeled fungicides specific for {disease} on {crop}."
                organic = "Apply neem oil (70% concentration) or organic copper octanoate soaps."
                cultural = "Avoid overhead irrigation, prune infected leaves, and maximize plant spacing."
                safety = "Always wear protective gear and avoid spraying near water bodies."

        return {
            "chemical": chemical,
            "organic": organic,
            "cultural": cultural,
            "safety": safety
        }
