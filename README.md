# SPIKE Prime Block Code to Python Converter

A comprehensive Python tool that converts SPIKE Prime visual programming into executable Python code. Supports both SVG diagrams and native .llsp3 project files, providing intelligent block analysis and code generation.

## Features

### Core Capabilities
- **Dual Format Support**: Processes both SVG diagrams and native .llsp3 project files
- **Intelligent Block Analysis**: Advanced pattern recognition for SPIKE block identification
- **Comprehensive Code Generation**: Creates clean, executable Python code
- **SPIKE Prime Compatible**: Generated code works with SPIKE Prime hub and MicroPython
- **Interactive Interface**: User-friendly console application for easy conversion

### Advanced Features
- **Deep .llsp3 Analysis**: Extracts blocks from compressed project archives
- **Pattern Matching**: Smart recognition of block types without AI dependencies
- **Multiple File Format Support**: JSON, SVG, and compressed project handling
- **Robust Error Handling**: Graceful handling of malformed or incomplete files

## Supported Block Types

### Control Blocks
- `when program starts` → Function definition
- `repeat N times` → For loops
- `forever` → While loops
- `if condition` → Conditional statements

### Action Blocks
- `motor X run for N seconds` → Motor control
- `motor X stop` → Motor stopping
- `led set to color` → LED control
- `wait N seconds` → Time delays
- `print "text"` → Console output
- `sound beep frequency duration` → Sound generation

### Input/Output
- Sensor readings
- Button press detection
- Variable assignments

## Installation

1. Make sure you have Python 3.11+ installed
2. Install required packages:
```bash
pip install beautifulsoup4 lxml xml-python zipfile-deflate64 spike-py
```

## File Types Supported

### .llsp3 Files (LEGO SPIKE Prime Projects)
- Native SPIKE Prime project files
- Complete block program data
- Full project metadata
- Compressed archive format

### SVG Files (Block Diagrams)  
- Visual representations of block code
- Text-based block descriptions
- Position and layout information
- Simple diagram format

## Usage

### Interactive Usage (Recommended)

```bash
python main.py
```

Choose from:
1. Convert SVG file
2. Convert .llsp3 project file  
3. Demo with included examples
4. Quit

### Programmatic Usage

#### For .llsp3 Files
```python
from llsp3_converter import LLSP3Analyzer

analyzer = LLSP3Analyzer()
python_code = analyzer.process_llsp3_file('your_project.llsp3')
print(python_code)
```

#### For SVG Files
```python
from spike_svg_converter import SpikeBlockParser

converter = SpikeBlockParser()
python_code = converter.parse_svg_file('your_blocks.svg')
print(python_code)
```

### Testing the Converter

```bash
python test_llsp3.py
```

This tests the .llsp3 converter with the included sumobot example.

## Example

### Input SVG
The converter can read SVG files like this:
```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 600">
    <g transform="translate(100, 50)">
        <text>when program starts</text>
    </g>
    <g transform="translate(100, 120)">
        <text>motor A run for 3 seconds</text>
    </g>
    <g transform="translate(100, 190)">
        <text>led set to red</text>
    </g>
</svg>
```

### Generated Python Code
```python
#!/usr/bin/env python3
"""
Generated Python code from Spike block diagram
"""

from spike import PrimeHub
import time

# Initialize the SPIKE Prime hub
hub = PrimeHub()

def main():
    """Main program entry point"""
    hub.port.A.motor.run_for_seconds(3.0)
    hub.led('red')

if __name__ == "__main__":
    main()
```

## File Structure

```
.
├── main.py                     # Interactive conversion interface
├── llsp3_converter.py          # .llsp3 project file processor
├── spike_svg_converter.py      # SVG diagram converter
├── test_llsp3.py              # Test script for .llsp3 conversion
├── example_spike_blocks.svg    # Example SVG file
├── complex_example.svg         # Complex example with nested blocks
├── sumobot_test.llsp3         # Real SPIKE Prime project file
├── generated_spike_code.py     # Generated Python output
├── sumobot_converted.py       # Converted sumobot code
└── README.md                   # This documentation
```

## How It Works

### For .llsp3 Files
1. **Archive Extraction**: Unzips the .llsp3 project file
2. **Data Mining**: Extracts JSON metadata and SVG diagrams 
3. **Block Discovery**: Finds block definitions in project data
4. **Pattern Analysis**: Matches blocks to known SPIKE Prime patterns
5. **Code Generation**: Converts blocks to Python using templates
6. **Structure Assembly**: Creates proper program flow and syntax

### For SVG Files
1. **XML Parsing**: Uses BeautifulSoup to parse SVG structure
2. **Text Extraction**: Finds text elements with block descriptions
3. **Position Analysis**: Sorts blocks spatially for code order
4. **Block Recognition**: Matches text patterns to block types
5. **Parameter Extraction**: Pulls numbers, colors, ports from text
6. **Code Generation**: Converts to equivalent Python statements

## Block Recognition Patterns

The converter uses pattern matching to identify blocks:

- **Motor blocks**: Look for "motor", "run", "stop" keywords plus port letters (A-F)
- **LED blocks**: Detect "led", "light" keywords plus color names
- **Wait blocks**: Find "wait", "sleep" keywords plus time values
- **Control blocks**: Recognize "repeat", "forever", "if" structures
- **Sound blocks**: Identify "sound", "beep" with frequency/duration

## Limitations

- Only processes text-based block representations in SVG
- Requires specific text patterns to recognize blocks
- May need manual adjustment for complex nested structures
- Does not handle all possible SPIKE block variations

## Contributing

To add support for new block types:

1. Add pattern recognition in `_identify_block_type()`
2. Add parameter extraction logic in `_extract_parameters()`
3. Add Python code template in `block_templates`
4. Add required imports to `imports` dictionary

## License

This project is open source. Feel free to modify and distribute.

## Examples and Testing

Run the main program to see the converter in action:

```bash
python main.py
```

This demonstrates converting the included example SVG file and shows both the input blocks and generated Python code.