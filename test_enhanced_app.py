#!/usr/bin/env python3
"""
Comprehensive Test Script for Enhanced FinHealth Application
Tests all conversation flows and data access
"""

import sys
import os
import json
from conversation_manager import ConversationManager
from hospital_data import HospitalDataManager
from insurance_analyzer import InsuranceAnalyzer

def test_conversation_manager():
    """Test the enhanced conversation manager"""
    print("🧪 Testing Enhanced Conversation Manager...")
    
    cm = ConversationManager()
    
    # Test scenarios that caused the original issue
    test_scenarios = [
        {
            "name": "Scenario 1: User provides form data, then asks for pricing",
            "context": {
                "user_location": "Lubbock",
                "required_procedures": ["X-ray"],
                "insurance_plan": "Aetna"
            },
            "message": "I need X-ray pricing information",
            "expected_type": "direct_price_analysis"
        },
        {
            "name": "Scenario 2: User in Texas asking for MRI pricing",
            "context": {
                "user_location": "Texas",
                "required_procedures": ["MRI"],
                "insurance_plan": "Aetna"
            },
            "message": "I need price comparison for medical procedures",
            "expected_type": "direct_price_analysis"
        },
        {
            "name": "Scenario 3: User provides location then asks about procedure",
            "context": {
                "user_location": "Dallas"
            },
            "message": "I need MRI pricing",
            "expected_type": "location_procedure_inquiry"
        },
        {
            "name": "Scenario 4: Completely new user asking for pricing",
            "context": {},
            "message": "I need MRI pricing in Houston, Texas",
            "expected_type": "location_procedure_inquiry"
        }
    ]
    
    for scenario in test_scenarios:
        print(f"\n📋 {scenario['name']}")
        response = cm.process_message(scenario["message"], scenario["context"])
        print(f"   ✅ Response type: {response.get('type', 'unknown')}")
        print(f"   📝 Message preview: {response.get('message', 'No message')[:100]}...")
        
        if response.get('type') == scenario.get('expected_type'):
            print("   ✅ PASSED: Expected response type")
        else:
            print(f"   ❌ FAILED: Expected {scenario.get('expected_type')}, got {response.get('type')}")

def test_hospital_data_manager():
    """Test the hospital data manager with Texas cities"""
    print("\n🏥 Testing Hospital Data Manager...")
    
    hdm = HospitalDataManager()
    
    # Test Texas cities
    texas_cities = ["Lubbock", "Houston", "Dallas", "Austin", "San Antonio"]
    
    for city in texas_cities:
        print(f"\n🏙️ Testing {city}, Texas:")
        hospitals = hdm.compare_hospitals(["X-ray", "MRI"], city)
        
        if hospitals:
            print(f"   ✅ Found {len(hospitals)} hospitals")
            cheapest = hospitals[0]
            print(f"   💰 Cheapest X-ray: ${cheapest['procedures'][0]['cash_price']} at {cheapest['hospital']['name']}")
            print(f"   ⭐ Rating: {cheapest['hospital']['rating']}/5")
            print(f"   ⏱️ Wait time: {cheapest['hospital']['average_wait_time']} minutes")
        else:
            print(f"   ❌ No hospitals found for {city}")

def test_insurance_analyzer():
    """Test insurance analysis functionality"""
    print("\n💳 Testing Insurance Analyzer...")
    
    ia = InsuranceAnalyzer()
    
    # Test with common procedures and insurance
    procedures = ["X-ray", "MRI"]
    insurance_plan = "Aetna"
    hospital = "Lubbock General Hospital"
    
    try:
        analysis = ia.analyze_coverage(procedures, insurance_plan, hospital)
        print(f"   ✅ Insurance analysis completed for {insurance_plan}")
        print(f"   📊 Analysis type: {type(analysis)}")
    except Exception as e:
        print(f"   ⚠️ Insurance analysis error: {e}")

def test_data_integrity():
    """Test data file integrity and accessibility"""
    print("\n📊 Testing Data Integrity...")
    
    data_files = [
        'data/nationwide_hospital_data.json',
        'data/hospital_pricing_data.json'
    ]
    
    for file_path in data_files:
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)
                
                print(f"   ✅ {file_path}: Valid JSON")
                print(f"   📏 File size: {os.path.getsize(file_path) / 1024 / 1024:.1f} MB")
                
                # Check for Texas data
                if 'hospitals' in data and 'Texas' in data['hospitals']:
                    texas_cities = len(data['hospitals']['Texas'])
                    print(f"   🏙️ Texas cities: {texas_cities}")
                    
                    # Check specifically for Lubbock
                    if 'Lubbock' in data['hospitals']['Texas']:
                        lubbock_hospitals = len(data['hospitals']['Texas']['Lubbock'])
                        print(f"   🏥 Lubbock hospitals: {lubbock_hospitals}")
                    else:
                        print("   ❌ Lubbock data not found")
                
            except json.JSONDecodeError as e:
                print(f"   ❌ {file_path}: Invalid JSON - {e}")
            except Exception as e:
                print(f"   ❌ {file_path}: Error - {e}")
        else:
            print(f"   ❌ {file_path}: File not found")

def test_full_conversation_flow():
    """Test a complete conversation flow"""
    print("\n🔄 Testing Full Conversation Flow...")
    
    cm = ConversationManager()
    
    # Simulate the problematic conversation flow
    print("\n   👤 User provides form data (like in the app)")
    context = {
        "user_location": "Lubbock, Texas",
        "required_procedures": ["X-ray"],
        "insurance_plan": "Aetna",
        "conversation_stage": "form_completed"
    }
    
    print("\n   👤 User asks: 'I need X-ray pricing information'")
    response = cm.process_message("I need X-ray pricing information", context)
    
    print(f"   🤖 Bot response type: {response.get('type')}")
    print(f"   📝 Bot message: {response.get('message', 'No message')[:200]}...")
    
    if response.get('hospitals'):
        print(f"   🏥 Found {len(response['hospitals'])} hospitals")
        if response['hospitals']:
            cheapest = response['hospitals'][0]
            print(f"   💰 Cheapest option: {cheapest['hospital']['name']} - ${cheapest['total_cash_cost']}")
    
    # Check if this is the correct behavior (no more asking for location)
    if "city" not in response.get('message', '').lower() and "location" not in response.get('message', '').lower():
        print("   ✅ SUCCESS: Bot doesn't ask for location again!")
    else:
        print("   ❌ FAILED: Bot is still asking for location information")

def run_all_tests():
    """Run all tests"""
    print("🚀 Starting Enhanced FinHealth Application Tests")
    print("=" * 60)
    
    try:
        test_data_integrity()
        test_hospital_data_manager()
        test_conversation_manager()
        test_insurance_analyzer()
        test_full_conversation_flow()
        
        print("\n" + "=" * 60)
        print("✅ All tests completed! Check results above.")
        
    except Exception as e:
        print(f"\n❌ Test suite failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    run_all_tests()
