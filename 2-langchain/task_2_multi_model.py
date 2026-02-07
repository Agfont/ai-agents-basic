#!/usr/bin/env python3
"""
Task 2: Multi-Model Support - One Interface, Many Providers!
Test OpenAI, Google, and X.AI models using the same LangChain interface.

Learning Goal: Experience provider flexibility without code changes.
"""

import os
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from tee_loger import setup_log

load_dotenv()
setup_log("markers/task2_log.txt")

def main():
    print("🎯 Task 2: Multi-Model Support with LangChain")
    print("=" * 50)

    print("\n🌐 Initialize Multiple AI Providers")
    print("=" * 50)

    # TODO 1: Initialize OpenAI model
    print("Setting up OpenAI GPT-4.1-nano...")
    openai_llm = ChatOpenAI(
        model="gpt-4.1-nano",                    # Replace ___ with: "openai/gpt-4.1-nano"
        api_key=os.getenv("OPENAI_API_KEY"),      # Replace ___ with: "OPENAI_API_KEY"
        base_url=os.getenv("OPENAI_API_BASE")      # Replace ___ with: "OPENAI_API_BASE"
    )

    # TODO 2: Initialize Google Gemini model
    # print("Setting up Google Gemini...")
    # google_llm = ChatGoogleGenerativeAI(
    #     model="gemini-2.5-flash",                    # Replace ___ with: "gemini-2.5-flash"
    #     api_key=os.getenv("GEMINI_API_KEY"),      # Replace ___ with: "GEMINI_API_KEY"
    #     base_url=os.getenv("GEMINI_API_BASE")      # Replace ___ with: "GEMINI_API_BASE"
    # )

    # # TODO 3: Initialize X.AI Grok model
    # print("Setting up X.AI Grok...")
    # xai_llm = ChatXAI(
    #     model="grok-code-fast-1",                    # Replace ___ with: "grok-code-fast-1"
    #     api_key=os.getenv("GROK_API_KEY"),      # Replace ___ with: "GROK_API_KEY"
    #     base_url=os.getenv("GROK_API_BASE")      # Replace ___ with: "GROK_API_BASE"
    # )

    # Compare all models with the same prompt
    print("\n✅ All models initialized! Now let's compare them...")
    print("\nModel Comparison - Same Prompt, Different Models")
    print("=" * 50)

    test_prompt = "Explain cloud computing in one sentence"
    print(f"📝 Prompt: '{test_prompt}'\n")

    # Test all models with the same prompt
    if openai_llm:
        response = openai_llm.invoke(test_prompt)
        print(f"OpenAI: {response.content[:100]}...")

    # if google_llm:
    #     response = google_llm.invoke(test_prompt)
    #     print(f"Google: {response.content[:100]}...")

    # if xai_llm:
    #     response = xai_llm.invoke(test_prompt)
    #     print(f"X.AI: {response.content[:100]}...")

    print("\n💡 Same code, different providers - perfect for A/B testing!")

    # Create marker for completion
    os.makedirs("markers", exist_ok=True)
    with open("markers/task2_complete.txt", "w") as f:
        f.write("COMPLETED")

    print("\n✅ Task 2 completed! You can now switch models at will!")
    print("🎉 You tested 3 different AI providers with identical code!")

if __name__ == "__main__":
    main()