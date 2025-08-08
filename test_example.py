#!/usr/bin/env python3
"""
Example usage of the OpenAI Key Tester

This script demonstrates how to use the OpenAIKeyTester class programmatically.
"""

from openai_key_tester import OpenAIKeyTester

def main():
    """Example of using the tester programmatically."""
    
    # Create a tester instance
    tester = OpenAIKeyTester()
    
    # Run individual tests
    print("Running individual tests...")
    
    # Test 1: Check API key format
    if tester.check_api_key_format():
        print("✅ API key format is valid")
    else:
        print("❌ API key format is invalid")
        return
    
    # Test 2: Test connectivity
    if tester.test_connectivity():
        print("✅ Connectivity test passed")
    else:
        print("❌ Connectivity test failed")
        return
    
    # Test 3: Check model availability
    if tester.test_model_availability():
        print("✅ Model availability test passed")
    else:
        print("❌ Model availability test failed")
    
    # Test 4: Test completion
    if tester.test_simple_completion():
        print("✅ Completion test passed")
    else:
        print("❌ Completion test failed")
    
    print("\n" + "="*50)
    print("Running comprehensive test...")
    print("="*50)
    
    # Run the comprehensive test
    results = tester.run_comprehensive_test()
    tester.print_summary(results)

if __name__ == "__main__":
    main()
