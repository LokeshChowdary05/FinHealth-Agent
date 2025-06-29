#!/usr/bin/env python3
"""
Enhanced Conversation Manager for FinHealth Bot
Provides intelligent conversation handling with context awareness and improved responses
"""

import json
import os
import re
import openai
from datetime import datetime
from medical_analyzer import MedicalAnalyzer
from hospital_data import HospitalDataManager
from insurance_analyzer import InsuranceAnalyzer

class ConversationManager:
    def __init__(self):
        # Initialize OpenAI
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        if self.openai_api_key:
            openai.api_key = self.openai_api_key
        
        # Initialize other components
        self.medical_analyzer = MedicalAnalyzer()
        self.hospital_data_manager = HospitalDataManager()
        self.insurance_analyzer = InsuranceAnalyzer()
        
        # Enhanced conversation context tracking
        self.conversation_context = {
            'user_location': None,
            'current_symptoms': None,
            'diagnosed_condition': None,
            'required_procedures': None,
            'insurance_plan': None,
            'conversation_stage': 'initial',
            'user_preferences': {},
            'previous_queries': []
        }
        
        # Comprehensive insurance plan database
        self.insurance_database = self._load_comprehensive_insurance_data()
        
        # Medical procedure database with detailed information
        self.procedure_database = self._load_procedure_database()
        
        # Hospital specialties and services
        self.hospital_services = self._load_hospital_services()

    def _load_comprehensive_insurance_data(self):
        """Load comprehensive insurance plan information"""
        return {
            # Major National Carriers
            "UnitedHealthcare": {
                "plans": ["Choice Plus PPO", "Core PPO", "Navigate HMO", "Select EPO"],
                "coverage_areas": "Nationwide",
                "website": "uhc.com",
                "customer_service": "1-877-842-3210",
                "average_deductible": "$2,500",
                "average_premium": "$450/month",
                "network_size": "Very Large (1.3M providers)"
            },
            "Anthem Blue Cross Blue Shield": {
                "plans": ["Blue Access PPO", "Pathway HMO", "InnovateHealth EPO"],
                "coverage_areas": "14 states + DC",
                "website": "anthem.com",
                "customer_service": "1-800-331-1476",
                "average_deductible": "$2,000",
                "average_premium": "$420/month",
                "network_size": "Large (900K providers)"
            },
            "Aetna": {
                "plans": ["Aetna Better Health PPO", "Aetna Open Choice HMO", "CVS Health EPO"],
                "coverage_areas": "Nationwide",
                "website": "aetna.com",
                "customer_service": "1-800-872-3862",
                "average_deductible": "$1,800",
                "average_premium": "$380/month",
                "network_size": "Large (690K providers)"
            },
            "Cigna": {
                "plans": ["Cigna Connect HMO", "Cigna Total Care PPO", "Cigna LocalPlus EPO"],
                "coverage_areas": "Nationwide",
                "website": "cigna.com", 
                "customer_service": "1-800-244-6224",
                "average_deductible": "$2,200",
                "average_premium": "$410/month",
                "network_size": "Large (950K providers)"
            },
            "Humana": {
                "plans": ["Humana Gold Plus HMO", "Humana Choice PPO", "Humana Value EPO"],
                "coverage_areas": "Nationwide",
                "website": "humana.com",
                "customer_service": "1-800-457-4708",
                "average_deductible": "$1,500",
                "average_premium": "$320/month",
                "network_size": "Medium (550K providers)"
            },
            "Kaiser Permanente": {
                "plans": ["Kaiser Silver HMO", "Kaiser Gold HMO", "Kaiser Platinum HMO"],
                "coverage_areas": "8 states + DC",
                "website": "kp.org",
                "customer_service": "1-800-464-4000",
                "average_deductible": "$1,000",
                "average_premium": "$390/month",
                "network_size": "Integrated (22K providers)"
            },
            "Medicare": {
                "plans": ["Original Medicare", "Medicare Advantage", "Medicare Supplement"],
                "coverage_areas": "Nationwide",
                "website": "medicare.gov",
                "customer_service": "1-800-633-4227",
                "average_deductible": "$1,600",
                "average_premium": "$170/month",
                "network_size": "Very Large (All Medicare providers)"
            },
            "Medicaid": {
                "plans": ["Traditional Medicaid", "Managed Care Organizations"],
                "coverage_areas": "All states",
                "website": "medicaid.gov",
                "customer_service": "Varies by state",
                "average_deductible": "$0",
                "average_premium": "$0-50/month",
                "network_size": "Large (Medicaid providers)"
            }
        }

    def _load_procedure_database(self):
        """Load detailed medical procedure information"""
        return {
            "ECG/EKG": {
                "full_name": "Electrocardiogram",
                "description": "Records electrical activity of the heart",
                "duration": "5-10 minutes",
                "preparation": "No special preparation needed",
                "when_needed": ["Chest pain", "Heart palpitations", "Shortness of breath"],
                "average_cost_range": "$150-$500",
                "urgent": False,
                "cpt_codes": ["93000", "93005", "93010"]
            },
            "MRI": {
                "full_name": "Magnetic Resonance Imaging",
                "description": "Uses magnetic fields to create detailed body images",
                "duration": "30-90 minutes",
                "preparation": "Remove metal objects, may need contrast",
                "when_needed": ["Brain symptoms", "Joint pain", "Spinal issues"],
                "average_cost_range": "$1,000-$4,000",
                "urgent": False,
                "cpt_codes": ["70551", "70552", "72148"]
            },
            "CT Scan": {
                "full_name": "Computed Tomography",
                "description": "X-ray imaging that creates cross-sectional views",
                "duration": "10-30 minutes",
                "preparation": "May need contrast, fasting for some scans",
                "when_needed": ["Head injury", "Abdominal pain", "Cancer screening"],
                "average_cost_range": "$500-$2,000",
                "urgent": True,
                "cpt_codes": ["70450", "74150", "71250"]
            },
            "Blood Tests": {
                "full_name": "Laboratory Blood Analysis",
                "description": "Analysis of blood samples for various conditions",
                "duration": "5-15 minutes",
                "preparation": "May need fasting for 8-12 hours",
                "when_needed": ["General checkup", "Diabetes screening", "Infection"],
                "average_cost_range": "$100-$400",
                "urgent": False,
                "cpt_codes": ["80053", "85025", "80061"]
            },
            "X-Ray": {
                "full_name": "Radiographic Imaging",
                "description": "Uses radiation to create images of bones and organs",
                "duration": "5-15 minutes",
                "preparation": "Remove jewelry and metal objects",
                "when_needed": ["Broken bones", "Chest pain", "Joint pain"],
                "average_cost_range": "$100-$400",
                "urgent": True,
                "cpt_codes": ["71020", "73610", "74020"]
            },
            "Ultrasound": {
                "full_name": "Sonography",
                "description": "Uses sound waves to create images",
                "duration": "15-45 minutes",
                "preparation": "May need full bladder for some scans",
                "when_needed": ["Pregnancy", "Abdominal pain", "Gallbladder issues"],
                "average_cost_range": "$200-$800",
                "urgent": False,
                "cpt_codes": ["76700", "76805", "93306"]
            },
            "Physical Examination": {
                "full_name": "Medical Physical Exam",
                "description": "Comprehensive health assessment by physician",
                "duration": "30-60 minutes",
                "preparation": "List current medications and symptoms",
                "when_needed": ["Annual checkup", "New symptoms", "Follow-up"],
                "average_cost_range": "$150-$500",
                "urgent": False,
                "cpt_codes": ["99213", "99214", "99395"]
            }
        }

    def _load_hospital_services(self):
        """Load hospital specialties and services information"""
        return {
            "Emergency Services": {
                "description": "24/7 emergency medical care",
                "typical_conditions": ["Heart attack", "Stroke", "Severe injuries", "Overdose"],
                "average_wait_time": "2-6 hours",
                "cost_range": "$500-$3000"
            },
            "Cardiology": {
                "description": "Heart and cardiovascular system care",
                "typical_conditions": ["Heart disease", "Chest pain", "High blood pressure"],
                "common_procedures": ["ECG", "Stress test", "Echocardiogram"],
                "specialist_required": True
            },
            "Orthopedics": {
                "description": "Bone, joint, and muscle care",
                "typical_conditions": ["Broken bones", "Joint pain", "Sports injuries"],
                "common_procedures": ["X-ray", "MRI", "CT scan"],
                "specialist_required": True
            },
            "Radiology": {
                "description": "Medical imaging services",
                "services": ["X-ray", "MRI", "CT scan", "Ultrasound", "Mammography"],
                "appointment_required": True,
                "same_day_available": True
            }
        }

    def process_message(self, message, context=None):
        """Enhanced message processing with intelligent conversation flow and context awareness"""
        message_lower = message.lower().strip()
        
        # Update conversation context with provided context
        if context:
            self.conversation_context.update(context)
        
        # Track conversation history
        self.conversation_context['previous_queries'].append({
            'message': message,
            'timestamp': datetime.now().isoformat()
        })
        
        # Extract entities from current message
        entities = self._extract_entities(message_lower)
        
        # Update context with newly extracted entities
        self._update_context_with_entities(entities)
        
        # Check if we have enough information to provide results
        if self._has_sufficient_context_for_analysis():
            return self._provide_direct_analysis(message_lower)
        
        # Analyze conversation flow for better reactivity
        self._analyze_conversation_flow(message_lower)

        # Use OpenAI if available, otherwise use enhanced natural conversation
        if self.openai_api_key:
            try:
                # Enhanced system prompt for healthcare assistant
                system_prompt = f"""You are FinHealth Bot, a specialized healthcare cost assistant. You help users save money on medical expenses across all 50 US states.
                
Your capabilities:
- Compare hospital prices for medical procedures
- Find the best hospitals in any US city
- Analyze insurance coverage for major plans
- Explain medical procedures and costs
- Find emergency care options
- Provide location-specific healthcare pricing

User context: {self.conversation_context}

Always be helpful, empathetic, and focus on saving the user money. If they mention a location, acknowledge it and offer specific help for that area. If they ask about procedures, provide pricing ranges and suggest finding local options."""
                
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": message}
                    ],
                    max_tokens=300,
                    temperature=0.7
                )
                assistant_message = response['choices'][0]['message']['content'].strip()
                return {
                    'type': 'ai_generated',
                    'message': assistant_message
                }
            except Exception as e:
                # Fallback to natural conversation system
                pass
        
        # Enhanced natural conversation fallback
        intent = self._analyze_intent(message_lower)
        
        # Generate intelligent response based on intent and context
        response = self._generate_response(intent, entities, message_lower)
        
        return response
    
    def _analyze_conversation_flow(self, message_lower):
        """Analyze conversation flow to improve responsiveness"""
        # Track conversation patterns for better context awareness
        previous_queries = self.conversation_context.get('previous_queries', [])
        
        if len(previous_queries) > 1:
            # Check if user is providing follow-up information
            last_query = previous_queries[-2]['message'].lower() if len(previous_queries) >= 2 else ""
            
            # If previous query asked for location and current message has location
            if any(word in last_query for word in ['city', 'location', 'where']) and self._has_location(message_lower):
                self.conversation_context['conversation_stage'] = 'location_provided'
            
            # If we had procedures in context and user provides location
            elif self.conversation_context.get('required_procedures') and self._has_location(message_lower):
                self.conversation_context['conversation_stage'] = 'ready_for_comparison'
            
            # If user is responding to suggestions
            elif any(word in message_lower for word in ['yes', 'sure', 'okay', 'please']):
                self.conversation_context['conversation_stage'] = 'affirmative_response'
        
        # Update conversation stage based on current content
        if self._has_location(message_lower) and self._has_procedure(message_lower):
            self.conversation_context['conversation_stage'] = 'complete_request'
        elif self._has_symptoms(message_lower):
            self.conversation_context['conversation_stage'] = 'symptom_analysis'
        elif self._has_insurance(message_lower):
            self.conversation_context['conversation_stage'] = 'insurance_inquiry'
    
    def _has_location(self, message_lower):
        """Check if message contains location information"""
        location_patterns = [
            r'\b([a-z]+\s*,\s*(texas|california|new york|florida|illinois|ohio|pennsylvania|michigan|georgia|north carolina|new jersey|virginia|washington|arizona|massachusetts|tennessee|indiana|missouri|maryland|wisconsin|colorado|minnesota|south carolina|alabama|louisiana|kentucky|oregon|oklahoma|connecticut|utah|iowa|nevada|arkansas|mississippi|kansas|new mexico|nebraska|west virginia|idaho|hawaii|new hampshire|maine|rhode island|montana|delaware|south dakota|north dakota|alaska|vermont|wyoming))\b',
            r'\b(\d{5})\b',  # ZIP codes
            r'\b(lubbock|houston|dallas|austin|san antonio|fort worth|el paso|arlington|corpus christi|plano|new york|los angeles|chicago|boston|miami|seattle|denver|atlanta|philadelphia|phoenix)\b'
        ]
        return any(re.search(pattern, message_lower) for pattern in location_patterns)
    
    def _has_procedure(self, message_lower):
        """Check if message contains medical procedure information"""
        procedure_patterns = [
            r'\b(ecg|ekg|electrocardiogram|x-ray|xray|mri|ct scan|cat scan|blood test|blood work|ultrasound|sonogram|physical exam|checkup)\b'
        ]
        return any(re.search(pattern, message_lower) for pattern in procedure_patterns)
    
    def _has_symptoms(self, message_lower):
        """Check if message contains symptom information"""
        symptom_patterns = [
            r'\b(chest pain|heart pain|headache|back pain|stomach pain|abdominal pain|joint pain|muscle pain|shortness of breath|difficulty breathing|dizziness|nausea|vomiting|fever|cough|sore throat|fatigue|weakness)\b'
        ]
        return any(re.search(pattern, message_lower) for pattern in symptom_patterns)
    
    def _has_insurance(self, message_lower):
        """Check if message contains insurance information"""
        insurance_patterns = [
            r'\b(unitedhealthcare|united health|aetna|blue cross|blue shield|cigna|humana|kaiser|medicare|medicaid|anthem|bcbs|insurance|coverage|plan)\b'
        ]
        return any(re.search(pattern, message_lower) for pattern in insurance_patterns)

    def _analyze_intent(self, message_lower):
        """Advanced natural language intent analysis"""
        # Check for location patterns first (cities, states, zip codes)
        location_patterns = [
            r'\b([a-z]+\s*,\s*(texas|california|new york|florida|illinois|ohio|pennsylvania|michigan|georgia|north carolina|new jersey|virginia|washington|arizona|massachusetts|tennessee|indiana|missouri|maryland|wisconsin|colorado|minnesota|south carolina|alabama|louisiana|kentucky|oregon|oklahoma|connecticut|utah|iowa|nevada|arkansas|mississippi|kansas|new mexico|nebraska|west virginia|idaho|hawaii|new hampshire|maine|rhode island|montana|delaware|south dakota|north dakota|alaska|vermont|wyoming))\b',
            r'\b(\d{5})\b',  # ZIP codes
            r'\b(lubbock|houston|dallas|austin|san antonio|fort worth|el paso|arlington|corpus christi|plano|irving|garland|laredo|amarillo|grand prairie|brownsville|pasadena|mesquite|mckinney|frisco|killeen|waco|midland|abilene|beaumont|round rock|richardson|lewisville|college station|pearland|tyler|denton|sugar land|carrollton|edinburg|bryan|pharr|mission|missouri city|temple|flower mound|baytown|harlingen|north richland hills|mansfield|cedar park|port arthur|san angelo|league city|longview|texas city|new braunfels|conroe|the woodlands|abilene|texas|tx)\b',  # Texas cities
            r'\b(new york|los angeles|chicago|houston|phoenix|philadelphia|san antonio|san diego|dallas|san jose|austin|jacksonville|fort worth|columbus|charlotte|san francisco|indianapolis|seattle|denver|washington|boston|el paso|detroit|nashville|portland|memphis|oklahoma city|las vegas|louisville|baltimore|milwaukee|albuquerque|tucson|fresno|mesa|sacramento|atlanta|kansas city|colorado springs|raleigh|omaha|miami|long beach|virginia beach|oakland|minneapolis|tulsa|cleveland|wichita|arlington)\b'
        ]
        
        # Check for medical procedures
        procedure_patterns = [
            r'\b(ecg|ekg|electrocardiogram|x-ray|xray|mri|ct scan|cat scan|blood test|blood work|ultrasound|sonogram|physical exam|checkup|stress test|colonoscopy|mammogram|endoscopy|biopsy)\b'
        ]
        
        # Check for symptoms
        symptom_patterns = [
            r'\b(chest pain|heart pain|headache|back pain|stomach pain|abdominal pain|joint pain|muscle pain|shortness of breath|difficulty breathing|dizziness|nausea|vomiting|fever|cough|sore throat|fatigue|weakness)\b'
        ]
        
        # Check for insurance
        insurance_patterns = [
            r'\b(unitedhealthcare|united health|aetna|blue cross|blue shield|cigna|humana|kaiser|medicare|medicaid|anthem|bcbs)\b'
        ]
        
        # Smart intent detection based on context and patterns
        if any(re.search(pattern, message_lower) for pattern in location_patterns):
            # If location is mentioned with procedure, it's a price inquiry
            if any(re.search(pattern, message_lower) for pattern in procedure_patterns):
                return 'location_procedure_inquiry'
            # If location is mentioned with insurance, it's insurance inquiry
            elif any(re.search(pattern, message_lower) for pattern in insurance_patterns):
                return 'location_insurance_inquiry'
            # Just location mentioned
            else:
                return 'location_response'
        
        # Check for procedure without location
        elif any(re.search(pattern, message_lower) for pattern in procedure_patterns):
            return 'procedure_location_request'
        
        # Check for insurance without location
        elif any(re.search(pattern, message_lower) for pattern in insurance_patterns):
            return 'insurance_location_request'
        
        # Check for symptoms
        elif any(re.search(pattern, message_lower) for pattern in symptom_patterns):
            return 'symptom_analysis'
        
        # Check for greetings
        elif any(word in message_lower for word in ['hello', 'hi', 'hey', 'good morning', 'good afternoon', 'good evening']):
            return 'greeting'
        
        # Check for emergencies
        elif any(word in message_lower for word in ['emergency', 'urgent', 'help', '911', 'ambulance']):
            return 'emergency'
        
        # Check for price/cost inquiries
        elif any(word in message_lower for word in ['cost', 'price', 'expensive', 'cheap', 'affordable', 'money', 'how much']):
            return 'price_inquiry'
        
        # Check for hospital inquiries
        elif any(word in message_lower for word in ['hospital', 'clinic', 'medical center', 'doctor', 'physician']):
            return 'hospital_inquiry'
        
        # Default to conversational response
        else:
            return 'conversational'

    def _extract_entities(self, message_lower):
        """Extract entities like cities, procedures, insurance plans"""
        entities = {
            'cities': [],
            'procedures': [],
            'insurance_plans': [],
            'symptoms': [],
            'numbers': []
        }
        
        # Extract cities (comprehensive US cities including any city, state pattern)
        city_patterns = [
            # Match any US city with potential state abbreviation
            r'\b([a-z\s]+),\s*[a-z]{2}\b',
            # Common major US cities by default (both city and city, state pattern)
            r'\b(aberdeen|abilene|akron|albany|albuquerque|anaheim|anchorage|ann arbor|antioch|arlington|athens|atlanta|augusta|austin|bakersfield|baltimore|baton rouge|beaumont|belmont|birmingham|boise|boston|bowling green|bridgeport|brownsville|buffalo|burbank|canton|cape coral|carrollton|cary|cedar rapids|champaign|charleston|charlotte|chattanooga|cherry hill|chesapeake|chicago|chula vista|cincinnati|clarksville|cleveland|colo springs|columbia|columbus|concord|coral springs|corpus christi|costa mesa|dallas|dayton|daytona beach|denton|denver|des moines|detroit|durham|edmond|el monte|el paso|elgin|elk grove|elkhart|erie|escondido|eugene|evansville|fairfield|fargo|fayetteville|fontana|fort collins|fort lauderdale|fort wayne|fort worth|fremont|fresno|frisco|fullerton|gainesville|garland|gilbert|glendale|grand prairie|grand rapids|greeley|green bay|greensboro|hampton|harrisburg|hartford|huntington beach|indianapolis|irving|jackson|jacksonville|joliet|kansas city|knoxville|lakeland|lakewood|lancaster|lansing|las vegas|lexington|lincoln|little rock|los angeles|louisville|lubbock|madison|manchester|mcallen|mckinney|medford|memphis|mesa|mesquite|miami|midland|milwaukee|minneapolis|minnetonka|modesto|montgomery|moreno valley|nampa|naperville|nashville|new haven|new orleans|new york|norfolk|norman|north las vegas|oakland|ocala|oceanside|oklahoma city|olathe|olympia|omaha|ontario|orange|orlando|overland park|oxnard|palm bay|pasadena|pembroke pines|peoria|philadelphia|phoenix|pittsburgh|plano|pomona|portland|providence|provo|raleigh|rancho cucamonga|reno|riverside|roanoke|rochester|rockford|roseville|sacramento|salem|salinas|salt lake city|san antonio|san bernardino|san diego|san francisco|san jose|san mateo|santa ana|santa clarita|santa maria|santa rosa|savannah|scottsdale|secaucus|seattle|shreveport|sioux falls|south bend|spokane|springfield|st louis|st paul|st petersburg|stanford|stockton|sunnyvale|syracuse|tacoma|tallahassee|tampa|temecula|tempe|thornton|toledo|topeka|torrance|tucson|tulsa|turlock|tyler|vallejo|vancouver|victorville|virginia beach|visalia|waco|warwick|washington|waterloo|west covina|west valley city|wichita|wilmington|winston-salem|wisconsin dells|woodbridge|yakima|yonkers|youngstown)\b'
        ]
        
        for pattern in city_patterns:
            matches = re.findall(pattern, message_lower)
            if matches:
                # Handle different match types
                if matches and isinstance(matches[0], str):
                    # Handle city, state pattern like "midland, tx" or "abbilyn, texas"
                    if ',' in message_lower:
                        city_state_pattern = r'\b([a-z\s]+),\s*([a-z]{2,})\b'
                        city_state_matches = re.findall(city_state_pattern, message_lower)
                        for city, state in city_state_matches:
                            city_name = city.strip().title()
                            entities['cities'].append(city_name)
                    else:
                        # For single city names
                        entities['cities'].extend([city.title() for city in matches if city])
        
        # Extract medical procedures with enhanced patterns
        procedure_patterns = [
            (r'\b(ecg|ekg|electrocardiogram)\b', 'ECG'),
            (r'\b(mri|magnetic resonance imaging?)\b', 'MRI'),
            (r'\b(ct scan|cat scan|computed tomography)\b', 'CT scan'),
            (r'\b(x-?ray|xray|radiograph)\b', 'X-ray'),
            (r'\b(blood test|blood work|lab work|laboratory)\b', 'Blood tests'),
            (r'\b(ultrasound|sonogram|sonography)\b', 'Ultrasound'),
            (r'\b(physical exam|checkup|physical examination)\b', 'Physical examination'),
            (r'\b(stress test|cardiac stress)\b', 'Stress test'),
            (r'\b(colonoscopy|colon screening)\b', 'Colonoscopy'),
            (r'\b(mammogram|mammography|breast exam)\b', 'Mammography'),
            (r'\b(endoscopy|scope)\b', 'Endoscopy'),
            (r'\b(bone density|dexa scan)\b', 'Bone density scan'),
            (r'\b(allergy test|allergy testing)\b', 'Allergy testing'),
            (r'\b(sleep study|sleep test)\b', 'Sleep study')
        ]
        
        for pattern, procedure_name in procedure_patterns:
            if re.search(pattern, message_lower):
                entities['procedures'].append(procedure_name)
        
        # Extract insurance plans
        insurance_patterns = [
            r'\b(aetna|blue cross|cigna|united|humana|kaiser)\b',
            r'\b(medicare|medicaid)\b'
        ]
        
        for pattern in insurance_patterns:
            matches = re.findall(pattern, message_lower)
            entities['insurance_plans'].extend(matches)
        
        # Extract symptoms
        symptom_patterns = [
            r'\b(chest pain|heart pain|cardiac)\b',
            r'\b(headache|head pain|migraine)\b',
            r'\b(back pain|spine|spinal)\b',
            r'\b(abdominal pain|stomach|belly)\b'
        ]
        
        for pattern in symptom_patterns:
            matches = re.findall(pattern, message_lower)
            entities['symptoms'].extend(matches)
        
        return entities

    def _update_context_with_entities(self, entities):
        """Update conversation context with extracted entities"""
        if entities['cities']:
            self.conversation_context['user_location'] = entities['cities'][0].title()
        
        if entities['procedures']:
            self.conversation_context['required_procedures'] = entities['procedures']
        
        if entities['insurance_plans']:
            self.conversation_context['insurance_plan'] = entities['insurance_plans'][0].title()
        
        if entities['symptoms']:
            self.conversation_context['current_symptoms'] = entities['symptoms']

    def _generate_response(self, intent, entities, message_lower):
        """Generate intelligent response based on intent and context"""
        # Check conversation stage for reactive responses
        stage = self.conversation_context.get('conversation_stage', 'initial')
        
        # React to conversation flow
        if stage == 'location_provided' and intent == 'location_response':
            return self._handle_follow_up_location_response(entities, message_lower)
        
        elif stage == 'ready_for_comparison' and self._has_location(message_lower):
            return self._handle_ready_comparison(entities, message_lower)
        
        elif stage == 'affirmative_response':
            return self._handle_affirmative_response(entities, message_lower)
        
        elif stage == 'complete_request':
            return self._handle_complete_request(entities, message_lower)
        
        # Default intent-based responses
        if intent == 'greeting':
            return self._handle_greeting()
        
        elif intent == 'location_response':
            return self._handle_location_response(entities, message_lower)
        
        elif intent == 'location_procedure_inquiry':
            return self._handle_location_procedure_inquiry(entities, message_lower)
        
        elif intent == 'location_insurance_inquiry':
            return self._handle_location_insurance_inquiry(entities, message_lower)
        
        elif intent == 'procedure_location_request':
            return self._handle_procedure_inquiry(entities)
        
        elif intent == 'insurance_location_request':
            return self._handle_insurance_inquiry(entities)
        
        elif intent == 'symptom_analysis':
            return self._handle_symptom_inquiry(entities, message_lower)
        
        elif intent == 'price_inquiry':
            return self._handle_price_inquiry(entities)
        
        elif intent == 'hospital_inquiry':
            return self._handle_hospital_inquiry(entities)
        
        elif intent == 'emergency':
            return self._handle_emergency()
        
        elif intent == 'conversational':
            return self._handle_conversational_response(message_lower, entities)
        
        else:
            return self._handle_general_inquiry()

    def _handle_greeting(self):
        """Handle greeting messages"""
        location = self.conversation_context.get('user_location')
        if location:
            return {
                'type': 'greeting_with_location',
                'message': f"Hello! Great to see you again! I remember you're in {location}. How can I help you save money on healthcare today?",
                'suggestions': [
                    "Compare hospital prices",
                    "Analyze insurance coverage", 
                    "Find emergency hospitals"
                ]
            }
        else:
            return {
                'type': 'greeting',
                'message': "Hello! I'm your FinHealth assistant. I can help you save money on healthcare costs across all 50 US states. What city are you in, and what can I help you with?",
                'suggestions': [
                    "I'm in [city name] and need medical help",
                    "Compare insurance plans",
                    "Find cheapest hospitals near me"
                ]
            }

    def _handle_symptom_inquiry(self, entities, message_lower):
        """Handle symptom-related inquiries"""
        # Analyze symptoms using medical analyzer
        condition = self.medical_analyzer.analyze_symptoms(message_lower)
        procedures = self.medical_analyzer.get_recommended_procedures(condition)
        
        self.conversation_context['diagnosed_condition'] = condition
        self.conversation_context['required_procedures'] = procedures
        
        location = self.conversation_context.get('user_location')
        
        response_msg = f"Based on your symptoms, you might be experiencing **{condition}**.\n\n"
        response_msg += "**Recommended procedures:**\n"
        
        for proc in procedures:
            if proc in self.procedure_database:
                proc_info = self.procedure_database[proc]
                response_msg += f"• **{proc}** ({proc_info['full_name']}) - {proc_info['average_cost_range']}\n"
                response_msg += f"  *{proc_info['description']}*\n"
        
        if location:
            response_msg += f"\n🏥 I can find the best prices for these procedures in {location}. Would you like me to compare hospitals?"
        else:
            response_msg += f"\n📍 What city are you in? I'll find the most affordable options for these procedures near you."
        
        return {
            'type': 'symptom_analysis',
            'message': response_msg,
            'condition': condition,
            'procedures': procedures,
            'location': location,
            'next_action': 'hospital_comparison' if location else 'location_request'
        }

    def _handle_price_inquiry(self, entities):
        """Handle price comparison requests - prioritize existing context"""
        # Prioritize existing context first, then fall back to entities
        location = self.conversation_context.get('user_location') or (entities['cities'][0].title() if entities['cities'] else None)
        procedures = self.conversation_context.get('required_procedures') or entities['procedures']
        insurance = self.conversation_context.get('insurance_plan')
        
        # If we don't have procedures from context or entities, try to extract from the current message
        if not procedures:
            procedures = ['Physical examination']  # Default fallback
        
        if location and procedures:
            # Get hospital comparison
            hospitals = self.hospital_data_manager.compare_hospitals(procedures, location)
            
            response_msg = f"💰 **Price Comparison for {', '.join(procedures)} in {location}**\n\n"
            
            if hospitals:
                cheapest = hospitals[0]
                most_expensive = hospitals[-1]
                
                response_msg += f"**🏆 Best Deal:** {cheapest['hospital']['name']}\n"
                response_msg += f"• Cash Price: ${cheapest['total_cash_cost']}\n"
                response_msg += f"• You Save: ${cheapest['total_savings_cash']}\n"
                response_msg += f"• Rating: ⭐ {cheapest['hospital']['rating']}/5\n"
                response_msg += f"• Wait Time: {cheapest['hospital']['average_wait_time']} minutes\n\n"
                
                # Add insurance information if available
                if insurance:
                    response_msg += f"**📋 With {insurance} Insurance:**\n"
                    response_msg += f"• Your out-of-pocket cost could be significantly lower\n"
                    response_msg += f"• Insurance typically covers 70-90% of procedure costs\n\n"
                
                response_msg += f"**💡 Price Range in {location}:**\n"
                response_msg += f"• Cheapest: ${cheapest['total_cash_cost']}\n"
                response_msg += f"• Most Expensive: ${most_expensive['total_cash_cost']}\n"
                response_msg += f"• **Potential Savings: ${most_expensive['total_cash_cost'] - cheapest['total_cash_cost']}**\n\n"
                
                response_msg += "Would you like to see the full comparison table or get directions to the best hospital?"
                
                return {
                    'type': 'price_comparison',
                    'message': response_msg,
                    'hospitals': hospitals[:5],  # Top 5 cheapest
                    'location': location,
                    'procedures': procedures,
                    'insurance': insurance
                }
            else:
                # Try to find nearby major cities if exact location doesn't have data
                major_texas_cities = ['Houston', 'Dallas', 'Austin', 'San Antonio', 'Fort Worth']
                if location and 'texas' in location.lower():
                    for city in major_texas_cities:
                        nearby_hospitals = self.hospital_data_manager.compare_hospitals(procedures, city)
                        if nearby_hospitals:
                            response_msg = f"I couldn't find data for {location}, but here are options in nearby {city}, Texas:\n\n"
                            cheapest = nearby_hospitals[0]
                            response_msg += f"**🏆 Best Option:** {cheapest['hospital']['name']}\n"
                            response_msg += f"• Cash Price: ${cheapest['total_cash_cost']}\n"
                            response_msg += f"• You Save: ${cheapest['total_savings_cash']}\n"
                            response_msg += f"• Rating: ⭐ {cheapest['hospital']['rating']}/5\n\n"
                            response_msg += f"Would you like to see more options in {city} or try another city?"
                            
                            return {
                                'type': 'nearby_options',
                                'message': response_msg,
                                'hospitals': nearby_hospitals[:3],
                                'suggested_location': city,
                                'original_location': location
                            }
                            break
                
                return {
                    'type': 'no_data',
                    'message': f"I couldn't find pricing data for {location}. Let me know a nearby major city, and I'll help you find the best deals!"
                }
        else:
            missing = []
            if not location:
                missing.append("your city")
            if not procedures:
                missing.append("the medical procedure you need")
            
            return {
                'type': 'missing_info',
                'message': f"To find the best prices, I need to know {' and '.join(missing)}. Can you provide that information?"
            }

    def _handle_insurance_inquiry(self, entities):
        """Handle insurance-related inquiries with detailed form collection"""
        insurance_plan = entities['insurance_plans'][0] if entities['insurance_plans'] else None
        
        # Check if we have location info
        location = entities['cities'][0].title() if entities['cities'] else self.conversation_context.get('user_location')
        
        if insurance_plan and location:
            # Get detailed insurance comparison for specific location
            return self._generate_location_insurance_comparison(insurance_plan, location)
        
        elif insurance_plan:
            # Get detailed insurance information but ask for location
            plan_info = self.insurance_database.get(insurance_plan.title())
            
            if plan_info:
                response_msg = f"📋 **{insurance_plan.title()} Insurance Information**\n\n"
                response_msg += f"**Plan Options:** {', '.join(plan_info['plans'])}\n"
                response_msg += f"**Coverage Area:** {plan_info['coverage_areas']}\n"
                response_msg += f"**Average Premium:** {plan_info['average_premium']}\n"
                response_msg += f"**Average Deductible:** {plan_info['average_deductible']}\n"
                response_msg += f"**Network Size:** {plan_info['network_size']}\n\n"
                
                response_msg += "📍 **To provide detailed cost comparison, please provide:**\n"
                response_msg += "• Your **State**\n"
                response_msg += "• Your **City**\n"
                response_msg += "• Your **ZIP Code** (optional for better accuracy)\n\n"
                response_msg += "Example: 'I'm in Dallas, Texas 75201' or 'Houston TX'"
                
                return {
                    'type': 'insurance_location_request',
                    'message': response_msg,
                    'insurance_plan': insurance_plan,
                    'plan_info': plan_info,
                    'next_step': 'location_collection'
                }
        
        # Show insurance form for detailed comparison
        response_msg = "🏥 **Insurance Comparison - Please Provide Details**\n\n"
        response_msg += "To give you the most accurate insurance comparison, I need:\n\n"
        response_msg += "📋 **Insurance Plan:** (e.g., UnitedHealthcare, Aetna, Blue Cross Blue Shield)\n"
        response_msg += "📍 **State:** (e.g., Texas, California, New York)\n"
        response_msg += "🏙️ **City:** (e.g., Dallas, Los Angeles, Chicago)\n"
        response_msg += "📮 **ZIP Code:** (optional, for precise local rates)\n\n"
        
        response_msg += "**Available Insurance Plans:**\n"
        for plan_name, info in list(self.insurance_database.items())[:6]:
            response_msg += f"• **{plan_name}** - {info['coverage_areas']}\n"
        
        response_msg += "\n💡 **Example:** 'I have UnitedHealthcare in Dallas, Texas 75201'\n"
        response_msg += "or 'Compare Aetna insurance in Chicago IL'"
        
        return {
            'type': 'insurance_form_request',
            'message': response_msg,
            'available_plans': list(self.insurance_database.keys()),
            'form_fields': ['insurance_plan', 'state', 'city', 'zip_code']
        }

    def _handle_hospital_inquiry(self, entities):
        """Handle hospital-related inquiries"""
        location = entities['cities'][0].title() if entities['cities'] else self.conversation_context.get('user_location')
        
        if location:
            # Get hospitals in the area
            hospitals = self.hospital_data_manager.find_city_hospitals(location)
            
            if hospitals:
                response_msg = f"🏥 **Hospitals in {location}** ({len(hospitals)} found)\n\n"
                
                # Show top-rated hospitals
                sorted_hospitals = sorted(hospitals, key=lambda x: x.get('rating', 0), reverse=True)[:5]
                
                for i, hospital in enumerate(sorted_hospitals, 1):
                    response_msg += f"**{i}. {hospital['name']}**\n"
                    response_msg += f"   ⭐ Rating: {hospital['rating']}/5\n"
                    response_msg += f"   🚨 Emergency: {'Yes' if hospital['emergency'] else 'No'}\n"
                    response_msg += f"   ⏱️ Avg Wait: {hospital['average_wait_time']} minutes\n"
                    response_msg += f"   🏢 Specialties: {', '.join(hospital['specialties'][:3])}\n"
                    response_msg += f"   💳 Accepts: {', '.join(hospital['insurance_accepted'][:3])}\n\n"
                
                response_msg += "💡 Would you like pricing comparison for specific procedures at these hospitals?"
                
                return {
                    'type': 'hospital_list',
                    'message': response_msg,
                    'hospitals': sorted_hospitals,
                    'location': location
                }
            else:
                return {
                    'type': 'no_hospitals',
                    'message': f"I couldn't find hospital data for {location}. Could you try a nearby major city?"
                }
        else:
            return {
                'type': 'location_needed',
                'message': "🌎 What city are you in? I can find hospitals and medical facilities in any US city, from major metros to smaller towns like Lubbock, Texas!"
            }

    def _handle_emergency(self):
        """Handle emergency situations"""
        location = self.conversation_context.get('user_location')
        
        response_msg = "🚨 **EMERGENCY MEDICAL SITUATIONS**\n\n"
        response_msg += "⚠️ **If this is a life-threatening emergency, call 911 immediately!**\n\n"
        
        if location:
            emergency_hospitals = self.hospital_data_manager.get_emergency_hospitals(location)
            if emergency_hospitals:
                response_msg += f"**Emergency Hospitals in {location}:**\n"
                for hospital in emergency_hospitals[:3]:
                    response_msg += f"• **{hospital['name']}** - {hospital['phone']}\n"
                    response_msg += f"  📍 {hospital['address']}\n\n"
        
        response_msg += "**Emergency Room Costs:**\n"
        response_msg += "• Emergency visit: $500 - $3,000\n"
        response_msg += "• Critical care: $1,500 - $10,000+\n"
        response_msg += "• Always call ahead if possible\n\n"
        response_msg += "💡 For non-emergency urgent care, I can find cheaper alternatives near you!"
        
        return {
            'type': 'emergency_info',
            'message': response_msg,
            'location': location
        }

    def _handle_procedure_inquiry(self, entities):
        """Handle medical procedure inquiries with enhanced location handling"""
        procedures = entities['procedures'] or self.conversation_context.get('required_procedures')
        location = entities['cities'][0].title() if entities['cities'] else self.conversation_context.get('user_location')
        
        if procedures and location:
            # Both procedure and location available - show comparison
            return self._generate_procedure_location_comparison(procedures, location)
        
        elif procedures:
            # Procedure available but no location - ask for location
            proc_names = [proc.upper() for proc in procedures]
            response_msg = f"🔬 **{', '.join(proc_names)} Information**\n\n"
            
            for proc in procedures[:3]:  # Limit to 3 procedures
                proc_key = self._find_procedure_key(proc)
                if proc_key:
                    info = self.procedure_database[proc_key]
                    response_msg += f"**{proc_key} - {info['full_name']}**\n"
                    response_msg += f"📋 {info['description']}\n"
                    response_msg += f"⏱️ Duration: {info['duration']}\n"
                    response_msg += f"💰 National Range: {info['average_cost_range']}\n"
                    response_msg += f"📝 Preparation: {info['preparation']}\n\n"
            
            response_msg += "📍 **To find the best prices in your area, please tell me:**\n"
            response_msg += "• Your **City and State** (e.g., Dallas, Texas)\n"
            response_msg += "• Or just your **ZIP Code**\n\n"
            response_msg += "💡 I'll then show you the cheapest hospitals for these procedures!"
            
            return {
                'type': 'procedure_location_request',
                'message': response_msg,
                'procedures': procedures,
                'next_step': 'location_collection'
            }
        else:
            response_msg = "🔬 **Popular Medical Procedures:**\n\n"
            popular_procedures = ['ECG/EKG', 'X-Ray', 'MRI', 'Blood Tests', 'CT Scan', 'Ultrasound']
            
            for proc_name in popular_procedures:
                if proc_name in self.procedure_database:
                    info = self.procedure_database[proc_name]
                    response_msg += f"• **{proc_name}** - {info['average_cost_range']}\n"
            
            response_msg += "\n💡 Which procedure do you need pricing for? Just tell me the name and your city!"
            
            return {
                'type': 'procedure_options',
                'message': response_msg,
                'available_procedures': popular_procedures
            }

    def _handle_comparison_request(self, entities):
        """Handle comparison requests"""
        location = entities['cities'][0].title() if entities['cities'] else self.conversation_context.get('user_location')
        procedures = entities['procedures'] or self.conversation_context.get('required_procedures', ['Physical examination'])
        
        if location and procedures:
            hospitals = self.hospital_data_manager.compare_hospitals(procedures, location)
            
            if hospitals:
                return {
                    'type': 'detailed_comparison',
                    'message': f"📊 Here's a detailed comparison of {len(hospitals)} hospitals in {location} for {', '.join(procedures)}:",
                    'hospitals': hospitals,
                    'location': location,
                    'procedures': procedures,
                    'action': 'show_comparison_table'
                }
        
        return {
            'type': 'comparison_help',
            'message': "I can compare hospitals, insurance plans, and procedure costs. What specifically would you like me to compare? Please include your city and the medical procedure you need."
        }

    def _handle_general_inquiry(self):
        """Handle general inquiries"""
        return {
            'type': 'general_help',
            'message': "I'm your comprehensive healthcare cost assistant! I can help you with:\n\n💰 **Compare hospital prices** across all 50 US states\n🏥 **Find best hospitals** with ratings and specialties\n📋 **Analyze insurance coverage** for 15+ major plans\n🔬 **Explain medical procedures** and their costs\n🚨 **Emergency hospital finder** in your area\n\nWhat would you like help with today? Just tell me your city and what you need!"
        }

    def _handle_custom_inquiry(self, message_lower):
        """Handle custom/general inquiries with natural language understanding"""
        location = self.conversation_context.get('user_location', 'your area')
        
        # Enhanced natural language processing for specific queries
        if any(word in message_lower for word in ['how much', 'cost', 'price', 'expensive']):
            return {
                'type': 'cost_inquiry',
                'message': f"I'd love to help you find the best healthcare prices! To give you accurate costs in {location}, could you tell me what specific medical procedure or service you need? For example, 'ECG', 'blood test', 'MRI', or 'doctor visit'?"
            }
        
        elif any(word in message_lower for word in ['where', 'find', 'hospital', 'clinic']):
            return {
                'type': 'location_help',
                'message': f"I can help you find the best medical facilities! In {location}, I have data on hospitals, clinics, and medical centers. What type of medical care are you looking for? Emergency care, routine checkup, specialist visit, or diagnostic tests?"
            }
        
        elif any(word in message_lower for word in ['insurance', 'coverage', 'plan']):
            return {
                'type': 'insurance_help',
                'message': "I can analyze insurance coverage and help you save money! Which insurance plan do you have? I work with UnitedHealthcare, Aetna, Blue Cross Blue Shield, Cigna, Humana, Kaiser Permanente, Medicare, Medicaid, and many others."
            }
        
        elif any(word in message_lower for word in ['sick', 'hurt', 'pain', 'feel']):
            return {
                'type': 'symptom_help',
                'message': "I'm sorry you're not feeling well. While I can't provide medical diagnosis, I can help you find affordable healthcare options. Could you describe what's bothering you? For example, 'chest pain', 'headache', 'stomach pain', or 'injury'? I'll suggest appropriate medical procedures and find the best prices."
            }
        
        elif any(word in message_lower for word in ['emergency', 'urgent', 'now', '911']):
            return self._handle_emergency()
        
        else:
            # Generic helpful response
            return {
                'type': 'general_assistance',
                'message': f"I'm your healthcare cost assistant! I can help you save money on medical expenses in {location} and across all 50 states. Here's what I can do:\n\n💰 Compare hospital prices for any procedure\n🏥 Find the best hospitals near you\n📋 Analyze your insurance coverage\n🔬 Explain medical procedures and costs\n🚨 Find emergency care options\n\nWhat would you like help with today? Just describe what you need in your own words!",
                'suggestions': [
                    "Find cheapest hospitals for blood test",
                    "Compare MRI prices in my area", 
                    "Check my insurance coverage",
                    "I have chest pain, what should I do?"
                ]
            }

    def _generate_location_insurance_comparison(self, insurance_plan, location):
        """Generate detailed insurance comparison for specific location"""
        plan_info = self.insurance_database.get(insurance_plan.title())
        
        if not plan_info:
            return {
                'type': 'unknown_insurance',
                'message': f"I couldn't find information for {insurance_plan}. Please check the spelling or choose from our supported plans."
            }
        
        network_hospitals = self.hospital_data_manager.find_insurance_hospitals(location, insurance_plan)
        
        response_msg = f"📋 **{insurance_plan.title()} Coverage Analysis for {location}**\n\n"
        
        # Plan details
        response_msg += f"**📊 Plan Overview:**\n"
        response_msg += f"• Premium: {plan_info['average_premium']}\n"
        response_msg += f"• Deductible: {plan_info['average_deductible']}\n"
        response_msg += f"• Network: {plan_info['network_size']}\n"
        response_msg += f"• Contact: {plan_info['customer_service']}\n\n"
        
        # Local network hospitals
        if network_hospitals:
            response_msg += f"**🏥 In-Network Hospitals in {location}:** ({len(network_hospitals)} found)\n"
            for hospital in network_hospitals[:5]:
                response_msg += f"• **{hospital['name']}** (⭐ {hospital['rating']}/5)\n"
                response_msg += f"  📍 {hospital['address']}\n"
                response_msg += f"  📞 {hospital['phone']}\n\n"
        else:
            response_msg += f"**⚠️ Network Coverage:** No specific in-network hospitals found for {location}. This may indicate limited local coverage.\n\n"
        
        # Cost comparison for common procedures
        common_procedures = ['ECG', 'Blood tests', 'X-ray', 'Physical examination']
        response_msg += f"**💰 Estimated Costs in {location}:**\n"
        
        for proc in common_procedures:
            if proc in self.procedure_database:
                proc_info = self.procedure_database[proc]
                estimated_cost = self._estimate_insurance_cost(proc_info['average_cost_range'], plan_info)
                response_msg += f"• **{proc}:** {estimated_cost} (with insurance)\n"
        
        response_msg += f"\n💡 **Recommendations:**\n"
        response_msg += f"• Compare with other plans for best value\n"
        response_msg += f"• Check if your preferred doctors are in-network\n"
        response_msg += f"• Consider urgent care for non-emergency visits\n\n"
        
        response_msg += "Would you like me to compare this with other insurance plans or find specific procedure costs?"
        
        return {
            'type': 'insurance_location_analysis',
            'message': response_msg,
            'insurance_plan': insurance_plan,
            'location': location,
            'network_hospitals': network_hospitals,
            'plan_info': plan_info
        }
    
    def _estimate_insurance_cost(self, cost_range, plan_info):
        """Estimate insurance cost based on plan deductible"""
        costs = re.findall(r'\$(\d+)', cost_range)
        if len(costs) >= 2:
            low_cost = int(costs[0])
            high_cost = int(costs[1])
            avg_cost = (low_cost + high_cost) / 2
            
            deductible = int(re.findall(r'\$(\d+)', plan_info['average_deductible'])[0])
            
            if avg_cost < deductible:
                estimated = f"${int(avg_cost)} (full cost - toward deductible)"
            else:
                copay = int(avg_cost * 0.2)  
                estimated = f"${copay} (after deductible)"
            
            return estimated
        
        return "Contact insurance for estimate"

    def _handle_location_response(self, entities, message_lower):
        """Handle when user just provides location information"""
        location = entities['cities'][0].title() if entities['cities'] else None
        
        if location:
            self.conversation_context['user_location'] = location
            
            # Check if we had previous context that needs location
            required_procedures = self.conversation_context.get('required_procedures')
            
            if required_procedures:
                # User previously asked about procedures, now provided location
                return self._generate_procedure_location_comparison(required_procedures, location)
            else:
                # Fresh location input
                response_msg = f"Perfect! I've noted you're in {location}. I'm your healthcare cost assistant! I can help you save money on medical expenses in {location} and across all 50 states. Here's what I can do:\n\n💰 Compare hospital prices for any procedure\n🏥 Find the best hospitals near you\n📋 Analyze your insurance coverage\n🔬 Explain medical procedures and costs\n🚨 Find emergency care options\n\nWhat would you like help with today? Just describe what you need in your own words!"
                
                return {
                    'type': 'location_confirmed',
                    'message': response_msg,
                    'location': location,
                    'suggestions': [
                        f"Find cheapest hospitals for blood test in {location}",
                        f"Compare MRI prices in {location}", 
                        f"Check insurance coverage in {location}",
                        "I have chest pain, what should I do?"
                    ]
                }
        
        return {
            'type': 'location_unclear',
            'message': "I didn't catch your location clearly. Could you tell me your city and state? For example: 'Dallas, Texas' or 'Chicago, Illinois'"
        }

    def _handle_location_procedure_inquiry(self, entities, message_lower):
        """Handle when user provides both location and procedure in same message"""
        location = entities['cities'][0].title() if entities['cities'] else None
        procedures = entities['procedures']
        
        if location and procedures:
            return self._generate_procedure_location_comparison(procedures, location)
        
        return {
            'type': 'incomplete_request',
            'message': "I understand you want procedure pricing. Could you please specify both the procedure (like ECG, MRI, blood test) and your city?"
        }

    def _handle_location_insurance_inquiry(self, entities, message_lower):
        """Handle when user provides both location and insurance in same message"""
        location = entities['cities'][0].title() if entities['cities'] else None
        insurance_plans = entities['insurance_plans']
        
        if location and insurance_plans:
            return self._generate_location_insurance_comparison(insurance_plans[0], location)
        
        return {
            'type': 'incomplete_insurance_request',
            'message': "I understand you want insurance information. Could you please specify both your insurance plan and your city?"
        }

    def _handle_conversational_response(self, message_lower, entities):
        """Handle conversational responses with natural language understanding"""
        location = self.conversation_context.get('user_location', 'your area')
        
        # Enhanced natural language understanding
        if any(word in message_lower for word in ['thanks', 'thank you', 'appreciate']):
            return {
                'type': 'gratitude_response',
                'message': f"You're very welcome! I'm here whenever you need help saving money on healthcare in {location}. Is there anything else I can help you with today?"
            }
        
        elif any(word in message_lower for word in ['no', 'nothing', 'that\'s all']):
            return {
                'type': 'conversation_end',
                'message': "Perfect! Remember, I'm always here to help you save money on healthcare costs. Take care and feel free to ask me anything anytime!"
            }
        
        elif any(word in message_lower for word in ['yes', 'sure', 'okay', 'ok']):
            # Check context for what they're agreeing to
            required_procedures = self.conversation_context.get('required_procedures')
            if required_procedures and location != 'your area':
                return self._generate_procedure_location_comparison(required_procedures, location)
            else:
                return {
                    'type': 'affirmative_response',
                    'message': "Great! What specific medical information or pricing would you like me to help you with?"
                }
        
        elif any(word in message_lower for word in ['how', 'what', 'when', 'where', 'why']):
            if 'work' in message_lower:
                return {
                    'type': 'how_it_works',
                    'message': "Here's how I help you save money on healthcare:\n\n1️⃣ **Tell me your location** (city/state)\n2️⃣ **Describe what you need** (symptoms, procedures, insurance)\n3️⃣ **I find the best prices** at local hospitals and clinics\n4️⃣ **You save money** by choosing the most affordable option!\n\nI have data on hospitals in all 50 states, from major cities to smaller towns. What would you like help with?"
                }
            else:
                return {
                    'type': 'general_question',
                    'message': f"I'd be happy to help answer your question! I specialize in healthcare costs and can help you with:\n\n💰 Medical procedure pricing\n🏥 Hospital comparisons\n📋 Insurance coverage analysis\n🔬 Medical procedure explanations\n\nWhat specifically would you like to know about healthcare in {location}?"
                }
        
        else:
            # Default conversational response
            return {
                'type': 'conversational',
                'message': f"I'm here to help you save money on healthcare! I can help you with medical costs in {location} and across all 50 states. What health-related question or concern can I assist you with today?",
                'suggestions': [
                    "Find hospital prices for medical procedures",
                    "Compare insurance plans",
                    "Explain medical procedures and costs",
                    "Find emergency hospitals near me"
                ]
            }

    def _find_procedure_key(self, procedure):
        """Find the correct procedure key in database"""
        procedure_lower = procedure.lower()
        
        # Map common variations to database keys
        procedure_mapping = {
            'ecg': 'ECG/EKG',
            'ekg': 'ECG/EKG',
            'electrocardiogram': 'ECG/EKG',
            'x-ray': 'X-Ray',
            'xray': 'X-Ray',
            'x ray': 'X-Ray',
            'mri': 'MRI',
            'magnetic resonance': 'MRI',
            'blood test': 'Blood Tests',
            'blood tests': 'Blood Tests',
            'blood work': 'Blood Tests',
            'ct scan': 'CT Scan',
            'cat scan': 'CT Scan',
            'ultrasound': 'Ultrasound',
            'sonogram': 'Ultrasound',
            'physical exam': 'Physical Examination',
            'physical examination': 'Physical Examination',
            'checkup': 'Physical Examination'
        }
        
        # Check direct mapping first
        if procedure_lower in procedure_mapping:
            return procedure_mapping[procedure_lower]
        
        # Check if it exists directly in database
        for key in self.procedure_database.keys():
            if procedure_lower in key.lower():
                return key
        
        return None

    def _generate_procedure_location_comparison(self, procedures, location):
        """Generate detailed procedure price comparison for location"""
        # Get hospital comparison
        hospitals = self.hospital_data_manager.compare_hospitals(procedures, location)
        
        if hospitals:
            response_msg = f"🔬 **{', '.join(procedures)} Pricing in {location}**\n\n"
            
            # Best value summary
            cheapest = hospitals[0]
            most_expensive = hospitals[-1]
            
            response_msg += f"**💰 Price Range:**\n"
            response_msg += f"• Cheapest: ${cheapest['total_cash_cost']} at {cheapest['hospital']['name']}\n"
            response_msg += f"• Most Expensive: ${most_expensive['total_cash_cost']} at {most_expensive['hospital']['name']}\n"
            response_msg += f"• **You can save up to ${most_expensive['total_cash_cost'] - cheapest['total_cash_cost']}** by choosing wisely!\n\n"
            
            # Procedure details
            for proc in procedures[:2]:  # Limit to 2 procedures for readability
                proc_key = self._find_procedure_key(proc)
                if proc_key and proc_key in self.procedure_database:
                    info = self.procedure_database[proc_key]
                    response_msg += f"**{proc_key} Details:**\n"
                    response_msg += f"📝 {info['description']}\n"
                    response_msg += f"⏱️ Duration: {info['duration']}\n"
                    response_msg += f"📋 Preparation: {info['preparation']}\n\n"
            
            response_msg += "Would you like to see the detailed hospital comparison table or check insurance coverage for these procedures?"
            
            return {
                'type': 'procedure_location_analysis',
                'message': response_msg,
                'hospitals': hospitals[:5],  # Top 5 results
                'location': location,
                'procedures': procedures,
                'action': 'show_detailed_table'
            }
        else:
            return {
                'type': 'no_procedure_data',
                'message': f"I couldn't find pricing data for {', '.join(procedures)} in {location}. Could you try a nearby major city, or let me know if you need a different procedure?"
            }

    def _has_sufficient_context_for_analysis(self):
        """Check if we have enough context to provide direct analysis"""
        location = self.conversation_context.get('user_location')
        procedures = self.conversation_context.get('required_procedures')
        
        # If we have both location and procedures, we can provide analysis
        return bool(location and procedures)
    
    def _provide_direct_analysis(self, message_lower):
        """Provide direct analysis when we have sufficient context"""
        location = self.conversation_context.get('user_location')
        procedures = self.conversation_context.get('required_procedures')
        insurance = self.conversation_context.get('insurance_plan')
        
        # Check if user is asking for price comparison specifically
        if any(word in message_lower for word in ['price', 'cost', 'comparison', 'compare', 'cheaper', 'affordable']):
            hospitals = self.hospital_data_manager.compare_hospitals(procedures, location)
            
            if hospitals:
                response_msg = f"💰 **Price Comparison for {', '.join(procedures)} in {location}**\n\n"
                
                cheapest = hospitals[0]
                most_expensive = hospitals[-1]
                
                response_msg += f"**🏆 Best Deal:** {cheapest['hospital']['name']}\n"
                response_msg += f"• Cash Price: ${cheapest['total_cash_cost']}\n"
                response_msg += f"• You Save: ${cheapest['total_savings_cash']}\n"
                response_msg += f"• Rating: ⭐ {cheapest['hospital']['rating']}/5\n"
                response_msg += f"• Wait Time: {cheapest['hospital']['average_wait_time']} minutes\n\n"
                
                if insurance:
                    coverage_analysis = self.insurance_analyzer.analyze_coverage(procedures, insurance, cheapest['hospital']['name'])
                    response_msg += f"**📋 With {insurance} Insurance:**\n"
                    response_msg += f"• Your estimated cost could be lower with insurance coverage\n\n"
                
                response_msg += f"**💡 Price Range in {location}:**\n"
                response_msg += f"• Cheapest: ${cheapest['total_cash_cost']}\n"
                response_msg += f"• Most Expensive: ${most_expensive['total_cash_cost']}\n"
                response_msg += f"• **You could save up to ${most_expensive['total_cash_cost'] - cheapest['total_cash_cost']}** by choosing the right hospital!\n\n"
                
                response_msg += "Would you like to see the full comparison table or get directions to the best hospital?"
                
                return {
                    'type': 'direct_price_analysis',
                    'message': response_msg,
                    'hospitals': hospitals[:5],
                    'location': location,
                    'procedures': procedures,
                    'insurance': insurance
                }
            else:
                return {
                    'type': 'no_data_available',
                    'message': f"I couldn't find specific pricing data for {', '.join(procedures)} in {location}. Let me try a nearby major city, or you can ask about a different procedure."
                }
        
        # For other queries with sufficient context, provide helpful response
        else:
            response_msg = f"I have your information: {location} for {', '.join(procedures)}"
            if insurance:
                response_msg += f" with {insurance} insurance"
            response_msg += ".\n\nWhat would you like me to help you with?\n\n"
            response_msg += "💰 Compare hospital prices\n"
            response_msg += "🏥 Find best hospitals nearby\n"
            response_msg += "📋 Analyze insurance coverage\n"
            response_msg += "🚨 Find emergency hospitals"
            
            return {
                'type': 'context_ready',
                'message': response_msg,
                'location': location,
                'procedures': procedures,
                'insurance': insurance,
                'suggestions': [
                    "Show me price comparison",
                    "Find best hospitals",
                    "Check insurance coverage",
                    "Emergency hospitals"
                ]
            }
    
    def _handle_follow_up_location_response(self, entities, message_lower):
        """Handle follow-up when user provides location after being asked"""
        location = entities['cities'][0].title() if entities['cities'] else None
        
        if location:
            self.conversation_context['user_location'] = location
            
            # Check if we had procedures in context
            procedures = self.conversation_context.get('required_procedures')
            
            if procedures:
                return self._generate_procedure_location_comparison(procedures, location)
            else:
                return {
                    'type': 'location_updated',
                    'message': f"Great! I've updated your location to {location}. What medical procedure or service would you like pricing information for?"
                }
        
        return {
            'type': 'location_unclear',
            'message': "I didn't catch your location clearly. Could you tell me your city and state? For example: 'Dallas, Texas' or 'Chicago, Illinois'"
        }
    
    def _handle_ready_comparison(self, entities, message_lower):
        """Handle when user is ready for comparison"""
        location = entities['cities'][0].title() if entities['cities'] else self.conversation_context.get('user_location')
        procedures = self.conversation_context.get('required_procedures', [])
        
        if location and procedures:
            return self._generate_procedure_location_comparison(procedures, location)
        
        return {
            'type': 'need_more_info',
            'message': "I need both your location and the medical procedure to provide accurate pricing. What information can you provide?"
        }
    
    def _handle_affirmative_response(self, entities, message_lower):
        """Handle when user gives affirmative response (yes, sure, okay)"""
        # Check what they might be agreeing to based on context
        location = self.conversation_context.get('user_location')
        procedures = self.conversation_context.get('required_procedures')
        
        if location and procedures:
            return self._generate_procedure_location_comparison(procedures, location)
        elif procedures and not location:
            return {
                'type': 'need_location',
                'message': f"Perfect! I understand you need pricing for {', '.join(procedures)}. What city are you in so I can find the best local prices?"
            }
        else:
            return {
                'type': 'affirmative_general',
                'message': "Great! What can I help you with? I can compare hospital prices, analyze insurance coverage, or find medical facilities in your area."
            }
    
    def _handle_complete_request(self, entities, message_lower):
        """Handle when user provides complete request with location and procedure"""
        location = entities['cities'][0].title() if entities['cities'] else self.conversation_context.get('user_location')
        procedures = entities['procedures'] or self.conversation_context.get('required_procedures')
        
        if location and procedures:
            return self._generate_procedure_location_comparison(procedures, location)
        
        return {
            'type': 'incomplete_request',
            'message': "I need both your location and the medical procedure to provide accurate pricing. Could you provide the missing information?"
        }

    def get_conversation_summary(self):
        """Get current conversation context summary"""
        return {
            'location': self.conversation_context.get('user_location'),
            'condition': self.conversation_context.get('diagnosed_condition'),
            'procedures': self.conversation_context.get('required_procedures'),
            'insurance': self.conversation_context.get('insurance_plan'),
            'stage': self.conversation_context.get('conversation_stage'),
            'query_count': len(self.conversation_context.get('previous_queries', []))
        }
