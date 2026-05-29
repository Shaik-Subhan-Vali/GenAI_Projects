# 🌐 Project 5: Agentic UI Streaming & Orchestration Test (E2E)

## 🎯 Objective
To build a robust end-to-end (E2E) UI test suite capable of handling non-deterministic, streaming AI responses. This project simulates real user interactions in the DOM via Server-Sent Events (SSE) and dynamically validates the AI's conversational state-machine and ReAct (Reason + Act) loop.

## 🛠️ Tech Stack & Frameworks
* **Automation Framework:** Playwright (TypeScript)
* **Backend Runtime:** Node.js
* **Mock Infrastructure:** Python HTTPServer (Simulating SSE chunk-based message streaming)
* **Testing Pattern:** Dynamic Assertions, DOM Class-flag synchronization

## 🧠 The Target Architecture
A user interacts with a conversational web frontend for a Transit-Booking AI Agent. 
* **Scenario:** User prompts, *"I need a bus from Hyderabad to Amalapuram tomorrow."*
* **The Challenge:** Traditional UI automation tools fail against AI chat interfaces because text renders fluidly across multiple event loops, and the final phrasing is non-deterministic (depending on the model's temperature setting).

## 🧪 Test Strategy & Matrix
The test explicitly avoids fragile `assertEqual` exact-string matches. Instead, it parses the DOM dynamically to verify the AI's logical routing.

| Test Case | Interaction / Validation | Expected Behavior | Assertion Type |
| :--- | :--- | :--- | :--- |
| **Stream Interception** | Wait for AI to finish typing | DOM registers `.streaming-done` class | `page.waitForSelector` |
| **Entity Extraction** | Read final message bubble | Mentions "Hyderabad" and "Amalapuram" | `toContain(entity)` |
| **Logical Routing** | Evaluate ReAct Path | AI either asks for Time OR confirms booking | `expect(A || B).toBeTruthy()` |

## 📊 Results & Architectural Discovery
**Pass Rate:** 100% (1/1 Passed)

1. **✅ Stream Synchronization Success:** * **Analysis:** The test successfully overcame Playwright's traditional timeout issues. By attaching a listener to the DOM and waiting for the backend event loop to flag completion (`.streaming-done`), the script safely captured the entire chunk-based response without triggering a race condition.
   * **Assertion Success:** The TypeScript logic correctly parsed the AI's non-deterministic sentence, verifying both the geographic entities and the conversational logic (asking the user for a departure time to continue the booking flow).

## 🚀 How to Run Locally
1. Clone the repository.
2. Install dependencies:
   ```bash
   npm install
   npm install -D @playwright/test
