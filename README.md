# EE-RI-Bot
Script 2 for building Electrical/Electronics Engineering Research & Innovation Scout with Sentient AGI

# EE Research & Innovation Scout Agent

AI agent built with **Sentient Agent Framework** for Electrical/Electronics Engineers. Discovers innovations in Power Management ICs, EMC/EMI solutions, Edge AI chips, and Embedded Systems (EU/Asia focus).

## Features

- 🔍 **Research**: IEEE, arXiv, Semantic Scholar, patents
- 🎯 **Domains**: Embedded Systems, Power Management, EMC/EMI, Edge AI
- 🌍 **Geographic**: EU/Asia markets (CE, RoHS, CCC compliance)
- 📊 **Deep Analysis**: Professional-grade technical reports
- 📦 **Supply Chain**: Availability and cost tracking
- 🧠 **Knowledge Graph**: Neo4j relationship tracking (optional)
- 🤖 **Multi-Provider**: OpenAI, Claude (Anthropic), OpenRouter

## Quick Start

```bash
# Clone
git clone <your-repo-url>
cd ee-research-scout-agent

# Setup
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configure
cp .env.example .env
nano .env  # Add API keys and set LLM_PROVIDER

# Run
python app.py
```

Agent runs on http://localhost:8000

## Docker Setup

cp .env.example .env
nano .env  # Add API keys
docker-compose up -d

## LLM Provider Configuration

In .env, set:
bash
LLM_PROVIDER=anthropic  # or openai or openrouter

Then add the corresponding API key:
- **Claude**: ANTHROPIC_API_KEY
- **OpenAI**: OPENAI_API_KEY
- **OpenRouter**: OPENROUTER_API_KEY

## Example Request

```
curl -X POST http://localhost:8000/assist \
  -H "Content-Type: application/json" \
  -d '{
    "session": {
      "user_id": "user_123",
      "session_id": "session_456",
      "processor_id": "proc_789",
      "activity_id": "activity_101",
      "request_id": "req_202",
      "interactions": []
    },
    "query": {
      "id": "query_303",
      "prompt": "Find latest GaN power ICs for automotive"
    }
  }'
```

## Example Queries

"What are the latest Edge AI chips for battery-powered systems?"
"Compare STM32H7 vs ESP32-S3 for industrial IoT"
"Check availability of nRF5340 in EU distributors"
"Recent EMI filtering innovations for high-speed PCBs"

## Response Events

**ANALYSIS**: Query understanding
**RESEARCH**: Literature search
**COMPONENT_ANALYSIS**: Datasheet extraction
**SUPPLY_CHAIN**: Availability checks
**FINAL_RESPONSE**: Streamed analysis