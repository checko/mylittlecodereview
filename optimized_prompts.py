#!/usr/bin/env python3
"""
Optimized prompts based on test results analysis
These prompts are tuned for better performance based on actual DeepSeek-R1-32B results
"""

# Improved security-focused prompt (was only 33.3% coverage)
SECURITY_FOCUSED_PROMPT = """You are a security expert specializing in C++ vulnerabilities and Android native security.

Perform a SECURITY-FOCUSED analysis of this code. Look specifically for:

## BUFFER OVERFLOW VULNERABILITIES
- strcpy, strcat, sprintf without bounds checking
- Array access without bounds validation  
- Gets() and other dangerous functions
- String buffer manipulation risks

## MEMORY CORRUPTION ATTACKS
- Use-after-free exploitation vectors
- Double-free attack possibilities
- Integer overflow leading to memory corruption
- Uninitialized memory access

## INPUT VALIDATION BYPASSES
- Missing null pointer checks
- Lack of input sanitization
- Buffer size assumptions
- Format string vulnerabilities

## PRIVILEGE ESCALATION RISKS
- Unsafe system() calls
- File permission issues
- Race condition in privileged operations
- Resource access without proper checks

## INFORMATION DISCLOSURE
- Uninitialized memory leaking data
- Error messages revealing internals
- Debug information in production code
- Resource handles exposed

For EACH vulnerability found:
1. **SEVERITY**: CRITICAL/HIGH/MEDIUM/LOW + CVE-style scoring
2. **ATTACK VECTOR**: How an attacker would exploit this
3. **IMPACT**: What damage could result
4. **EXPLOIT SCENARIO**: Concrete example of exploitation
5. **FIX**: Specific secure coding solution

Rate exploitability: EASY/MEDIUM/HARD

Code to analyze:
```cpp
{code}
```"""

# Enhanced comprehensive prompt (already 75% coverage, let's push to 90%+)
COMPREHENSIVE_ENHANCED_PROMPT = """You are an expert C++ security engineer and Android native developer with 15+ years experience.

Perform a COMPREHENSIVE code review focusing on production-quality Android native components.

## PRIMARY ANALYSIS AREAS

### 🚨 CRITICAL SECURITY ISSUES (Priority 1)
- Buffer overflows: strcpy, strcat, sprintf, gets usage
- Memory corruption: double-free, use-after-free, uninitialized access
- Integer vulnerabilities: overflow, underflow, signed/unsigned issues
- Input validation: null checks, bounds validation, format string bugs

### 💾 MEMORY MANAGEMENT (Priority 1)  
- Resource leaks: new/delete mismatches, malloc/free pairs
- RAII violations: missing destructors, exception safety
- Smart pointer opportunities: raw pointer risks
- Resource cleanup: files, mutexes, JNI references

### 🧵 CONCURRENCY ISSUES (Priority 2)
- Race conditions: shared data access patterns
- Deadlock potential: lock ordering, nested locks
- Thread safety: singleton patterns, global variables
- Synchronization: mutex initialization, atomic operations

### 📱 ANDROID-SPECIFIC ISSUES (Priority 1 for AOSP)
- JNI resource management: string release, exception handling
- Android lifecycle: service/activity integration
- Performance: main thread blocking, memory allocation patterns
- Security: SELinux compliance, permission boundaries

### 🐛 LOGIC ERRORS (Priority 2)
- Off-by-one: array bounds, loop conditions
- Null pointer dereferences: missing checks
- Edge cases: empty inputs, boundary conditions
- Error propagation: return code handling

## ANALYSIS METHODOLOGY
1. **Scan for dangerous function patterns** (strcpy, gets, etc.)
2. **Trace memory allocation/deallocation pairs**
3. **Identify shared resource access points**
4. **Check error handling completeness**
5. **Validate Android/JNI specific practices**

## OUTPUT FORMAT
For each issue:
- **SEVERITY**: CRITICAL/HIGH/MEDIUM/LOW
- **CATEGORY**: Security/Memory/Concurrency/Logic/Android
- **LOCATION**: Function name and approximate line reference
- **DESCRIPTION**: What the issue is and why it matters
- **IMPACT**: Consequences (crash, data loss, security breach)
- **FIX**: Specific, actionable solution with example code

## QUALITY REQUIREMENTS
- Prioritize CRITICAL and HIGH severity issues
- Provide specific function/location references
- Include code examples for fixes when helpful
- Focus on issues that affect stability and security

Code to review:
```cpp
{code}
```"""

# Memory-focused prompt (already 83.3%, let's get to 95%+)
MEMORY_ENHANCED_PROMPT = """You are a memory safety expert specializing in C++ and Android native development.

MEMORY SAFETY DEEP ANALYSIS - Focus exclusively on memory-related vulnerabilities.

## ALLOCATION/DEALLOCATION ANALYSIS
🔍 **Trace every memory allocation:**
- new/delete pairs - look for missing deletes
- malloc/free pairs - check for unmatched calls
- Resource acquisition (files, mutexes) - verify cleanup
- JNI string/array acquisition - check release calls

## MEMORY CORRUPTION VULNERABILITIES
🚨 **Critical memory safety issues:**
- **Buffer overflows**: strcpy, strcat, sprintf without bounds
- **Use-after-free**: accessing freed memory (double-free patterns)
- **Uninitialized access**: reading unset memory locations
- **Array bounds**: off-by-one errors, negative indexing
- **Stack corruption**: local buffer overflows

## ANDROID NATIVE MEMORY PATTERNS  
📱 **Android-specific memory issues:**
- JNI string handling: GetStringUTFChars without Release
- Exception safety in JNI calls
- Android service memory lifecycle
- Binder memory management patterns

## DETECTION METHODOLOGY
1. **Follow allocation sites**: Every new/malloc must have delete/free
2. **Track pointer lifetime**: Identify use-after-free opportunities  
3. **Buffer analysis**: Check all string/array operations for bounds
4. **Exception paths**: Verify cleanup in error conditions
5. **JNI patterns**: Validate resource acquisition/release pairs

## SEVERITY CLASSIFICATION
- **CRITICAL**: Remote code execution, heap corruption
- **HIGH**: Information disclosure, denial of service
- **MEDIUM**: Memory leaks, resource exhaustion  
- **LOW**: Style issues, minor inefficiencies

## DETAILED REPORTING
For each memory issue:
- **TYPE**: Buffer overflow/Memory leak/Use-after-free/Double-free/Uninitialized
- **LOCATION**: Specific function and operation
- **VULNERABLE CODE**: Exact problematic statement
- **EXPLOIT SCENARIO**: How memory corruption occurs
- **ANDROID IMPACT**: Effect on Android system/app stability
- **SECURE FIX**: Replacement code with bounds checking/RAII

Analyze this code for memory safety:
```cpp
{code}
```"""

