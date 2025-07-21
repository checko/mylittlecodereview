# Prompt Engineering for AOSP Code Review

## Overview
Effective prompt engineering is crucial for getting high-quality code reviews from your LLM. This guide covers strategies specifically tailored for Android Open Source Project development.

## Core Prompt Engineering Principles

### 1. **Specificity is Key**
Instead of generic prompts, be specific about what you're looking for:

```python
# Generic (Poor)
"Review this code"

# Specific (Better)  
"Review this Android framework Java code for AOSP coding style compliance, thread safety issues, and performance impact on the Android runtime"
```

### 2. **Context Matters**
Always provide context about the code's purpose and environment:

```python
# Without Context
"Check this C++ code for issues"

# With Context
"Review this Android HAL implementation for memory safety, JNI best practices, and compatibility with Android 12+ security requirements"
```

### 3. **Structured Output**
Request structured reviews for consistency:

```python
prompt = """
Review this code and provide feedback in the following format:

## Security Issues
- [List any security vulnerabilities]

## Performance Concerns  
- [List performance-related issues]

## Style Violations
- [List AOSP style guide violations]

## Suggestions
- [Provide specific improvement recommendations]

Code:
{code}
"""
```

## AOSP-Specific Prompt Templates

### Android Framework (Java/Kotlin)
```python
aosp_framework_prompt = """
You are an expert Android framework developer. Review this {language} code from the Android framework for:

**Critical Issues:**
1. AOSP Java/Kotlin coding style compliance
2. Android API stability and backward compatibility
3. Binder IPC usage and thread safety
4. SystemServer integration patterns
5. Permission and security model adherence

**Performance Analysis:**
1. Memory allocation and GC pressure
2. Main thread blocking operations
3. Resource management (files, cursors, etc.)
4. Battery life impact

**Code Quality:**
1. Proper error handling and logging
2. Null safety and defensive programming  
3. Documentation and comments
4. Test coverage considerations

Focus on issues that could affect Android system stability or user experience.

Code:
```{language}
{code}
```

Provide specific, actionable feedback with line numbers where possible.
"""
```

### Native C/C++ Code
```python
aosp_native_prompt = """
You are an expert Android native developer. Analyze this C/C++ code for:

**Memory Safety:**
1. Buffer overflows and underflows
2. Use-after-free vulnerabilities
3. Memory leaks and resource management
4. ASAN/HWASAN compatibility

**Android Integration:**
1. JNI best practices and error handling
2. Android.bp/Android.mk build compatibility
3. Bionic libc usage patterns
4. NDK API compliance

**Security:**
1. SELinux policy compliance
2. Sandboxing and privilege boundaries
3. Input validation and sanitization
4. Secure coding practices

**Performance:**
1. CPU and memory efficiency
2. Power management considerations
3. Hardware abstraction layer standards
4. Real-time constraints

Code:
```cpp
{code}
```

Rate issues as: CRITICAL, HIGH, MEDIUM, LOW priority.
"""
```

### Linux Kernel Code
```python
kernel_prompt = """
You are an expert Linux kernel developer working on Android. Review this kernel code for:

**Android-Specific:**
1. Compatibility with Android userspace
2. Android-specific optimizations (lowmemorykiller, etc.)
3. Power management and suspend/resume
4. Mobile workload performance

**Security:**
1. Privilege escalation vulnerabilities  
2. Information disclosure risks
3. Input validation from userspace
4. Race condition vulnerabilities

**Code Quality:**
1. Linux kernel coding style compliance
2. Proper error handling and cleanup
3. Locking and synchronization
4. Resource management

**Performance:**
1. Latency impact on user experience
2. Memory usage efficiency  
3. CPU usage patterns
4. Scalability considerations

Code:
```c
{code}
```

Focus on issues that could impact Android device security or performance.
"""
```

## Advanced Prompt Techniques

### 1. **Few-Shot Learning**
Provide examples of good and bad code patterns:

```python
few_shot_prompt = """
Here are examples of common Android code issues:

BAD EXAMPLE:
```java
// Poor - blocking main thread
public void loadData() {
    String data = networkCall(); // Blocks UI
    updateUI(data);
}
```

GOOD EXAMPLE:
```java  
// Good - async operation
public void loadData() {
    AsyncTask.execute(() -> {
        String data = networkCall();
        runOnUiThread(() -> updateUI(data));
    });
}
```

Now review this code using similar analysis:
{code}
"""
```

### 2. **Chain-of-Thought Prompting**
Ask the model to explain its reasoning:

```python
reasoning_prompt = """
Analyze this Android code step by step:

1. First, identify what this code is trying to accomplish
2. Then, examine each section for potential issues
3. Consider the Android-specific implications
4. Finally, provide prioritized recommendations

Think through each step before providing your final assessment.

Code: {code}
"""
```

### 3. **Role-Based Prompting**
Assign specific expertise roles:

```python
expert_prompt = """
You are a senior Android security engineer conducting a security review. 
Your expertise includes:
- Android security model and permissions
- Common vulnerability patterns in Android apps
- Secure coding practices for mobile
- Android framework security mechanisms

Review this code specifically for security issues: {code}
"""
```

## Prompt Optimization Strategies

### 1. **Iterative Refinement**
Start with basic prompts and refine based on results:

```python
# Version 1: Basic
"Review this Android code for issues"

# Version 2: More specific  
"Review this Android service code for memory leaks and thread safety"

# Version 3: Comprehensive
"Review this Android service for memory leaks, thread safety, lifecycle issues, and AOSP coding standards"
```

### 2. **Context Window Management**
For large files, use focused prompts:

```python
large_file_prompt = """
This is a large Android file. Focus your review on:
1. The onCreate() and onDestroy() methods (lines 50-100)  
2. The data processing logic (lines 200-300)
3. Any obvious security issues throughout

Code: {code}
"""
```

### 3. **Multi-Pass Review**
Use different prompts for different aspects:

```python
# Pass 1: Security focus
security_prompt = "Review this code specifically for security vulnerabilities..."

# Pass 2: Performance focus  
performance_prompt = "Review this code specifically for performance issues..."

# Pass 3: Style focus
style_prompt = "Review this code for AOSP coding style compliance..."
```

## Measuring Prompt Effectiveness

### Key Metrics:
1. **Accuracy**: Does it catch real issues?
2. **Precision**: Are flagged issues actually problems?
3. **Completeness**: Does it miss obvious issues?
4. **Actionability**: Are suggestions specific and implementable?

### Testing Framework:
```python
def test_prompt_effectiveness(prompt_template, test_cases):
    results = {}
    for test_case in test_cases:
        review = get_llm_review(prompt_template, test_case.code)
        results[test_case.name] = {
            'caught_known_issues': check_known_issues(review, test_case.known_issues),
            'false_positives': count_false_positives(review, test_case.code),
            'actionability_score': rate_actionability(review)
        }
    return results
```

## Best Practices Summary

1. **Be Specific**: Clear, focused instructions work better than generic ones
2. **Provide Context**: Include file purpose, Android version, component type
3. **Structure Output**: Request organized, consistent feedback format
4. **Use Examples**: Show the model what good/bad patterns look like
5. **Iterate**: Refine prompts based on actual review quality
6. **Test Thoroughly**: Validate prompt effectiveness with known code issues
7. **Consider Token Limits**: Balance comprehensiveness with context window constraints

## Example Test Script Usage

The provided test script demonstrates these principles in action. Run it to see how different prompt types perform with your models:

```bash
python3 test_ollama_code_review.py
```

This will help you understand which prompt engineering approaches work best with your specific Ollama setup and models.