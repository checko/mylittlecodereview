#!/usr/bin/env python3
"""
Inline Code Reviewer - Embeds LLM review comments directly into source code
Creates annotated source files with review comments beside problematic code
"""

import requests
import json
import re
import time
from typing import Dict, List, Tuple

class InlineCodeReviewer:
    def __init__(self, ollama_server: str, model_name: str):
        self.ollama_server = ollama_server
        self.model_name = model_name
        
    def review_with_line_numbers(self, code: str, file_type: str = "cpp") -> Dict:
        """Get comprehensive review with specific line number references"""
        
        # Enhanced prompt that asks for line number references
        prompt = f"""You are an expert C++ and Android security reviewer. 

Please review this {file_type} code and provide feedback WITH SPECIFIC LINE NUMBER REFERENCES.

For each issue you find, you MUST provide:
1. **LINE NUMBER(S)**: Exact line number where the issue occurs
2. **ISSUE TYPE**: Security/Memory/Logic/Style/Performance  
3. **SEVERITY**: CRITICAL/HIGH/MEDIUM/LOW
4. **DESCRIPTION**: Brief description of the problem
5. **FIX**: Specific solution

Format each issue as:
LINE X: [SEVERITY] Issue description and fix recommendation

Here's the code with line numbers:

```cpp
{self._add_line_numbers(code)}
```

Focus on the most serious issues and be very specific about line numbers."""

        data = {
            "model": self.model_name,
            "messages": [{"role": "user", "content": prompt}],
            "stream": False
        }
        
        try:
            response = requests.post(f"{self.ollama_server}/api/chat", json=data, timeout=300)
            if response.status_code == 200:
                result = response.json()
                review_text = result.get("message", {}).get("content", "")
                return {"success": True, "review": review_text}
            else:
                return {"success": False, "error": f"HTTP {response.status_code}"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _add_line_numbers(self, code: str) -> str:
        """Add line numbers to code for LLM reference"""
        lines = code.split('\n')
        numbered_lines = []
        for i, line in enumerate(lines, 1):
            numbered_lines.append(f"{i:3d}: {line}")
        return '\n'.join(numbered_lines)
    
    def parse_line_based_issues(self, review_text: str) -> List[Dict]:
        """Parse LLM review to extract line-specific issues"""
        issues = []
        
        # Patterns to match line references
        patterns = [
            r"LINE (\d+):\s*\[(\w+)\]\s*(.*)",  # LINE X: [SEVERITY] description
            r"Line (\d+):\s*(\w+):\s*(.*)",     # Line X: SEVERITY: description
            r"Lines? (\d+)[-–](\d+):\s*(.*)",   # Line X-Y: description
            r"(\d+):\s*(.+)",                   # X: description (simple format)
        ]
        
        for line in review_text.split('\n'):
            line = line.strip()
            if not line:
                continue
                
            for pattern in patterns:
                match = re.search(pattern, line, re.IGNORECASE)
                if match:
                    if "LINE" in pattern or "Line" in pattern:
                        if len(match.groups()) == 3:
                            line_num, severity, description = match.groups()
                        else:
                            line_num, description = match.groups()
                            severity = "MEDIUM"  # default
                    else:
                        line_num, description = match.groups()
                        severity = "MEDIUM"
                    
                    issues.append({
                        "line": int(line_num),
                        "severity": severity.upper(),
                        "description": description.strip(),
                        "type": self._classify_issue_type(description)
                    })
                    break
        
        return issues
    
    def _classify_issue_type(self, description: str) -> str:
        """Classify issue type based on description"""
        description_lower = description.lower()
        
        if any(word in description_lower for word in ['buffer', 'overflow', 'security', 'injection', 'exploit']):
            return "SECURITY"
        elif any(word in description_lower for word in ['memory', 'leak', 'free', 'allocation']):
            return "MEMORY"
        elif any(word in description_lower for word in ['race', 'thread', 'mutex', 'deadlock']):
            return "CONCURRENCY"
        elif any(word in description_lower for word in ['jni', 'android', 'native']):
            return "ANDROID"
        elif any(word in description_lower for word in ['performance', 'slow', 'optimize']):
            return "PERFORMANCE"
        else:
            return "LOGIC"
    
    def create_annotated_source(self, source_code: str, issues: List[Dict], filename: str = "reviewed_code") -> str:
        """Create annotated source code with inline comments"""
        
        lines = source_code.split('\n')
        annotated_lines = []
        
        # Group issues by line number
        issues_by_line = {}
        for issue in issues:
            line_num = issue["line"]
            if line_num not in issues_by_line:
                issues_by_line[line_num] = []
            issues_by_line[line_num].append(issue)
        
        # Add header
        annotated_lines.extend([
            f"/*",
            f" * AUTOMATED CODE REVIEW RESULTS",
            f" * File: {filename}",
            f" * Reviewed by: {self.model_name}",
            f" * Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}",
            f" * Total Issues Found: {len(issues)}",
            f" *",
            f" * Legend:",
            f" *   🔴 CRITICAL - Immediate security/stability risk",
            f" *   🟠 HIGH     - Important issue, fix soon", 
            f" *   🟡 MEDIUM   - Should be addressed",
            f" *   🟢 LOW      - Minor improvement",
            f" */",
            f""
        ])
        
        # Process each line
        for i, line in enumerate(lines, 1):
            # Add the original line
            annotated_lines.append(line)
            
            # Add review comments for this line
            if i in issues_by_line:
                for issue in issues_by_line[i]:
                    severity_icon = {
                        "CRITICAL": "🔴",
                        "HIGH": "🟠", 
                        "MEDIUM": "🟡",
                        "LOW": "🟢"
                    }.get(issue["severity"], "⚪")
                    
                    comment_lines = [
                        f"/* {severity_icon} {issue['severity']} [{issue['type']}] LINE {i}:",
                        f" * ISSUE: {issue['description']}",
                        f" */"
                    ]
                    annotated_lines.extend(comment_lines)
            
            # Add spacing for readability
            if i in issues_by_line:
                annotated_lines.append("")
        
        # Add summary at the end
        summary = self._generate_summary(issues)
        annotated_lines.extend([
            "",
            "/*",
            " * ========================================",
            " * REVIEW SUMMARY",
            " * ========================================",
        ])
        
        for line in summary.split('\n'):
            annotated_lines.append(f" * {line}")
        
        annotated_lines.extend([
            " */",
            ""
        ])
        
        return '\n'.join(annotated_lines)
    
    def _generate_summary(self, issues: List[Dict]) -> str:
        """Generate summary statistics"""
        if not issues:
            return "No issues found."
        
        # Count by severity
        severity_counts = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0}
        type_counts = {}
        
        for issue in issues:
            severity_counts[issue["severity"]] = severity_counts.get(issue["severity"], 0) + 1
            type_counts[issue["type"]] = type_counts.get(issue["type"], 0) + 1
        
        summary_lines = [
            f"Total Issues: {len(issues)}",
            "",
            "By Severity:",
            f"  CRITICAL: {severity_counts['CRITICAL']} (🔴 Fix immediately!)",
            f"  HIGH:     {severity_counts['HIGH']} (🟠 Fix soon)",
            f"  MEDIUM:   {severity_counts['MEDIUM']} (🟡 Should address)",
            f"  LOW:      {severity_counts['LOW']} (🟢 Minor improvements)",
            "",
            "By Category:",
        ]
        
        for issue_type, count in sorted(type_counts.items()):
            summary_lines.append(f"  {issue_type}: {count}")
        
        # Top priority recommendations
        critical_and_high = [i for i in issues if i["severity"] in ["CRITICAL", "HIGH"]]
        if critical_and_high:
            summary_lines.extend([
                "",
                "TOP PRIORITY FIXES:",
            ])
            for i, issue in enumerate(critical_and_high[:5], 1):  # Top 5
                summary_lines.append(f"  {i}. Line {issue['line']}: {issue['description'][:60]}...")
        
        return '\n'.join(summary_lines)
    
    def review_file_inline(self, input_file: str, output_file: str = None) -> bool:
        """Complete workflow: review file and create annotated version"""
        
        try:
            # Read source file
            with open(input_file, 'r') as f:
                source_code = f.read()
            
            print(f"📄 Loaded {input_file}: {len(source_code)} characters")
            
            # Get file extension for context
            file_ext = input_file.split('.')[-1].lower()
            file_type = {
                'cpp': 'cpp', 'c': 'c', 'h': 'cpp',
                'java': 'java', 'kt': 'kotlin'
            }.get(file_ext, 'cpp')
            
            print(f"🔍 Reviewing with {self.model_name}...")
            
            # Get review with line references
            review_result = self.review_with_line_numbers(source_code, file_type)
            
            if not review_result["success"]:
                print(f"❌ Review failed: {review_result['error']}")
                return False
            
            print(f"✅ Review completed")
            
            # Parse issues with line numbers
            issues = self.parse_line_based_issues(review_result["review"])
            print(f"📊 Found {len(issues)} line-specific issues")
            
            # Create annotated source
            annotated_source = self.create_annotated_source(source_code, issues, input_file)
            
            # Save annotated version
            if output_file is None:
                base_name = input_file.rsplit('.', 1)[0]
                output_file = f"{base_name}_reviewed.{file_ext}"
            
            with open(output_file, 'w') as f:
                f.write(annotated_source)
            
            print(f"💾 Saved annotated version to: {output_file}")
            print(f"📈 Summary: {len(issues)} issues found and annotated inline")
            
            return True
            
        except Exception as e:
            print(f"❌ Error: {e}")
            return False

