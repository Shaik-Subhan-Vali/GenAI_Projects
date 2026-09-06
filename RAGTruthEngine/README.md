# 🧠 Project : RAG Hallucination & Truth Engine

## 🎯 Objective
To evaluate the data integrity of a Retrieval-Augmented Generation (RAG) pipeline. This project implements a custom Python automation framework using an "LLM-as-a-Judge" to mathematically detect AI hallucinations and ensure the model's output remains strictly faithful to the injected Vector Database context.

## 🛠️ Tech Stack & Frameworks
* **Automation Framework:** Python, Pytest
* **Target LLM:** Google Gemini 2.5 Flash (via API)
* **Architecture:** Custom API Wrapper with Async Retry-Logic & Randomized Jitter
* **Evaluation Strategy:** Contextual Faithfulness Scoring (JSON-based semantic grading)

## 🧠 The Target Architecture
The system simulates a corporate RAG pipeline querying a sports database:
* **Source Context:** Chennai Super Kings (CSK) won the IPL 5 times under MS Dhoni.
* **Injected Bug:** A simulated hallucination where the LLM outputs that CSK won the title *6 times*.
* **The Judge:** An independent LLM instructed to mathematically grade the output against the source context (0.0 for hallucination, 1.0 for perfect accuracy).

## 🧪 Test Strategy & Matrix
Instead of exact string matching, this suite uses an independent AI judge to evaluate semantic truthfulness.

| Test Case | Scenario | Expected Behavior | Assertion Type |
| :--- | :--- | :--- | :--- |
| **Faithfulness Check** | Output claims 6 wins; Context says 5 wins. | Judge detects contradiction and scores < 0.7. | `assert score >= 0.7` (Fails) |
| **Thundering Herd Fix** | Parallel async calls hit API rate limits (429 errors). | Custom retry loop intercepts 429s, applies backoff, and succeeds. | Infrastructure Handling |

## 📊 Results & Architectural Discovery
**Pass Rate:** 100% (Successfully caught the hallucination)

1. **✅ Hallucination Caught:** The AI Judge successfully detected the numeric contradiction, returning a score of 0.0 with the reason: *"The output states 6 wins, which directly contradicts the source context of 5 wins."*
2. **⚙️ Infrastructure Vulnerability Discovered (The Thundering Herd):**
   * **The Issue:** Concurrent async evaluation calls instantly drained the free-tier API token bucket, causing synchronized `429 Resource Exhausted` crashes.
   * **The Fix:** Engineered a robust, custom LLM wrapper that catches 429 errors, implements a 45-second sleep, and adds a randomized `Jitter` variable to stagger request wake-ups, successfully bypassing enterprise rate limits.

## 🚀 How to Run Locally
1. Clone the repository.
2. Install dependencies: `pip install pytest google-generativeai python-dotenv`
3. Create a `.env` file and add your `GEMINI_API_KEY`.
4. Execute the pipeline:
   ```bash
   pytest test_rag.py -s
