# ESG Risk Analyzer

A production-ready Python tool that analyzes ESG (Environmental, Social, Governance) risks for a list of companies using the OpenAI GPT-4o-mini API. 

## Features

- **Concurrent Processing**: Leverages `asyncio` and `AsyncOpenAI` for high-throughput API calls.
- **Robust Parsing**: Enforces strict JSON structures and handles LLM hallucination safely.
- **Incremental Saving**: Results are saved progressively, meaning you never lose data if the process stops midway.
- **Rate Limit Protection**: Built-in delays to respect API quotas.
- **Resumable Runs**: Already processed companies are automatically skipped on subsequent runs.

## Setup

```bash
git clone <repo>
cd esg-risk-analyzer

python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Configure

Create a `.env` file in the root directory:

```env
ANTIGRAVITY_API_KEY=your_key_here
```

## Run

Execute the analyzer:

```bash
python main.py
```

Check the generated `esg_risk_output.csv` for the final structured output and `logs/app.log` for execution details.
