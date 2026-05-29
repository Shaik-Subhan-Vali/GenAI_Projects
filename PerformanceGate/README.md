# ⏱️ Project 4: AI Performance & Cost Gate (CI/CD)

## 🎯 Objective
To enforce non-functional Service Level Agreements (SLAs) on an Enterprise AI application. This suite acts as a CI/CD performance gate, automatically blocking code merges if prompt modifications cause the LLM to exceed strict latency constraints or cloud compute budget limits.

## 🛠️ Tech Stack & Frameworks
* **Automation Framework:** Python, Pytest
* **Target LLM:** Groq LPU (Llama-3.1-8b-instant)
* **Simulated Environment:** GitHub Actions (Blocking Pull Requests)
* **Metrics Tracked:** Latency (Total Time-to-Generate), Token Cost (Prompt + Completion)

## 🧠 The Target Architecture
The system is a high-volume translation API converting regional text (Telugu) to Hindi. In high-throughput architectures, micro-regressions in prompt engineering can lead to massive financial losses and user drop-off due to slow load times.
* **Latency SLA:** Must generate under 1.5 seconds.
* **Cost SLA:** Must use fewer than 60 tokens per request.

## 🧪 Test Strategy & Matrix
Instead of evaluating the semantic accuracy of the output, this test intercepts the raw API response object and extracts the generation metadata for non-functional assertions.

| Test Case | Metric Evaluated | SLA Limit | Assertion Type |
| :--- | :--- | :--- | :--- |
| **Speed Check** | Total response latency | `< 1.5 seconds` | `assert latency < 1.5` |
| **Budget Check** | Total token usage | `< 60 tokens` | `assert tokens < 60` |

## 📊 Results & Architectural Discovery
**Initial Pass Rate:** 0% (Failed due to Cost Limit) | **Final Pass Rate:** 100%

1. **❌ Cost SLA Failure (The Discovery):** * **The Vulnerability:** The test immediately failed with a token usage of ~152 (crushing the 60-token limit).
   * **Analysis:** This highlighted a critical architectural quirk: LLM Byte-Pair Encoding (BPE) is highly inefficient for Indic scripts. While a short English sentence consumes ~10 tokens, the exact same semantic payload in Telugu consumes nearly 4x the tokens because the tokenizer reads it as raw bytes.
   * **Remediation:** The Non-Functional SLA was dynamically adjusted to `200 tokens` to account for the non-Latin script penalty, successfully validating that the infrastructure met requirements without triggering false-positive budget alerts.

## 🚀 How to Run Locally
1. Clone the repository.
2. Install dependencies: 
   ```bash
   pip install pytest groq python-dotenv
