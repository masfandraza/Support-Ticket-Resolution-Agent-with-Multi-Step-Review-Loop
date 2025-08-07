# AI-Powered-Support-Ticket-Resolution-Agent (LangGraph + Ollama)

This project implements a multi-step customer support resolution agent using [LangGraph](https://www.langgraph.dev/) and [Ollama](https://ollama.com/). It simulates a real-world production-grade AI workflow that classifies support tickets, retrieves relevant context, drafts a response, performs multi-step review, and escalates when needed.

---

## Features

- **Ticket Classification** — routes support requests by category (e.g., Billing, Technical)
- **Context Retrieval** — retrieves relevant policies and knowledge for reply
- **LLM-Based Draft Generator** — generates empathetic and compliant responses
- **Multi-Step Review Loop** — allows up to 2 retries before escalation
- **LLM Reviewer (Llama 3 via Ollama)** — validates tone, accuracy, and policy compliance
- **Escalation Logging** — stores rejected responses in `escalation_log.csv`
- **Test Mode Toggle** — simulate approval or rejection behavior using an environment variable

---

## ⚙Installation

### 1. Clone this repository

```bash
git clone https://github.com/yourusername/support-ticket-agent.git
cd support-ticket-agent
```
2. Set up Python environment
```bash
python -m venv .venv
source .venv/bin/activate      # On Windows: .venv\Scripts\activate
```
3. Install dependencies
```bash
pip install -r requirements.txt
Note: Requires Ollama running locally (ollama run llama3) and the langchain_ollama module.
```

Running the Agent
  Normal run
  ```bash
  python main.py
  ```

By default, the system starts with a sample ticket:
```bash
{
  "subject": "Refund request not processed",
  "description": "I was promised a refund last week but haven't received it yet."
}
```

The agent will:
  - > Classify the ticket 
  - > Retrieve relevant policy context
  - > Generate a draft reply
  - > Review the reply using Ollama
  - > Retry if rejected (up to 2 times)
  - > Escalate and log if still rejected

For Demo Purposes
  Force Approval:
```bash
$env:TEST_MODE="approve"     # Windows PowerShell
python main.py
Remove-Item Env:\TEST_MODE
```
  Force Rejection:
```bash
$env:TEST_MODE="reject"
python main.py
Remove-Item Env:\TEST_MODE
```

Output Sample
If the response is rejected after all retries, the rejected draft is logged to:
```bash
./data/escalation_log.csv
```

CSV Columns:
  - > timestamp
  - > subject
  - > description
  - > failed_draft
  - > review_feedback

Project Structure
```bash
├── main.py                # Entry point and workflow
├── nodes/
│   ├── classifier.py
│   ├── retriever.py
│   ├── draft_generator.py
│   ├── reviewer.py        # Uses langchain_ollama ChatOllama
│   └── escalation.py
├── data/
│   └── escalation_log.csv # Logged rejected drafts
├── requirements.txt
└── README.md
```

Notes & Limitations
  - > Requires Ollama running locally with llama3 model (ollama run llama3)
  - > If the langchain_ollama package is missing, install via:
```bash
pip install langchain-ollama
```


Built by M. Asfand Raza | GitHub: https://github.com/masfandraza

