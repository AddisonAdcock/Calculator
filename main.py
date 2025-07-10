import webview
import json

class CalculatorAPI:
    def add(self, a, b):
        try:
            return float(a) + float(b)
        except (ValueError, TypeError):
            return "Error: Invalid input"
    
    def subtract(self, a, b):
        try:
            return float(a) - float(b)
        except (ValueError, TypeError):
            return "Error: Invalid input"
    
    def multiply(self, a, b):
        try:
            return float(a) * float(b)
        except (ValueError, TypeError):
            return "Error: Invalid input"
    
    def divide(self, a, b):
        try:
            a, b = float(a), float(b)
            if b == 0:
                return "Error: Division by zero"
            return a / b
        except (ValueError, TypeError):
            return "Error: Invalid input"
    
    def calculate(self, expression):
        try:
            expression = expression.replace('×', '*').replace('÷', '/')
            
            allowed_chars = set('0123456789+-*/.() ')
            if not all(c in allowed_chars for c in expression):
                return "Error: Invalid characters"
            
            result = eval(expression)
            return result
        except ZeroDivisionError:
            return "Error: Division by zero"
        except (ValueError, SyntaxError, TypeError):
            return "Error: Invalid expression"
        except Exception as e:
            return f"Error: {str(e)}"
    
    def clear(self):
        return 0
    
    def get_pi(self):
        import math
        return math.pi
    
    def get_e(self):
        import math
        return math.e

html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Python Calculator</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            margin: 0;
            padding: 20px;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
        }
        
        .calculator {
            background: white;
            border-radius: 20px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
            padding: 30px;
            width: 350px;
        }
        
        .display {
            width: 100%;
            height: 80px;
            font-size: 2em;
            text-align: right;
            border: 2px solid #ddd;
            border-radius: 10px;
            padding: 10px;
            margin-bottom: 20px;
            background: #f8f9fa;
            box-sizing: border-box;
        }
        
        .buttons {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 10px;
        }
        
        button {
            height: 60px;
            font-size: 1.2em;
            border: none;
            border-radius: 10px;
            cursor: pointer;
            transition: all 0.2s;
            font-weight: bold;
        }
        
        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
        }
        
        .number {
            background: #f8f9fa;
            color: #333;
        }
        
        .operator {
            background: #007bff;
            color: white;
        }
        
        .equals {
            background: #28a745;
            color: white;
        }
        
        .clear {
            background: #dc3545;
            color: white;
        }
        
        .function {
            background: #6c757d;
            color: white;
            font-size: 1em;
        }
        
        .wide {
            grid-column: span 2;
        }
        

    </style>
</head>
<body>
    <div class="calculator">
        <input type="text" id="display" class="display" readonly>
        
        <div class="buttons">
            <button class="clear" onclick="clearDisplay()">C</button>
            <button class="function" onclick="appendToDisplay('/')">/</button>
            <button class="function" onclick="appendToDisplay('*')">×</button>
            <button class="function" onclick="deleteLast()">⌫</button>
            
            <button class="number" onclick="appendToDisplay('7')">7</button>
            <button class="number" onclick="appendToDisplay('8')">8</button>
            <button class="number" onclick="appendToDisplay('9')">9</button>
            <button class="operator" onclick="appendToDisplay('-')">-</button>
            
            <button class="number" onclick="appendToDisplay('4')">4</button>
            <button class="number" onclick="appendToDisplay('5')">5</button>
            <button class="number" onclick="appendToDisplay('6')">6</button>
            <button class="operator" onclick="appendToDisplay('+')">+</button>
            
            <button class="number" onclick="appendToDisplay('1')">1</button>
            <button class="number" onclick="appendToDisplay('2')">2</button>
            <button class="number" onclick="appendToDisplay('3')">3</button>
            <button class="equals" onclick="calculate()" rowspan="2">=</button>
            
            <button class="number wide" onclick="appendToDisplay('0')">0</button>
            <button class="number" onclick="appendToDisplay('.')">.</button>
        </div>
    </div>

    <script>
        let display = document.getElementById('display');
        
        function appendToDisplay(value) {
            display.value += value;
        }
        
        function clearDisplay() {
            display.value = '';
            // Call Python API to clear
            pywebview.api.clear().then(result => {
                console.log('Cleared:', result);
            });
        }
        
        function deleteLast() {
            display.value = display.value.slice(0, -1);
        }
        
        async function calculate() {
            if (display.value === '') return;
            
            try {
                // Call Python API to calculate
                const result = await pywebview.api.calculate(display.value);
                display.value = result;
            } catch (error) {
                display.value = 'Error';
                console.error('Calculation error:', error);
            }
        }
        
        // Keyboard support
        document.addEventListener('keydown', function(event) {
            const key = event.key;
            
            if (key >= '0' && key <= '9') {
                appendToDisplay(key);
            } else if (key === '.') {
                appendToDisplay('.');
            } else if (key === '+') {
                appendToDisplay('+');
            } else if (key === '-') {
                appendToDisplay('-');
            } else if (key === '*') {
                appendToDisplay('*');
            } else if (key === '/') {
                event.preventDefault(); // Prevent browser search
                appendToDisplay('/');
            } else if (key === 'Enter' || key === '=') {
                calculate();
            } else if (key === 'Escape' || key === 'Delete') {
                clearDisplay();
            } else if (key === 'Backspace') {
                deleteLast();
            }
        });
    </script>
</body>
</html>
"""

def create_calculator_app():
    api = CalculatorAPI()
    
    webview.create_window(
        title='Python Calculator',
        html=html_content,
        js_api=api,
        width=400,
        height=550,
        resizable=True,
        min_size=(350, 600)
    )
    webview.start(debug=False)

if __name__ == '__main__':
    create_calculator_app()