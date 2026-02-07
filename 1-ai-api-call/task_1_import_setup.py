#!/usr/bin/env python3
"""
Task 1: Import Required Libraries
Learn what libraries we need for AI API calls.
"""

# Step 1: Import the OpenAI library
# This library helps us talk to AI models
import openai  # TODO: Import "openai"

# Step 2: Import os for environment variables
# This helps us access API keys safely
import os  # TODO: Import "os"
from tee_loger import setup_log

setup_log("markers/task1_log.txt")

print("✅ Step 1 Complete: Libraries imported!")
print("- openai: For making API calls")
print("- os: For accessing environment variables")

# Create marker
os.makedirs("markers", exist_ok=True)
with open("markers/task1_imports_complete.txt", "w") as f:
    f.write("SUCCESS")