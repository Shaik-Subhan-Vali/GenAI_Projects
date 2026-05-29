import os
import time
import pytest
from groq import Groq
from dotenv import load_dotenv

# Load secrets
load_dotenv()

# We set strict Service Level Agreements (SLAs) for our pipeline
MAX_LATENCY_SECONDS = 1.5  # Translation must be faster than 1.5 seconds
MAX_TOKEN_COST_LIMIT = 60  # Total tokens per translation must stay under 60

@pytest.fixture
def groq_client():
    return Groq(api_key=os.getenv("GROQ_API_KEY"))

def test_telugu_to_hindi_performance_gate(groq_client):
    # 1. The High-Volume Data Payload
    telugu_sentence = "హైదరాబాద్‌లో బిర్యానీ చాలా బాగుంటుంది." # "Biryani is very good in Hyderabad."
    
    system_prompt = "You are a high-speed translation API. Translate the user's Telugu text into Hindi. Output ONLY the Hindi translation, nothing else."

    # 2. Start the Stopwatch
    start_time = time.time()

    # 3. Execute the API Call
    response = groq_client.chat.completions.create(
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": telugu_sentence}
        ],
        model="llama-3.1-8b-instant",
        temperature=0.1
    )

    # 4. Stop the Stopwatch
    end_time = time.time()
    latency = end_time - start_time

    # 5. Extract Token Usage from the API Metadata
    total_tokens = response.usage.total_tokens
    translation_output = response.choices[0].message.content

    print(f"\n[Result] Output: {translation_output}")
    print(f"[Metric] Latency: {latency:.2f} seconds")
    print(f"[Metric] Token Usage: {total_tokens} tokens")

    # 6. NON-FUNCTIONAL ASSERTIONS (The Performance Gate)
    assert latency < MAX_LATENCY_SECONDS, f"🚨 LATENCY FAILURE: Translation took {latency:.2f}s, which exceeds the {MAX_LATENCY_SECONDS}s SLA limit!"
    assert total_tokens < MAX_TOKEN_COST_LIMIT, f"🚨 COST FAILURE: Translation used {total_tokens} tokens, exceeding the budget limit of {MAX_TOKEN_COST_LIMIT}!"