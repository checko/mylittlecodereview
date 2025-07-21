/*
 * BAD C++ Sample Code for Testing LLM Code Review
 * 
 * This file intentionally contains multiple categories of issues:
 * - Memory leaks and management issues
 * - Logic errors and edge cases
 * - Bad coding practices and style violations
 * - Security vulnerabilities
 * - Android/AOSP-specific anti-patterns
 * 
 * DO NOT USE THIS CODE IN PRODUCTION!
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <pthread.h>
#include <jni.h>
#include <android/log.h>
#include <vector>
#include <map>
#include <memory>

#define LOG_TAG "BadSampleCode"
#define LOGI(...) __android_log_print(ANDROID_LOG_INFO, LOG_TAG, __VA_ARGS__)

// Global variables (bad practice)
char* g_buffer = NULL;
int g_counter = 0;
pthread_mutex_t g_mutex; // Never initialized!

// Issue 1: Memory leak in constructor
class BadResourceManager {
public:
    BadResourceManager() {
        data = new char[1024];  // Never deleted!
        file_handle = fopen("/data/temp.txt", "w");  // Never closed!
        buffer_size = 1024;
    }
    
    // Issue 2: Missing virtual destructor
    ~BadResourceManager() {
        // Missing: delete[] data;
        // Missing: fclose(file_handle);
    }
    
    // Issue 3: Shallow copy constructor
    BadResourceManager(const BadResourceManager& other) {
        data = other.data;  // Sharing same memory!
        file_handle = other.file_handle;  // Sharing same file handle!
        buffer_size = other.buffer_size;
    }
    
private:
    char* data;
    FILE* file_handle;
    int buffer_size;
};

// Issue 4: Improper inheritance without virtual destructor
class DerivedBadClass : public BadResourceManager {
public:
    DerivedBadClass() {
        extra_data = malloc(2048);  // Mixed new/malloc, never freed
    }
    
    void* extra_data;
};

// Issue 5: Buffer overflow vulnerability
void unsafe_string_operation(const char* input) {
    char local_buffer[64];
    
    // Multiple buffer overflow risks
    strcpy(local_buffer, input);  // No bounds checking!
    strcat(local_buffer, "_suffix");  // Could overflow!
    
    // Issue 6: Using dangerous functions
    gets(local_buffer);  // Deprecated and unsafe!
    
    printf("Result: %s\n", local_buffer);
}

// Issue 7: Race condition and thread safety problems
void* thread_function(void* arg) {
    // Issue 8: No mutex lock for shared data
    g_counter++;
    
    // Issue 9: Accessing potentially null pointer
    if (g_buffer != NULL) {
        strcpy(g_buffer, "Thread was here");  // Still unsafe!
    }
    
    // Issue 10: Memory allocation without checking return value
    char* temp = (char*)malloc(1000);
    strcpy(temp, "Some data");
    // Never freed - memory leak!
    
    return NULL;
}

// Issue 11: Integer overflow and logical errors
int calculate_buffer_size(int num_elements, int element_size) {
    // Issue 12: No overflow checking
    int total_size = num_elements * element_size;
    
    // Issue 13: Logic error - should be <=
    if (total_size > 0) {
        return total_size;
    }
    
    // Issue 14: Returning uninitialized value in some paths
    int result;
    return result;  // Undefined behavior!
}

// Issue 15: Improper error handling
FILE* open_config_file(const char* filename) {
    FILE* file = fopen(filename, "r");
    
    // Issue 16: No error checking
    char buffer[256];
    fread(buffer, 1, 256, file);  // file might be NULL!
    
    return file;  // Might return NULL
}

// Issue 17: JNI errors and bad practices
extern "C" JNIEXPORT jstring JNICALL
Java_com_example_BadClass_processString(JNIEnv *env, jobject thiz, jstring input) {
    // Issue 18: No null checking
    const char* native_string = env->GetStringUTFChars(input, NULL);
    
    // Issue 19: Buffer overflow risk
    char result[100];
    sprintf(result, "Processed: %s with extra long suffix that might overflow", native_string);
    
    // Issue 20: Memory leak - not releasing JNI string
    // Missing: env->ReleaseStringUTFChars(input, native_string);
    
    // Issue 21: No exception checking
    return env->NewStringUTF(result);
}

// Issue 22: Array bounds errors
void array_processing_errors() {
    int numbers[10];
    
    // Issue 23: Off-by-one error
    for (int i = 0; i <= 10; i++) {  // Should be < 10
        numbers[i] = i * 2;  // Buffer overflow on last iteration
    }
    
    // Issue 24: Accessing negative index
    int index = -1;
    int value = numbers[index];  // Undefined behavior
    
    // Issue 25: Using uninitialized memory
    int* dynamic_array = (int*)malloc(20 * sizeof(int));
    for (int i = 0; i < 20; i++) {
        printf("%d ", dynamic_array[i]);  // Uninitialized values
    }
    // Memory leak - never freed
}

// Issue 26: Double free and use-after-free
void memory_corruption_example() {
    char* buffer1 = (char*)malloc(256);
    char* buffer2 = buffer1;  // Aliasing
    
    strcpy(buffer1, "Hello");
    free(buffer1);
    
    // Issue 27: Use after free
    printf("Buffer content: %s\n", buffer2);
    
    // Issue 28: Double free
    free(buffer2);  // Same memory already freed!
}

// Issue 29: Resource leaks in exception paths
void exception_safety_issues() {
    FILE* file = fopen("test.txt", "w");
    char* buffer = new char[1000];
    
    // Issue 30: If an exception occurs here, resources leak
    std::vector<int> vec;
    vec.at(100);  // Will throw, but no cleanup!
    
    // These lines might never execute:
    fclose(file);
    delete[] buffer;
}

// Issue 31: Improper container usage
void container_misuse() {
    std::map<int, char*> string_map;
    
    for (int i = 0; i < 100; i++) {
        char* str = (char*)malloc(50);
        sprintf(str, "String %d", i);
        string_map[i] = str;  // Storing raw pointers
    }
    
    // Issue 32: Never freeing the allocated strings
    string_map.clear();  // Only clears pointers, not the memory they point to!
}

// Issue 33: Ignoring return values
void ignoring_return_values() {
    // Issue 34: Ignoring malloc failure
    char* buffer = (char*)malloc(1000000000);  // Might fail!
    strcpy(buffer, "This will crash if malloc failed");
    
    // Issue 35: Ignoring function return codes
    system("rm -rf /");  // Dangerous command, return value ignored
}

// Issue 36: Singleton pattern implementation issues
class BadSingleton {
public:
    static BadSingleton* getInstance() {
        if (instance == nullptr) {
            // Issue 37: Not thread-safe
            instance = new BadSingleton();  // Memory leak - never deleted
        }
        return instance;
    }
    
    // Issue 38: Public destructor in singleton
    ~BadSingleton() {}
    
private:
    BadSingleton() {
        data = new int[1000];  // Another leak
    }
    
    static BadSingleton* instance;
    int* data;
};

BadSingleton* BadSingleton::instance = nullptr;

// Issue 39: Recursive function without base case
int fibonacci_bad(int n) {
    // Issue 40: Missing base case handling for negative numbers
    if (n <= 1) return n;
    
    // Issue 41: Potential stack overflow for large n
    return fibonacci_bad(n-1) + fibonacci_bad(n-2);
}

// Issue 42: Main function with multiple problems
int main(int argc, char* argv[]) {
    // Issue 43: No argument validation
    printf("First argument: %s\n", argv[1]);  // Might crash if no args
    
    // Issue 44: Creating objects that leak
    BadResourceManager* manager = new BadResourceManager();  // Never deleted
    DerivedBadClass derived;  // Destructor issues
    
    // Issue 45: Thread creation without proper cleanup
    pthread_t thread1, thread2;
    pthread_create(&thread1, NULL, thread_function, NULL);
    pthread_create(&thread2, NULL, thread_function, NULL);
    // No pthread_join() - resource leak
    
    // Issue 46: Using uninitialized mutex
    pthread_mutex_lock(&g_mutex);  // Undefined behavior - never initialized
    g_counter++;
    pthread_mutex_unlock(&g_mutex);
    
    // Issue 47: Calling dangerous functions
    unsafe_string_operation("This is a very long string that will definitely cause buffer overflow");
    
    // Issue 48: More memory leaks
    array_processing_errors();
    memory_corruption_example();
    container_misuse();
    
    // Issue 49: Potential division by zero
    int divisor = 0;
    int result = 100 / divisor;  // Runtime error
    
    // Issue 50: Function that always throws
    exception_safety_issues();
    
    return 0;  // Program might crash before reaching here
}

/*
 * Summary of issues in this code:
 * 
 * Memory Management:
 * - Memory leaks (new without delete, malloc without free)
 * - Double free errors
 * - Use after free
 * - Mixed allocation methods (new/malloc)
 * 
 * Buffer Safety:
 * - Buffer overflows (strcpy, strcat, sprintf)
 * - Array bounds violations
 * - Using dangerous functions (gets, strcpy)
 * 
 * Logic Errors:
 * - Off-by-one errors
 * - Missing base cases
 * - Integer overflow
 * - Division by zero
 * 
 * Threading Issues:
 * - Race conditions
 * - Uninitialized mutexes
 * - Missing thread cleanup
 * 
 * Error Handling:
 * - Ignoring return values
 * - No null pointer checks
 * - Poor exception safety
 * 
 * Style/Design Issues:
 * - Global variables
 * - Missing virtual destructors
 * - Non-thread-safe singleton
 * - Poor RAII practices
 * 
 * Security Issues:
 * - Input validation missing
 * - Command injection potential
 * - Information disclosure
 * - Privilege escalation risks
 */