#!/usr/bin/env python3
"""
Quick test script for your Ollama server at 192.168.145.77
Simple test to verify connectivity and basic code review functionality
"""

import requests
import json

# Your server configuration
OLLAMA_SERVER = "http://192.168.145.77:11434"

def quick_test():
    print("🚀 Testing Ollama server connectivity...")
    
    # Test 1: Check server availability
    try:
        response = requests.get(f"{OLLAMA_SERVER}/api/tags", timeout=10)
        if response.status_code == 200:
            models = response.json().get('models', [])
            print(f"✅ Server is online!")
            print(f"📋 Available models: {[m['name'] for m in models]}")
            
            if not models:
                print("❌ No models found on server!")
                return
                
        else:
            print(f"❌ Server responded with status: {response.status_code}")
            return
            
    except Exception as e:
        print(f"❌ Cannot connect to server: {e}")
        return
    
    # Test 2: Simple code review test
    print("\n🔍 Testing code review capability...")
    
    # Simple test code with obvious issues
    test_code = """
public class TestClass {
    public void problemMethod(String input) {
        String result = null;
        result.toLowerCase();  // NullPointerException!
        
        // No input validation
        if (input == "test") {  // Should use .equals()
            System.out.println("Found: " + input);
        }
        
        // Resource leak
        FileInputStream fis = new FileInputStream("test.txt");
        // Missing try-catch and close()
    }
}
"""
    
    # Use first available model
    model_name = models[0]['name'] if models else "deepseek-r1:7b"  # fallback
    print(f"🤖 Using model: {model_name}")
    
    prompt = f"""Please review this Java code and identify any bugs or issues:

{test_code}

Focus on:
1. Runtime exceptions
2. Resource leaks  
3. Code style issues

Keep the review concise."""

    data = {
        "model": model_name,
        "messages": [{"role": "user", "content": prompt}],
        "stream": False
    }
    
    try:
        print("⏳ Sending review request...")
        response = requests.post(f"{OLLAMA_SERVER}/api/chat", json=data, timeout=60)
        
        if response.status_code == 200:
            result = response.json()
            review = result.get("message", {}).get("content", "No response")
            print("✅ Code review completed!")
            print("\n" + "="*50)
            print("📝 REVIEW RESULTS:")
            print("="*50)
            print(review)
            print("="*50)
            
        else:
            print(f"❌ Review request failed: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error during review: {e}")

if __name__ == "__main__":
    quick_test()