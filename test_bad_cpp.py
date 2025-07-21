#!/usr/bin/env python3
"""
Test script to evaluate LLM code review capabilities using bad C++ sample
This will test how well your Ollama models can identify various types of issues
"""

import requests
import json
import time

OLLAMA_SERVER = "http://192.168.145.77:11434"

def load_bad_cpp_sample():
    """Load the bad C++ sample code"""
    try:
        with open('bad_cpp_sample.cpp', 'r') as f:
            return f.read()
    except FileNotFoundError:
        print("❌ bad_cpp_sample.cpp not found!")
        return None

def test_comprehensive_review(model_name, code):
    """Test comprehensive code review capabilities"""
    
    prompt = """You are an expert C++ and Android native development security reviewer. 

Please perform a comprehensive security and quality review of this C++ code that might be used in an Android native library or system component.

Analyze the code for:

## CRITICAL SECURITY ISSUES
- Buffer overflows and memory corruption vulnerabilities
- Use-after-free and double-free errors  
- Integer overflows and underflows
- Input validation failures
- Command injection risks

## MEMORY MANAGEMENT PROBLEMS
- Memory leaks (new/delete, malloc/free mismatches)
- Resource leaks (file handles, mutexes, etc.)
- RAII violations
- Exception safety issues

## THREAD SAFETY & CONCURRENCY
- Race conditions
- Deadlock potential
- Uninitialized synchronization primitives
- Shared resource access issues

## LOGIC ERRORS
- Off-by-one errors
- Null pointer dereferences
- Array bounds violations
- Infinite loops/recursion

## ANDROID-SPECIFIC ISSUES
- JNI best practice violations
- Android lifecycle issues
- Resource management in Android context
- SELinux policy compliance

## CODE QUALITY
- Style guide violations
- Poor error handling patterns
- Maintainability issues
- Performance problems

For each issue found, please provide:
1. **Severity**: CRITICAL, HIGH, MEDIUM, LOW
2. **Location**: Line number or function name
3. **Description**: What the issue is
4. **Impact**: Why it's problematic
5. **Fix**: Specific recommendation

Focus on the most serious issues first. Be thorough but concise.

Code to review:
```cpp
""" + code + """
```"""

    data = {
        "model": model_name,
        "messages": [{"role": "user", "content": prompt}],
        "stream": False
    }
    
    try:
        print(f"🔍 Starting comprehensive review with {model_name}...")
        start_time = time.time()
        
        response = requests.post(f"{OLLAMA_SERVER}/api/chat", json=data, timeout=300)
        
        end_time = time.time()
        
        if response.status_code == 200:
            result = response.json()
            review_content = result.get("message", {}).get("content", "")
            
            return {
                "success": True,
                "review": review_content,
                "response_time": round(end_time - start_time, 2),
                "model": model_name
            }
        else:
            return {
                "success": False,
                "error": f"HTTP {response.status_code}: {response.text}",
                "model": model_name
            }
            
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "model": model_name
        }

def test_focused_review(model_name, code):
    """Test focused review on specific issue categories"""
    
    focused_tests = [
        {
            "name": "Memory Safety Focus",
            "prompt": f"""Focus specifically on MEMORY SAFETY issues in this C++ code:
            
1. Memory leaks (new without delete, malloc without free)
2. Double free errors
3. Use-after-free vulnerabilities  
4. Buffer overflows and underflows
5. Uninitialized memory access

For each memory issue found, specify:
- Exact location (line/function)
- Type of memory error
- Potential exploit scenario
- Recommended fix

Code:
```cpp
{code}
```"""
        },
        {
            "name": "Security Vulnerabilities",
            "prompt": f"""Focus on SECURITY VULNERABILITIES in this C++ code:

1. Buffer overflow attack vectors
2. Input validation bypasses
3. Command injection possibilities
4. Information disclosure risks
5. Privilege escalation potential

Rate each vulnerability by exploitability and impact.

Code:
```cpp
{code}
```"""
        },
        {
            "name": "Android JNI Issues", 
            "prompt": f"""Focus on ANDROID JNI and native development issues:

1. JNI resource management errors
2. Exception handling in JNI calls
3. Android-specific memory management
4. Thread safety in JNI context
5. Performance issues for mobile

Code:
```cpp
{code}
```"""
        }
    ]
    
    results = {}
    
    for test in focused_tests:
        print(f"  📋 Testing: {test['name']}")
        
        data = {
            "model": model_name,
            "messages": [{"role": "user", "content": test['prompt']}],
            "stream": False
        }
        
        try:
            start_time = time.time()
            response = requests.post(f"{OLLAMA_SERVER}/api/chat", json=data, timeout=180)
            end_time = time.time()
            
            if response.status_code == 200:
                result = response.json()
                review_content = result.get("message", {}).get("content", "")
                results[test['name']] = {
                    "success": True,
                    "review": review_content,
                    "response_time": round(end_time - start_time, 2)
                }
            else:
                results[test['name']] = {
                    "success": False,
                    "error": f"HTTP {response.status_code}"
                }
                
        except Exception as e:
            results[test['name']] = {
                "success": False,
                "error": str(e)
            }
    
    return results

