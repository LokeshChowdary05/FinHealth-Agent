from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
import json
import requests
from datetime import datetime
from medical_analyzer import MedicalAnalyzer
from hospital_data import HospitalDataManager
from insurance_analyzer import InsuranceAnalyzer
from conversation_manager import ConversationManager

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'your-secret-key-here')
CORS(app)

# Initialize components
medical_analyzer = MedicalAnalyzer()
hospital_data_manager = HospitalDataManager()
insurance_analyzer = InsuranceAnalyzer()
conversation_manager = ConversationManager()

@app.route('/')
def index():
    """Main page with chatbot interface"""
    return render_template('index.html')

@app.route('/api/analyze-symptoms', methods=['POST'])
def analyze_symptoms():
    """Analyze user symptoms and predict medical condition"""
    try:
        data = request.get_json()
        symptoms = data.get('symptoms', '')
        
        if not symptoms:
            return jsonify({'error': 'No symptoms provided'}), 400
        
        # Analyze symptoms using AI
        condition = medical_analyzer.analyze_symptoms(symptoms)
        procedures = medical_analyzer.get_recommended_procedures(condition)
        
        return jsonify({
            'condition': condition,
            'procedures': procedures,
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        return jsonify({'error': f'Analysis failed: {str(e)}'}), 500

@app.route('/api/compare-hospitals', methods=['POST'])
def compare_hospitals():
    """Compare hospital prices for given procedures"""
    try:
        data = request.get_json()
        procedures = data.get('procedures', [])
        location = data.get('location', 'New York')
        
        if not procedures:
            return jsonify({'error': 'No procedures provided'}), 400
        
        # Get hospital comparison data
        hospital_comparison = hospital_data_manager.compare_hospitals(procedures, location)
        
        return jsonify({
            'hospitals': hospital_comparison,
            'location': location,
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        return jsonify({'error': f'Hospital comparison failed: {str(e)}'}), 500

@app.route('/api/analyze-insurance', methods=['POST'])
def analyze_insurance():
    """Analyze insurance coverage vs out-of-pocket costs"""
    try:
        data = request.get_json()
        procedures = data.get('procedures', [])
        insurance_plan = data.get('insurance_plan', '')
        hospital = data.get('hospital', '')
        
        if not procedures or not insurance_plan:
            return jsonify({'error': 'Missing required information'}), 400
        
        # Analyze insurance coverage
        coverage_analysis = insurance_analyzer.analyze_coverage(
            procedures, insurance_plan, hospital
        )
        
        return jsonify({
            'coverage_analysis': coverage_analysis,
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        return jsonify({'error': f'Insurance analysis failed: {str(e)}'}), 500

@app.route('/api/chat', methods=['POST'])
def chat():
    """Main chatbot endpoint"""
    try:
        data = request.get_json()
        message = data.get('message', '')
        context = data.get('context', {})
        
        if not message:
            return jsonify({'error': 'No message provided'}), 400
        
        # Process the chat message
        response = process_chat_message(message, context)
        
        return jsonify({
            'response': response,
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        return jsonify({'error': f'Chat processing failed: {str(e)}'}), 500

@app.route('/api/initial-form', methods=['POST'])
def handle_initial_form():
    """Handle initial form submission"""
    try:
        data = request.get_json()
        location = data.get('location', '')
        procedure = data.get('procedure', '')
        insurance = data.get('insurance', '')
        
        # Create context from form data
        form_context = {
            'user_location': location,
            'required_procedures': [procedure] if procedure else [],
            'insurance_plan': insurance if insurance else None,
            'conversation_stage': 'form_completed'
        }
        
        # Generate a response based on form data
        if location and procedure:
            # If we have both location and procedure, get pricing
            hospitals = hospital_data_manager.compare_hospitals([procedure], location)
            
            response_msg = f"Thank you for providing your information!\n\n"
            response_msg += f"📍 **Location:** {location}\n"
            response_msg += f"🔬 **Procedure:** {procedure}\n"
            if insurance:
                response_msg += f"🏥 **Insurance:** {insurance}\n\n"
            else:
                response_msg += f"🏥 **Insurance:** Not provided\n\n"
            
            if hospitals:
                cheapest = hospitals[0]
                most_expensive = hospitals[-1]
                
                response_msg += f"**💰 Price Analysis for {procedure} in {location}:**\n"
                response_msg += f"• Best Price: ${cheapest['total_cash_cost']} at {cheapest['hospital']['name']}\n"
                response_msg += f"• Highest Price: ${most_expensive['total_cash_cost']} at {most_expensive['hospital']['name']}\n"
                response_msg += f"• **Potential Savings: ${most_expensive['total_cash_cost'] - cheapest['total_cash_cost']}**\n\n"
                
                if insurance:
                    # Analyze insurance coverage
                    coverage_analysis = insurance_analyzer.analyze_coverage([procedure], insurance, cheapest['hospital']['name'])
                    response_msg += f"**📋 Insurance Analysis:**\n"
                    response_msg += f"With {insurance}, your estimated out-of-pocket cost could be significantly lower.\n\n"
                
                response_msg += "Would you like to see the detailed hospital comparison or need help with anything else?"
                
                return jsonify({
                    'response': {
                        'type': 'form_analysis',
                        'message': response_msg,
                        'hospitals': hospitals[:5],
                        'location': location,
                        'procedure': procedure,
                        'insurance': insurance
                    },
                    'context': form_context,
                    'timestamp': datetime.now().isoformat()
                })
            else:
                response_msg += f"I couldn't find specific pricing data for {procedure} in {location}, but I can still help you with:\n\n"
                response_msg += f"• Finding nearby hospitals\n"
                response_msg += f"• General procedure information\n"
                response_msg += f"• Insurance coverage analysis\n\n"
                response_msg += "What would you like to know more about?"
                
                return jsonify({
                    'response': {
                        'type': 'form_no_data',
                        'message': response_msg
                    },
                    'context': form_context,
                    'timestamp': datetime.now().isoformat()
                })
        else:
            # Incomplete form data
            response_msg = "Thank you for the information! "
            if not location:
                response_msg += "Please provide your city and state so I can find the best healthcare options near you. "
            if not procedure:
                response_msg += "What medical procedure or service are you looking for? "
            
            return jsonify({
                'response': {
                    'type': 'form_incomplete',
                    'message': response_msg
                },
                'context': form_context,
                'timestamp': datetime.now().isoformat()
            })
    
    except Exception as e:
        return jsonify({'error': f'Form processing failed: {str(e)}'}), 500

def process_chat_message(message, context):
    """Process chat message and return appropriate response"""
    response = conversation_manager.process_message(message, context)
    
    return response

def extract_location_from_message(message_lower):
    """Extract location from user message - supports all US cities"""
    # Major cities mapping with state and nickname variations
    locations = {
        # Alabama
        'birmingham': 'Birmingham', 'montgomery': 'Montgomery', 'mobile': 'Mobile', 'huntsville': 'Huntsville',
        'tuscaloosa': 'Tuscaloosa', 'hoover': 'Hoover', 'dothan': 'Dothan', 'auburn': 'Auburn',
        
        # Alaska
        'anchorage': 'Anchorage', 'fairbanks': 'Fairbanks', 'juneau': 'Juneau', 'sitka': 'Sitka',
        
        # Arizona
        'phoenix': 'Phoenix', 'tucson': 'Tucson', 'mesa': 'Mesa', 'chandler': 'Chandler',
        'scottsdale': 'Scottsdale', 'glendale': 'Glendale', 'gilbert': 'Gilbert', 'tempe': 'Tempe',
        'arizona': 'Phoenix',
        
        # Arkansas  
        'little rock': 'Little Rock', 'fort smith': 'Fort Smith', 'fayetteville': 'Fayetteville',
        'springdale': 'Springdale', 'jonesboro': 'Jonesboro',
        
        # California
        'los angeles': 'Los Angeles', 'la': 'Los Angeles', 'hollywood': 'Los Angeles',
        'san diego': 'San Diego', 'san jose': 'San Jose', 'san francisco': 'San Francisco',
        'fresno': 'Fresno', 'sacramento': 'Sacramento', 'long beach': 'Long Beach',
        'oakland': 'Oakland', 'bakersfield': 'Bakersfield', 'anaheim': 'Anaheim',
        'santa ana': 'Santa Ana', 'riverside': 'Riverside', 'stockton': 'Stockton',
        'irvine': 'Irvine', 'chula vista': 'Chula Vista', 'beverly hills': 'Los Angeles',
        'santa monica': 'Los Angeles',
        
        # Colorado
        'denver': 'Denver', 'colorado springs': 'Colorado Springs', 'aurora': 'Aurora',
        'fort collins': 'Fort Collins', 'lakewood': 'Lakewood', 'thornton': 'Thornton',
        
        # Connecticut
        'bridgeport': 'Bridgeport', 'new haven': 'New Haven', 'hartford': 'Hartford',
        'stamford': 'Stamford', 'waterbury': 'Waterbury', 'norwalk': 'Norwalk',
        
        # Delaware
        'wilmington': 'Wilmington', 'dover': 'Dover', 'newark': 'Newark',
        
        # Florida
        'jacksonville': 'Jacksonville', 'miami': 'Miami', 'tampa': 'Tampa',
        'orlando': 'Orlando', 'st. petersburg': 'St. Petersburg', 'hialeah': 'Hialeah',
        'tallahassee': 'Tallahassee', 'fort lauderdale': 'Fort Lauderdale',
        'port st. lucie': 'Port St. Lucie', 'cape coral': 'Cape Coral', 'hollywood': 'Hollywood',
        'gainesville': 'Gainesville', 'coral springs': 'Coral Springs', 'south beach': 'Miami',
        'florida': 'Miami',
        
        # Georgia
        'atlanta': 'Atlanta', 'augusta': 'Augusta', 'columbus': 'Columbus',
        'macon': 'Macon', 'savannah': 'Savannah', 'athens': 'Athens',
        'sandy springs': 'Sandy Springs', 'roswell': 'Roswell', 'georgia': 'Atlanta',
        
        # Hawaii
        'honolulu': 'Honolulu', 'pearl city': 'Pearl City', 'hilo': 'Hilo',
        'kailua': 'Kailua', 'waipahu': 'Waipahu',
        
        # Idaho
        'boise': 'Boise', 'meridian': 'Meridian', 'nampa': 'Nampa',
        'idaho falls': 'Idaho Falls', 'pocatello': 'Pocatello',
        
        # Illinois
        'chicago': 'Chicago', 'aurora': 'Aurora', 'rockford': 'Rockford',
        'joliet': 'Joliet', 'naperville': 'Naperville', 'springfield': 'Springfield',
        'peoria': 'Peoria', 'elgin': 'Elgin', 'waukegan': 'Waukegan',
        'illinois': 'Chicago', 'windy city': 'Chicago',
        
        # Indiana
        'indianapolis': 'Indianapolis', 'fort wayne': 'Fort Wayne', 'evansville': 'Evansville',
        'south bend': 'South Bend', 'carmel': 'Carmel', 'fishers': 'Fishers',
        
        # Iowa
        'des moines': 'Des Moines', 'cedar rapids': 'Cedar Rapids', 'davenport': 'Davenport',
        'sioux city': 'Sioux City', 'iowa city': 'Iowa City', 'waterloo': 'Waterloo',
        
        # Kansas
        'wichita': 'Wichita', 'overland park': 'Overland Park', 'kansas city': 'Kansas City',
        'topeka': 'Topeka', 'olathe': 'Olathe', 'lawrence': 'Lawrence',
        
        # Kentucky
        'louisville': 'Louisville', 'lexington': 'Lexington', 'bowling green': 'Bowling Green',
        'owensboro': 'Owensboro', 'covington': 'Covington',
        
        # Louisiana
        'new orleans': 'New Orleans', 'baton rouge': 'Baton Rouge', 'shreveport': 'Shreveport',
        'lafayette': 'Lafayette', 'lake charles': 'Lake Charles',
        
        # Maine
        'portland': 'Portland', 'lewiston': 'Lewiston', 'bangor': 'Bangor',
        
        # Maryland
        'baltimore': 'Baltimore', 'columbia': 'Columbia', 'germantown': 'Germantown',
        'silver spring': 'Silver Spring', 'waldorf': 'Waldorf',
        
        # Massachusetts
        'boston': 'Boston', 'worcester': 'Worcester', 'springfield': 'Springfield',
        'cambridge': 'Cambridge', 'lowell': 'Lowell', 'brockton': 'Brockton',
        'massachusetts': 'Boston',
        
        # Michigan
        'detroit': 'Detroit', 'grand rapids': 'Grand Rapids', 'warren': 'Warren',
        'sterling heights': 'Sterling Heights', 'ann arbor': 'Ann Arbor', 'lansing': 'Lansing',
        
        # Minnesota
        'minneapolis': 'Minneapolis', 'saint paul': 'Saint Paul', 'rochester': 'Rochester',
        'duluth': 'Duluth', 'bloomington': 'Bloomington',
        
        # Mississippi
        'jackson': 'Jackson', 'gulfport': 'Gulfport', 'southaven': 'Southaven',
        'hattiesburg': 'Hattiesburg', 'biloxi': 'Biloxi',
        
        # Missouri
        'kansas city': 'Kansas City', 'saint louis': 'Saint Louis', 'springfield': 'Springfield',
        'columbia': 'Columbia', 'independence': 'Independence',
        
        # Montana
        'billings': 'Billings', 'missoula': 'Missoula', 'great falls': 'Great Falls',
        'bozeman': 'Bozeman', 'butte': 'Butte',
        
        # Nebraska
        'omaha': 'Omaha', 'lincoln': 'Lincoln', 'bellevue': 'Bellevue',
        
        # Nevada
        'las vegas': 'Las Vegas', 'henderson': 'Henderson', 'reno': 'Reno',
        'north las vegas': 'North Las Vegas', 'sparks': 'Sparks',
        
        # New Hampshire
        'manchester': 'Manchester', 'nashua': 'Nashua', 'concord': 'Concord',
        
        # New Jersey
        'newark': 'Newark', 'jersey city': 'Jersey City', 'paterson': 'Paterson',
        'elizabeth': 'Elizabeth', 'edison': 'Edison', 'trenton': 'Trenton',
        
        # New Mexico
        'albuquerque': 'Albuquerque', 'las cruces': 'Las Cruces', 'rio rancho': 'Rio Rancho',
        'santa fe': 'Santa Fe', 'roswell': 'Roswell',
        
        # New York
        'new york': 'New York', 'nyc': 'New York', 'manhattan': 'New York',
        'brooklyn': 'New York', 'queens': 'New York', 'bronx': 'New York',
        'buffalo': 'Buffalo', 'rochester': 'Rochester', 'yonkers': 'Yonkers',
        'syracuse': 'Syracuse', 'albany': 'Albany',
        
        # North Carolina
        'charlotte': 'Charlotte', 'raleigh': 'Raleigh', 'greensboro': 'Greensboro',
        'durham': 'Durham', 'winston-salem': 'Winston-Salem', 'fayetteville': 'Fayetteville',
        
        # North Dakota
        'fargo': 'Fargo', 'bismarck': 'Bismarck', 'grand forks': 'Grand Forks',
        
        # Ohio
        'columbus': 'Columbus', 'cleveland': 'Cleveland', 'cincinnati': 'Cincinnati',
        'toledo': 'Toledo', 'akron': 'Akron', 'dayton': 'Dayton',
        
        # Oklahoma
        'oklahoma city': 'Oklahoma City', 'tulsa': 'Tulsa', 'norman': 'Norman',
        'broken arrow': 'Broken Arrow', 'lawton': 'Lawton',
        
        # Oregon
        'portland': 'Portland', 'eugene': 'Eugene', 'salem': 'Salem',
        'gresham': 'Gresham', 'hillsboro': 'Hillsboro', 'bend': 'Bend',
        
        # Pennsylvania
        'philadelphia': 'Philadelphia', 'pittsburgh': 'Pittsburgh', 'allentown': 'Allentown',
        'erie': 'Erie', 'reading': 'Reading', 'scranton': 'Scranton',
        
        # Rhode Island
        'providence': 'Providence', 'warwick': 'Warwick', 'cranston': 'Cranston',
        
        # South Carolina
        'charleston': 'Charleston', 'columbia': 'Columbia', 'north charleston': 'North Charleston',
        'mount pleasant': 'Mount Pleasant', 'rock hill': 'Rock Hill',
        
        # South Dakota
        'sioux falls': 'Sioux Falls', 'rapid city': 'Rapid City', 'aberdeen': 'Aberdeen',
        
        # Tennessee
        'nashville': 'Nashville', 'memphis': 'Memphis', 'knoxville': 'Knoxville',
        'chattanooga': 'Chattanooga', 'clarksville': 'Clarksville',
        
        # Texas - Including Lubbock as requested
        'houston': 'Houston', 'san antonio': 'San Antonio', 'dallas': 'Dallas',
        'austin': 'Austin', 'fort worth': 'Fort Worth', 'el paso': 'El Paso',
        'arlington': 'Arlington', 'corpus christi': 'Corpus Christi', 'plano': 'Plano',
        'lubbock': 'Lubbock', 'laredo': 'Laredo', 'irving': 'Irving',
        'garland': 'Garland', 'frisco': 'Frisco', 'mckinney': 'McKinney',
        'amarillo': 'Amarillo', 'grand prairie': 'Grand Prairie', 'brownsville': 'Brownsville',
        'pasadena': 'Pasadena', 'mesquite': 'Mesquite', 'texas': 'Houston',
        
        # Utah
        'salt lake city': 'Salt Lake City', 'west valley city': 'West Valley City',
        'provo': 'Provo', 'west jordan': 'West Jordan', 'orem': 'Orem',
        
        # Vermont
        'burlington': 'Burlington', 'essex': 'Essex', 'south burlington': 'South Burlington',
        
        # Virginia
        'virginia beach': 'Virginia Beach', 'norfolk': 'Norfolk', 'chesapeake': 'Chesapeake',
        'richmond': 'Richmond', 'newport news': 'Newport News', 'alexandria': 'Alexandria',
        
        # Washington
        'seattle': 'Seattle', 'spokane': 'Spokane', 'tacoma': 'Tacoma',
        'vancouver': 'Vancouver', 'bellevue': 'Bellevue', 'kent': 'Kent',
        'washington': 'Seattle',
        
        # West Virginia
        'charleston': 'Charleston', 'huntington': 'Huntington', 'parkersburg': 'Parkersburg',
        
        # Wisconsin
        'milwaukee': 'Milwaukee', 'madison': 'Madison', 'green bay': 'Green Bay',
        'kenosha': 'Kenosha', 'racine': 'Racine',
        
        # Wyoming
        'cheyenne': 'Cheyenne', 'casper': 'Casper', 'laramie': 'Laramie'
    }
    
    # Find the longest matching city name first (for better accuracy)
    matches = []
    for key, value in locations.items():
        if key in message_lower:
            matches.append((key, value, len(key)))
    
    if matches:
        # Return the longest match (most specific)
        matches.sort(key=lambda x: x[2], reverse=True)
        return matches[0][1]
    
    return None

def extract_procedures_from_message(message_lower):
    """Extract medical procedures from user message"""
    procedure_map = {
        'ecg': 'ECG',
        'ekg': 'ECG', 
        'electrocardiogram': 'ECG',
        'x-ray': 'X-ray',
        'xray': 'X-ray',
        'mri': 'MRI',
        'ct scan': 'CT scan',
        'cat scan': 'CT scan',
        'blood test': 'Blood tests',
        'blood work': 'Blood tests',
        'ultrasound': 'Ultrasound',
        'physical exam': 'Physical examination',
        'checkup': 'Physical examination'
    }
    
    found_procedures = []
    for key, value in procedure_map.items():
        if key in message_lower and value not in found_procedures:
            found_procedures.append(value)
    
    return found_procedures if found_procedures else ['Physical examination']

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    })

if __name__ == '__main__':
    # Create data directory if it doesn't exist
    os.makedirs('data', exist_ok=True)
    
    # Run the application
    app.run(
        debug=os.getenv('FLASK_DEBUG', 'True').lower() == 'true',
        host='0.0.0.0',
        port=int(os.getenv('PORT', 5000))
    )
