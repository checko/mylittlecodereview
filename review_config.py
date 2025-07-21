#!/usr/bin/env python3
"""
Configuration file for inline code reviewer
Modify these settings to match your setup
"""

# Ollama server configuration
OLLAMA_SERVER = "http://192.168.145.77:11434"

# Model to use for reviews (you can change this)
MODEL_NAME = "deepseek-r1:32b"  # Your best performing model

# Alternative models you can switch to:
# MODEL_NAME = "deepseek-r1:14b"      # Faster, good quality
# MODEL_NAME = "starcoder2:15b"       # Code-specialized
# MODEL_NAME = "deepseek-coder:6.7b"  # Lighter weight

# Default input file when none specified
DEFAULT_INPUT_FILE = "bad_cpp_sample.cpp"

# Review prompt templates for different file types
REVIEW_PROMPTS = {
    "cpp": "Android native C++ security and memory safety review",
    "c": "Linux kernel and system programming review", 
    "java": "Android framework Java code review",
    "kotlin": "Android Kotlin development review"
}

# Output formatting options
USE_EMOJIS = True  # 🔴🟠🟡🟢 severity indicators
INCLUDE_SUMMARY = True
MAX_ISSUES_IN_SUMMARY = 10