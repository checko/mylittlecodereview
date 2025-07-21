# LLM Code Review System for AOSP Development

A comprehensive system for automated code review using local LLM inference, specifically optimized for Android Open Source Project (AOSP) development with C/C++, Java, and Kotlin.

## 🚀 Quick Start

### Prerequisites
- Python 3.7+
- Ollama server running locally or on network
- DeepSeek-R1-32B (recommended) or other compatible models

### Basic Usage

```bash
# Test server connectivity
./quick_test.py

# Review a source file with inline comments
./review MyCode.cpp                    # Creates MyCode_REVIEWED.cpp
./review MyCode.java MyReview.java     # Custom output name
./review                               # Uses default test file

# Run comprehensive model evaluation
python3 test_bad_cpp.py

# Test optimized prompts
python3 run_optimized_test.py
```

## 📁 Project Structure

### Core Files
- **`inline_code_reviewer.py`** - Main script for inline code reviews
- **`review`** - Simple wrapper script for easy usage
- **`review_config.py`** - Configuration settings

### Documentation & Research
- **`llm-code-review-discussion.md`** - Complete research findings and recommendations
- **`prompt_engineering_guide.md`** - Guide for effective prompt engineering
- **`bad_cpp_sample.cpp`** - Test sample with 50+ intentional issues

### Testing & Validation Scripts
- **`quick_test.py`** - Basic connectivity and functionality test
- **`test_bad_cpp.py`** - Comprehensive model evaluation framework
- **`test_ollama_code_review.py`** - AOSP-specific testing suite
- **`run_optimized_test.py`** - Optimized prompt performance testing
- **`optimized_prompts.py`** - Enhanced prompts based on test results

## 🎯 Features

### Inline Code Reviews
- **Embedded comments** next to problematic code
- **Severity indicators** (🔴 CRITICAL, 🟠 HIGH, 🟡 MEDIUM, 🟢 LOW)
- **Automatic output naming** (file_REVIEWED.ext)
- **Summary statistics** with top priority fixes

### AOSP-Specific Analysis
- **Android framework** Java/Kotlin review
- **Native C/C++ code** security and memory safety
- **JNI best practices** validation
- **Kernel code** review for Android compatibility
- **Build system** integration (Android.bp/mk)

### Performance Benchmarking
- **Quantitative metrics** for review quality
- **Model comparison** capabilities
- **Response time measurement**
- **Coverage analysis** (% of issues caught)

## 🔧 Configuration

Edit `review_config.py` to customize:
```python
OLLAMA_SERVER = "http://your-server:11434"
MODEL_NAME = "deepseek-r1:32b"  # or your preferred model
```

## 📊 Model Performance (Tested Results)

Based on testing with DeepSeek-R1-32B:
- **Comprehensive Review**: 75% coverage, 89.56s response time
- **Memory Safety**: 83.3% coverage - excellent for C++
- **Android JNI**: 91.7% coverage - outstanding for AOSP
- **Security Analysis**: 33.3% coverage - room for improvement

## 🛠️ Integration Examples

### Git Pre-commit Hook
```bash
#!/bin/bash
changed_files=$(git diff --cached --name-only | grep -E '\.(cpp|c|h|java|kt)$')
for file in $changed_files; do
    ./review "$file"
    if grep -q "🔴 CRITICAL" "${file%.*}_REVIEWED.${file##*.}"; then
        echo "❌ CRITICAL issues found - fix before committing"
        exit 1
    fi
done
```

### Batch Processing
```bash
# Review all C++ files
find . -name "*.cpp" -exec ./review {} \;

# Review AOSP framework files
find frameworks/base -name "*.java" | xargs -I {} ./review {}
```

## 📈 Testing & Validation

### Run Model Evaluation
```bash
# Comprehensive test with known issues
python3 test_bad_cpp.py

# Results show:
# - Issues caught: X/12 critical patterns
# - Coverage percentage
# - Response time benchmarks
# - Quality analysis
```

### Test Optimized Prompts
```bash
# Compare baseline vs enhanced prompts
python3 run_optimized_test.py

# Shows improvement in:
# - Security vulnerability detection
# - Memory safety analysis
# - Android-specific issues
```

## 🎯 Use Cases

### Individual Developer
- Pre-commit code review automation
- Learning tool for identifying common issues
- Security vulnerability scanning

### Team Development
- Consistent review standards across team
- Automated first-pass review before human review
- Training junior developers on best practices

### Enterprise/Organization  
- Large-scale codebase analysis
- Security audit automation
- Compliance checking for coding standards

## 🔍 What Issues Are Detected

### Security Issues
- Buffer overflows and memory corruption
- Input validation failures
- Use-after-free vulnerabilities
- Integer overflow risks

### Memory Management
- Memory leaks (new/delete, malloc/free mismatches)
- Double-free errors
- Resource leaks (files, mutexes)
- RAII violations

### AOSP-Specific
- JNI resource management
- Android lifecycle issues
- Binder IPC best practices
- SELinux policy compliance

### Code Quality
- Thread safety issues
- Logic errors and edge cases
- Style guide violations
- Performance bottlenecks

## 📚 Documentation

- **Research findings**: Complete analysis in `llm-code-review-discussion.md`
- **Prompt engineering**: Best practices in `prompt_engineering_guide.md`
- **Test results**: Quantitative evaluation in testing scripts

## 🤝 Contributing

1. Test new models using the evaluation framework
2. Enhance prompts based on test results
3. Add support for additional languages
4. Improve integration with development tools

## 📄 License

This project is designed for defensive security and code quality improvement purposes only.