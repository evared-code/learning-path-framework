#!/bin/bash

# Test script for Learning Path Framework
# Usage: ./test.sh [backend_url]

BACKEND_URL="${1:-http://localhost:8000}"

echo "=================================="
echo "Testing Learning Path Framework"
echo "Backend: $BACKEND_URL"
echo "=================================="
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test 1: Health Check
echo -n "1. Health Check... "
HEALTH=$(curl -s "$BACKEND_URL/health")
if echo "$HEALTH" | grep -q "healthy"; then
    echo -e "${GREEN}PASS${NC}"
    echo "   $HEALTH"
else
    echo -e "${RED}FAIL${NC}"
    echo "   Response: $HEALTH"
    exit 1
fi
echo ""

# Test 2: List Courses
echo -n "2. List Courses... "
COURSES=$(curl -s "$BACKEND_URL/courses")
if echo "$COURSES" | grep -q "C01"; then
    echo -e "${GREEN}PASS${NC}"
    COUNT=$(echo "$COURSES" | grep -o "C[0-9][0-9]" | wc -l)
    echo "   Found $COUNT courses"
else
    echo -e "${RED}FAIL${NC}"
    exit 1
fi
echo ""

# Test 3: List Phases
echo -n "3. List SDLC Phases... "
PHASES=$(curl -s "$BACKEND_URL/phases")
if echo "$PHASES" | grep -q "Requirements"; then
    echo -e "${GREEN}PASS${NC}"
    echo "   All phases loaded"
else
    echo -e "${RED}FAIL${NC}"
    exit 1
fi
echo ""

# Test 4: Generate Path (Heuristic)
echo -n "4. Generate Path (Heuristic)... "
HEURISTIC=$(curl -s -X POST "$BACKEND_URL/generate_path" \
    -H "Content-Type: application/json" \
    -d '{
        "current": [1,1,1,1,0,0,0,1,1,0,1,1],
        "target": [2,2,2,2,2,2,2,2,2,2,2,2],
        "mode": "heuristic",
        "participant_id": "TEST001",
        "participant_name": "Test User"
    }')

if echo "$HEURISTIC" | grep -q "success"; then
    echo -e "${GREEN}PASS${NC}"
    GAP_REDUCTION=$(echo "$HEURISTIC" | grep -o '"gap_reduction":[0-9.]*' | cut -d':' -f2)
    echo "   Gap Reduction: $GAP_REDUCTION%"
else
    echo -e "${RED}FAIL${NC}"
    echo "   Response: $HEURISTIC"
    exit 1
fi
echo ""

# Test 5: Generate Path (LLM) - Optional
echo -n "5. Generate Path (LLM)... "
LLM=$(curl -s -X POST "$BACKEND_URL/generate_path" \
    -H "Content-Type: application/json" \
    -d '{
        "current": [1,1,1,1,0,0,0,1,1,0,1,1],
        "target": [2,2,2,2,2,2,2,2,2,2,2,2],
        "mode": "llm",
        "participant_id": "TEST002",
        "participant_name": "LLM Test User"
    }')

if echo "$LLM" | grep -q "success"; then
    echo -e "${GREEN}PASS${NC}"
    GAP_REDUCTION=$(echo "$LLM" | grep -o '"gap_reduction":[0-9.]*' | cut -d':' -f2)
    echo "   Gap Reduction: $GAP_REDUCTION%"
elif echo "$LLM" | grep -q "API key"; then
    echo -e "${YELLOW}SKIP${NC} (No API key configured)"
else
    echo -e "${RED}FAIL${NC}"
    echo "   Response: $LLM"
fi
echo ""

# Test 6: History
echo -n "6. Check History... "
HISTORY=$(curl -s "$BACKEND_URL/history?limit=5")
if echo "$HISTORY" | grep -q "TEST001"; then
    echo -e "${GREEN}PASS${NC}"
    COUNT=$(echo "$HISTORY" | grep -o "TEST[0-9]*" | wc -l)
    echo "   Found $COUNT entries in history"
else
    echo -e "${YELLOW}WARN${NC}"
    echo "   No history entries found (database may be empty)"
fi
echo ""

echo "=================================="
echo -e "${GREEN}All tests completed!${NC}"
echo "=================================="
echo ""
echo "Next steps:"
echo "  - Open API docs: $BACKEND_URL/docs"
echo "  - Test frontend with this backend URL"
echo "  - Upload sample_data.csv to test full flow"
echo ""