def main():
    """Main function with command line argument support"""
    import sys
    import os
    
    # Configuration
    OLLAMA_SERVER = "http://192.168.145.77:11434"
    MODEL_NAME = "deepseek-r1:32b"
    DEFAULT_INPUT_FILE = "bad_cpp_sample.cpp"
    
    # Parse command line arguments
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
        if len(sys.argv) > 2:
            output_file = sys.argv[2]
        else:
            # Auto-generate output filename
            base_name, ext = os.path.splitext(input_file)
            output_file = f"{base_name}_REVIEWED{ext}"
    else:
        input_file = DEFAULT_INPUT_FILE
        output_file = "bad_cpp_sample_REVIEWED.cpp"
    
    print("🚀 INLINE CODE REVIEWER")
    print(f"Model: {MODEL_NAME}")
    print(f"Server: {OLLAMA_SERVER}")
    
    # Check if input file exists
    if not os.path.exists(input_file):
        print(f"❌ Input file not found: {input_file}")
        if input_file != DEFAULT_INPUT_FILE:
            print(f"💡 Tip: Make sure the file path is correct")
            print(f"💡 Usage: python3 {sys.argv[0]} <input_file> [output_file]")
            print(f"💡 Example: python3 {sys.argv[0]} MyCode.cpp MyCode_REVIEWED.cpp")
        else:
            print(f"💡 Default file '{DEFAULT_INPUT_FILE}' not found in current directory")
            print(f"💡 Usage: python3 {sys.argv[0]} <your_source_file>")
        return
    
    print(f"📥 Input file: {input_file}")
    print(f"📤 Output file: {output_file}")
    
    reviewer = InlineCodeReviewer(OLLAMA_SERVER, MODEL_NAME)
    
    success = reviewer.review_file_inline(input_file, output_file)
    
    if success:
        print(f"\n✅ SUCCESS!")
        print(f"📁 Original: {input_file}")
        print(f"📁 Reviewed: {output_file}")
        print(f"\nThe annotated file contains:")
        print(f"  • Original source code")
        print(f"  • Inline comments for each issue") 
        print(f"  • Severity indicators (🔴🟠🟡🟢)")
        print(f"  • Summary statistics")
        print(f"  • Top priority fixes")
        print(f"\n💡 Usage examples:")
        print(f"  python3 {sys.argv[0]}                           # Use default file")
        print(f"  python3 {sys.argv[0]} MyCode.cpp                # Review MyCode.cpp")
        print(f"  python3 {sys.argv[0]} MyCode.cpp MyReview.cpp   # Custom output name")
    else:
        print(f"❌ Review failed")

if __name__ == "__main__":
    main()