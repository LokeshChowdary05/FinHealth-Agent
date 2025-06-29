import json
import os
from datetime import datetime

class HospitalDataManager:
    def __init__(self):
        # Load data from JSON file
        self.data = self._load_hospital_data()
        self.hospitals_data = self.data.get('hospitals', {})
        self.insurance_plans = self.data.get('insurance_plans', {})
        self.medical_conditions = self.data.get('medical_conditions', {})
        
        # Create a city-to-state mapping for easy lookups
        self.city_to_state = self._create_city_state_mapping()
    
    def _load_hospital_data(self):
        """Load hospital pricing data from JSON file"""
        try:
            # Try nationwide data first
            nationwide_file = os.path.join('data', 'nationwide_hospital_data.json')
            if os.path.exists(nationwide_file):
                with open(nationwide_file, 'r') as f:
                    return json.load(f)
            
            # Fallback to original data
            data_file = os.path.join('data', 'hospital_pricing_data.json')
            if os.path.exists(data_file):
                with open(data_file, 'r') as f:
                    return json.load(f)
            else:
                # Fallback data if file doesn't exist
                return self._get_fallback_data()
        except Exception as e:
            print(f"Error loading hospital data: {e}")
            return self._get_fallback_data()
    
    def _get_fallback_data(self):
        """Fallback data structure"""
        return {
            "hospitals": {
                "New York": [
                    {
                        "name": "NYC General Hospital",
                        "rating": 4.2,
                        "address": "123 Medical Center Dr, New York, NY",
                        "phone": "(212) 555-1234",
                        "emergency": True,
                        "insurance_accepted": ["Aetna", "Blue Cross", "Cigna", "UnitedHealth"],
                        "procedures": {
                            "ECG": {"base_price": 250, "insurance_price": 180, "cash_price": 212}
                        }
                    }
                ]
            },
            "insurance_plans": {},
            "medical_conditions": {}
        }

    def compare_hospitals(self, procedures, location="New York"):
        """Compare hospital prices for given procedures"""
        # Use the new city lookup system
        hospitals = self.find_city_hospitals(location)
        
        # If no hospitals found, try fallback
        if not hospitals:
            hospitals = self.hospitals_data.get(location, [])
            if not hospitals and "New York" in self.hospitals_data:
                hospitals = self.find_city_hospitals("New York")
        
        comparison_results = []
        
        for hospital in hospitals:
            hospital_pricing = self._calculate_hospital_pricing(hospital, procedures)
            comparison_results.append(hospital_pricing)
        
        # Sort by total cash cost (most relevant for users)
        comparison_results.sort(key=lambda x: x['total_cash_cost'])
        
        return comparison_results
    
    def _calculate_hospital_pricing(self, hospital, procedures):
        """Calculate pricing for a specific hospital using real data"""
        procedure_costs = []
        total_cost = 0
        total_cash_cost = 0
        cash_discount = hospital.get('cash_discount', 15)
        
        hospital_procedures = hospital.get('procedures', {})
        
        for procedure in procedures:
            if procedure in hospital_procedures:
                proc_data = hospital_procedures[procedure]
                base_price = proc_data.get('base_price', 0)
                cash_price = proc_data.get('cash_price', base_price * 0.85)
                insurance_price = proc_data.get('insurance_price', base_price * 0.75)
                
                procedure_cost = {
                    "procedure": procedure,
                    "base_price": base_price,
                    "cash_price": cash_price,
                    "insurance_price": insurance_price,
                    "savings_cash": base_price - cash_price
                }
                
                procedure_costs.append(procedure_cost)
                total_cost += base_price
                total_cash_cost += cash_price
        
        return {
            "hospital": {
                "name": hospital.get('name', ''),
                "rating": hospital.get('rating', 0),
                "address": hospital.get('address', ''),
                "phone": hospital.get('phone', ''),
                "emergency": hospital.get('emergency', False),
                "insurance_accepted": hospital.get('insurance_accepted', []),
                "specialties": hospital.get('specialties', []),
                "average_wait_time": hospital.get('average_wait_time', 45)
            },
            "procedures": procedure_costs,
            "total_cost": round(total_cost, 2),
            "total_cash_cost": round(total_cash_cost, 2),
            "total_savings_cash": round(total_cost - total_cash_cost, 2),
            "cash_discount_percent": cash_discount,
            "estimated_wait_time": f"{hospital.get('average_wait_time', 45)} minutes"
        }
    
    def get_hospital_details(self, hospital_name, location="New York"):
        """Get detailed information about a specific hospital"""
        hospitals = self.hospitals_data.get(location, self.hospitals_data["New York"])
        
        for hospital in hospitals:
            if hospital["name"].lower() == hospital_name.lower():
                return hospital
        
            return None
    
    def _create_city_state_mapping(self):
        """Create a mapping from city names to states for easy lookup"""
        city_state_map = {}
        for state, state_data in self.hospitals_data.items():
            if isinstance(state_data, dict):  # New nationwide format
                for city in state_data.keys():
                    city_state_map[city.lower()] = state
            else:  # Old format fallback
                city_state_map[state.lower()] = state
        return city_state_map
    
    def find_city_hospitals(self, city_name):
        """Find hospitals in a specific city, handling both old and new data formats"""
        city_lower = city_name.lower()
        
        # Check if we have the new state-based structure
        for state, state_data in self.hospitals_data.items():
            if isinstance(state_data, dict):  # New format: state -> city -> hospitals
                for city, hospitals in state_data.items():
                    if city.lower() == city_lower:
                        return hospitals
            else:  # Old format: city -> hospitals
                if state.lower() == city_lower:
                    return state_data
        
        # Try partial matching for city names
        for state, state_data in self.hospitals_data.items():
            if isinstance(state_data, dict):
                for city, hospitals in state_data.items():
                    if city_lower in city.lower() or city.lower() in city_lower:
                        return hospitals
        
        return []
    
    def search_hospitals_by_insurance(self, insurance_plan, location="New York"):
        """Find hospitals that accept specific insurance"""
        hospitals = self.find_city_hospitals(location)
        
        if not hospitals:
            hospitals = self.find_city_hospitals("New York")
        
        matching_hospitals = []
        
        for hospital in hospitals:
            if insurance_plan.lower() in [ins.lower() for ins in hospital.get("insurance_accepted", [])]:
                matching_hospitals.append(hospital)
        
        return matching_hospitals
    
    def get_emergency_hospitals(self, location="New York"):
        """Get hospitals with emergency services"""
        hospitals = self.find_city_hospitals(location)
        
        if not hospitals:
            hospitals = self.find_city_hospitals("New York")
        
        emergency_hospitals = [h for h in hospitals if h.get("emergency", False)]
        return emergency_hospitals
