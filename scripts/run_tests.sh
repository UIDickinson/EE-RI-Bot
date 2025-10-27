#!/bin/bash

# Comprehensive test runner script
# Usage: ./scripts/run_tests.sh [quick|full|integration|coverage]

set -e

TEST_MODE=${1:-quick}
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
LOG_DIR="test_logs"
LOG_FILE="$LOG_DIR/test_run_$TIMESTAMP.log"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Create log directory
mkdir -p $LOG_DIR

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  EE Research Scout - Test Suite${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""
echo "Test Mode: $TEST_MODE"
echo "Log File: $LOG_FILE"
echo ""

# Function to run tests and log
run_test() {
    local test_name=$1
    local test_cmd=$2
    
    echo -e "${YELLOW}Running: $test_name${NC}"
    
    if eval "$test_cmd" 2>&1 | tee -a $LOG_FILE; then
        echo -e "${GREEN}✅ $test_name PASSED${NC}\n"
        return 0
    else
        echo -e "${RED}❌ $test_name FAILED${NC}\n"
        return 1
    fi
}

# Check environment
echo -e "${YELLOW}Checking environment...${NC}"
if [ ! -f .env ]; then
    echo -e "${RED}❌ .env file not found${NC}"
    echo "Create .env from .env.example and add your API keys"
    exit 1
fi

# Check dependencies
echo -e "${YELLOW}Checking dependencies...${NC}"
if ! python -c "import pytest" 2>/dev/null; then
    echo -e "${RED}❌ pytest not installed${NC}"
    echo "Installing test dependencies..."
    pip install -r requirements-test.txt
fi

echo -e "${GREEN}✅ Environment OK${NC}\n"

# Initialize counters
TOTAL=0
PASSED=0
FAILED=0

case $TEST_MODE in
    quick)
        echo -e "${BLUE}Running Quick Tests (no API calls)${NC}\n"
        
        run_test "Tool Tests" "python -m pytest tests/test_tools.py -v -m 'not slow'" && ((PASSED++)) || ((FAILED++))
        ((TOTAL++))
        
        run_test "Compliance Tests" "python -m pytest tests/test_compliance.py -v" && ((PASSED++)) || ((FAILED++))
        ((TOTAL++))
        
        run_test "Edge Cases" "python -m pytest tests/test_edge_cases.py -v" && ((PASSED++)) || ((FAILED++))
        ((TOTAL++))
        ;;
    
    full)
        echo -e "${BLUE}Running Full Test Suite (includes API calls)${NC}\n"
        
        run_test "Tool Tests" "python -m pytest tests/test_tools.py -v" && ((PASSED++)) || ((FAILED++))
        ((TOTAL++))
        
        run_test "LLM Provider Tests" "python -m pytest tests/test_llm_provider.py -v" && ((PASSED++)) || ((FAILED++))
        ((TOTAL++))
        
        run_test "Compliance Tests" "python -m pytest tests/test_compliance.py -v" && ((PASSED++)) || ((FAILED++))
        ((TOTAL++))
        
        run_test "Integration Tests" "python -m pytest tests/test_integration.py -v" && ((PASSED++)) || ((FAILED++))
        ((TOTAL++))
        
        run_test "Edge Cases" "python -m pytest tests/test_edge_cases.py -v" && ((PASSED++)) || ((FAILED++))
        ((TOTAL++))
        ;;
    
    integration)
        echo -e "${BLUE}Running Integration Tests Only${NC}\n"
        
        run_test "Integration Tests" "python -m pytest tests/test_integration.py -v" && ((PASSED++)) || ((FAILED++))
        ((TOTAL++))
        
        run_test "API Endpoint Tests" "python -m pytest tests/test_api_endpoint.py -v" && ((PASSED++)) || ((FAILED++))
        ((TOTAL++))
        ;;
    
    coverage)
        echo -e "${BLUE}Running Tests with Coverage${NC}\n"
        
        run_test "Full Coverage" "python -m pytest tests/ -v --cov=. --cov-report=html --cov-report=term" && ((PASSED++)) || ((FAILED++))
        ((TOTAL++))
        
        echo -e "\n${BLUE}Coverage report generated in htmlcov/index.html${NC}"
        ;;
    
    *)
        echo -e "${RED}Unknown test mode: $TEST_MODE${NC}"
        echo "Usage: ./scripts/run_tests.sh [quick|full|integration|coverage]"
        exit 1
        ;;
esac

# Summary
echo ""
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  Test Summary${NC}"
echo -e "${BLUE}========================================${NC}"
echo "Total Tests: $TOTAL"
echo -e "${GREEN}Passed: $PASSED${NC}"
echo -e "${RED}Failed: $FAILED${NC}"

PASS_RATE=$((PASSED * 100 / TOTAL))
echo "Pass Rate: $PASS_RATE%"

echo ""
echo "Full log: $LOG_FILE"

if [ $FAILED -eq 0 ]; then
    echo -e "\n${GREEN}🎉 All tests passed!${NC}"
    exit 0
else
    echo -e "\n${RED}⚠️  Some tests failed${NC}"
    exit 1
fi
