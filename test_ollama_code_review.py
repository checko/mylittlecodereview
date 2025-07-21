#!/usr/bin/env python3
"""
Test script for Ollama code review capabilities
Server: 192.168.145.77:11434
"""

import requests
import json
import time
from typing import Dict, List

# Configuration
OLLAMA_SERVER = "http://192.168.145.77:11434"
MODELS = ["deepseek-r1:32b", "starcoder2:15b", "deepseek-r1:7b"]  # Add models you have available

class OllamaCodeReviewer:
    def __init__(self, server_url: str):
        self.server_url = server_url
        self.available_models = self.get_available_models()
        
    def get_available_models(self) -> List[str]:
        """Check which models are available on the server"""
        try:
            response = requests.get(f"{self.server_url}/api/tags")
            if response.status_code == 200:
                models = [model['name'] for model in response.json().get('models', [])]
                print(f"Available models: {models}")
                return models
            else:
                print(f"Failed to get models: {response.status_code}")
                return []
        except Exception as e:
            print(f"Error connecting to server: {e}")
            return []
    
    def review_code(self, code: str, model: str, prompt_type: str = "general") -> Dict:
        """Send code for review to Ollama"""
        prompts = {
            "general": f"""Please review this code for:
1. Bugs and potential issues
2. Performance improvements  
3. Code style and best practices
4. Security vulnerabilities

Code:
```
{code}
```

Provide specific, actionable feedback.""",

            "aosp_java": f"""Review this Android framework Java/Kotlin code for:
1. AOSP coding style compliance
2. Android API stability and compatibility
3. Binder IPC usage and thread safety
4. Memory management and GC pressure
5. Permission model adherence
6. Performance impact on Android runtime

Focus on AOSP-specific patterns and anti-patterns.

Code:
```
{code}
```""",

            "aosp_cpp": f"""Review this Android native C/C++ code for:
1. Android.bp build system compatibility
2. JNI best practices and error handling
3. Memory safety (ASAN/HWASAN compatibility)
4. Bionic libc usage patterns
5. SELinux policy compliance
6. Hardware abstraction layer standards
7. Power management efficiency

Code:
```
{code}
```""",

            "kernel": f"""Review this Linux kernel code for Android for:
1. Linux kernel coding style compliance
2. Android-specific optimizations (lowmemorykiller, etc.)
3. Security implications and privilege boundaries
4. Power management and suspend/resume
5. Compatibility with Android userspace
6. Performance impact on mobile workloads

Code:
```
{code}
```"""
        }
        
        prompt = prompts.get(prompt_type, prompts["general"])
        
        data = {
            "model": model,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "stream": False
        }
        
        try:
            start_time = time.time()
            response = requests.post(f"{self.server_url}/api/chat", json=data, timeout=300)
            end_time = time.time()
            
            if response.status_code == 200:
                result = response.json()
                return {
                    "success": True,
                    "review": result.get("message", {}).get("content", ""),
                    "model": model,
                    "response_time": round(end_time - start_time, 2),
                    "prompt_type": prompt_type
                }
            else:
                return {
                    "success": False,
                    "error": f"HTTP {response.status_code}: {response.text}",
                    "model": model,
                    "prompt_type": prompt_type
                }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "model": model,
                "prompt_type": prompt_type
            }