def analyze_review_quality(review_text):
    """Analyze the quality and completeness of the review"""
    
    # Key issues that should be caught (reference list)
    critical_issues = [
        "buffer overflow", "memory leak", "double free", "use after free",
        "null pointer", "array bounds", "uninitialized", "race condition",
        "integer overflow", "strcpy", "gets", "sprintf"
    ]
    
    # Count how many critical issues were mentioned
    caught_issues = []
    for issue in critical_issues:
        if issue.lower() in review_text.lower():
            caught_issues.append(issue)
    
    # Basic quality metrics
    word_count = len(review_text.split())
    line_count = len(review_text.split('\n'))
    
    return {
        "caught_critical_issues": caught_issues,
        "coverage_percentage": round((len(caught_issues) / len(critical_issues)) * 100, 1),
        "word_count": word_count,
        "line_count": line_count,
        "has_specific_recommendations": "fix" in review_text.lower() or "recommend" in review_text.lower(),
        "mentions_severity": any(sev in review_text.lower() for sev in ["critical", "high", "medium", "low"])
    }

def main():
    print("=" * 60)
    print("🧪 BAD C++ CODE REVIEW TEST")
    print("=" * 60)
    
    # Load the bad C++ sample
    code = load_bad_cpp_sample()
    if not code:
        return
    
    print(f"📄 Loaded sample with {len(code)} characters")
    print(f"📊 Code contains 50+ intentional issues across multiple categories")
    
    # Get available models
    try:
        response = requests.get(f"{OLLAMA_SERVER}/api/tags")
        if response.status_code == 200:
            models = [m['name'] for m in response.json().get('models', [])]
            print(f"🤖 Available models: {models}")
        else:
            print("❌ Cannot get model list")
            return
    except Exception as e:
        print(f"❌ Server connection failed: {e}")
        return
    
    if not models:
        print("❌ No models available")
        return
    
    # Test with first available model (you can modify this)
    test_model = models[22]
    print(f"\n🎯 Testing with model: {test_model}")
    
    # Run comprehensive review
    print("\n" + "=" * 50)
    print("🔍 COMPREHENSIVE REVIEW TEST")
    print("=" * 50)
    
    comprehensive_result = test_comprehensive_review(test_model, code)
    
    if comprehensive_result["success"]:
        print(f"✅ Review completed in {comprehensive_result['response_time']}s")
        
        # Analyze review quality
        quality_analysis = analyze_review_quality(comprehensive_result["review"])
        
        print(f"\n📊 REVIEW QUALITY ANALYSIS:")
        print(f"  Critical issues caught: {len(quality_analysis['caught_critical_issues'])}/12")
        print(f"  Coverage: {quality_analysis['coverage_percentage']}%")
        print(f"  Issues identified: {', '.join(quality_analysis['caught_critical_issues'])}")
        print(f"  Word count: {quality_analysis['word_count']}")
        print(f"  Has specific fixes: {quality_analysis['has_specific_recommendations']}")
        print(f"  Uses severity ratings: {quality_analysis['mentions_severity']}")
        
        print(f"\n📝 FULL REVIEW RESULTS:")
        print("-" * 50)
        print(comprehensive_result["review"])
        
    else:
        print(f"❌ Comprehensive review failed: {comprehensive_result['error']}")
    
    # Run focused reviews
    print(f"\n" + "=" * 50)
    print("🎯 FOCUSED REVIEW TESTS")
    print("=" * 50)
    
    focused_results = test_focused_review(test_model, code)
    
    for test_name, result in focused_results.items():
        print(f"\n--- {test_name} ---")
        if result["success"]:
            print(f"✅ Completed in {result['response_time']}s")
            quality = analyze_review_quality(result["review"])
            print(f"Coverage: {quality['coverage_percentage']}% | Words: {quality['word_count']}")
            
            # Show first 300 chars of review
            preview = result["review"][:300] + "..." if len(result["review"]) > 300 else result["review"]
            print(f"Preview: {preview}")
        else:
            print(f"❌ Failed: {result['error']}")

if __name__ == "__main__":
    main()
