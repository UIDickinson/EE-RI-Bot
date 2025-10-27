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

## Make the test scripts executable
```
chmod +x test_runner.py
``` 

## Testing

### Quick Health Check

Before running tests, verify all components are working:
```bash
python scripts/health_check.py
```

This checks:
- ✅ Environment variables configured
- ✅ All modules import correctly
- ✅ LLM provider initializes
- ✅ Tools initialize properly
- ✅ Required files exist

### Running Tests

**Quick tests** (no API calls, ~30 seconds):
```bash
./scripts/run_tests.sh quick
```

**Full test suite** (includes API calls, ~5 minutes):
```bash
./scripts/run_tests.sh full
```

**Integration tests only**:
```bash
./scripts/run_tests.sh integration
```

**With coverage report**:
```bash
./scripts/run_tests.sh coverage
# View report: open htmlcov/index.html
```

### Manual Testing

**Individual test files**:
```bash
# Tool tests
python -m pytest tests/test_tools.py -v

# LLM provider tests (uses API credits)
python -m pytest tests/test_llm_provider.py -v

# Edge cases
python -m pytest tests/test_edge_cases.py -v
```

**Comprehensive test runner**:
```bash
python test_runner.py
```

### Test Coverage

Current test coverage includes:
- ✅ Research tools (arXiv, Semantic Scholar)
- ✅ Component analysis
- ✅ Supply chain tracking
- ✅ Datasheet parsing
- ✅ Patent search
- ✅ Compliance checking
- ✅ Cost estimation
- ✅ LLM provider initialization
- ✅ Edge cases and error handling
- ✅ API endpoint validation

### Continuous Testing

For development, run tests on file changes:
```bash
pip install pytest-watch
ptw tests/ -- -v
```

### make your database script executable
```bash
chmod +x database/init_db.py

chmod +x scripts/setup_postgres.sh
```
## setup cmds
```bash
# 1. Install PostgreSQL (choose one)
./scripts/setup_postgres.sh    # For Linux/ChromeOS
# OR
brew install postgresql@15      # For macOS
# OR
docker run --name ee-postgres -e POSTGRES_PASSWORD=password -p 5432:5432 -d postgres:15-alpine

# 2. Install Python dependencies
pip install psycopg2-binary sqlalchemy alembic

# 3. Update .env file
cat >> .env << EOF
POSTGRES_USER=ee_user
POSTGRES_PASSWORD=your_secure_password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=ee_research_scout
EOF

# 4. Initialize database
python database/init_db.py

# 5. Verify connection
python -c "from database.connection import db_manager; print('✅ Connected!' if db_manager.test_connection() else '❌ Failed')"

```