def test_code_samples():
    """Test code samples for different AOSP scenarios"""
    
    # Java/Kotlin Android Framework code
    java_code = """
public class SystemService extends Service {
    private static final String TAG = "SystemService";
    private Handler mHandler;
    
    @Override
    public void onCreate() {
        super.onCreate();
        mHandler = new Handler(Looper.getMainLooper());
        
        // Potential issue: no null check
        String config = getSystemService(Context.ACTIVITY_SERVICE).toString();
        Log.d(TAG, "Service created with config: " + config);
    }
    
    public void performOperation(String data) {
        // Potential issue: running on main thread
        try {
            Thread.sleep(5000);  // Blocking operation
            processData(data);
        } catch (InterruptedException e) {
            Log.e(TAG, "Operation interrupted", e);
        }
    }
    
    private void processData(String data) {
        // Missing input validation
        data.toLowerCase();
    }
}
"""
    
    # C++ Native Android code
    cpp_code = """
#include <jni.h>
#include <android/log.h>
#include <string.h>

#define LOG_TAG "NativeLib"
#define LOGI(...) __android_log_print(ANDROID_LOG_INFO, LOG_TAG, __VA_ARGS__)

extern "C" JNIEXPORT jstring JNICALL
Java_com_android_example_MainActivity_processData(JNIEnv *env, jobject thiz, jstring input) {
    const char* nativeInput = env->GetStringUTFChars(input, 0);
    
    // Potential issues: no null check, buffer overflow risk
    char result[100];
    strcpy(result, nativeInput);  // Unsafe copy
    strcat(result, "_processed"); // Could overflow
    
    // Memory leak: not releasing string
    return env->NewStringUTF(result);
}

// Missing JNI error handling
JNIEXPORT jint JNICALL
Java_com_android_example_MainActivity_calculateSum(JNIEnv *env, jobject thiz, jintArray array) {
    jint *elements = env->GetIntArrayElements(array, NULL);
    jsize length = env->GetArrayLength(array);
    
    int sum = 0;
    for (int i = 0; i <= length; i++) {  // Off-by-one error
        sum += elements[i];
    }
    
    return sum;
}
"""
    
    # Kernel module code
    kernel_code = """
#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/proc_fs.h>
#include <linux/uaccess.h>

static struct proc_dir_entry *proc_entry;
static char kernel_buffer[1024];

static ssize_t proc_write(struct file *file, const char __user *buffer, size_t count, loff_t *pos) {
    // Security issue: no bounds checking
    if (copy_from_user(kernel_buffer, buffer, count)) {
        return -EFAULT;
    }
    
    // Missing null termination
    printk(KERN_INFO "Received: %s\\n", kernel_buffer);
    return count;
}

static ssize_t proc_read(struct file *file, char __user *buffer, size_t count, loff_t *pos) {
    int len = strlen(kernel_buffer);
    
    if (*pos >= len) return 0;
    
    // Potential information leak
    if (copy_to_user(buffer, kernel_buffer, len)) {
        return -EFAULT;
    }
    
    *pos += len;
    return len;
}

static const struct proc_ops proc_fops = {
    .proc_read = proc_read,
    .proc_write = proc_write,
};

static int __init hello_init(void) {
    proc_entry = proc_create("android_test", 0666, NULL, &proc_fops);  // Too permissive
    if (!proc_entry) {
        return -ENOMEM;
    }
    return 0;
}

static void __exit hello_exit(void) {
    proc_remove(proc_entry);
}

MODULE_LICENSE("GPL");
"""
    
    return {
        "java": java_code,
        "cpp": cpp_code, 
        "kernel": kernel_code
    }

def main():
    print("=== Ollama Code Review Test ===")
    print(f"Server: {OLLAMA_SERVER}")
    
    reviewer = OllamaCodeReviewer(OLLAMA_SERVER)
    
    if not reviewer.available_models:
        print("No models available or server unreachable!")
        return
    
    test_samples = test_code_samples()
    
    # Test configurations
    test_configs = [
        ("java", "aosp_java", "Android Framework Java Code"),
        ("cpp", "aosp_cpp", "Android Native C++ Code"), 
        ("kernel", "kernel", "Android Kernel Module"),
    ]
    
    for sample_name, prompt_type, description in test_configs:
        print(f"\n{'='*60}")
        print(f"Testing: {description}")
        print(f"{'='*60}")
        
        code = test_samples[sample_name]
        print(f"Code snippet (first 200 chars):\n{code[:200]}...\n")
        
        # Test with first available model
        if reviewer.available_models:
            model = reviewer.available_models[0]
            print(f"Using model: {model}")
            
            result = reviewer.review_code(code, model, prompt_type)
            
            if result["success"]:
                print(f"✅ Review completed in {result['response_time']}s")
                print(f"Review:\n{result['review'][:500]}...")
                if len(result['review']) > 500:
                    print("[Review truncated for display]")
            else:
                print(f"❌ Review failed: {result['error']}")
        
        print("-" * 40)

if __name__ == "__main__":
    main()