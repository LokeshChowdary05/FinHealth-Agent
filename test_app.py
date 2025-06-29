#!/usr/bin/env python3
"""
FinHealth Bot - Test Script
Tests all major functionality to ensure everything works correctly
"""

import json
import os
import sys
from pathlib import Path

def test_imports():
    """Test that all required modules can be imported"""
    print("🔍 Testing imports...")
    try:
        import flask
        import requests
        from medical_analyzer import MedicalAnalyzer
        from hospital_data import HospitalDataManager
        from insurance_analyzer import InsuranceAnalyzer
        from conversation_manager import ConversationManager
        print("✅ All imports successful")
        return True
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False

def test_data_files():
    """Test that all data files exist and are valid JSON"""
    print("🔍 Testing data files...")
    data_files = [
        'data/nationwide_hospital_data.json',
        'data/hospital_pricing_data.json'
    ]
    
    for file_path in data_files:
        if not os.path.exists(file_path):
            print(f"❌ Missing data file: {file_path}")
            return False
        
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
                if isinstance(data, dict) and len(data) > 0:
                    print(f"✅ {file_path} - Valid JSON with {len(data)} entries")
                elif isinstance(data, list) and len(data) > 0:
                    print(f"✅ {file_path} - Valid JSON with {len(data)} items")
                else:
                    print(f"⚠️ {file_path} - Empty or invalid structure")
        except Exception as e:
            print(f"❌ Error reading {file_path}: {e}")
            return False
    
    return True

def test_hospital_data_manager():
    """Test hospital data manager functionality"""
    print("🔍 Testing Hospital Data Manager...")
    try:
        hdm = HospitalDataManager()
        hdm.load_hospital_data()
        
        # Test hospital search
        hospitals = hdm.find_hospitals_by_location('Texas')
        if hospitals:
            print(f"✅ Found {len(hospitals)} hospitals in Texas")
        else:
            print("⚠️ No hospitals found in Texas")
        
        # Test price comparison
        comparison = hdm.compare_hospital_prices(['X-ray'], 'Dallas')
        if comparison:
            print(f"✅ Price comparison successful - {len(comparison)} results")
        else:
            print("⚠️ Price comparison returned no results")
        
        return True
    except Exception as e:
        print(f"❌ Hospital Data Manager error: {e}")
        return False

def test_insurance_analyzer():
    """Test insurance analyzer functionality"""
    print("🔍 Testing Insurance Analyzer...")
    try:
        ia = InsuranceAnalyzer()
        
        # Test insurance analysis
        analysis = ia.analyze_insurance_coverage('UnitedHealthcare', ['X-ray'], 'Dallas')
        if analysis:
            print("✅ Insurance analysis successful")
        else:
            print("⚠️ Insurance analysis returned no results")
        
        return True
    except Exception as e:
        print(f"❌ Insurance Analyzer error: {e}")
        return False

def test_conversation_manager():
    """Test conversation manager functionality"""
    print("🔍 Testing Conversation Manager...")
    try:
        cm = ConversationManager()
        
        # Test message processing
        response = cm.process_message("chest pain in Dallas", {})
        if response and 'type' in response:
            print(f"✅ Conversation processing successful - Type: {response['type']}")
        else:
            print("⚠️ Conversation processing returned unexpected result")
        
        return True
    except Exception as e:
        print(f"❌ Conversation Manager error: {e}")
        return False

def test_environment():
    """Test environment setup"""
    print("🔍 Testing environment...")
    
    # Check Python version
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
    else:
        print(f"⚠️ Python version {version.major}.{version.minor} - Recommended 3.8+")
    
    # Check virtual environment
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("✅ Virtual environment active")
    else:
        print("⚠️ Virtual environment not detected")
    
    # Check .env file
    if os.path.exists('.env'):
        print("✅ .env file exists")
    else:
        print("⚠️ .env file not found - create from .env.example")
    
    return True

def main():
    """Run all tests"""
    print("🚀 FinHealth Bot - Test Suite")
    print("=" * 50)
    
    tests = [
        test_environment,
        test_imports,
        test_data_files,
        test_hospital_data_manager,
        test_insurance_analyzer,
        test_conversation_manager
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
            failed += 1
        print()
    
    print("=" * 50)
    print(f"🎯 Test Results: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("🎉 All tests passed! FinHealth Bot is ready to use!")
        print("\n🚀 Next steps:")
        print("1. Set up your API keys in the .env file")
        print("2. Run: python app.py")
        print("3. Open: http://localhost:5000")
    else:
        print("⚠️ Some tests failed. Please check the errors above.")
    
    return failed == 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
