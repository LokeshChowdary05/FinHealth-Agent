#!/usr/bin/env python3
"""
Demo script to show the professional tabular output format
"""

from conversation_manager import ConversationManager

def demo_professional_output():
    """Demonstrate the enhanced professional tabular output"""
    print("🎯 FinHealth Professional Output Demo")
    print("=" * 60)
    
    cm = ConversationManager()
    
    # Simulate the exact scenario from the screenshot
    context = {
        "location": "Lubbock, Texas", 
        "procedures": ["X-ray"],
        "insurance": "Aetna"
    }
    
    print("\n📋 User Context:")
    print(f"   📍 Location: {context['location']}")
    print(f"   🔬 Procedure: {', '.join(context['procedures'])}")
    print(f"   🛡️ Insurance: {context['insurance']}")
    
    print("\n👤 User Input: 'I need X-ray pricing information'")
    print("\n" + "="*60)
    print("🤖 FINHEALTH RESPONSE:")
    print("="*60)
    
    # Get the professional response
    response = cm.process_message("I need X-ray pricing information", context)
    
    # Display the formatted response
    print(response.get('message', 'No response available'))
    
    print("\n" + "="*60)
    print("✅ Professional tabular format demonstration complete!")

if __name__ == "__main__":
    demo_professional_output()
