#!/usr/bin/env python3
"""
Task 5: Complete Chain - Combining Everything!
Build complete AI pipelines using LangChain's chain composition.

Learning Goal: Master chain composition with the pipe operator (|).
"""

import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.output_parsers import CommaSeparatedListOutputParser
from dotenv import load_dotenv
from tee_loger import setup_log

load_dotenv()
setup_log("markers/task5_log.txt")

def main():
    print("🎯 Task 5: Chain Composition with |")
    print("=" * 50)

    # Initialize LLM once
    llm = ChatOpenAI(
        model="gpt-4.1-nano",
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("OPENAI_API_BASE"),
        temperature=0.3
    )

    # Chain 1: Simple Analysis Chain
    print("\n⛓️ Chain 1: Simple Analysis")
    print("=" * 50)

    # Create analysis prompt
    analysis_prompt = PromptTemplate(
        template="Analyze {technology} and provide pros and cons in 2-3 sentences",
        input_variables=["technology"]
    )

    # String parser for text output
    str_parser = StrOutputParser()

    # TODO 1: Build analysis chain using pipe operator
    analysis_chain = analysis_prompt | llm | str_parser  # Replace ___ with: analysis_prompt, llm, str_parser

    # Test the analysis chain
    if analysis_chain:
        result = analysis_chain.invoke({
            "technology": "blockchain"
        })
        print(f"📝 Input: 'Analyze blockchain'")
        print(f"✅ Output: {result}")

    # Chain 2: List Generation Chain
    print("\n⛓️ Chain 2: List Generation with Parser")
    print("=" * 50)

    # Create list prompt
    list_prompt = PromptTemplate(
        template="List 3 use cases for {technology} (comma-separated):",
        input_variables=["technology"]
    )

    # List parser for structured output
    list_parser = CommaSeparatedListOutputParser()

    # TODO 2: Build list chain with different parser
    list_chain = list_prompt | llm | list_parser  # Replace ___ with: list_prompt, llm, list_parser

    # Test the list chain
    if list_chain:
        result = list_chain.invoke({
            "technology": "blockchain"
        })
        print(f"📝 Input: 'List use cases for blockchain'")
        print(f"✅ Output: {result}")
        print(f"✅ Type: {type(result)} - Python list!")

    # Demonstrate the power of chains
    print("\n🎉 Complete Pipeline Example")
    print("=" * 50)

    test_tech = "artificial intelligence"
    print(f"Technology: {test_tech}\n")

    # Run both chains on the same input
    if analysis_chain and list_chain:
        # Chain 1: Get analysis
        analysis = analysis_chain.invoke({"technology": test_tech})
        print(f"1️⃣ Analysis:\n   {analysis}")

        # Chain 2: Get use cases
        use_cases = list_chain.invoke({"technology": test_tech})
        print(f"\n2️⃣ Use Cases:")
        for i, use_case in enumerate(use_cases, 1):
            print(f"   {i}. {use_case}")

    # Show the magic
    print("\n💡 Chain Composition Magic:")
    print("  ✓ The pipe | operator connects everything")
    print("  ✓ prompt | llm | parser = complete pipeline")
    print("  ✓ Different parsers = different output formats")
    print("  ✓ Same LLM, infinite possibilities!")

    # Create marker for completion
    os.makedirs("markers", exist_ok=True)
    with open("markers/task5_complete.txt", "w") as f:
        f.write("COMPLETED")

    print("\n✅ Task 5 completed! You've mastered LangChain chains!")
    print("🏆 You can now build any AI pipeline with the | operator!")

if __name__ == "__main__":
    main()