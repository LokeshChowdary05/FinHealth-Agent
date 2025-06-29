import os
import requests
from dotenv import load_dotenv
import json

load_dotenv()

class MedicalAnalyzer:
    def __init__(self):
        self.together_api_key = os.getenv('TOGETHER_API_KEY')
        self.api_url = "https://api.together.xyz/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {self.together_api_key}",
            "Content-Type": "application/json"
        }
        
        # Load medical conditions data
        self.medical_conditions = self._load_data()
        
        # Common medical procedures mapped to conditions
        self.procedure_mapping = {
            "chest pain": ["ECG", "Chest X-ray", "Blood tests", "Stress test"],
            "headache": ["CT scan", "MRI", "Blood tests", "Physical examination"],
            "abdominal pain": ["Ultrasound", "CT scan", "Blood tests", "Physical examination"],
            "back pain": ["X-ray", "MRI", "Physical examination"],
            "fever": ["Blood tests", "Chest X-ray", "Physical examination"],
            "shortness of breath": ["Chest X-ray", "ECG", "Blood tests"],
            "joint pain": ["X-ray", "MRI", "Blood tests", "Physical examination"],
            "skin rash": ["Physical examination", "Blood tests"]
        }

    def analyze_symptoms(self, symptoms):
        """Analyze symptoms using AI to predict medical condition"""
        if not self.together_api_key or self.together_api_key == "your_together_ai_api_key_here":
            # Fallback to rule-based analysis
            return self._fallback_analysis(symptoms)
        
        try:
            context = """You are a medical assistant. Based on the symptoms described, provide the most likely medical condition in 1-3 words. Be conservative and suggest seeing a healthcare professional. Only provide the condition name, no additional explanation."""
            
            payload = {
                "model": "meta-llama/Llama-2-70b-chat-hf",
                "messages": [
                    {"role": "system", "content": context},
                    {"role": "user", "content": f"Symptoms: {symptoms}"}
                ],
                "temperature": 0.1,
                "top_p": 0.7,
                "max_tokens": 50
            }
            
            response = requests.post(self.api_url, headers=self.headers, json=payload)
            
            if response.status_code == 200:
                result = response.json()
                condition = result['choices'][0]['message']['content'].strip()
                return condition
            else:
                return self._fallback_analysis(symptoms)
                
        except Exception as e:
            print(f"AI analysis failed: {e}")
            return self._fallback_analysis(symptoms)
    
    def _fallback_analysis(self, symptoms):
        """Fallback rule-based symptom analysis"""
        symptoms_lower = symptoms.lower()

        if 'chest pain' in symptoms_lower:
            return "chest pain"
        elif 'headache' in symptoms_lower:
            return "headache"
        elif 'abdominal pain' in symptoms_lower:
            return "abdominal pain"
        elif 'back pain' in symptoms_lower:
            return "back pain"
        elif 'fever' in symptoms_lower:
            return "fever"
        else:
            return "general consultation needed"
            
    def get_recommended_procedures(self, condition):
        """Get recommended medical procedures for a condition based on data."""
        # First try to get from the loaded data
        if condition.lower() in self.medical_conditions:
            return self.medical_conditions[condition.lower()].get('common_procedures', [])
        
        # Fallback to hardcoded mapping
        return self.procedure_mapping.get(condition.lower(), [])

    def _load_data(self):
        """Load medical data from JSON file"""
        try:
            data_file = os.path.join('data', 'hospital_pricing_data.json')
            if os.path.exists(data_file):
                with open(data_file, 'r') as f:
                    data = json.load(f)
                    return data.get('medical_conditions', {})
            else:
                return {}
        except Exception as e:
            print(f"Error loading data: {e}")
            return {}

    def analyze_symptoms_using_data(self, symptoms):
        """Use dataset to analyze symptoms and suggest procedures"""
        condition = self.analyze_symptoms(symptoms)
        return self.medical_conditions.get(condition.lower(), {})
    
    def get_procedure_codes(self, procedures):
        """Get medical procedure codes (CPT/HCPCS)"""
        procedure_codes = {
            "ECG": "93000",
            "Chest X-ray": "71020",
            "Blood tests": "80053",
            "CT scan": "74150",
            "MRI": "73721",
            "Ultrasound": "76700",
            "Physical examination": "99213",
            "X-ray": "73610",
            "Endoscopy": "43235",
            "Stress test": "93015"
        }
        
        codes = []
        for procedure in procedures:
            if procedure in procedure_codes:
                codes.append({
                    "procedure": procedure,
                    "code": procedure_codes[procedure]
                })
            else:
                codes.append({
                    "procedure": procedure,
                    "code": "99999"  # Generic code
                })
        
        return codes
