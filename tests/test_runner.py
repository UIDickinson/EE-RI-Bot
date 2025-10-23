#!/usr/bin/env python3
"""
Comprehensive test runner for EE Research Scout Agent
Runs all tests and generates a detailed report
"""

import sys
import subprocess
import time
from pathlib import Path
from datetime import datetime
import json


class TestRunner:
    def __init__(self):
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "tests": {},
            "summary": {
                "total": 0,
                "passed": 0,
                "failed": 0,
                "skipped": 0
            }
        }
    
    def print_header(self, text):
        """Print formatted header"""
        print("\n" + "=" * 80)
        print(f"  {text}")
        print("=" * 80 + "\n")
    
    def run_command(self, cmd, test_name):
        """Run a command and capture results"""
        print(f"Running: {test_name}...")
        start_time = time.time()
        
        try:
            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )
            
            duration = time.time() - start_time
            success = result.returncode == 0
            
            self.results["tests"][test_name] = {
                "passed": success,
                "duration": round(duration, 2),
                "output": result.stdout if success else result.stderr
            }
            
            if success:
                print(f"✅ {test_name} PASSED ({duration:.2f}s)")
                self.results["summary"]["passed"] += 1
            else:
                print(f"❌ {test_name} FAILED ({duration:.2f}s)")
                print(f"Error: {result.stderr[:200]}")
                self.results["summary"]["failed"] += 1
            
            self.results["summary"]["total"] += 1
            
            return success
            
        except subprocess.TimeoutExpired:
            print(f"⏱️  {test_name} TIMEOUT")
            self.results["tests"][test_name] = {
                "passed": False,
                "duration": 300,
                "output": "Test timeout after 5 minutes"
            }
            self.results["summary"]["failed"] += 1
            self.results["summary"]["total"] += 1
            return False
        
        except Exception as e:
            print(f"❌ {test_name} ERROR: {e}")
            self.results["tests"][test_name] = {
                "passed": False,
                "duration": 0,
                "output": str(e)
            }
            self.results["summary"]["failed"] += 1
            self.results["summary"]["total"] += 1
            return False
    
    def run_all_tests(self):
        """Run all test suites"""
        self.print_header("EE RESEARCH SCOUT AGENT - TEST SUITE")
        
        # Check environment
        print("Checking environment variables...")
        from dotenv import load_dotenv
        import os
        
        load_dotenv()
        
        if not os.getenv("LLM_PROVIDER"):
            print("⚠️  Warning: LLM_PROVIDER not set, defaulting to 'anthropic'")
        
        provider = os.getenv("LLM_PROVIDER", "anthropic")
        api_key_var = f"{provider.upper()}_API_KEY"
        
        if not os.getenv(api_key_var):
            print(f"❌ Error: {api_key_var} not set in .env file")
            print("Please set your API key before running tests.")
            return False
        
        print(f"✅ Using provider: {provider}")
        print(f"✅ API key configured\n")
        
        # Test suites
        test_suites = [
            ("Environment Check", "python -c \"from dotenv import load_dotenv; import os; load_dotenv(); print('✅ Environment loaded')\""),
            ("Tool Tests", "python -m pytest tests/test_tools.py -v -m 'not slow'"),
            ("LLM Provider Tests (Quick)", "python -m pytest tests/test_llm_provider.py -v -m 'not slow'"),
            ("Compliance Tests", "python -m pytest tests/test_compliance.py -v"),
            ("Integration Tests", "python -m pytest tests/test_integration.py -v"),
        ]
        
        all_passed = True
        
        for test_name, cmd in test_suites:
            self.print_header(test_name)
            if not self.run_command(cmd, test_name):
                all_passed = False
        
        # Optional slow tests
        print("\n" + "-" * 80)
        run_slow = input("\n⚠️  Run slow tests (LLM API calls)? This will use API credits. (y/N): ")
        
        if run_slow.lower() == 'y':
            self.print_header("SLOW TESTS (LLM API Calls)")
            slow_tests = [
                ("LLM Completion Test", "python -m pytest tests/test_llm_provider.py::TestLLMProvider::test_completion -v -s"),
                ("LLM Streaming Test", "python -m pytest tests/test_llm_provider.py::TestLLMProvider::test_streaming -v -s"),
            ]
            
            for test_name, cmd in slow_tests:
                self.run_command(cmd, test_name)
        
        return all_passed
    
    def generate_report(self):
        """Generate test report"""
        self.print_header("TEST REPORT")
        
        summary = self.results["summary"]
        total = summary["total"]
        passed = summary["passed"]
        failed = summary["failed"]
        
        pass_rate = (passed / total * 100) if total > 0 else 0
        
        print(f"Total Tests: {total}")
        print(f"✅ Passed: {passed}")
        print(f"❌ Failed: {failed}")
        print(f"Pass Rate: {pass_rate:.1f}%")
        
        # Detailed results
        print("\nDetailed Results:")
        print("-" * 80)
        
        for test_name, result in self.results["tests"].items():
            status = "✅ PASS" if result["passed"] else "❌ FAIL"
            duration = result["duration"]
            print(f"{status}  {test_name:<40} ({duration}s)")
        
        # Save report
        report_file = Path("test_results.json")
        with open(report_file, 'w') as f:
            json.dump(self.results, f, indent=2)
        
        print(f"\n📄 Full report saved to: {report_file}")
        
        # Return success status
        return failed == 0
    
    def check_dependencies(self):
        """Check if pytest is installed"""
        try:
            import pytest
            print("✅ pytest is installed")
            return True
        except ImportError:
            print("❌ pytest not installed")
            print("Install with: pip install pytest pytest-asyncio")
            return False


def main():
    """Main entry point"""
    runner = TestRunner()
    
    # Check dependencies
    if not runner.check_dependencies():
        print("\n❌ Please install required dependencies first:")
        print("pip install pytest pytest-asyncio")
        sys.exit(1)
    
    # Run tests
    start_time = time.time()
    all_passed = runner.run_all_tests()
    total_duration = time.time() - start_time
    
    # Generate report
    success = runner.generate_report()
    
    print(f"\n⏱️  Total test duration: {total_duration:.2f}s")
    
    if success:
        print("\n🎉 All tests passed!")
        sys.exit(0)
    else:
        print("\n⚠️  Some tests failed. Check the report above.")
        sys.exit(1)


if __name__ == "__main__":
    main()