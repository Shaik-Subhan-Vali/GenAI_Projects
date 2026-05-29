import os
import json
import pytest
import google.generativeai as genai
from dotenv import load_dotenv

# Load secrets and configure the API
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def test_csk_rag_hallucination_catcher():
    # 1. THE DATA PAYLOAD
    retrieved_context = "Chennai Super Kings (CSK) has won the IPL championship a total of 5 times, securing titles in 2010, 2011, 2018, 2021, and 2023. MS Dhoni captained the team during all five runs."
    
    # THE BUG: We are feeding it '6 times' to simulate a production hallucination
    actual_llm_output = "CSK has won the IPL title 6 times under the exceptional captaincy of MS Dhoni."

    # 2. THE CUSTOM AI JUDGE PROMPT
    judge_prompt = f"""
    You are an automated test runner evaluating a RAG system.
    Compare the LLM Output against the Source Context. 
    Does the LLM Output hallucinate or contradict the Source Context?
    
    Source Context: {retrieved_context}
    LLM Output: {actual_llm_output}

    Respond ONLY with a raw JSON object in this exact format:
    {{"score": 0.0, "reason": "brief explanation"}}
    
    If the LLM Output makes claims not supported by the context, score it 0.0. 
    If it is fully supported and perfectly accurate, score it 1.0.
    """

    # 3. THE QUOTA BYPASS
    # We drained 'gemini-2.5-flash', so we are switching to 'gemini-1.5-pro' for a fresh quota bucket!
    model = genai.GenerativeModel("gemini-1.5-pro")
    
    print("\n[Connecting] Asking the AI Judge to evaluate...")
    response = model.generate_content(judge_prompt)
    
    # 4. PARSE AND ASSERT
    try:
        clean_json_text = response.text.strip().replace("```json", "").replace("```", "")
        result = json.loads(clean_json_text)
        
        print(f"\n[AI Judge Verdict]: {result['reason']}")
        
        # The Pytest assertion that fails the pipeline if a hallucination is caught
        assert result['score'] >= 0.7, f"\n🚨 HALLUCINATION DETECTED! 🚨\nScore: {result['score']}\nWhy it failed: {result['reason']}"
        
    except json.JSONDecodeError:
        pytest.fail("The test runner failed to parse the AI Judge's JSON response.")