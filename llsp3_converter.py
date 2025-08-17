#!/usr/bin/env python3
"""
LLSP3 to Python Converter

This program processes LEGO SPIKE Prime .llsp3 project files, extracts the block data,
analyzes the blocks using pattern recognition, and converts them to Python code.
"""

import zipfile
import json
import os
import re
import xml.etree.ElementTree as ET
from typing import Dict, List, Any, Optional
from pathlib import Path


class LLSP3Analyzer:
    """Analyzer for LEGO SPIKE Prime .llsp3 project files"""
    
    def __init__(self):
        # Block type patterns and their Python equivalents
        self.block_patterns = {
            # Event blocks
            'when_program_starts': {
                'patterns': ['when.*program.*start', 'when.*started', 'green.*flag'],
                'python': 'def main():\n    """Main program entry point"""'
            },
            'when_button_pressed': {
                'patterns': ['when.*button.*pressed', 'when.*key.*pressed'],
                'python': 'def on_button_press():\n    """When button is pressed"""'
            },
            
            # Motor blocks
            'motor_run_seconds': {
                'patterns': ['motor.*run.*second', 'run.*motor.*second'],
                'python': 'hub.port.{port}.motor.run_for_seconds({seconds})'
            },
            'motor_run_rotations': {
                'patterns': ['motor.*run.*rotation', 'run.*motor.*rotation'],
                'python': 'hub.port.{port}.motor.run_for_rotations({rotations})'
            },
            'motor_run_degrees': {
                'patterns': ['motor.*run.*degree', 'run.*motor.*degree'],
                'python': 'hub.port.{port}.motor.run_for_degrees({degrees})'
            },
            'motor_stop': {
                'patterns': ['motor.*stop', 'stop.*motor'],
                'python': 'hub.port.{port}.motor.stop()'
            },
            'motor_set_speed': {
                'patterns': ['motor.*speed', 'set.*motor.*speed'],
                'python': 'hub.port.{port}.motor.set_default_speed({speed})'
            },
            
            # LED blocks
            'led_set_color': {
                'patterns': ['led.*color', 'light.*color', 'set.*led'],
                'python': 'hub.led({color})'
            },
            'led_off': {
                'patterns': ['led.*off', 'light.*off'],
                'python': 'hub.led()'
            },
            
            # Sound blocks
            'sound_beep': {
                'patterns': ['sound.*beep', 'beep', 'play.*beep'],
                'python': 'hub.sound.beep({frequency}, {duration})'
            },
            'sound_play': {
                'patterns': ['sound.*play', 'play.*sound'],
                'python': 'hub.sound.play("{sound_file}")'
            },
            
            # Control blocks
            'wait_seconds': {
                'patterns': ['wait.*second', 'sleep.*second', 'pause.*second'],
                'python': 'time.sleep({seconds})'
            },
            'repeat_times': {
                'patterns': ['repeat.*time', 'loop.*time'],
                'python': 'for i in range({count}):'
            },
            'repeat_forever': {
                'patterns': ['forever', 'repeat.*forever', 'loop.*forever'],
                'python': 'while True:'
            },
            'if_condition': {
                'patterns': ['if.*then', 'if.*condition'],
                'python': 'if {condition}:'
            },
            
            # Sensor blocks
            'distance_sensor': {
                'patterns': ['distance.*sensor', 'ultrasonic.*sensor'],
                'python': 'hub.port.{port}.device.get_distance_cm()'
            },
            'color_sensor': {
                'patterns': ['color.*sensor', 'colour.*sensor'],
                'python': 'hub.port.{port}.device.get_color()'
            },
            'force_sensor': {
                'patterns': ['force.*sensor', 'pressure.*sensor'],
                'python': 'hub.port.{port}.device.get_force_percentage()'
            },
            
            # Variable blocks
            'set_variable': {
                'patterns': ['set.*variable', 'variable.*set', 'set.*to'],
                'python': '{variable} = {value}'
            },
            'change_variable': {
                'patterns': ['change.*variable', 'variable.*change', 'increase.*variable'],
                'python': '{variable} += {value}'
            },
            
            # Display blocks
            'display_text': {
                'patterns': ['display.*text', 'show.*text', 'print.*text'],
                'python': 'print("{text}")'
            },
            'display_image': {
                'patterns': ['display.*image', 'show.*image'],
                'python': 'hub.light_matrix.show_image("{image}")'
            }
        }
        
        # Required imports for different block categories
        self.imports = {
            'motor': 'from spike import PrimeHub',
            'led': 'from spike import PrimeHub', 
            'sound': 'from spike import PrimeHub',
            'sensor': 'from spike import PrimeHub',
            'display': 'from spike import PrimeHub',
            'wait': 'import time',
            'math': 'import math'
        }
        
        self.used_imports = set()
    
    def process_llsp3_file(self, file_path: str) -> str:
        """Process .llsp3 file and convert to Python"""
        try:
            # Extract and analyze the .llsp3 file
            project_data = self._extract_llsp3_data(file_path)
            
            # Find blocks in the project data
            blocks = self._find_blocks_in_project(project_data)
            
            # Analyze blocks and convert to Python
            python_code = self._convert_blocks_to_python(blocks)
            
            return python_code
            
        except Exception as e:
            return f"# Error processing .llsp3 file: {e}\n"
    
    def _extract_llsp3_data(self, file_path: str) -> Dict:
        """Extract data from .llsp3 zip file"""
        project_data = {}
        
        with zipfile.ZipFile(file_path, 'r') as zip_file:
            # List all files in the zip
            file_list = zip_file.namelist()
            
            for file_name in file_list:
                try:
                    if file_name.endswith('.json'):
                        # Extract JSON files (project metadata)
                        with zip_file.open(file_name) as json_file:
                            content = json.loads(json_file.read().decode('utf-8'))
                            project_data[file_name] = content
                    
                    elif file_name.endswith('.svg'):
                        # Extract SVG files (block diagrams)
                        with zip_file.open(file_name) as svg_file:
                            content = svg_file.read().decode('utf-8')
                            project_data[file_name] = content
                    
                    elif file_name.endswith(('.py', '.txt')):
                        # Extract text files
                        with zip_file.open(file_name) as text_file:
                            content = text_file.read().decode('utf-8')
                            project_data[file_name] = content
                
                except Exception as e:
                    print(f"Warning: Could not read {file_name}: {e}")
        
        return project_data
    
    def _find_blocks_in_project(self, project_data: Dict) -> List[Dict]:
        """Find and extract block information from project data"""
        blocks = []
        
        # Check JSON files for block definitions
        for file_name, content in project_data.items():
            if file_name.endswith('.json') and isinstance(content, dict):
                blocks.extend(self._extract_blocks_from_json(content))
        
        # Check SVG files for visual block representations
        for file_name, content in project_data.items():
            if file_name.endswith('.svg') and isinstance(content, str):
                blocks.extend(self._extract_blocks_from_svg(content))
        
        return blocks
    
    def _extract_blocks_from_json(self, json_data: Dict) -> List[Dict]:
        """Extract block information from JSON data"""
        blocks = []
        
        def search_for_blocks(obj, path=""):
            """Recursively search for block-like structures"""
            if isinstance(obj, dict):
                # Look for common SPIKE block structure patterns
                if 'opcode' in obj or 'blockType' in obj or 'type' in obj:
                    block_info = {
                        'source': 'json',
                        'path': path,
                        'data': obj,
                        'text': self._extract_block_text(obj),
                        'type': obj.get('opcode', obj.get('blockType', obj.get('type', 'unknown'))),
                        'params': self._extract_json_parameters(obj)
                    }
                    blocks.append(block_info)
                
                # Continue searching in nested objects
                for key, value in obj.items():
                    search_for_blocks(value, f"{path}.{key}")
            
            elif isinstance(obj, list):
                for i, item in enumerate(obj):
                    search_for_blocks(item, f"{path}[{i}]")
        
        search_for_blocks(json_data)
        return blocks
    
    def _extract_blocks_from_svg(self, svg_content: str) -> List[Dict]:
        """Extract block information from SVG content"""
        blocks = []
        
        try:
            # Parse SVG content
            root = ET.fromstring(svg_content)
            
            # Find text elements that might represent blocks
            for element in root.iter():
                if element.tag.endswith('text') or element.tag.endswith('tspan'):
                    text_content = element.text or ''
                    if text_content.strip():
                        block_info = {
                            'source': 'svg',
                            'text': text_content.strip(),
                            'type': self._identify_block_type(text_content),
                            'params': self._extract_svg_parameters(text_content)
                        }
                        blocks.append(block_info)
        
        except ET.ParseError as e:
            print(f"Warning: Could not parse SVG content: {e}")
        
        return blocks
    
    def _extract_block_text(self, block_data: Dict) -> str:
        """Extract readable text from block data"""
        # Try various common fields for block text
        for field in ['text', 'label', 'name', 'opcode', 'blockType', 'type']:
            if field in block_data and isinstance(block_data[field], str):
                return block_data[field]
        
        # If no direct text, try to construct it from available data
        if 'inputs' in block_data:
            inputs = block_data['inputs']
            if isinstance(inputs, dict):
                text_parts = []
                for key, value in inputs.items():
                    if isinstance(value, (str, int, float)):
                        text_parts.append(f"{key}: {value}")
                if text_parts:
                    return " ".join(text_parts)
        
        return str(block_data.get('opcode', block_data.get('type', 'unknown')))
    
    def _extract_json_parameters(self, block_data: Dict) -> Dict:
        """Extract parameters from JSON block data"""
        params = {}
        
        # Extract from inputs field
        if 'inputs' in block_data:
            inputs = block_data['inputs']
            if isinstance(inputs, dict):
                for key, value in inputs.items():
                    if isinstance(value, (str, int, float)):
                        params[key.lower()] = value
        
        # Extract from fields field
        if 'fields' in block_data:
            fields = block_data['fields']
            if isinstance(fields, dict):
                for key, value in fields.items():
                    if isinstance(value, (str, int, float)):
                        params[key.lower()] = value
                    elif isinstance(value, list) and len(value) > 0:
                        params[key.lower()] = value[0]
        
        # Extract common parameters directly
        for param in ['port', 'seconds', 'rotations', 'degrees', 'speed', 'color', 'sound']:
            if param in block_data:
                params[param] = block_data[param]
        
        return params
    
    def _extract_svg_parameters(self, text: str) -> Dict:
        """Extract parameters from SVG text content"""
        params = {}
        
        # Extract numbers
        numbers = re.findall(r'\d+(?:\.\d+)?', text)
        if numbers:
            params['numbers'] = [float(n) for n in numbers]
        
        # Extract port letters
        ports = re.findall(r'\b[A-F]\b', text)
        if ports:
            params['ports'] = ports
        
        # Extract colors
        colors = re.findall(r'\b(red|green|blue|yellow|white|black|orange|purple|pink|cyan)\b', text.lower())
        if colors:
            params['colors'] = colors
        
        # Extract quoted strings
        strings = re.findall(r'"([^"]*)"', text)
        if not strings:
            strings = re.findall(r"'([^']*)'", text)
        if strings:
            params['strings'] = strings
        
        return params
    
    def _identify_block_type(self, text: str) -> str:
        """Identify block type from text using pattern matching"""
        text_lower = text.lower()
        
        for block_type, info in self.block_patterns.items():
            for pattern in info['patterns']:
                if re.search(pattern, text_lower):
                    return block_type
        
        return 'unknown'
    
    def _convert_blocks_to_python(self, blocks: List[Dict]) -> str:
        """Convert analyzed blocks to Python code"""
        python_lines = []
        
        # Add file header
        python_lines.extend([
            '#!/usr/bin/env python3',
            '"""',
            'Generated Python code from SPIKE Prime .llsp3 project',
            'Converted using intelligent block analysis',
            '"""',
            ''
        ])
        
        # Determine required imports
        needed_imports = self._determine_imports(blocks)
        
        # Add imports
        for import_line in sorted(needed_imports):
            python_lines.append(import_line)
        
        if needed_imports:
            python_lines.append('')
        
        # Initialize hub if needed
        if any('PrimeHub' in imp for imp in needed_imports):
            python_lines.extend([
                '# Initialize the SPIKE Prime hub',
                'hub = PrimeHub()',
                ''
            ])
        
        # Convert blocks to code
        indent_level = 0
        in_main_function = False
        
        for block in blocks:
            block_type = block['type']
            params = block['params']
            text = block['text']
            
            # Generate Python code for this block
            python_code = self._generate_block_code(block_type, params, text, indent_level)
            
            if python_code:
                if block_type == 'when_program_starts' and not in_main_function:
                    python_lines.append('def main():')
                    python_lines.append('    """Main program entry point"""')
                    indent_level = 1
                    in_main_function = True
                elif block_type in ['repeat_times', 'repeat_forever', 'if_condition']:
                    python_lines.append('    ' * indent_level + python_code)
                    indent_level += 1
                else:
                    python_lines.append('    ' * indent_level + python_code)
        
        # Add main execution
        if in_main_function:
            python_lines.extend(['', 'if __name__ == "__main__":', '    main()'])
        
        return '\n'.join(python_lines)
    
    def _determine_imports(self, blocks: List[Dict]) -> set:
        """Determine which imports are needed based on blocks"""
        imports = set()
        
        for block in blocks:
            block_type = block['type']
            
            if any(keyword in block_type for keyword in ['motor', 'led', 'sound', 'sensor', 'display']):
                imports.add('from spike import PrimeHub')
            
            if 'wait' in block_type:
                imports.add('import time')
            
            if any(keyword in block_type for keyword in ['math', 'calculation']):
                imports.add('import math')
        
        return imports
    
    def _generate_block_code(self, block_type: str, params: Dict, text: str, indent: int) -> str:
        """Generate Python code for a specific block"""
        if block_type in self.block_patterns:
            template = self.block_patterns[block_type]['python']
            
            # Fill in template parameters
            try:
                if block_type == 'motor_run_seconds':
                    port = params.get('ports', ['A'])[0] if 'ports' in params else 'A'
                    seconds = params.get('numbers', [1])[0] if 'numbers' in params else 1
                    return template.format(port=port, seconds=seconds)
                
                elif block_type == 'motor_stop':
                    port = params.get('ports', ['A'])[0] if 'ports' in params else 'A'
                    return template.format(port=port)
                
                elif block_type == 'led_set_color':
                    color = params.get('colors', ['white'])[0] if 'colors' in params else 'white'
                    return template.format(color=f'"{color}"')
                
                elif block_type == 'wait_seconds':
                    seconds = params.get('numbers', [1])[0] if 'numbers' in params else 1
                    return template.format(seconds=seconds)
                
                elif block_type == 'repeat_times':
                    count = int(params.get('numbers', [10])[0]) if 'numbers' in params else 10
                    return template.format(count=count)
                
                elif block_type == 'sound_beep':
                    numbers = params.get('numbers', [440, 0.5])
                    frequency = numbers[0] if len(numbers) > 0 else 440
                    duration = numbers[1] if len(numbers) > 1 else 0.5
                    return template.format(frequency=frequency, duration=duration)
                
                elif block_type == 'display_text':
                    text_content = params.get('strings', [text])[0] if 'strings' in params else text
                    return template.format(text=text_content)
                
                else:
                    return template
                    
            except (IndexError, KeyError, ValueError):
                return f"# {text}"
        
        else:
            # Unknown block type - add as comment
            return f"# {text}"


