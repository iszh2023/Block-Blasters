#!/usr/bin/env python3
"""
Spike Block Code SVG to Python Converter

This program parses SVG diagrams of Spike block code and converts them to Python.
It identifies common block patterns and generates equivalent Python code.
"""

import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import re
import json
from typing import Dict, List, Any, Optional


class SpikeBlockParser:
    """Parser for Spike block code SVG diagrams"""
    
    def __init__(self):
        # Map of block types to Python code templates
        self.block_templates = {
            'when_started': 'def main():\n    """Main program entry point"""\n',
            'when_button_pressed': 'def on_button_press():\n    """When button is pressed"""\n',
            'motor_run': '    hub.port.{port}.motor.run_for_seconds({seconds})\n',
            'motor_stop': '    hub.port.{port}.motor.stop()\n',
            'led_set': '    hub.led({color})\n',
            'wait': '    time.sleep({seconds})\n',
            'print': '    print("{text}")\n',
            'sound_beep': '    hub.sound.beep({frequency}, {duration})\n',
            'repeat': '    for i in range({count}):\n',
            'forever': '    while True:\n',
            'if_condition': '    if {condition}:\n',
            'variable_set': '    {name} = {value}\n',
            'function_call': '    {function_name}({parameters})\n'
        }
        
        # Required imports for different block types
        self.imports = {
            'motor': 'from spike import PrimeHub',
            'led': 'from spike import PrimeHub',
            'sound': 'from spike import PrimeHub',
            'wait': 'import time',
            'sensor': 'from spike import PrimeHub'
        }
        
        self.used_imports = set()
        self.indent_level = 0
        
    def parse_svg_file(self, svg_file_path: str) -> str:
        """Parse SVG file and convert to Python code"""
        try:
            with open(svg_file_path, 'r', encoding='utf-8') as file:
                svg_content = file.read()
            return self.parse_svg_content(svg_content)
        except Exception as e:
            return f"# Error reading SVG file: {e}\n"
    
    def parse_svg_content(self, svg_content: str) -> str:
        """Parse SVG content and extract block structure"""
        try:
            # Use BeautifulSoup for more robust SVG parsing
            soup = BeautifulSoup(svg_content, 'xml')
            
            # Extract text elements and their positions
            blocks = self._extract_blocks_from_svg(soup)
            
            # Sort blocks by position (top to bottom, left to right)
            sorted_blocks = self._sort_blocks_by_position(blocks)
            
            # Convert blocks to Python code
            python_code = self._convert_blocks_to_python(sorted_blocks)
            
            return python_code
            
        except Exception as e:
            return f"# Error parsing SVG: {e}\n"
    
    def _extract_blocks_from_svg(self, soup: BeautifulSoup) -> List[Dict]:
        """Extract block information from SVG elements"""
        blocks = []
        
        # Look for text elements that might contain block information
        text_elements = soup.find_all(['text', 'tspan'])
        
        for element in text_elements:
            text_content = element.get_text().strip()
            if not text_content:
                continue
                
            # Get position information
            x = self._get_numeric_attr(element, 'x', 0)
            y = self._get_numeric_attr(element, 'y', 0)
            
            # Check parent elements for additional positioning
            parent = element.parent
            while parent and parent.name in ['g', 'svg']:
                transform_attr = parent.get('transform')
                if transform_attr:
                    # Extract translate values from transform
                    translate = self._extract_translate(str(transform_attr))
                    x += translate[0]
                    y += translate[1]
                parent = parent.parent
            
            # Identify block type from text content
            block_type = self._identify_block_type(text_content)
            
            blocks.append({
                'text': text_content,
                'x': x,
                'y': y,
                'type': block_type,
                'params': self._extract_parameters(text_content)
            })
        
        return blocks
    
    def _get_numeric_attr(self, element, attr_name: str, default: float) -> float:
        """Extract numeric value from SVG attribute"""
        try:
            value = element.get(attr_name, default)
            if isinstance(value, str):
                # Remove units like 'px', 'pt', etc.
                value = re.sub(r'[a-zA-Z%]', '', value)
                return float(value) if value else default
            return float(value)
        except (ValueError, TypeError):
            return default
    
    def _extract_translate(self, transform: str) -> tuple:
        """Extract translate values from SVG transform attribute"""
        match = re.search(r'translate\s*\(\s*([^,\)]+)(?:,\s*([^,\)]+))?\s*\)', transform)
        if match:
            x = float(match.group(1)) if match.group(1) else 0
            y = float(match.group(2)) if match.group(2) else 0
            return (x, y)
        return (0, 0)
    
    def _identify_block_type(self, text: str) -> str:
        """Identify the type of Spike block from text content"""
        text_lower = text.lower()
        
        # Common Spike block patterns
        if 'when started' in text_lower or 'when program starts' in text_lower:
            return 'when_started'
        elif 'when button' in text_lower and 'pressed' in text_lower:
            return 'when_button_pressed'
        elif 'motor' in text_lower and 'run' in text_lower:
            return 'motor_run'
        elif 'motor' in text_lower and 'stop' in text_lower:
            return 'motor_stop'
        elif 'led' in text_lower or 'light' in text_lower:
            return 'led_set'
        elif 'wait' in text_lower or 'sleep' in text_lower:
            return 'wait'
        elif 'print' in text_lower or 'say' in text_lower:
            return 'print'
        elif 'sound' in text_lower or 'beep' in text_lower:
            return 'sound_beep'
        elif 'repeat' in text_lower and ('times' in text_lower or re.search(r'\d+', text)):
            return 'repeat'
        elif 'forever' in text_lower:
            return 'forever'
        elif 'if' in text_lower:
            return 'if_condition'
        elif 'set' in text_lower and 'to' in text_lower:
            return 'variable_set'
        else:
            return 'unknown'
    
    def _extract_parameters(self, text: str) -> Dict[str, Any]:
        """Extract parameters from block text"""
        params = {}
        
        # Extract numbers
        numbers = re.findall(r'\d+(?:\.\d+)?', text)
        
        # Extract port letters (A, B, C, D, E, F)
        ports = re.findall(r'\b[A-F]\b', text)
        
        # Extract colors
        colors = re.findall(r'\b(red|green|blue|yellow|white|black|orange|purple)\b', text.lower())
        
        # Extract quoted strings
        strings = re.findall(r'"([^"]*)"', text)
        if not strings:
            strings = re.findall(r"'([^']*)'", text)
        
        if numbers:
            params['numbers'] = [float(n) for n in numbers]
        if ports:
            params['ports'] = ports
        if colors:
            params['colors'] = colors
        if strings:
            params['strings'] = strings
            
        return params
    
    def _sort_blocks_by_position(self, blocks: List[Dict]) -> List[Dict]:
        """Sort blocks by their position (top to bottom, left to right)"""
        return sorted(blocks, key=lambda b: (b['y'], b['x']))
    
    def _convert_blocks_to_python(self, blocks: List[Dict]) -> str:
        """Convert sorted blocks to Python code"""
        python_lines = []
        
        # Add file header
        python_lines.append('#!/usr/bin/env python3')
        python_lines.append('"""')
        python_lines.append('Generated Python code from Spike block diagram')
        python_lines.append('"""')
        python_lines.append('')
        
        # Track what imports we need
        needed_imports = set()
        
        # Process blocks to determine imports
        for block in blocks:
            block_type = block['type']
            if 'motor' in block_type:
                needed_imports.add('motor')
            elif 'led' in block_type:
                needed_imports.add('led')
            elif 'sound' in block_type:
                needed_imports.add('sound')
            elif 'wait' in block_type:
                needed_imports.add('wait')
        
        # Add imports (avoid duplicates)
        unique_imports = set()
        for import_type in needed_imports:
            if import_type in self.imports:
                unique_imports.add(self.imports[import_type])
        
        for import_line in sorted(unique_imports):
            python_lines.append(import_line)
        
        if unique_imports:
            python_lines.append('')
        
        # Initialize hub if needed
        if any(imp in needed_imports for imp in ['motor', 'led', 'sound', 'sensor']):
            python_lines.append('# Initialize the SPIKE Prime hub')
            python_lines.append('hub = PrimeHub()')
            python_lines.append('')
        
        # Convert blocks to code with better structure
        indent = 0
        in_main = False
        in_loop = False
        
        for i, block in enumerate(blocks):
            block_type = block['type']
            params = block['params']
            
            # Check if we're entering or exiting indented blocks
            if block_type == 'when_started':
                python_lines.append('def main():')
                python_lines.append('    """Main program entry point"""')
                indent = 1
                in_main = True
                
            elif block_type == 'repeat':
                count = params.get('numbers', [10])[0]
                line = f"{'    ' * indent}for i in range({int(count)}):"
                python_lines.append(line)
                indent += 1
                in_loop = True
                
            elif block_type == 'forever':
                line = f"{'    ' * indent}while True:"
                python_lines.append(line)
                indent += 1
                in_loop = True
                
            elif block_type == 'motor_run':
                port = params.get('ports', ['A'])[0]
                seconds = params.get('numbers', [1])[0]
                line = f"{'    ' * indent}hub.port.{port}.motor.run_for_seconds({seconds})"
                python_lines.append(line)
                
            elif block_type == 'motor_stop':
                port = params.get('ports', ['A'])[0]
                line = f"{'    ' * indent}hub.port.{port}.motor.stop()"
                python_lines.append(line)
                
            elif block_type == 'led_set':
                color = params.get('colors', ['white'])[0]
                line = f"{'    ' * indent}hub.led('{color}')"
                python_lines.append(line)
                
            elif block_type == 'wait':
                seconds = params.get('numbers', [1])[0]
                line = f"{'    ' * indent}time.sleep({seconds})"
                python_lines.append(line)
                
            elif block_type == 'print':
                text = params.get('strings', [block['text']])[0]
                line = f"{'    ' * indent}print('{text}')"
                python_lines.append(line)
                
            elif block_type == 'sound_beep':
                numbers = params.get('numbers', [440, 0.5])
                freq = numbers[0] if len(numbers) > 0 else 440
                duration = numbers[1] if len(numbers) > 1 else 0.5
                line = f"{'    ' * indent}hub.sound.beep({freq}, {duration})"
                python_lines.append(line)
                
            elif block_type == 'unknown' and block['text'].strip():
                # Add as comment for unknown blocks
                line = f"{'    ' * indent}# {block['text']}"
                python_lines.append(line)
            
            # Check if this is the last block in a loop (simple heuristic based on position)
            if in_loop and i < len(blocks) - 1:
                next_block = blocks[i + 1]
                # If next block is at a lower indentation level or is a control block, end the loop
                if (next_block['x'] <= block['x'] - 20 or 
                    next_block['type'] in ['when_started', 'repeat', 'forever'] or
                    i == len(blocks) - 1):
                    indent = max(1, indent - 1)
                    in_loop = False
        
        # Add main execution
        if in_main:
            python_lines.append('')
            python_lines.append('if __name__ == "__main__":')
            python_lines.append('    main()')
        
        return '\n'.join(python_lines)


