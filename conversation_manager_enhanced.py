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
        if self._has_sufficient_context_for_analysis(message_lower):
            return self._provide_direct_analysis(message_lower)
        
        # Analyze conversation flow for better reactivity
        self._analyze_conversation_flow(message_lower)

        # Enhanced natural conversation
        intent = self._analyze_intent(message_lower)
        
        # Generate intelligent response based on intent and context
        response = self._generate_response(intent, entities, message_lower)
        
        return response

    def _has_sufficient_context_for_analysis(self, message_lower):
        """Check if we have enough context to provide direct analysis"""
        location = self.conversation_context.get('user_location')
        procedures = self.conversation_context.get('required_procedures')
        
        # If we have both location and procedures, and user is asking for pricing/comparison
        pricing_keywords = ['price', 'cost', 'comparison', 'compare', 'cheaper', 'affordable', 'pricing', 'information']
        has_pricing_request = any(word in message_lower for word in pricing_keywords)
        
        return bool(location and procedures and has_pricing_request)
    
    def _provide_direct_analysis(self, message_lower):
        """Provide direct analysis when we have sufficient context"""
        location = self.conversation_context.get('user_location')
        procedures = self.conversation_context.get('required_procedures')
        insurance = self.conversation_context.get('insurance_plan')
        
        # Get hospital comparison
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
                response_msg += f"**📋 With {insurance} Insurance:**\n"
                response_msg += f"• Your estimated cost could be lower with insurance coverage\n"
                response_msg += f"• Insurance typically covers 70-90% of procedure costs\n\n"
            
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
            # Try to find nearby major cities if exact location doesn't have data
            if location and 'texas' in location.lower():
                major_texas_cities = ['Houston', 'Dallas', 'Austin', 'San Antonio', 'Fort Worth', 'Lubbock']
                for city in major_texas_cities:
                    nearby_hospitals = self.hospital_data_manager.compare_hospitals(procedures, city)
                    if nearby_hospitals:
                        response_msg = f"I found pricing data for {city}, Texas (near {location}):\n\n"
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
                'type': 'no_data_available',
                'message': f"I couldn't find specific pricing data for {', '.join(procedures)} in {location}. Let me try a nearby major city, or you can ask about a different procedure."
            }

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
        elif any(word in message_lower for word in ['cost', 'price', 'expensive', 'cheap', 'affordable', 'money', 'how much', 'pricing', 'comparison', 'compare']):
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
            r'\b(lubbock|houston|dallas|austin|san antonio|fort worth|el paso|arlington|corpus christi|plano|irving|garland|laredo|amarillo|grand prairie|brownsville|pasadena|mesquite|mckinney|frisco|killeen|waco|midland|abilene|beaumont|round rock|richardson|lewisville|college station|pearland|tyler|denton|sugar land|carrollton|edinburg|bryan|pharr|mission|missouri city|temple|flower mound|baytown|harlingen|north richland hills|mansfield|cedar park|port arthur|san angelo|league city|longview|texas city|new braunfels|conroe|the woodlands|new york|los angeles|chicago|boston|miami|seattle|denver|atlanta|philadelphia|phoenix)\b'
        ]
        
        for pattern in city_patterns:
            matches = re.findall(pattern, message_lower)
            if matches:
                # Handle different match types
                if matches and isinstance(matches[0], str):
                    # Handle city, state pattern like "lubbock, tx" or "lubbock, texas"
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
        
        # Default intent-based responses
        if intent == 'greeting':
            return self._handle_greeting()
        
        elif intent == 'location_response':
            return self._handle_location_response(entities, message_lower)
        
        elif intent == 'location_procedure_inquiry':
            return self._handle_location_procedure_inquiry(entities, message_lower)
        
        elif intent == 'procedure_location_request':
            return self._handle_procedure_inquiry(entities)
        
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
                major_texas_cities = ['Houston', 'Dallas', 'Austin', 'San Antonio', 'Fort Worth', 'Lubbock']
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

    def _handle_location_response(self, entities, message_lower):
        """Handle when user provides location"""
        location = entities['cities'][0].title() if entities['cities'] else None
        
        if location:
            self.conversation_context['user_location'] = location
            return {
                'type': 'location_confirmed',
                'message': f"Great! I've noted that you're in {location}. What medical procedure or service would you like pricing information for? I can help with MRI, X-rays, blood tests, and many other procedures.",
                'location': location,
                'suggestions': [
                    "MRI pricing",
                    "X-ray costs", 
                    "Blood test prices",
                    "Physical exam costs"
                ]
            }
        else:
            return {
                'type': 'location_unclear',
                'message': "I didn't catch your location clearly. Could you tell me your city and state? For example: 'Dallas, Texas' or 'Chicago, Illinois'"
            }

    def _handle_location_procedure_inquiry(self, entities, message_lower):
        """Handle when user provides both location and procedure"""
        location = entities['cities'][0].title() if entities['cities'] else self.conversation_context.get('user_location')
        procedures = entities['procedures'] or self.conversation_context.get('required_procedures', [])
        
        if location and procedures:
            self.conversation_context['user_location'] = location
            self.conversation_context['required_procedures'] = procedures
            
            # Get hospital comparison
            hospitals = self.hospital_data_manager.compare_hospitals(procedures, location)
            
            if hospitals:
                response_msg = f"Perfect! Here's the pricing for {', '.join(procedures)} in {location}:\n\n"
                cheapest = hospitals[0]
                response_msg += f"**🏆 Best Deal:** {cheapest['hospital']['name']}\n"
                response_msg += f"• Cash Price: ${cheapest['total_cash_cost']}\n"
                response_msg += f"• Rating: ⭐ {cheapest['hospital']['rating']}/5\n\n"
                response_msg += "Would you like to see the full comparison or information about insurance coverage?"
                
                return {
                    'type': 'complete_analysis',
                    'message': response_msg,
                    'hospitals': hospitals[:3],
                    'location': location,
                    'procedures': procedures
                }
            else:
                return {
                    'type': 'no_data',
                    'message': f"I couldn't find pricing data for {location}. Let me try a nearby major city. What's the closest big city to you?"
                }
        else:
            return {
                'type': 'incomplete_info',
                'message': "I need both your location and the medical procedure to help you. Could you provide the missing information?"
            }

    def _handle_procedure_inquiry(self, entities):
        """Handle when user asks about procedures without location"""
        procedures = entities['procedures']
        location = self.conversation_context.get('user_location')
        
        if procedures:
            self.conversation_context['required_procedures'] = procedures
            
            if location:
                # We have location in context, provide immediate analysis
                return self._handle_location_procedure_inquiry(entities, "")
            else:
                # Ask for location
                return {
                    'type': 'need_location',
                    'message': f"I can help you find the best prices for {', '.join(procedures)}! What city are you in so I can find the most affordable options near you?",
                    'procedures': procedures,
                    'suggestions': [
                        "I'm in Houston, Texas",
                        "Dallas, Texas",
                        "Austin, Texas",
                        "San Antonio, Texas"
                    ]
                }
        else:
            return {
                'type': 'procedure_unclear',
                'message': "What medical procedure do you need? I can help with MRI, X-rays, blood tests, CT scans, ultrasounds, and many other medical services."
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
            response_msg += f"• **{proc}** - Typically costs $200-$800\n"
        
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

    def _handle_hospital_inquiry(self, entities):
        """Handle hospital-related inquiries"""
        location = self.conversation_context.get('user_location') or (entities['cities'][0].title() if entities['cities'] else None)
        
        if location:
            # Get general hospital information for the location
            procedures = ['Physical examination']  # Default procedure for hospital search
            hospitals = self.hospital_data_manager.compare_hospitals(procedures, location)
            
            if hospitals:
                response_msg = f"Here are the top hospitals in {location}:\n\n"
                for i, hospital_data in enumerate(hospitals[:3], 1):
                    hospital = hospital_data['hospital']
                    response_msg += f"**{i}. {hospital['name']}**\n"
                    response_msg += f"• Rating: ⭐ {hospital['rating']}/5\n"
                    response_msg += f"• Emergency Services: {'Yes' if hospital['emergency'] else 'No'}\n"
                    response_msg += f"• Average Wait: {hospital['average_wait_time']} minutes\n\n"
                
                response_msg += "Would you like pricing information for a specific procedure?"
                
                return {
                    'type': 'hospital_list',
                    'message': response_msg,
                    'hospitals': hospitals[:3],
                    'location': location
                }
            else:
                return {
                    'type': 'no_hospitals',
                    'message': f"I couldn't find hospital data for {location}. Let me know a nearby major city and I'll help you find great healthcare options!"
                }
        else:
            return {
                'type': 'need_location_hospital',
                'message': "I'd be happy to help you find hospitals! What city are you looking in?"
            }

    def _handle_emergency(self):
        """Handle emergency situations"""
        location = self.conversation_context.get('user_location')
        
        emergency_msg = "🚨 **EMERGENCY ASSISTANCE** 🚨\n\n"
        emergency_msg += "**If this is a life-threatening emergency, call 911 immediately!**\n\n"
        
        if location:
            emergency_msg += f"For urgent care in {location}:\n"
            emergency_msg += "• Call 911 for ambulance\n"
            emergency_msg += "• Go to nearest emergency room\n"
            emergency_msg += "• Call urgent care centers\n\n"
            emergency_msg += "Would you like me to find emergency hospitals near you?"
        else:
            emergency_msg += "• Call 911 for immediate help\n"
            emergency_msg += "• Go to your nearest emergency room\n"
            emergency_msg += "• Tell me your location and I can find emergency hospitals\n\n"
        
        return {
            'type': 'emergency',
            'message': emergency_msg,
            'urgent': True
        }

    def _handle_conversational_response(self, message_lower, entities):
        """Handle general conversational responses"""
        # Check if user is asking for help with context we already have
        location = self.conversation_context.get('user_location')
        procedures = self.conversation_context.get('required_procedures')
        
        if location and procedures:
            response_msg = f"I remember you're in {location} and interested in {', '.join(procedures)}. "
            response_msg += "Would you like me to find the best prices for you?"
            
            return {
                'type': 'contextual_help',
                'message': response_msg,
                'location': location,
                'procedures': procedures
            }
        elif location:
            response_msg = f"I know you're in {location}. What medical procedure would you like pricing information for?"
            
            return {
                'type': 'location_known',
                'message': response_msg,
                'location': location
            }
        else:
            return {
                'type': 'general_help',
                'message': "I can help you save money on healthcare! I can compare hospital prices, analyze insurance coverage, and find the best medical care in your area. What city are you in and what do you need help with?"
            }

    def _handle_general_inquiry(self):
        """Handle general inquiries"""
        return {
            'type': 'general',
            'message': "I'm here to help you save money on healthcare costs! I can:\n\n• Compare hospital prices across all 50 states\n• Analyze insurance coverage\n• Find the cheapest medical procedures near you\n• Help with emergency hospital locations\n\nWhat city are you in and how can I help you today?",
            'suggestions': [
                "Find cheap hospitals near me",
                "Compare procedure prices",
                "Analyze my insurance",
                "Emergency hospitals"
            ]
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