def main():
    """Main function for interactive .llsp3 processing"""
    print("LEGO SPIKE Prime .llsp3 to Python Converter")
    print("=" * 50)
    print()
    
    analyzer = LLSP3Analyzer()
    
    while True:
        # Ask for file path
        file_path = input("Enter path to .llsp3 file (or 'quit' to exit): ").strip()
        
        if file_path.lower() in ['quit', 'exit', 'q']:
            print("Goodbye!")
            break
        
        if not file_path:
            continue
        
        # Check if file exists
        if not os.path.exists(file_path):
            print(f"Error: File '{file_path}' not found.")
            continue
        
        # Check if it's a .llsp3 file
        if not file_path.lower().endswith('.llsp3'):
            print("Warning: File doesn't have .llsp3 extension, but will try to process it anyway.")
        
        print(f"\nProcessing {file_path}...")
        print("-" * 40)
        
        try:
            # Convert the file
            python_code = analyzer.process_llsp3_file(file_path)
            
            print("Generated Python Code:")
            print("=" * 30)
            print(python_code)
            print("=" * 30)
            
            # Ask if user wants to save the code
            save_choice = input("\nSave to file? (y/n): ").strip().lower()
            if save_choice in ['y', 'yes']:
                output_name = Path(file_path).stem + '_converted.py'
                with open(output_name, 'w') as f:
                    f.write(python_code)
                print(f"✓ Saved to {output_name}")
            
        except Exception as e:
            print(f"Error processing file: {e}")
        
        print("\n" + "=" * 50)


if __name__ == "__main__":
    main()