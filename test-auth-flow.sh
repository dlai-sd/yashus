#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "================================"
echo "Testing Auth Flow - Backend & UI"
echo "================================"
echo ""

# Test 1: Backend Health Check
echo -e "${YELLOW}[Test 1]${NC} Backend Health Check"
HEALTH=$(curl -s http://localhost:8000/api/health)
if echo "$HEALTH" | grep -q "healthy"; then
    echo -e "${GREEN}✓ Backend is running and healthy${NC}"
    echo "Response: $HEALTH"
else
    echo -e "${RED}✗ Backend health check failed${NC}"
    echo "Response: $HEALTH"
    exit 1
fi
echo ""

# Test 2: Login Endpoint with Valid Credentials
echo -e "${YELLOW}[Test 2]${NC} Login with Valid Credentials"
LOGIN_RESPONSE=$(curl -s -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@agentshome.com","password":"TestPassword123"}')

if echo "$LOGIN_RESPONSE" | grep -q "test-jwt-token"; then
    echo -e "${GREEN}✓ Login successful - JWT token received${NC}"
    echo "Response: $LOGIN_RESPONSE"
    TOKEN=$(echo "$LOGIN_RESPONSE" | grep -o '"token":"[^"]*' | cut -d'"' -f4)
    echo "Extracted Token: $TOKEN"
else
    echo -e "${RED}✗ Login failed${NC}"
    echo "Response: $LOGIN_RESPONSE"
    exit 1
fi
echo ""

# Test 3: Login with Invalid Credentials
echo -e "${YELLOW}[Test 3]${NC} Login with Invalid Credentials (Should Fail)"
INVALID_LOGIN=$(curl -s -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"wrong@email.com","password":"wrongpass"}')

if echo "$INVALID_LOGIN" | grep -q "401\|Invalid"; then
    echo -e "${GREEN}✓ Invalid login correctly rejected${NC}"
    echo "Response: $INVALID_LOGIN"
else
    echo -e "${YELLOW}⚠ Unexpected response to invalid credentials${NC}"
    echo "Response: $INVALID_LOGIN"
fi
echo ""

# Test 4: Signup Endpoint
echo -e "${YELLOW}[Test 4]${NC} Signup Endpoint"
SIGNUP_RESPONSE=$(curl -s -X POST http://localhost:8000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"newuser@agentshome.com","password":"NewPass123","name":"New User"}')

if echo "$SIGNUP_RESPONSE" | grep -q "token"; then
    echo -e "${GREEN}✓ Signup successful${NC}"
    echo "Response: $SIGNUP_RESPONSE"
else
    echo -e "${RED}✗ Signup failed${NC}"
    echo "Response: $SIGNUP_RESPONSE"
fi
echo ""

# Test 5: CORS Headers Test
echo -e "${YELLOW}[Test 5]${NC} CORS Headers Check"
CORS_RESPONSE=$(curl -s -i -X OPTIONS http://localhost:8000/api/auth/login \
  -H "Origin: https://ubiquitous-waddle-v69grgqwjxq436gv5-4200.app.github.dev" \
  -H "Access-Control-Request-Method: POST" 2>&1)

if echo "$CORS_RESPONSE" | grep -q "Access-Control-Allow"; then
    echo -e "${GREEN}✓ CORS headers present${NC}"
    echo "$CORS_RESPONSE" | grep "Access-Control"
else
    echo -e "${YELLOW}⚠ CORS headers not found (may still work with *)${NC}"
    echo "$CORS_RESPONSE" | head -20
fi
echo ""

# Test 6: Frontend Server Check
echo -e "${YELLOW}[Test 6]${NC} Frontend Server Status"
if nc -z localhost 4200 2>/dev/null; then
    echo -e "${GREEN}✓ Frontend server is listening on port 4200${NC}"
else
    echo -e "${RED}✗ Frontend server not responding on port 4200${NC}"
fi
echo ""

echo "================================"
echo "Backend Tests Complete!"
echo "================================"
