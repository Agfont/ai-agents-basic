#!/usr/bin/env python3
"""
Task 3: LLM Integration
Configure the AI generation engine using pre-configured OpenAI API
"""

import os
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from tee_loger import setup_log

load_dotenv()
setup_log("markers/task3_log.txt")

print("🤖 Task 3: LLM Integration")
print("=" * 50)

# Get environment variables
api_base = os.getenv("OPENAI_API_BASE")
api_key = os.getenv("OPENAI_API_KEY")

# TODO 1: Initialize LangChain ChatOpenAI client
# Hint: Use ChatOpenAI(api_key=api_key, base_url=api_base, model="gpt-4.1-nano")
client = ChatOpenAI(
    api_key=api_key,  # Replace ___ with api_key
    base_url=api_base,  # Replace ___ with api_base
    model="gpt-4.1-nano"  # Replace ___ with gpt-4.1-nano
)

print("✅ OpenAI client initialized")
print(f"   Using API: {api_base}")

# Test the LLM with a simple generation
def test_generation():
    """Test basic LLM generation"""

    # TODO 2: Set temperature for focused answers
    # Hint: Use 0.3 for deterministic responses
    temperature = 0.3  # Replace ___ with 0.3

    # TODO 3: Set max tokens for concise responses
    # Hint: Use 500 to limit response length
    max_tokens = 500  # Replace ___ with 500
    # Update client with temperature and max_tokens
    client.temperature = temperature
    client.max_tokens = max_tokens

    print(f"\n📝 Testing gpt-4.1-nano with temperature={temperature}")

    # Create messages for the query
    messages = [
        {"role": "system", "content": "You are a helpful AI assistant."},
        {"role": "user", "content": "What is RAG in AI? Answer in one sentence."}
    ]

    # Generate response using invoke method
    response = client.invoke(messages)
    answer = response.content

    print(f"\n🤖 Test Response: {answer}")

    return True

# Run the test
try:
    success = test_generation()

    print("\n" + "=" * 50)
    print("🎉 LLM Integration Successful!")
    print("   - Model: gpt-4.1-nano")
    print("   - Temperature: 0.3 (focused)")
    print("   - Max tokens: 500 (concise)")
    print("   - LangChain integration ready for RAG!")
    print("=" * 50)

    # Create marker file
    os.makedirs("markers", exist_ok=True)
    with open("markers/task3_llm_complete.txt", "w") as f:
        f.write("TASK3_COMPLETE:LLM_READY")

except Exception as e:
    print(f"\n❌ Error: {e}")
    print("\n💡 Check that OPENAI_API_BASE and OPENAI_API_KEY are set!")

print("\n💡 LLM ready to generate answers from retrieved context!")
print("\n✅ Task 3 completed!")