# JNI-focused prompt (already 91.7%, let's maintain excellence)
JNI_EXPERT_PROMPT = """You are a senior Android framework engineer specializing in JNI and native integration.

ANDROID JNI & NATIVE DEVELOPMENT EXPERT REVIEW

## JNI RESOURCE MANAGEMENT
🔍 **Critical JNI patterns:**
- String handling: GetStringUTFChars → ReleaseStringUTFChars
- Array access: GetArrayElements → ReleaseArrayElements  
- Exception checking: Check after every JNI call
- Local/Global references: Proper reference management

## ANDROID NATIVE INTEGRATION
📱 **Android-specific concerns:**
- Thread safety in JNI callbacks
- Android lifecycle integration (onCreate/onDestroy)
- Performance on main thread vs background
- Memory pressure on Android devices
- SELinux policy compliance

## PERFORMANCE OPTIMIZATION
⚡ **Mobile-specific optimizations:**
- Minimize JNI transitions (expensive on mobile)
- Battery life impact of native operations
- Memory allocation patterns for Android
- CPU usage patterns for mobile workloads

## SECURITY IN NATIVE CODE
🛡️ **Android security model:**
- Input validation from Java layer
- Sandboxing and permission boundaries
- Secure coding for privileged operations
- Information leakage prevention

## ANALYSIS FOCUS AREAS
1. **JNI Call Patterns**: Verify proper resource cleanup
2. **Exception Handling**: JNI exception propagation
3. **Thread Safety**: Native code in multi-threaded Android
4. **Performance**: Mobile optimization opportunities
5. **Security**: Android security model compliance

## EXPERT EVALUATION CRITERIA
- **Correctness**: JNI usage follows Android guidelines
- **Safety**: Resource leaks and crash prevention
- **Performance**: Mobile-optimized implementations
- **Security**: Android security model adherence
- **Maintainability**: Code quality for Android framework

## DETAILED FEEDBACK FORMAT
For each JNI/Android issue:
- **CATEGORY**: JNI/Performance/Security/Thread Safety/Lifecycle
- **SEVERITY**: CRITICAL/HIGH/MEDIUM/LOW
- **JNI FUNCTION**: Specific JNI call involved
- **ANDROID CONTEXT**: How this affects Android system
- **MOBILE IMPACT**: Battery/memory/CPU implications
- **BEST PRACTICE**: Android-recommended approach
- **CODE EXAMPLE**: Corrected implementation

Review this Android native code:
```cpp
{code}
```"""

def test_optimized_prompts(server_url, model_name, code):
    """Test the optimized prompts"""
    
    prompts = {
        "Enhanced Security": SECURITY_FOCUSED_PROMPT,
        "Enhanced Comprehensive": COMPREHENSIVE_ENHANCED_PROMPT, 
        "Enhanced Memory Safety": MEMORY_ENHANCED_PROMPT,
        "Enhanced JNI Expert": JNI_EXPERT_PROMPT
    }
    
    results = {}
    
    for prompt_name, prompt_template in prompts.items():
        print(f"🧪 Testing: {prompt_name}")
        
        formatted_prompt = prompt_template.format(code=code)
        
        data = {
            "model": model_name,
            "messages": [{"role": "user", "content": formatted_prompt}],
            "stream": False
        }
        
        try:
            import requests
            import time
            
            start_time = time.time()
            response = requests.post(f"{server_url}/api/chat", json=data, timeout=300)
            end_time = time.time()
            
            if response.status_code == 200:
                result = response.json()
                review_content = result.get("message", {}).get("content", "")
                
                # Quick quality analysis
                critical_issues = [
                    "buffer overflow", "memory leak", "double free", "use after free",
                    "null pointer", "array bounds", "uninitialized", "race condition",
                    "integer overflow", "strcpy", "gets", "sprintf"
                ]
                
                caught_issues = [issue for issue in critical_issues 
                               if issue.lower() in review_content.lower()]
                
                results[prompt_name] = {
                    "success": True,
                    "response_time": round(end_time - start_time, 2),
                    "word_count": len(review_content.split()),
                    "coverage": round((len(caught_issues) / len(critical_issues)) * 100, 1),
                    "caught_issues": caught_issues,
                    "preview": review_content[:200] + "..." if len(review_content) > 200 else review_content
                }
            else:
                results[prompt_name] = {"success": False, "error": f"HTTP {response.status_code}"}
                
        except Exception as e:
            results[prompt_name] = {"success": False, "error": str(e)}
    
    return results

if __name__ == "__main__":
    print("🚀 Optimized Prompt Testing")
    print("Run this with: python3 -c 'import optimized_prompts; optimized_prompts.test_optimized_prompts(...)'")