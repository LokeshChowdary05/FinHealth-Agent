import json
import os

class InsuranceAnalyzer:
    def __init__(self):
        # Load insurance data from the hospital data file
        self.insurance_plans = self._load_insurance_data()
    
    def _load_insurance_data(self):
        """Load insurance plans data from JSON file"""
        try:
            # Try nationwide data first
            nationwide_file = os.path.join('data', 'nationwide_hospital_data.json')
            if os.path.exists(nationwide_file):
                with open(nationwide_file, 'r') as f:
                    data = json.load(f)
                    return data.get('insurance_plans', {})
            
            # Fallback to original data
            data_file = os.path.join('data', 'hospital_pricing_data.json')
            if os.path.exists(data_file):
                with open(data_file, 'r') as f:
                    data = json.load(f)
                    return data.get('insurance_plans', {})
            else:
                return self._get_fallback_insurance_data()
        except Exception as e:
            print(f"Error loading insurance data: {e}")
            return self._get_fallback_insurance_data()
    
    def _get_fallback_insurance_data(self):
        """Fallback insurance data"""
        return {
            "Aetna": {
                "deductible": 1500,
                "out_of_pocket_max": 3500,
                "coverage_percent": 80
            },
            "Blue Cross Blue Shield": {
                "deductible": 1000,
                "out_of_pocket_max": 3000,
                "coverage_percent": 75
            },
            "Cigna": {
                "deductible": 1200,
                "out_of_pocket_max": 3200,
                "coverage_percent": 85
            },
            "UnitedHealth": {
                "deductible": 2000,
                "out_of_pocket_max": 4000,
                "coverage_percent": 70
            }
        }

    def analyze_coverage(self, procedures, insurance_plan, hospital):
        """Calculate costs for covered procedures vs out-of-pocket expenses"""
        plan = self.insurance_plans.get(insurance_plan)

        if not plan:
            return {'error': 'Insurance plan not found'}

        total_procedures_cost = sum(p['price'] for p in procedures)
        coverage_amount = (plan['coverage_percent'] / 100) * total_procedures_cost

        # Calculate costs
        insured_cost = min(plan['out_of_pocket_max'], max(plan['deductible'], coverage_amount))
        uninsured_cost = total_procedures_cost * 0.85  # Flat 15% discount for uninsured

        details = {
            'hospital': hospital['name'],
            'insurance_plan': insurance_plan,
            'total_procedures_cost': total_procedures_cost,
            'insured_cost': insured_cost,
            'uninsured_cost': uninsured_cost,
            'savings_with_insurance': max(0, total_procedures_cost - insured_cost),
            'savings_without_insurance': max(0, total_procedures_cost - uninsured_cost),
            'deductible': plan['deductible'],
            'out_of_pocket_max': plan['out_of_pocket_max'],
            'coverage_percent': plan['coverage_percent']
        }

        return details

    def add_insurance_plan(self, insurance_name, deductible, out_of_pocket_max, coverage_percent):
        """Add a new insurance plan"""
        self.insurance_plans[insurance_name] = {
            "deductible": deductible,
            "out_of_pocket_max": out_of_pocket_max,
            "coverage_percent": coverage_percent
        }

    def update_insurance_plan(self, insurance_name, **kwargs):
        """Update existing insurance plan details"""
        plan = self.insurance_plans.get(insurance_name)

        if not plan:
            return {'error': 'Insurance plan not found'}

        for key, value in kwargs.items():
            if key in plan:
                plan[key] = value

        return plan