def main():
    """Main function to demonstrate the converter"""
    converter = SpikeBlockParser()
    
    # Example: Create a sample SVG for testing
    sample_svg = '''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 600">
    <g transform="translate(50, 50)">
        <text x="0" y="20">when program starts</text>
    </g>
    <g transform="translate(50, 100)">
        <text x="0" y="20">motor A run for 2 seconds</text>
    </g>
    <g transform="translate(50, 150)">
        <text x="0" y="20">wait 1 seconds</text>
    </g>
    <g transform="translate(50, 200)">
        <text x="0" y="20">led set to green</text>
    </g>
    <g transform="translate(50, 250)">
        <text x="0" y="20">print "Hello World"</text>
    </g>
</svg>'''
    
    print("Spike Block Code SVG to Python Converter")
    print("=" * 45)
    print()
    
    # Convert sample SVG
    python_code = converter.parse_svg_content(sample_svg)
    print("Generated Python code from sample SVG:")
    print("-" * 40)
    print(python_code)
    print()
    
    # Instructions for use
    print("Usage Instructions:")
    print("1. Save your Spike block diagram as an SVG file")
    print("2. Use converter.parse_svg_file('your_file.svg') to convert")
    print("3. The generated Python code will work with SPIKE Prime hub")


if __name__ == "__main__":
    main()