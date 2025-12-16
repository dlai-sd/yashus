#!/usr/bin/env python3
"""
Simple Calculator Web Server for Codespace
Runs on port 3000 - no Docker or database needed
Access via Codespace forwarded port URL
"""

from http.server import HTTPServer, SimpleHTTPRequestHandler
import json

PORT = 3000
HISTORY = []

class CalculatorHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(HTML_PAGE.encode())
        elif self.path == '/api/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "ok"}).encode())
        elif self.path == '/api/history':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(HISTORY).encode())
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == '/api/calculate':
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)
            data = json.loads(body.decode())
            
            try:
                operand1 = float(data['operand1'])
                operand2 = float(data['operand2'])
                operation = data['operation']
                
                if operation == 'add':
                    result = operand1 + operand2
                elif operation == 'subtract':
                    result = operand1 - operand2
                elif operation == 'multiply':
                    result = operand1 * operand2
                elif operation == 'divide':
                    if operand2 == 0:
                        raise ValueError("Cannot divide by zero")
                    result = operand1 / operand2
                else:
                    raise ValueError("Invalid operation")
                
                record = {
                    "operation": operation,
                    "operand1": operand1,
                    "operand2": operand2,
                    "result": result
                }
                HISTORY.append(record)
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(record).encode())
            except Exception as e:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode())
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        print(f"[{self.client_address[0]}] {format % args}")

HTML_PAGE = '''<!DOCTYPE html>
<html>
<head>
    <title>The Hunter - Calculator</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #0B2447 0%, #1a3d5f 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        .container {
            background: white;
            border-radius: 12px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            padding: 40px;
            max-width: 500px;
            width: 100%;
        }
        h1 {
            text-align: center;
            color: #0B2447;
            margin-bottom: 30px;
            font-size: 28px;
        }
        .form-group {
            margin-bottom: 20px;
        }
        label {
            display: block;
            margin-bottom: 8px;
            color: #333;
            font-weight: 500;
        }
        input, select {
            width: 100%;
            padding: 12px;
            border: 2px solid #e0e0e0;
            border-radius: 6px;
            font-size: 16px;
            transition: border-color 0.3s;
        }
        input:focus, select:focus {
            outline: none;
            border-color: #F97316;
        }
        button {
            width: 100%;
            padding: 12px;
            background: linear-gradient(135deg, #0B2447 0%, #1a3d5f 100%);
            color: white;
            border: none;
            border-radius: 6px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
            margin-top: 10px;
        }
        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 20px rgba(11, 36, 71, 0.3);
        }
        button:disabled {
            opacity: 0.6;
            cursor: not-allowed;
        }
        .result {
            margin-top: 20px;
            padding: 15px;
            background: #f5f5f5;
            border-radius: 6px;
            display: none;
        }
        .result.show {
            display: block;
        }
        .result-value {
            font-size: 24px;
            font-weight: bold;
            color: #0B2447;
            text-align: center;
        }
        .error {
            color: #d32f2f;
            padding: 10px;
            background: #ffebee;
            border-radius: 4px;
            display: none;
        }
        .error.show {
            display: block;
        }
        .history {
            margin-top: 30px;
            padding-top: 20px;
            border-top: 2px solid #e0e0e0;
        }
        .history h2 {
            color: #0B2447;
            font-size: 16px;
            margin-bottom: 15px;
        }
        .history-item {
            padding: 10px;
            background: #f9f9f9;
            border-left: 3px solid #F97316;
            margin-bottom: 10px;
            border-radius: 4px;
            font-size: 14px;
        }
        .loading {
            display: inline-block;
            width: 20px;
            height: 20px;
            border: 3px solid #f3f3f3;
            border-top: 3px solid #0B2447;
            border-radius: 50%;
            animation: spin 1s linear infinite;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        .status {
            text-align: center;
            color: #666;
            font-size: 12px;
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>The Hunter - Calculator</h1>
        
        <div class="form-group">
            <label>First Number</label>
            <input type="number" id="operand1" placeholder="Enter first number" step="any">
        </div>
        
        <div class="form-group">
            <label>Operation</label>
            <select id="operation">
                <option value="add">Add (+)</option>
                <option value="subtract">Subtract (-)</option>
                <option value="multiply">Multiply (x)</option>
                <option value="divide">Divide (/)</option>
            </select>
        </div>
        
        <div class="form-group">
            <label>Second Number</label>
            <input type="number" id="operand2" placeholder="Enter second number" step="any">
        </div>
        
        <button id="calculate" onclick="calculate()">Calculate</button>
        
        <div class="error" id="error"></div>
        <div class="result" id="result">
            <div style="color: #999; font-size: 12px; margin-bottom: 5px;">Result</div>
            <div class="result-value" id="resultValue">0</div>
        </div>
        
        <div class="history" id="historyContainer" style="display: none;">
            <h2>Recent Calculations</h2>
            <div id="historyList"></div>
        </div>
        
        <div class="status">
            RUNNING on Codespace | API Ready
        </div>
    </div>

    <script>
        async function calculate() {
            const operand1 = parseFloat(document.getElementById('operand1').value);
            const operand2 = parseFloat(document.getElementById('operand2').value);
            const operation = document.getElementById('operation').value;
            const errorDiv = document.getElementById('error');
            const resultDiv = document.getElementById('result');
            const btn = document.getElementById('calculate');
            
            errorDiv.classList.remove('show');
            resultDiv.classList.remove('show');
            
            if (isNaN(operand1) || isNaN(operand2)) {
                errorDiv.textContent = 'Please enter valid numbers';
                errorDiv.classList.add('show');
                return;
            }
            
            btn.disabled = true;
            btn.innerHTML = '<div class="loading" style="margin: 0 auto;"></div>';
            
            try {
                const response = await fetch('/api/calculate', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ operand1, operand2, operation })
                });
                
                const data = await response.json();
                
                if (response.ok) {
                    document.getElementById('resultValue').textContent = data.result.toFixed(4);
                    resultDiv.classList.add('show');
                    loadHistory();
                } else {
                    errorDiv.textContent = data.error || 'Calculation failed';
                    errorDiv.classList.add('show');
                }
            } catch (err) {
                errorDiv.textContent = 'Error: ' + err.message;
                errorDiv.classList.add('show');
            } finally {
                btn.disabled = false;
                btn.innerHTML = 'Calculate';
            }
        }
        
        async function loadHistory() {
            try {
                const response = await fetch('/api/history');
                const history = await response.json();
                
                if (history.length > 0) {
                    const container = document.getElementById('historyContainer');
                    const list = document.getElementById('historyList');
                    list.innerHTML = '';
                    
                    history.slice(-5).reverse().forEach(item => {
                        const symbol = {add: '+', subtract: '-', multiply: 'x', divide: '/'}[item.operation];
                        const html = `<div class="history-item">
                            ${item.operand1} ${symbol} ${item.operand2} = <strong>${item.result.toFixed(4)}</strong>
                        </div>`;
                        list.innerHTML += html;
                    });
                    
                    container.style.display = 'block';
                }
            } catch (err) {
                console.error('History error:', err);
            }
        }
        
        loadHistory();
        
        document.getElementById('operand2').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') calculate();
        });
    </script>
</body>
</html>
'''

if __name__ == '__main__':
    print(f">> The Hunter Calculator running on http://localhost:{PORT}")
    print(f">> Access via Codespace forwarded URL")
    server = HTTPServer(('0.0.0.0', PORT), CalculatorHandler)
    server.serve_forever()
