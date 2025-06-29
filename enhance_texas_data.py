#!/usr/bin/env python3
"""
Enhanced Texas Data Generator
Adds comprehensive hospital data for all major and minor Texas cities
"""

import json
import random
import os

def generate_texas_hospital_data():
    """Generate comprehensive hospital data for Texas cities"""
    
    # Major Texas cities with detailed hospital data
    texas_cities = [
        "Houston", "San Antonio", "Dallas", "Austin", "Fort Worth", "El Paso",
        "Arlington", "Corpus Christi", "Plano", "Lubbock", "Laredo", "Irving",
        "Garland", "Frisco", "McKinney", "Amarillo", "Grand Prairie", "Brownsville",
        "Pasadena", "Mesquite", "Killeen", "Waco", "Midland", "Abilene",
        "Beaumont", "Round Rock", "Richardson", "Lewisville", "College Station",
        "Pearland", "Tyler", "Denton", "Sugar Land", "Carrollton", "Edinburg",
        "Bryan", "Pharr", "Mission", "Missouri City", "Temple", "Flower Mound",
        "Baytown", "Harlingen", "North Richland Hills", "Mansfield", "Cedar Park",
        "Port Arthur", "San Angelo", "League City", "Longview", "Texas City",
        "New Braunfels", "Conroe", "The Woodlands"
    ]
    
    # Medical procedures with realistic price ranges
    procedures = {
        "ECG": {"min_base": 150, "max_base": 500},
        "X-ray": {"min_base": 200, "max_base": 600},
        "Blood tests": {"min_base": 100, "max_base": 400},
        "CT scan": {"min_base": 600, "max_base": 2000},
        "MRI": {"min_base": 1500, "max_base": 4000},
        "Ultrasound": {"min_base": 300, "max_base": 800},
        "Physical examination": {"min_base": 100, "max_base": 400},
        "Stress test": {"min_base": 300, "max_base": 1200},
        "Endoscopy": {"min_base": 800, "max_base": 2500},
        "Colonoscopy": {"min_base": 1000, "max_base": 2500},
        "Mammography": {"min_base": 150, "max_base": 500},
        "Bone density scan": {"min_base": 100, "max_base": 350},
        "Allergy testing": {"min_base": 200, "max_base": 600},
        "Sleep study": {"min_base": 1000, "max_base": 2000}
    }
    
    # Insurance providers
    insurance_providers = [
        "Aetna", "Blue Cross Blue Shield", "Cigna", "UnitedHealth Group", 
        "Humana", "Kaiser Permanente", "Anthem Inc", "Medicare", "Medicaid",
        "Tricare", "Oscar Health", "Molina Healthcare", "Centene Corporation",
        "GEHA"
    ]
    
    # Medical specialties
    specialties = [
        "Family Medicine", "Internal Medicine", "Emergency Medicine", "Cardiology",
        "Oncology", "Neurology", "Orthopedics", "Pediatrics", "OB/GYN",
        "Gastroenterology", "Dermatology", "Psychiatry", "Radiology",
        "Anesthesiology", "Pathology", "Urology", "ENT", "Ophthalmology",
        "Endocrinology", "Nephrology", "Pulmonology", "Rheumatology",
        "Infectious Disease", "Critical Care", "Sports Medicine", "Plastic Surgery",
        "Vascular Surgery", "Allergy and Immunology"
    ]
    
    texas_data = {}
    
    for city in texas_cities:
        # Generate 2-4 hospitals per city
        num_hospitals = random.randint(2, 4)
        hospitals = []
        
        for i in range(num_hospitals):
            # Generate hospital name
            hospital_types = ["General Hospital", "Medical Center", "Regional Medical Center", 
                            "University Hospital", "Community Hospital", "Health System"]
            hospital_name = f"{city} {random.choice(hospital_types)}"
            
            # Generate hospital data
            hospital = {
                "id": f"{city.lower().replace(' ', '_')}_texas_hospital_{i+1:03d}",
                "name": hospital_name,
                "rating": round(random.uniform(3.0, 5.0), 1),
                "address": f"{random.randint(1000, 9999)} {random.choice(['Medical Center Dr', 'Hospital Rd', 'Healthcare Blvd', 'Wellness St', 'Care Way', 'Health Plaza'])}, {city}, TX {random.randint(70000, 79999)}",
                "phone": f"({random.randint(200, 999)}) {random.randint(200, 999)}-{random.randint(1000, 9999)}",
                "emergency": random.choice([True, False]),
                "specialties": random.sample(specialties, random.randint(2, 8)),
                "insurance_accepted": random.sample(insurance_providers, random.randint(3, 8)),
                "cash_discount": random.randint(15, 35),
                "average_wait_time": random.randint(15, 75),
                "procedures": {}
            }
            
            # Generate procedure pricing for this hospital
            for proc_name, price_range in procedures.items():
                base_price = random.randint(price_range["min_base"], price_range["max_base"])
                cash_discount_pct = hospital["cash_discount"] / 100
                insurance_discount_pct = random.uniform(0.20, 0.40)  # 20-40% discount
                
                cash_price = int(base_price * (1 - cash_discount_pct))
                insurance_price = int(base_price * (1 - insurance_discount_pct))
                
                hospital["procedures"][proc_name] = {
                    "base_price": base_price,
                    "insurance_price": insurance_price,
                    "cash_price": cash_price
                }
            
            hospitals.append(hospital)
        
        texas_data[city] = hospitals
    
    return texas_data

def update_nationwide_data():
    """Update the nationwide hospital data file with enhanced Texas data"""
    
    # Load existing data
    data_file = os.path.join('data', 'nationwide_hospital_data.json')
    
    try:
        with open(data_file, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {"hospitals": {}, "insurance_plans": {}}
    
    # Generate new Texas data
    texas_data = generate_texas_hospital_data()
    
    # Update Texas section
    if "hospitals" not in data:
        data["hospitals"] = {}
    
    data["hospitals"]["Texas"] = texas_data
    
    # Save updated data
    with open(data_file, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"✅ Updated nationwide data with {len(texas_data)} Texas cities")
    print(f"📁 Total data size: {len(json.dumps(data)) / 1024 / 1024:.1f} MB")
    
    # Print some cities for verification
    print("\n🏙️ Texas cities added:")
    for i, city in enumerate(list(texas_data.keys())[:10]):
        print(f"   {i+1}. {city} - {len(texas_data[city])} hospitals")
    if len(texas_data) > 10:
        print(f"   ... and {len(texas_data) - 10} more cities")

if __name__ == "__main__":
    update_nationwide_data()
