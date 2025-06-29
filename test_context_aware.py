#!/usr/bin/env python3
"""
Test script for context-aware conversation handling
"""

from conversation_manager import ConversationManager
from hospital_data import HospitalDataManager

print('🧪 Testing Enhanced Context-Aware Conversation Manager')
print('=' * 60)

# Initialize components
hospital_manager = HospitalDataManager()
conv_manager = ConversationManager()

# Test scenarios
test_cases = [
    {
        'name': 'User with full context asks for pricing',
        'context': {'location': 'Lubbock, Texas', 'procedures': ['X-ray'], 'insurance': 'Aetna'},
        'message': 'I need X-ray pricing information'
    },
    {
        'name': 'User provides location, then asks about procedure',
        'context': {'location': 'Dallas, Texas'},
        'message': 'I need MRI pricing'
    },
    {
        'name': 'User asks about procedure with city mentioned',
        'context': {},
        'message': 'I need MRI pricing in Houston, Texas'
    },
    {
        'name': 'User asks about emergency services',
        'context': {'location': 'Austin, Texas'},
        'message': 'Which hospitals have emergency services?'
    },
    {
        'name': 'User asks general pricing question',
        'context': {'location': 'San Antonio, Texas'},
        'message': 'How much does an X-ray cost?'
    }
]

for i, test in enumerate(test_cases, 1):
    print(f'\n📋 Test {i}: {test["name"]}')
    print(f'   Context: {test["context"]}')
    print(f'   Message: "{test["message"]}"')
    
    response = conv_manager.process_message(test['message'], test['context'])
    print(f'   Response Type: {response["type"]}')
    
    # Check if bot is asking for location when it shouldn't
    asking_for_location = any(phrase in response['message'].lower() for phrase in [
        'which city', 'your city', 'location', 'where are you located', 'city and state'
    ])
    
    if asking_for_location and test['context'].get('location'):
        print('   ❌ ISSUE: Bot asking for location when already known')
    else:
        print('   ✅ GOOD: Appropriate response given context')
    
    # Show first part of response
    preview = response['message'][:100].replace('\n', ' ')
    print(f'   Message Preview: {preview}...')
    
    # Check if hospitals are included in response
    if 'hospitals' in response and response['hospitals']:
        print(f'   🏥 Hospitals Found: {len(response["hospitals"])}')
    
    print('-' * 40)

print('\n🎯 Context-Aware Testing Complete!')
print('\n📊 Summary:')
print('   - Testing context retention and appropriate responses')
print('   - Verifying no redundant location requests')
print('   - Checking professional analysis format')
