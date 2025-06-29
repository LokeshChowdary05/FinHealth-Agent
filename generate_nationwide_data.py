#!/usr/bin/env python3
"""
Comprehensive Nationwide Hospital and Insurance Data Generator
Generates realistic data for hospitals and insurance companies across all 50 US states
"""

import json
import random
import os
from datetime import datetime

class NationwideDataGenerator:
    def __init__(self):
        # All 50 US States with major cities and area codes
        self.states_data = {
            "Alabama": {
                "cities": ["Birmingham", "Montgomery", "Mobile", "Huntsville", "Tuscaloosa", "Hoover", "Dothan", "Auburn", "Decatur", "Madison"],
                "area_codes": ["205", "251", "256", "334", "938"],
                "zip_ranges": ["35000-36999"]
            },
            "Alaska": {
                "cities": ["Anchorage", "Fairbanks", "Juneau", "Sitka", "Ketchikan", "Wasilla", "Kenai", "Kodiak", "Bethel", "Palmer"],
                "area_codes": ["907"],
                "zip_ranges": ["99500-99999"]
            },
            "Arizona": {
                "cities": ["Phoenix", "Tucson", "Mesa", "Chandler", "Scottsdale", "Glendale", "Gilbert", "Tempe", "Peoria", "Surprise"],
                "area_codes": ["480", "520", "602", "623", "928"],
                "zip_ranges": ["85000-86999"]
            },
            "Arkansas": {
                "cities": ["Little Rock", "Fort Smith", "Fayetteville", "Springdale", "Jonesboro", "North Little Rock", "Conway", "Rogers", "Pine Bluff", "Bentonville"],
                "area_codes": ["479", "501", "870"],
                "zip_ranges": ["71600-72999"]
            },
            "California": {
                "cities": ["Los Angeles", "San Diego", "San Jose", "San Francisco", "Fresno", "Sacramento", "Long Beach", "Oakland", "Bakersfield", "Anaheim", "Santa Ana", "Riverside", "Stockton", "Irvine", "Chula Vista"],
                "area_codes": ["209", "213", "310", "323", "408", "415", "424", "442", "510", "530", "559", "562", "619", "626", "628", "650", "657", "661", "669", "707", "714", "747", "760", "805", "818", "831", "858", "909", "916", "925", "949", "951"],
                "zip_ranges": ["90000-96999"]
            },
            "Colorado": {
                "cities": ["Denver", "Colorado Springs", "Aurora", "Fort Collins", "Lakewood", "Thornton", "Arvada", "Westminster", "Pueblo", "Centennial"],
                "area_codes": ["303", "719", "720", "970"],
                "zip_ranges": ["80000-81999"]
            },
            "Connecticut": {
                "cities": ["Bridgeport", "New Haven", "Hartford", "Stamford", "Waterbury", "Norwalk", "Danbury", "New Britain", "West Hartford", "Greenwich"],
                "area_codes": ["203", "475", "860", "959"],
                "zip_ranges": ["06000-06999"]
            },
            "Delaware": {
                "cities": ["Wilmington", "Dover", "Newark", "Middletown", "Smyrna", "Milford", "Seaford", "Georgetown", "Elsmere", "New Castle"],
                "area_codes": ["302"],
                "zip_ranges": ["19700-19999"]
            },
            "Florida": {
                "cities": ["Jacksonville", "Miami", "Tampa", "Orlando", "St. Petersburg", "Hialeah", "Tallahassee", "Fort Lauderdale", "Port St. Lucie", "Cape Coral", "Pembroke Pines", "Hollywood", "Gainesville", "Miramar", "Coral Springs"],
                "area_codes": ["239", "305", "321", "352", "386", "407", "561", "689", "727", "754", "772", "786", "813", "850", "863", "904", "941", "954"],
                "zip_ranges": ["32000-34999"]
            },
            "Georgia": {
                "cities": ["Atlanta", "Augusta", "Columbus", "Macon", "Savannah", "Athens", "Sandy Springs", "Roswell", "Johns Creek", "Albany"],
                "area_codes": ["229", "404", "470", "478", "678", "706", "762", "770", "912"],
                "zip_ranges": ["30000-31999"]
            },
            "Hawaii": {
                "cities": ["Honolulu", "East Honolulu", "Pearl City", "Hilo", "Kailua", "Waipahu", "Kaneohe", "Kailua-Kona", "Kahului", "Mililani"],
                "area_codes": ["808"],
                "zip_ranges": ["96700-96999"]
            },
            "Idaho": {
                "cities": ["Boise", "Meridian", "Nampa", "Idaho Falls", "Pocatello", "Caldwell", "Coeur d'Alene", "Twin Falls", "Lewiston", "Post Falls"],
                "area_codes": ["208", "986"],
                "zip_ranges": ["83200-83999"]
            },
            "Illinois": {
                "cities": ["Chicago", "Aurora", "Rockford", "Joliet", "Naperville", "Springfield", "Peoria", "Elgin", "Waukegan", "Cicero"],
                "area_codes": ["217", "224", "309", "312", "331", "618", "630", "708", "773", "779", "815", "847", "872"],
                "zip_ranges": ["60000-62999"]
            },
            "Indiana": {
                "cities": ["Indianapolis", "Fort Wayne", "Evansville", "South Bend", "Carmel", "Fishers", "Bloomington", "Hammond", "Gary", "Muncie"],
                "area_codes": ["219", "260", "317", "463", "574", "765", "812", "930"],
                "zip_ranges": ["46000-47999"]
            },
            "Iowa": {
                "cities": ["Des Moines", "Cedar Rapids", "Davenport", "Sioux City", "Iowa City", "Waterloo", "Council Bluffs", "Ames", "West Des Moines", "Dubuque"],
                "area_codes": ["319", "515", "563", "641", "712"],
                "zip_ranges": ["50000-52999"]
            },
            "Kansas": {
                "cities": ["Wichita", "Overland Park", "Kansas City", "Topeka", "Olathe", "Lawrence", "Shawnee", "Manhattan", "Lenexa", "Salina"],
                "area_codes": ["316", "620", "785", "913"],
                "zip_ranges": ["66000-67999"]
            },
            "Kentucky": {
                "cities": ["Louisville", "Lexington", "Bowling Green", "Owensboro", "Covington", "Hopkinsville", "Richmond", "Florence", "Georgetown", "Henderson"],
                "area_codes": ["270", "364", "502", "606", "859"],
                "zip_ranges": ["40000-42999"]
            },
            "Louisiana": {
                "cities": ["New Orleans", "Baton Rouge", "Shreveport", "Lafayette", "Lake Charles", "Kenner", "Bossier City", "Monroe", "Alexandria", "Houma"],
                "area_codes": ["225", "318", "337", "504", "985"],
                "zip_ranges": ["70000-71599"]
            },
            "Maine": {
                "cities": ["Portland", "Lewiston", "Bangor", "South Portland", "Auburn", "Biddeford", "Sanford", "Saco", "Augusta", "Westbrook"],
                "area_codes": ["207"],
                "zip_ranges": ["03900-04999"]
            },
            "Maryland": {
                "cities": ["Baltimore", "Columbia", "Germantown", "Silver Spring", "Waldorf", "Glen Burnie", "Ellicott City", "Frederick", "Dundalk", "Rockville"],
                "area_codes": ["240", "301", "410", "443", "667"],
                "zip_ranges": ["20600-21999"]
            },
            "Massachusetts": {
                "cities": ["Boston", "Worcester", "Springfield", "Cambridge", "Lowell", "Brockton", "Quincy", "Lynn", "Fall River", "Newton"],
                "area_codes": ["339", "351", "413", "508", "617", "774", "781", "857", "978"],
                "zip_ranges": ["01000-02999"]
            },
            "Michigan": {
                "cities": ["Detroit", "Grand Rapids", "Warren", "Sterling Heights", "Ann Arbor", "Lansing", "Flint", "Dearborn", "Livonia", "Westland"],
                "area_codes": ["231", "248", "269", "313", "517", "586", "616", "734", "810", "906", "947", "989"],
                "zip_ranges": ["48000-49999"]
            },
            "Minnesota": {
                "cities": ["Minneapolis", "Saint Paul", "Rochester", "Duluth", "Bloomington", "Brooklyn Park", "Plymouth", "Saint Cloud", "Eagan", "Woodbury"],
                "area_codes": ["218", "320", "507", "612", "651", "763", "952"],
                "zip_ranges": ["55000-56999"]
            },
            "Mississippi": {
                "cities": ["Jackson", "Gulfport", "Southaven", "Hattiesburg", "Biloxi", "Meridian", "Tupelo", "Greenville", "Olive Branch", "Horn Lake"],
                "area_codes": ["228", "601", "662", "769"],
                "zip_ranges": ["38600-39999"]
            },
            "Missouri": {
                "cities": ["Kansas City", "Saint Louis", "Springfield", "Columbia", "Independence", "Lee's Summit", "O'Fallon", "Saint Joseph", "Saint Charles", "Blue Springs"],
                "area_codes": ["314", "417", "573", "636", "660", "816"],
                "zip_ranges": ["63000-65999"]
            },
            "Montana": {
                "cities": ["Billings", "Missoula", "Great Falls", "Bozeman", "Butte", "Helena", "Kalispell", "Havre", "Anaconda", "Miles City"],
                "area_codes": ["406"],
                "zip_ranges": ["59000-59999"]
            },
            "Nebraska": {
                "cities": ["Omaha", "Lincoln", "Bellevue", "Grand Island", "Kearney", "Fremont", "Hastings", "North Platte", "Norfolk", "Columbus"],
                "area_codes": ["308", "402", "531"],
                "zip_ranges": ["68000-69999"]
            },
            "Nevada": {
                "cities": ["Las Vegas", "Henderson", "Reno", "North Las Vegas", "Sparks", "Carson City", "Fernley", "Elko", "Mesquite", "Boulder City"],
                "area_codes": ["702", "725", "775"],
                "zip_ranges": ["89000-89999"]
            },
            "New Hampshire": {
                "cities": ["Manchester", "Nashua", "Concord", "Derry", "Rochester", "Salem", "Dover", "Merrimack", "Londonderry", "Hudson"],
                "area_codes": ["603"],
                "zip_ranges": ["03000-03999"]
            },
            "New Jersey": {
                "cities": ["Newark", "Jersey City", "Paterson", "Elizabeth", "Edison", "Woodbridge", "Lakewood", "Toms River", "Hamilton", "Trenton"],
                "area_codes": ["201", "551", "609", "732", "848", "856", "862", "908", "973"],
                "zip_ranges": ["07000-08999"]
            },
            "New Mexico": {
                "cities": ["Albuquerque", "Las Cruces", "Rio Rancho", "Santa Fe", "Roswell", "Farmington", "Clovis", "Hobbs", "Alamogordo", "Carlsbad"],
                "area_codes": ["505", "575"],
                "zip_ranges": ["87000-88999"]
            },
            "New York": {
                "cities": ["New York", "Buffalo", "Rochester", "Yonkers", "Syracuse", "Albany", "New Rochelle", "Mount Vernon", "Schenectady", "Utica"],
                "area_codes": ["212", "315", "332", "347", "516", "518", "585", "607", "631", "646", "680", "716", "718", "845", "914", "917", "929", "934"],
                "zip_ranges": ["10000-14999"]
            },
            "North Carolina": {
                "cities": ["Charlotte", "Raleigh", "Greensboro", "Durham", "Winston-Salem", "Fayetteville", "Cary", "Wilmington", "High Point", "Greenville"],
                "area_codes": ["252", "336", "704", "743", "828", "910", "919", "980", "984"],
                "zip_ranges": ["27000-28999"]
            },
            "North Dakota": {
                "cities": ["Fargo", "Bismarck", "Grand Forks", "Minot", "West Fargo", "Williston", "Dickinson", "Mandan", "Jamestown", "Wahpeton"],
                "area_codes": ["701"],
                "zip_ranges": ["58000-58999"]
            },
            "Ohio": {
                "cities": ["Columbus", "Cleveland", "Cincinnati", "Toledo", "Akron", "Dayton", "Parma", "Canton", "Youngstown", "Lorain"],
                "area_codes": ["216", "220", "234", "330", "380", "419", "440", "513", "567", "614", "740", "937"],
                "zip_ranges": ["43000-45999"]
            },
            "Oklahoma": {
                "cities": ["Oklahoma City", "Tulsa", "Norman", "Broken Arrow", "Lawton", "Edmond", "Moore", "Midwest City", "Enid", "Stillwater"],
                "area_codes": ["405", "539", "580", "918"],
                "zip_ranges": ["73000-74999"]
            },
            "Oregon": {
                "cities": ["Portland", "Eugene", "Salem", "Gresham", "Hillsboro", "Bend", "Beaverton", "Medford", "Springfield", "Corvallis"],
                "area_codes": ["458", "503", "541", "971"],
                "zip_ranges": ["97000-97999"]
            },
            "Pennsylvania": {
                "cities": ["Philadelphia", "Pittsburgh", "Allentown", "Erie", "Reading", "Scranton", "Bethlehem", "Lancaster", "Harrisburg", "Altoona"],
                "area_codes": ["215", "267", "272", "412", "445", "484", "570", "610", "717", "724", "814", "878"],
                "zip_ranges": ["15000-19999"]
            },
            "Rhode Island": {
                "cities": ["Providence", "Warwick", "Cranston", "Pawtucket", "East Providence", "Woonsocket", "Newport", "Central Falls", "Westerly", "North Providence"],
                "area_codes": ["401"],
                "zip_ranges": ["02800-02999"]
            },
            "South Carolina": {
                "cities": ["Charleston", "Columbia", "North Charleston", "Mount Pleasant", "Rock Hill", "Greenville", "Summerville", "Sumter", "Goose Creek", "Hilton Head Island"],
                "area_codes": ["803", "843", "854", "864"],
                "zip_ranges": ["29000-29999"]
            },
            "South Dakota": {
                "cities": ["Sioux Falls", "Rapid City", "Aberdeen", "Brookings", "Watertown", "Mitchell", "Yankton", "Pierre", "Huron", "Vermillion"],
                "area_codes": ["605"],
                "zip_ranges": ["57000-57999"]
            },
            "Tennessee": {
                "cities": ["Nashville", "Memphis", "Knoxville", "Chattanooga", "Clarksville", "Murfreesboro", "Franklin", "Jackson", "Johnson City", "Bartlett"],
                "area_codes": ["423", "615", "629", "731", "865", "901", "931"],
                "zip_ranges": ["37000-38599"]
            },
            "Texas": {
                "cities": ["Houston", "San Antonio", "Dallas", "Austin", "Fort Worth", "El Paso", "Arlington", "Corpus Christi", "Plano", "Lubbock", "Laredo", "Irving", "Garland", "Frisco", "McKinney", "Amarillo", "Grand Prairie", "Brownsville", "Pasadena", "Mesquite"],
                "area_codes": ["214", "254", "281", "325", "346", "361", "409", "430", "432", "469", "512", "713", "726", "737", "806", "817", "830", "832", "903", "915", "936", "940", "956", "972", "979"],
                "zip_ranges": ["73300-73399", "75000-79999", "77000-77999", "78000-79999"]
            },
            "Utah": {
                "cities": ["Salt Lake City", "West Valley City", "Provo", "West Jordan", "Orem", "Sandy", "Ogden", "St. George", "Layton", "Taylorsville"],
                "area_codes": ["385", "435", "801"],
                "zip_ranges": ["84000-84999"]
            },
            "Vermont": {
                "cities": ["Burlington", "Essex", "South Burlington", "Colchester", "Rutland", "Montpelier", "Winooski", "St. Albans", "Newport", "Vergennes"],
                "area_codes": ["802"],
                "zip_ranges": ["05000-05999"]
            },
            "Virginia": {
                "cities": ["Virginia Beach", "Norfolk", "Chesapeake", "Richmond", "Newport News", "Alexandria", "Hampton", "Portsmouth", "Suffolk", "Roanoke"],
                "area_codes": ["276", "434", "540", "571", "703", "757", "804"],
                "zip_ranges": ["20100-20199", "22000-24699"]
            },
            "Washington": {
                "cities": ["Seattle", "Spokane", "Tacoma", "Vancouver", "Bellevue", "Kent", "Everett", "Renton", "Spokane Valley", "Federal Way"],
                "area_codes": ["206", "253", "360", "425", "509", "564"],
                "zip_ranges": ["98000-99499"]
            },
            "West Virginia": {
                "cities": ["Charleston", "Huntington", "Parkersburg", "Morgantown", "Wheeling", "Martinsburg", "Fairmont", "Beckley", "Clarksburg", "Lewisburg"],
                "area_codes": ["304", "681"],
                "zip_ranges": ["24700-26999"]
            },
            "Wisconsin": {
                "cities": ["Milwaukee", "Madison", "Green Bay", "Kenosha", "Racine", "Appleton", "Waukesha", "Oshkosh", "Eau Claire", "Janesville"],
                "area_codes": ["262", "414", "534", "608", "715", "920"],
                "zip_ranges": ["53000-54999"]
            },
            "Wyoming": {
                "cities": ["Cheyenne", "Casper", "Laramie", "Gillette", "Rock Springs", "Sheridan", "Green River", "Evanston", "Riverton", "Jackson"],
                "area_codes": ["307"],
                "zip_ranges": ["82000-83199"]
            }
        }
        
        # Comprehensive Insurance Companies (Major and Regional)
        self.insurance_companies = {
            # Major National Carriers
            "UnitedHealth Group": {
                "subsidiaries": ["UnitedHealthcare", "Optum", "Amil"],
                "coverage_areas": "all_states",
                "plan_types": ["HMO", "PPO", "EPO", "POS"],
                "deductible_range": [500, 8000],
                "coverage_percent_range": [70, 90],
                "out_of_pocket_max_range": [2000, 15000]
            },
            "Anthem Inc": {
                "subsidiaries": ["Blue Cross Blue Shield", "Anthem Blue Cross", "Empire BlueCross"],
                "coverage_areas": "all_states",
                "plan_types": ["HMO", "PPO", "EPO"],
                "deductible_range": [750, 7500],
                "coverage_percent_range": [75, 85],
                "out_of_pocket_max_range": [2500, 12000]
            },
            "Aetna": {
                "subsidiaries": ["CVS Health", "Aetna Better Health"],
                "coverage_areas": "all_states",
                "plan_types": ["HMO", "PPO", "EPO", "POS"],
                "deductible_range": [1000, 6500],
                "coverage_percent_range": [70, 85],
                "out_of_pocket_max_range": [3000, 14000]
            },
            "Cigna": {
                "subsidiaries": ["Cigna Healthcare", "Express Scripts"],
                "coverage_areas": "all_states",
                "plan_types": ["HMO", "PPO", "EPO"],
                "deductible_range": [800, 7000],
                "coverage_percent_range": [75, 90],
                "out_of_pocket_max_range": [2800, 13500]
            },
            "Humana": {
                "subsidiaries": ["Humana Military", "CenterWell"],
                "coverage_areas": "all_states",
                "plan_types": ["HMO", "PPO", "POS"],
                "deductible_range": [600, 6000],
                "coverage_percent_range": [70, 85],
                "out_of_pocket_max_range": [2200, 11000]
            },
            "Kaiser Permanente": {
                "subsidiaries": ["Kaiser Foundation Health Plan"],
                "coverage_areas": ["California", "Colorado", "Georgia", "Hawaii", "Maryland", "Oregon", "Virginia", "Washington", "Washington DC"],
                "plan_types": ["HMO"],
                "deductible_range": [0, 4500],
                "coverage_percent_range": [80, 95],
                "out_of_pocket_max_range": [1500, 9000]
            },
            "Centene Corporation": {
                "subsidiaries": ["Ambetter", "WellCare", "Fidelis Care", "Health Net"],
                "coverage_areas": "all_states",
                "plan_types": ["HMO", "PPO"],
                "deductible_range": [0, 5500],
                "coverage_percent_range": [70, 80],
                "out_of_pocket_max_range": [1800, 10000]
            },
            "Molina Healthcare": {
                "subsidiaries": ["Molina Medicaid Solutions"],
                "coverage_areas": ["California", "Florida", "Illinois", "Michigan", "Mississippi", "New Mexico", "New York", "Ohio", "Puerto Rico", "South Carolina", "Texas", "Utah", "Virginia", "Washington", "Wisconsin"],
                "plan_types": ["HMO", "PPO"],
                "deductible_range": [0, 4000],
                "coverage_percent_range": [75, 85],
                "out_of_pocket_max_range": [2000, 8500]
            },
            # Government Programs
            "Medicare": {
                "subsidiaries": ["Medicare Advantage", "Medicare Supplement"],
                "coverage_areas": "all_states",
                "plan_types": ["Original Medicare", "Medicare Advantage", "Medigap"],
                "deductible_range": [233, 1600],
                "coverage_percent_range": [80, 100],
                "out_of_pocket_max_range": [0, 8000]
            },
            "Medicaid": {
                "subsidiaries": ["State Medicaid Programs"],
                "coverage_areas": "all_states",
                "plan_types": ["Traditional Medicaid", "Managed Care"],
                "deductible_range": [0, 0],
                "coverage_percent_range": [90, 100],
                "out_of_pocket_max_range": [0, 2000]
            },
            # Regional and State-Specific Carriers
            "Independence Blue Cross": {
                "coverage_areas": ["Pennsylvania", "New Jersey", "Delaware"],
                "plan_types": ["HMO", "PPO", "EPO"],
                "deductible_range": [1000, 5000],
                "coverage_percent_range": [75, 85],
                "out_of_pocket_max_range": [3000, 10000]
            },
            "Highmark": {
                "coverage_areas": ["Pennsylvania", "West Virginia", "Delaware"],
                "plan_types": ["HMO", "PPO"],
                "deductible_range": [800, 6000],
                "coverage_percent_range": [70, 85],
                "out_of_pocket_max_range": [2500, 12000]
            },
            "Florida Blue": {
                "coverage_areas": ["Florida"],
                "plan_types": ["HMO", "PPO", "EPO"],
                "deductible_range": [750, 5500],
                "coverage_percent_range": [75, 90],
                "out_of_pocket_max_range": [2800, 11500]
            },
            "Oscar Health": {
                "coverage_areas": ["New York", "California", "Texas", "Florida", "Tennessee", "Ohio", "Arizona", "Michigan", "Pennsylvania", "Virginia"],
                "plan_types": ["EPO", "HMO"],
                "deductible_range": [0, 7000],
                "coverage_percent_range": [70, 85],
                "out_of_pocket_max_range": [2000, 15000]
            },
            "Emblem Health": {
                "coverage_areas": ["New York"],
                "plan_types": ["HMO", "PPO"],
                "deductible_range": [500, 4000],
                "coverage_percent_range": [80, 90],
                "out_of_pocket_max_range": [2000, 9000]
            },
            "GEHA": {
                "coverage_areas": "all_states",
                "plan_types": ["PPO", "HDHP"],
                "deductible_range": [400, 3000],
                "coverage_percent_range": [80, 90],
                "out_of_pocket_max_range": [1500, 8000]
            },
            "Tricare": {
                "coverage_areas": "all_states",
                "plan_types": ["Prime", "Select", "Reserve Select"],
                "deductible_range": [0, 700],
                "coverage_percent_range": [85, 100],
                "out_of_pocket_max_range": [0, 3500]
            }
        }
        
        # Medical specialties
        self.medical_specialties = [
            "Cardiology", "Neurology", "Orthopedics", "Gastroenterology", "Dermatology",
            "Psychiatry", "Oncology", "Endocrinology", "Pulmonology", "Nephrology",
            "Rheumatology", "Hematology", "Infectious Disease", "Emergency Medicine",
            "Family Medicine", "Internal Medicine", "Pediatrics", "OB/GYN", "Urology",
            "Ophthalmology", "ENT", "Anesthesiology", "Radiology", "Pathology",
            "Physical Medicine", "Geriatrics", "Sports Medicine", "Pain Management",
            "Allergy and Immunology", "Critical Care", "Plastic Surgery", "Vascular Surgery"
        ]
        
        # Hospital types and naming patterns
        self.hospital_types = [
            "General Hospital", "Medical Center", "Regional Medical Center", "University Hospital",
            "Community Hospital", "Memorial Hospital", "Baptist Hospital", "Presbyterian Hospital",
            "Methodist Hospital", "Catholic Medical Center", "Veterans Affairs Medical Center",
            "Children's Hospital", "Cancer Center", "Heart Institute", "Orthopedic Hospital"
        ]
        
        # Procedures with realistic price ranges
        self.procedures = {
            "ECG": {"min_price": 150, "max_price": 500},
            "Chest X-ray": {"min_price": 200, "max_price": 600},
            "Blood tests": {"min_price": 100, "max_price": 400},
            "CT scan": {"min_price": 500, "max_price": 2000},
            "MRI": {"min_price": 1000, "max_price": 4000},
            "Ultrasound": {"min_price": 200, "max_price": 800},
            "Physical examination": {"min_price": 150, "max_price": 500},
            "Stress test": {"min_price": 300, "max_price": 1200},
            "Endoscopy": {"min_price": 800, "max_price": 2500},
            "Colonoscopy": {"min_price": 1000, "max_price": 3000},
            "Mammography": {"min_price": 150, "max_price": 450},
            "Bone density scan": {"min_price": 100, "max_price": 300},
            "Allergy testing": {"min_price": 200, "max_price": 600},
            "Sleep study": {"min_price": 800, "max_price": 2000}
        }
        
        # Medical conditions with procedures
        self.medical_conditions = {
            "chest pain": {
                "common_procedures": ["ECG", "Chest X-ray", "Blood tests", "Stress test"],
                "urgency_level": "high",
                "estimated_cost_range": [500, 2500]
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
            },
            "shortness of breath": {
                "common_procedures": ["Chest X-ray", "ECG", "Blood tests", "Pulmonary function test"],
                "urgency_level": "high",
                "estimated_cost_range": [400, 1800]
            },
            "joint pain": {
                "common_procedures": ["X-ray", "MRI", "Blood tests", "Physical examination"],
                "urgency_level": "low",
                "estimated_cost_range": [300, 2000]
            },
            "skin rash": {
                "common_procedures": ["Physical examination", "Allergy testing", "Blood tests"],
                "urgency_level": "low",
                "estimated_cost_range": [150, 700]
            }
        }

    def generate_nationwide_hospitals(self, hospitals_per_city=8):
        """Generate hospitals for all states and cities"""
        print("🏥 Generating comprehensive nationwide hospital dataset...")
        all_hospitals = {}
        total_hospitals = 0
        
        for state, state_info in self.states_data.items():
            print(f"Generating hospitals for {state}...")
            state_hospitals = {}
            
            for city in state_info["cities"]:
                city_hospitals = []
                for i in range(hospitals_per_city):
                    hospital = self._generate_hospital(city, state, state_info, i)
                    city_hospitals.append(hospital)
                    total_hospitals += 1
                
                state_hospitals[city] = city_hospitals
            
            all_hospitals[state] = state_hospitals
        
        print(f"✅ Generated {total_hospitals} hospitals across {len(self.states_data)} states")
        return all_hospitals

    def _generate_hospital(self, city, state, state_info, index):
        """Generate a single hospital with realistic data"""
        hospital_id = f"{city.lower().replace(' ', '_')}_{state.lower().replace(' ', '_')}_hospital_{index+1:03d}"
        
        # Generate hospital name
        if index < 3:
            # First few hospitals get "real" names
            hospital_names = [
                f"{city} General Hospital",
                f"{city} Medical Center", 
                f"{city} Regional Medical Center"
            ]
            name = hospital_names[index]
        else:
            # Rest get type-based names
            hospital_type = random.choice(self.hospital_types)
            name = f"{city} {hospital_type}"
        
        # Generate address
        street_number = random.randint(100, 9999)
        street_names = ["Medical Center Dr", "Hospital Rd", "Health Way", "Care Blvd", "Wellness St", "First Ave", "Main St", "Oak St", "Park Ave", "Center St"]
        street_name = random.choice(street_names)
        
        # Get ZIP code from state range
        zip_base = int(state_info["zip_ranges"][0].split("-")[0])
        zip_code = zip_base + random.randint(0, 999)
        
        address = f"{street_number} {street_name}, {city}, {state[:2]} {zip_code}"
        
        # Generate phone number
        area_code = random.choice(state_info["area_codes"])
        phone = f"({area_code}) {random.randint(200, 999)}-{random.randint(1000, 9999)}"
        
        # Generate other attributes
        rating = round(random.uniform(3.0, 5.0), 1)
        emergency = random.choice([True, False])
        specialties = random.sample(self.medical_specialties, random.randint(2, 8))
        
        # Generate insurance acceptance (more comprehensive)
        available_insurances = list(self.insurance_companies.keys())
        # Filter by coverage area
        state_insurances = []
        for ins, info in self.insurance_companies.items():
            coverage = info.get("coverage_areas", [])
            if coverage == "all_states" or state in coverage:
                state_insurances.append(ins)
        
        insurance_accepted = random.sample(state_insurances, random.randint(3, min(8, len(state_insurances))))
        
        cash_discount = random.randint(15, 35)
        average_wait_time = random.randint(15, 60)
        
        # Generate procedure pricing
        procedures = {}
        for proc_name, price_range in self.procedures.items():
            base_price = random.randint(price_range["min_price"], price_range["max_price"])
            insurance_price = int(base_price * random.uniform(0.6, 0.85))
            cash_price = int(base_price * (1 - cash_discount/100))
            
            procedures[proc_name] = {
                "base_price": base_price,
                "insurance_price": insurance_price,
                "cash_price": cash_price
            }
        
        return {
            "id": hospital_id,
            "name": name,
            "rating": rating,
            "address": address,
            "phone": phone,
            "emergency": emergency,
            "specialties": specialties,
            "insurance_accepted": insurance_accepted,
            "cash_discount": cash_discount,
            "average_wait_time": average_wait_time,
            "procedures": procedures
        }

    def generate_comprehensive_insurance_plans(self):
        """Generate comprehensive insurance plan data"""
        print("💳 Generating comprehensive insurance plans...")
        insurance_plans = {}
        
        for company, info in self.insurance_companies.items():
            subsidiaries = info.get("subsidiaries", [company])
            
            for subsidiary in subsidiaries:
                plan_types = info.get("plan_types", ["PPO"])
                
                for plan_type in plan_types:
                    plan_name = f"{subsidiary} {plan_type}"
                    
                    deductible_range = info.get("deductible_range", [1000, 5000])
                    coverage_range = info.get("coverage_percent_range", [70, 85])
                    oop_range = info.get("out_of_pocket_max_range", [3000, 12000])
                    
                    insurance_plans[plan_name] = {
                        "parent_company": company,
                        "plan_type": plan_type,
                        "deductible": random.randint(deductible_range[0], deductible_range[1]),
                        "out_of_pocket_max": random.randint(oop_range[0], oop_range[1]),
                        "coverage_percent": random.randint(coverage_range[0], coverage_range[1]),
                        "coverage_areas": info.get("coverage_areas", "all_states"),
                        "copay_primary_care": random.randint(15, 50),
                        "copay_specialist": random.randint(30, 80),
                        "copay_emergency": random.randint(100, 400),
                        "prescription_coverage": random.choice([True, False]),
                        "network_size": random.choice(["Large", "Medium", "Small"])
                    }
        
        print(f"✅ Generated {len(insurance_plans)} insurance plans from {len(self.insurance_companies)} companies")
        return insurance_plans

    def generate_comprehensive_data(self, hospitals_per_city=8):
        """Generate the complete nationwide dataset"""
        print("🇺🇸 Generating comprehensive nationwide healthcare data...")
        
        # Generate hospitals for all states
        hospitals = self.generate_nationwide_hospitals(hospitals_per_city)
        
        # Generate insurance plans
        insurance_plans = self.generate_comprehensive_insurance_plans()
        
        # Medical conditions data
        medical_conditions = self.medical_conditions
        
        # Calculate total hospitals
        total_hospitals = sum(
            len(city_hospitals) 
            for state_hospitals in hospitals.values() 
            for city_hospitals in state_hospitals.values()
        )
        
        print(f"\n📊 Dataset Summary:")
        print(f"   🏥 Total Hospitals: {total_hospitals}")
        print(f"   🏛️ States Covered: {len(self.states_data)}")
        print(f"   🏙️ Cities Covered: {sum(len(state_info['cities']) for state_info in self.states_data.values())}")
        print(f"   💳 Insurance Plans: {len(insurance_plans)}")
        print(f"   🩺 Medical Conditions: {len(medical_conditions)}")
        
        return {
            "hospitals": hospitals,
            "insurance_plans": insurance_plans,
            "medical_conditions": medical_conditions,
            "metadata": {
                "generated_date": datetime.now().isoformat(),
                "total_hospitals": total_hospitals,
                "total_states": len(self.states_data),
                "total_cities": sum(len(state_info['cities']) for state_info in self.states_data.values()),
                "total_insurance_plans": len(insurance_plans),
                "hospitals_per_city": hospitals_per_city
            }
        }

    def save_data(self, data, filename="data/nationwide_hospital_data.json"):
        """Save the generated data to JSON file"""
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"💾 Saved comprehensive data to {filename}")
        
        # Print file size
        file_size = os.path.getsize(filename)
        print(f"📁 File size: {file_size:,} bytes ({file_size/1024/1024:.1f} MB)")

if __name__ == "__main__":
    # Generate comprehensive nationwide data
    generator = NationwideDataGenerator()
    
    # Generate with 8 hospitals per city (50 states × ~10 cities × 8 hospitals = ~4000 hospitals)
    data = generator.generate_comprehensive_data(hospitals_per_city=8)
    
    # Save the data
    generator.save_data(data)
    
    print("\n🎉 Comprehensive nationwide healthcare data generation complete!")
    print("The system now covers all 50 US states with comprehensive hospital and insurance data.")
