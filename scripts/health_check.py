#!/usr/bin/env python3
"""
Quick health check for all backend components
"""

import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
load_dotenv()


def check_environment():
    """Check environment variables"""
    print("🔍 Checking Environment Variables...")
    
    required = ["LLM_PROVIDER"]
    provider = os.getenv("LLM_PROVIDER", "anthropic")
    
    if provider == "anthropic":
        required.append("ANTHROPIC_API_KEY")
    elif provider == "openai":
        required.append("OPENAI_API_KEY")
    elif provider == "openrouter":
        required.append("OPENROUTER_API_KEY")
    
    issues = []
    for var in required:
        if not os.getenv(var):
            issues.append(f"  ❌ {var} not set")
        else:
            print(f"  ✅ {var} configured")
    
    if issues:
        print("\n".join(issues))
        return False
    return True


def check_imports():
    """Check all imports work"""
    print("\n🔍 Checking Module Imports...")
    
    modules = [
        ("app", "EEResearchScout"),
        ("tools.research_tools", "ResearchTools"),
        ("tools.component_tools", "ComponentAnalyzer"),
        ("tools.supply_chain", "SupplyChainTracker"),
        ("utils.compliance_checker", "ComplianceChecker"),
        ("utils.cost_estimator", "CostEstimator"),
    ]
    
    issues = []
    for module_name, class_name in modules:
        try:
            module = __import__(module_name, fromlist=[class_name])
            getattr(module, class_name)
            print(f"  ✅ {module_name}.{class_name}")
        except Exception as e:
            issues.append(f"  ❌ {module_name}.{class_name}: {e}")
    
    if issues:
        print("\n".join(issues))
        return False
    return True


def check_llm_provider():
    """Check LLM provider initializes"""
    print("\n🔍 Checking LLM Provider...")
    
    try:
        from app import LLMProvider
        llm = LLMProvider()
        print(f"  ✅ Provider: {llm.provider}")
        print(f"  ✅ Model: {llm.model}")
        print(f"  ✅ Client initialized")
        return True
    except Exception as e:
        print(f"  ❌ LLM Provider Error: {e}")
        return False


def check_tools():
    """Check tools initialize"""
    print("\n🔍 Checking Tools...")
    
    try:
        from tools.research_tools import ResearchTools
        from tools.component_tools import ComponentAnalyzer
        from tools.supply_chain import SupplyChainTracker
        
        tools = [
            ("ResearchTools", ResearchTools()),
            ("ComponentAnalyzer", ComponentAnalyzer()),
            ("SupplyChainTracker", SupplyChainTracker()),
        ]
        
        for name, tool in tools:
            print(f"  ✅ {name} initialized")
        
        return True
    except Exception as e:
        print(f"  ❌ Tools Error: {e}")
        return False


def check_files():
    """Check all required files exist"""
    print("\n🔍 Checking File Structure...")
    
    required_files = [
        "app.py",
        "requirements.txt",
        ".env",
        "static/index.html",
        "tools/__init__.py",
        "tools/research_tools.py",
        "tools/component_tools.py",
        "tools/supply_chain.py",
        "config/domains.json",
    ]
    
    issues = []
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"  ✅ {file_path}")
        else:
            issues.append(f"  ❌ {file_path} missing")
    
    if issues:
        print("\n".join(issues))
        return False
    return True


def main():
    """Run all health checks"""
    print("=" * 60)
    print("  EE Research Scout - Health Check")
    print("=" * 60)
    
    checks = [
        ("File Structure", check_files),
        ("Environment", check_environment),
        ("Module Imports", check_imports),
        ("LLM Provider", check_llm_provider),
        ("Tools", check_tools),
    ]
    
    results = []
    for check_name, check_func in checks:
        try:
            result = check_func()
            results.append((check_name, result))
        except Exception as e:
            print(f"\n❌ {check_name} failed with exception: {e}")
            results.append((check_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("  Health Check Summary")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for check_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}  {check_name}")
    
    print(f"\nResult: {passed}/{total} checks passed")
    
    if passed == total:
        print("\n🎉 All systems operational!")
        return 0
    else:
        print("\n⚠️  Some checks failed. Please review above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
