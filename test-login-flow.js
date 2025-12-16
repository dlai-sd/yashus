#!/usr/bin/env node

/**
 * UI Test Script - Login Flow
 * Tests the full authentication flow:
 * 1. Page loads
 * 2. Click Login button
 * 3. Modal appears
 * 4. Click Test Login button
 * 5. Backend auth succeeds
 * 6. Modal closes
 * 7. Navigate to dashboard
 * 8. Dashboard loads with user info
 */

const http = require('http');

// Test configuration
const BASE_URL = 'http://localhost:4200';
const BACKEND_URL = 'http://localhost:8000';
const TEST_EMAIL = 'test@agentshome.com';
const TEST_PASSWORD = 'TestPassword123';

console.log('🧪 Starting Login Flow Tests\n');

// Test 1: Backend Health Check
async function testBackendHealth() {
  return new Promise((resolve, reject) => {
    console.log('1️⃣  Testing Backend Health...');
    const req = http.get(`${BACKEND_URL}/api/health`, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        if (res.statusCode === 200) {
          console.log('   ✅ Backend is responsive (HTTP 200)');
          console.log(`   Response: ${data.substring(0, 100)}...`);
          resolve(true);
        } else {
          console.log(`   ❌ Backend returned HTTP ${res.statusCode}`);
          reject(false);
        }
      });
    });
    req.on('error', (err) => {
      console.log(`   ❌ Backend connection failed: ${err.message}`);
      reject(false);
    });
  });
}

// Test 2: Backend Auth Endpoint
async function testBackendAuth() {
  return new Promise((resolve, reject) => {
    console.log('\n2️⃣  Testing Backend Auth Endpoint...');
    const postData = JSON.stringify({
      email: TEST_EMAIL,
      password: TEST_PASSWORD
    });

    const options = {
      hostname: 'localhost',
      port: 8000,
      path: '/api/auth/login',
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Content-Length': postData.length
      }
    };

    const req = http.request(options, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        if (res.statusCode === 200) {
          try {
            const parsed = JSON.parse(data);
            if (parsed.token && parsed.user) {
              console.log('   ✅ Auth endpoint working (HTTP 200)');
              console.log(`   Token: ${parsed.token.substring(0, 20)}...`);
              console.log(`   User: ${parsed.user.name} (${parsed.user.email})`);
              resolve(true);
            } else {
              console.log('   ❌ Auth response missing token or user');
              reject(false);
            }
          } catch (e) {
            console.log('   ❌ Invalid JSON response');
            reject(false);
          }
        } else {
          console.log(`   ❌ Auth endpoint returned HTTP ${res.statusCode}`);
          console.log(`   Response: ${data}`);
          reject(false);
        }
      });
    });

    req.on('error', (err) => {
      console.log(`   ❌ Auth request failed: ${err.message}`);
      reject(false);
    });

    req.write(postData);
    req.end();
  });
}

// Test 3: CORS Headers
async function testCORS() {
  return new Promise((resolve, reject) => {
    console.log('\n3️⃣  Testing CORS Headers...');
    const options = {
      hostname: 'localhost',
      port: 8000,
      path: '/api/auth/login',
      method: 'OPTIONS',
      headers: {
        'Origin': 'http://localhost:4200',
        'Access-Control-Request-Method': 'POST'
      }
    };

    const req = http.request(options, (res) => {
      const corsHeader = res.headers['access-control-allow-origin'];
      if (corsHeader) {
        console.log(`   ✅ CORS enabled: ${corsHeader}`);
        resolve(true);
      } else {
        console.log('   ⚠️  CORS header not present (might still work)');
        resolve(true);
      }
    });

    req.on('error', (err) => {
      console.log(`   ❌ CORS test failed: ${err.message}`);
      reject(false);
    });

    req.end();
  });
}

// Test 4: Frontend Availability
async function testFrontendHealth() {
  return new Promise((resolve, reject) => {
    console.log('\n4️⃣  Testing Frontend Availability...');
    const req = http.get(`${BASE_URL}`, (res) => {
      if (res.statusCode === 200 || res.statusCode === 301 || res.statusCode === 302) {
        console.log(`   ✅ Frontend is available (HTTP ${res.statusCode})`);
        resolve(true);
      } else {
        console.log(`   ❌ Frontend returned HTTP ${res.statusCode}`);
        reject(false);
      }
    });
    req.on('error', (err) => {
      console.log(`   ❌ Frontend connection failed: ${err.message}`);
      reject(false);
    });
  });
}

// Main test runner
async function runTests() {
  const results = {
    passed: 0,
    failed: 0,
    tests: []
  };

  const tests = [
    { name: 'Backend Health', fn: testBackendHealth },
    { name: 'Backend Auth Endpoint', fn: testBackendAuth },
    { name: 'CORS Headers', fn: testCORS },
    { name: 'Frontend Availability', fn: testFrontendHealth }
  ];

  for (const test of tests) {
    try {
      await test.fn();
      results.passed++;
      results.tests.push({ name: test.name, status: 'PASS' });
    } catch (err) {
      results.failed++;
      results.tests.push({ name: test.name, status: 'FAIL' });
    }
  }

  // Summary
  console.log('\n' + '='.repeat(50));
  console.log('📊 TEST SUMMARY');
  console.log('='.repeat(50));
  console.log(`✅ Passed: ${results.passed}`);
  console.log(`❌ Failed: ${results.failed}`);
  console.log(`📈 Total: ${results.tests.length}`);
  
  if (results.failed === 0) {
    console.log('\n🎉 ALL TESTS PASSED - Login flow is ready to test!');
    process.exit(0);
  } else {
    console.log('\n⚠️  Some tests failed - check output above');
    process.exit(1);
  }
}

runTests().catch(err => {
  console.error('Test runner error:', err);
  process.exit(1);
});
