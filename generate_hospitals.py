import json
import random

def generate_hospital_data():
    """Generate comprehensive hospital data with 20+ hospitals per major city"""
    
    # Base hospital types and naming patterns
    hospital_types = [
        "General Hospital", "Medical Center", "Regional Medical Center", "Community Hospital",
        "University Hospital", "Memorial Hospital", "Health System", "Medical Institute",
        "Specialty Hospital", "Healthcare Center", "Medical Plaza", "Clinic"
    ]
    
    # Real hospital network names for authenticity
    networks = [
        "HCA Healthcare", "Kaiser Permanente", "Providence", "Ascension", "CommonSpirit",
        "Trinity Health", "Tenet Healthcare", "Universal Health Services", "Prime Healthcare",
        "LifePoint Health", "Community Health Systems", "Steward Health Care"
    ]
    
    # Medical specialties
    specialties_pool = [
        "Emergency Medicine", "Cardiology", "Neurology", "Orthopedics", "Oncology",
        "Pediatrics", "Geriatrics", "Internal Medicine", "Family Medicine", "Surgery",
        "Radiology", "Pathology", "Anesthesiology", "Psychiatry", "Dermatology",
        "Ophthalmology", "ENT", "Urology", "Gastroenterology", "Pulmonology",
        "Endocrinology", "Rheumatology", "Nephrology", "Infectious Disease", "Trauma Surgery"
    ]
    
    # Insurance providers
    insurance_options = [
        "Aetna", "Blue Cross Blue Shield", "Cigna", "UnitedHealth", "Humana",
        "Kaiser", "Medicare", "Medicaid", "Health Net", "Molina Healthcare",
        "Emblem Health", "GEHA", "Tricare"
    ]
    
    # City-specific data
    cities_data = {
        "New York": {
            "area_codes": ["212", "718", "917", "646", "347"],
            "zip_codes": ["10001", "10002", "10003", "10004", "10005", "10010", "10011", "10012"],
            "neighborhoods": ["Manhattan", "Brooklyn", "Queens", "Bronx", "Staten Island", "Harlem", "Chelsea", "SoHo"]
        },
        "Los Angeles": {
            "area_codes": ["213", "323", "310", "424", "818"],
            "zip_codes": ["90001", "90002", "90003", "90028", "90210", "90211", "90212"],
            "neighborhoods": ["Hollywood", "Beverly Hills", "Santa Monica", "West Hollywood", "Downtown", "Pasadena", "Burbank"]
        },
        "Chicago": {
            "area_codes": ["312", "773", "708", "847", "630"],
            "zip_codes": ["60601", "60602", "60603", "60604", "60605", "60606"],
            "neighborhoods": ["Downtown", "North Side", "South Side", "West Side", "Lincoln Park", "River North"]
        },
        "Miami": {
            "area_codes": ["305", "786", "954"],
            "zip_codes": ["33101", "33102", "33103", "33104", "33105"],
            "neighborhoods": ["South Beach", "Downtown", "Coral Gables", "Aventura", "Kendall", "Hialeah"]
        },
        "Boston": {
            "area_codes": ["617", "857", "781", "978"],
            "zip_codes": ["02101", "02102", "02103", "02104", "02105"],
            "neighborhoods": ["Back Bay", "Beacon Hill", "Cambridge", "Somerville", "Brookline", "Newton"]
        },
        "Houston": {
            "area_codes": ["713", "281", "832", "409"],
            "zip_codes": ["77001", "77002", "77003", "77004", "77005"],
            "neighborhoods": ["Downtown", "Medical Center", "River Oaks", "The Heights", "Montrose", "Galleria"]
        },
        "Atlanta": {
            "area_codes": ["404", "678", "770", "470"],
            "zip_codes": ["30301", "30302", "30303", "30304", "30305"],
            "neighborhoods": ["Downtown", "Midtown", "Buckhead", "Virginia Highland", "Little Five Points", "Decatur"]
        },
        "Seattle": {
            "area_codes": ["206", "425", "253", "360"],
            "zip_codes": ["98101", "98102", "98103", "98104", "98105"],
            "neighborhoods": ["Capitol Hill", "Queen Anne", "Belltown", "Fremont", "Ballard", "University District"]
        },
        "Phoenix": {
            "area_codes": ["602", "623", "480", "520"],
            "zip_codes": ["85001", "85002", "85003", "85004", "85005"],
            "neighborhoods": ["Downtown", "Scottsdale", "Tempe", "Mesa", "Glendale", "Chandler"]
        }
    }
    
    def generate_procedure_prices():
        """Generate realistic procedure prices with variation"""
        base_prices = {
            "ECG": random.randint(200, 350),
            "Chest X-ray": random.randint(250, 400),
            "Blood tests": random.randint(150, 250),
            "CT scan": random.randint(900, 1500),
            "MRI": random.randint(1500, 2500),
            "Ultrasound": random.randint(300, 600),
            "Physical examination": random.randint(200, 400),
            "Stress test": random.randint(500, 850)
        }
        
        procedures = {}
        for proc, base_price in base_prices.items():
            insurance_price = int(base_price * random.uniform(0.70, 0.85))
            cash_discount = random.uniform(0.80, 0.95)
            cash_price = int(base_price * cash_discount)
            
            procedures[proc] = {
                "base_price": base_price,
                "insurance_price": insurance_price,
                "cash_price": cash_price
            }
        
        return procedures
    
    def generate_hospitals_for_city(city_name, city_data, count=22):
        """Generate specified number of hospitals for a city"""
        hospitals = []
        
        for i in range(count):
            hospital_id = f"{city_name.lower().replace(' ', '_')}_hospital_{i+1:03d}"
            
            # Generate hospital name
            if i < 5:  # Use real-sounding names for first few
                real_names = [
                    f"{city_name} General Hospital",
                    f"{city_name} Medical Center", 
                    f"{city_name} University Hospital",
                    f"{city_name} Regional Medical Center",
                    f"{city_name} Memorial Hospital"
                ]
                name = real_names[i] if i < len(real_names) else f"{random.choice(city_data['neighborhoods'])} {random.choice(hospital_types)}"
            else:
                neighborhood = random.choice(city_data['neighborhoods'])
                hospital_type = random.choice(hospital_types)
                name = f"{neighborhood} {hospital_type}"
            
            # Generate address
            street_num = random.randint(100, 9999)
            street_names = ["Main St", "First Ave", "Medical Dr", "Health Blvd", "Care Way", "Hospital Rd", "Center St"]
            street = random.choice(street_names)
            zip_code = random.choice(city_data['zip_codes'])
            state_abbrev = {"New York": "NY", "Los Angeles": "CA", "Chicago": "IL", "Miami": "FL", 
                          "Boston": "MA", "Houston": "TX", "Atlanta": "GA", "Seattle": "WA", "Phoenix": "AZ"}
            address = f"{street_num} {street}, {city_name}, {state_abbrev[city_name]} {zip_code}"
            
            # Generate phone
            area_code = random.choice(city_data['area_codes'])
            phone = f"({area_code}) {random.randint(200,999)}-{random.randint(1000,9999)}"
            
            # Generate other attributes
            rating = round(random.uniform(3.5, 4.8), 1)
            emergency = random.choice([True, True, True, False])  # 75% have emergency
            cash_discount = random.randint(10, 25)
            wait_time = random.randint(20, 80)
            
            # Generate specialties (3-5 per hospital)
            num_specialties = random.randint(3, 5)
            specialties = random.sample(specialties_pool, num_specialties)
            
            # Generate insurance acceptance (5-8 plans per hospital)
            num_insurance = random.randint(5, 8)
            insurance_accepted = random.sample(insurance_options, num_insurance)
            
            hospital = {
                "id": hospital_id,
                "name": name,
                "rating": rating,
                "address": address,
                "phone": phone,
                "emergency": emergency,
                "specialties": specialties,
                "insurance_accepted": insurance_accepted,
                "cash_discount": cash_discount,
                "average_wait_time": wait_time,
                "procedures": generate_procedure_prices()
            }
            
            hospitals.append(hospital)
        
        return hospitals
    
    # Generate hospitals for all cities
    all_hospitals = {}
    for city_name, city_data in cities_data.items():
        print(f"Generating hospitals for {city_name}...")
        all_hospitals[city_name] = generate_hospitals_for_city(city_name, city_data, 22)
    
    # Insurance plans data (keep existing)
    insurance_plans = {
        "Aetna": {
            "deductible": 1500,
            "out_of_pocket_max": 3500,
            "copay_primary": 25,
            "copay_specialist": 40,
            "copay_emergency": 150,
            "coverage_percent": 80,
            "networks": ["Aetna Better Health", "Aetna Choice", "Aetna Select"]
        },
        "Blue Cross Blue Shield": {
            "deductible": 1000,
            "out_of_pocket_max": 3000,
            "copay_primary": 20,
            "copay_specialist": 35,
            "copay_emergency": 100,
            "coverage_percent": 75,
            "networks": ["PPO", "HMO", "EPO"]
        },
        "Cigna": {
            "deductible": 1200,
            "out_of_pocket_max": 3200,
            "copay_primary": 25,
            "copay_specialist": 45,
            "copay_emergency": 125,
            "coverage_percent": 85,
            "networks": ["Cigna Connect", "Cigna LocalPlus"]
        },
        "UnitedHealth": {
            "deductible": 2000,
            "out_of_pocket_max": 4000,
            "copay_primary": 30,
            "copay_specialist": 50,
            "copay_emergency": 200,
            "coverage_percent": 70,
            "networks": ["Choice Plus", "Navigate", "Options PPO"]
        },
        "Medicare": {
            "deductible": 1484,
            "out_of_pocket_max": 7050,
            "copay_primary": 0,
            "copay_specialist": 20,
            "copay_emergency": 389,
            "coverage_percent": 80,
            "networks": ["Original Medicare", "Medicare Advantage"]
        },
        "Medicaid": {
            "deductible": 0,
            "out_of_pocket_max": 0,
            "copay_primary": 0,
            "copay_specialist": 5,
            "copay_emergency": 10,
            "coverage_percent": 100,
            "networks": ["Medicaid Managed Care"]
        }
    }
    
    # Medical conditions data (keep existing)
    medical_conditions = {
        "chest pain": {
            "common_procedures": ["ECG", "Chest X-ray", "Blood tests", "Stress test"],
            "urgency_level": "high",
            "estimated_cost_range": [500, 2000]
        },
        "headache": {
            "common_procedures": ["CT scan", "MRI", "Blood tests", "Physical examination"],
            "urgency_level": "medium",
            "estimated_cost_range": [300, 3500]
        },
        "abdominal pain": {
            "common_procedures": ["Ultrasound", "CT scan", "Blood tests", "Physical examination"],
            "urgency_level": "medium",
            "estimated_cost_range": [400, 2800]
        },
        "back pain": {
            "common_procedures": ["X-ray", "MRI", "Physical examination"],
            "urgency_level": "low",
            "estimated_cost_range": [250, 2200]
        },
        "fever": {
            "common_procedures": ["Blood tests", "Chest X-ray", "Physical examination"],
            "urgency_level": "medium",
            "estimated_cost_range": [200, 800]
        }
    }
    
    # Combine all data
    full_data = {
        "hospitals": all_hospitals,
        "insurance_plans": insurance_plans,
        "medical_conditions": medical_conditions
    }
    
    return full_data

if __name__ == "__main__":
    print("🏥 Generating massive hospital dataset...")
    data = generate_hospital_data()
    
    # Save to file
    with open('data/hospital_pricing_data.json', 'w') as f:
        json.dump(data, f, indent=2)
    
    # Print summary
    total_hospitals = sum(len(hospitals) for hospitals in data['hospitals'].values())
    print(f"✅ Generated {total_hospitals} hospitals across {len(data['hospitals'])} cities:")
    for city, hospitals in data['hospitals'].items():
        print(f"   {city}: {len(hospitals)} hospitals")
    
    print("💾 Saved to data/hospital_pricing_data.json")
