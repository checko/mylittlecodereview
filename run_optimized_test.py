#!/usr/bin/env python3
"""
Runner script to test optimized prompts with DeepSeek-R1-32B
Usage: python3 run_optimized_test.py
"""

import requests
import json
import time
from optimized_prompts import (
    SECURITY_FOCUSED_PROMPT, 
    COMPREHENSIVE_ENHANCED_PROMPT,
    MEMORY_ENHANCED_PROMPT,
    JNI_EXPERT_PROMPT
)

# Configuration
OLLAMA_SERVER = "http://192.168.145.77:11434"
MODEL_NAME = "deepseek-r1:32b"

def load_test_code():
    """Load the bad C++ sample for testing"""
    try:
        with open('bad_cpp_sample.cpp', 'r') as f:
            return f.read()
    except FileNotFoundError:
        print("❌ bad_cpp_sample.cpp not found! Make sure you're in the right directory.")
        return None

def run_single_prompt_test(prompt_template, prompt_name, code):
    """Run a single optimized prompt test"""
    print(f"\n{'='*60}")
    print(f"🧪 Testing: {prompt_name}")
    print(f"{'='*60}")
    
    # Format the prompt with code
    formatted_prompt = prompt_template.format(code=code)
    
    data = {
        "model": MODEL_NAME,
        "messages": [{"role": "user", "content": formatted_prompt}],
        "stream": False
    }
    
    try:
        print(f"⏳ Sending request to {MODEL_NAME}...")
        start_time = time.time()
        
        response = requests.post(f"{OLLAMA_SERVER}/api/chat", json=data, timeout=300)
        
        end_time = time.time()
        response_time = round(end_time - start_time, 2)
        
        if response.status_code == 200:
            result = response.json()
            review_content = result.get("message", {}).get("content", "")
            
            # Analyze quality
            analysis = analyze_review_quality(review_content)
            
            print(f"✅ Review completed in {response_time}s")
            print(f"\n📊 QUALITY METRICS:")
            print(f"  Word count: {analysis['word_count']}")
            print(f"  Critical issues caught: {len(analysis['caught_issues'])}/12")
            print(f"  Coverage: {analysis['coverage']}%")
            print(f"  Issues found: {', '.join(analysis['caught_issues'])}")
            print(f"  Has severity ratings: {analysis['has_severity']}")
            print(f"  Has specific fixes: {analysis['has_fixes']}")
            
            print(f"\n📝 REVIEW RESULTS:")
            print("-" * 50)
            print(review_content)
            
            return {
                "success": True,
                "response_time": response_time,
                "analysis": analysis,
                "review": review_content
            }
            
        else:
            print(f"❌ Request failed: HTTP {response.status_code}")
            print(f"Error: {response.text}")
            return {"success": False, "error": f"HTTP {response.status_code}"}
            
    except requests.exceptions.Timeout:
        print("❌ Request timed out (5 minutes)")
        return {"success": False, "error": "Timeout"}
    except Exception as e:
        print(f"❌ Error: {e}")
        return {"success": False, "error": str(e)}

def analyze_review_quality(review_text):
    """Analyze the quality of the review"""
    critical_issues = [
        "buffer overflow", "memory leak", "double free", "use after free",
        "null pointer", "array bounds", "uninitialized", "race condition",
        "integer overflow", "strcpy", "gets", "sprintf"
    ]
    
    caught_issues = [issue for issue in critical_issues 
                    if issue.lower() in review_text.lower()]
    
    word_count = len(review_text.split())
    
    return {
        "word_count": word_count,
        "caught_issues": caught_issues,
        "coverage": round((len(caught_issues) / len(critical_issues)) * 100, 1),
        "has_severity": any(sev in review_text.lower() 
                          for sev in ["critical", "high", "medium", "low"]),
        "has_fixes": any(fix_word in review_text.lower() 
                        for fix_word in ["fix", "recommend", "replace", "use instead"])
    }

def compare_with_baseline():
    """Compare optimized prompts with baseline results"""
    baseline_results = {
        "Comprehensive": {"coverage": 75.0, "time": 89.56},
        "Memory Safety": {"coverage": 83.3, "time": 115.58},
        "Security": {"coverage": 33.3, "time": 51.76},
        "JNI": {"coverage": 91.7, "time": 150.2}
    }
    
    print(f"\n{'='*60}")
    print("📈 BASELINE COMPARISON")
    print(f"{'='*60}")
    print("Previous results with original prompts:")
    for test_name, results in baseline_results.items():
        print(f"  {test_name}: {results['coverage']}% coverage in {results['time']}s")
    
    print("\nGoal: Improve coverage while maintaining or reducing response time")

def main():
    print("🚀 OPTIMIZED PROMPT TESTING")
    print(f"Model: {MODEL_NAME}")
    print(f"Server: {OLLAMA_SERVER}")
    
    # Load test code
    code = load_test_code()
    if not code:
        return
    
    print(f"📄 Loaded test code: {len(code)} characters")
    
    # Test server connectivity
    try:
        response = requests.get(f"{OLLAMA_SERVER}/api/tags", timeout=10)
        if response.status_code == 200:
            models = [m['name'] for m in response.json().get('models', [])]
            if MODEL_NAME in models:
                print(f"✅ Connected to server, model {MODEL_NAME} available")
            else:
                print(f"❌ Model {MODEL_NAME} not found!")
                print(f"Available models: {models}")
                return
        else:
            print(f"❌ Server error: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Cannot connect to server: {e}")
        return
    
    # Show baseline comparison
    compare_with_baseline()
    
    # Test each optimized prompt
    prompts_to_test = [
        (COMPREHENSIVE_ENHANCED_PROMPT, "Enhanced Comprehensive Review"),
        (SECURITY_FOCUSED_PROMPT, "Enhanced Security Analysis"), 
        (MEMORY_ENHANCED_PROMPT, "Enhanced Memory Safety"),
        (JNI_EXPERT_PROMPT, "Enhanced JNI Expert Review")
    ]
    
    results = {}
    
    for prompt_template, prompt_name in prompts_to_test:
        result = run_single_prompt_test(prompt_template, prompt_name, code)
        results[prompt_name] = result
        
        # Add a small delay between tests to avoid overwhelming the server
        if result["success"]:
            time.sleep(2)
    
    # Summary
    print(f"\n{'='*60}")
    print("📋 FINAL SUMMARY")
    print(f"{'='*60}")
    
    for prompt_name, result in results.items():
        if result["success"]:
            analysis = result["analysis"]
            print(f"\n{prompt_name}:")
            print(f"  ✅ Coverage: {analysis['coverage']}% ({len(analysis['caught_issues'])}/12 issues)")
            print(f"  ⏱️  Response time: {result['response_time']}s")
            print(f"  📝 Word count: {analysis['word_count']}")
            print(f"  🎯 Has severity: {analysis['has_severity']}")
            print(f"  🔧 Has fixes: {analysis['has_fixes']}")
        else:
            print(f"\n{prompt_name}:")
            print(f"  ❌ Failed: {result['error']}")
    
    print(f"\n🎯 Best performing prompt based on coverage and response time balance")

if __name__ == "__main__":
    main()