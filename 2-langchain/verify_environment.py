#!/usr/bin/env python3
"""
Environment Verification Script
Verify that the LangChain lab environment is properly configured.
"""

import sys
import os
import subprocess
from dotenv import load_dotenv
load_dotenv()

def verify_environment():
    """Verify that all required packages and environment variables are available."""
    print("🔍 Verifying LangChain Lab Environment")
    print("=" * 60)

    # Check Python version
    python_version = sys.version_info
    print(f"✅ Python version: {python_version.major}.{python_version.minor}.{python_version.micro}")

    # Check if running in virtual environment
    print("\n📦 Virtual Environment Check:")
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("✅ Running in virtual environment")
    else:
        venv_path = ".venv"
        if os.path.exists(venv_path):
            print(f"⚠️  Virtual environment exists at {venv_path}")
            print("   Please activate it with: source .venv/bin/activate")
            print("   Then run this script again!")
            return False
        else:
            print("⚠️  No virtual environment detected")
            print("   This is OK for KodeKloud environment")

    # Check required packages
    print("\n📚 Required Packages:")
    packages_to_check = [
        ('openai', 'OpenAI SDK'),
        ('langchain', 'LangChain Core'),
        ('langchain_openai', 'LangChain OpenAI'),
        ('pydantic', 'Data Validation')
    ]

    missing_packages = []

    for package, description in packages_to_check:
        try:
            __import__(package)
            print(f"✅ {description} ({package}) - Installed")
        except ImportError:
            print(f"❌ {description} ({package}) - Missing")
            missing_packages.append(package)

    # Check environment variables
    print("\n🔑 API Configuration:")
    api_key = os.getenv('OPENAI_API_KEY')
    api_base = os.getenv('OPENAI_API_BASE')

    if api_key:
        print("✅ OPENAI_API_KEY - Configured")
    else:
        print("⚠️  OPENAI_API_KEY - Not set (will be configured in tasks)")

    if api_base:
        print("✅ OPENAI_API_BASE - Configured")
    else:
        print("⚠️  OPENAI_API_BASE - Not set (will be configured in tasks)")

    # Check directories
    print("\n📁 Required Directories:")
    directories = ['markers']
    for directory in directories:
        if os.path.exists(directory):
            print(f"✅ {directory} - Exists")
        else:
            os.makedirs(directory, exist_ok=True)
            print(f"✅ {directory} - Created")

    # Final status
    print("\n" + "=" * 60)
    if missing_packages:
        print("❌ ENVIRONMENT INCOMPLETE")
        print(f"\nMissing packages: {', '.join(missing_packages)}")
        print("\nTo fix, run:")
        print("  source .venv/bin/activate")
        print("  pip install openai langchain langchain-openai")
        return False
    else:
        print("🎉 ENVIRONMENT READY!")
        print("\nYou can now proceed with the LangChain tasks:")
        print("  - Task 1: OpenAI vs LangChain comparison")
        print("  - Task 2: Multi-model support")
        print("  - Task 3: Prompt templates")
        print("  - Task 4: Output parsers")
        print("  - Task 5: Complete chain composition")

        # Create verification marker
        with open("markers/environment_verified.txt", "w") as f:
            f.write("VERIFIED")

        print("\n💡 Remember to activate the virtual environment:")
        print("   source .venv/bin/activate")

        return True

if __name__ == "__main__":
    success = verify_environment()
    sys.exit(0 if success else 1)