# Spike Block Code SVG to Python Converter

A powerful Python tool that converts SVG diagrams of SPIKE Prime block code into executable Python programs. This converter helps bridge the gap between visual programming and text-based coding.

## Features

- **SVG Parsing**: Reads SVG files containing SPIKE block diagrams
- **Block Recognition**: Identifies common SPIKE blocks and their parameters
- **Python Generation**: Creates clean, executable Python code
- **SPIKE Prime Compatible**: Generated code works with the SPIKE Prime hub
- **Multiple Block Types**: Supports motors, sensors, LEDs, sounds, and control structures

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

1. Make sure you have Python 3.7+ installed
2. Install required packages:
```bash
pip install beautifulsoup4 lxml xml-python
```

## Usage

### Basic Usage

```python
from spike_svg_converter import SpikeBlockParser

# Create converter instance
converter = SpikeBlockParser()

# Convert SVG file to Python
python_code = converter.parse_svg_file('your_blocks.svg')
print(python_code)

# Or convert SVG content directly
python_code = converter.parse_svg_content(svg_string)
```

### Command Line Usage

```bash
python main.py
```

This will convert the included example SVG and show the generated Python code.

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
├── main.py                     # Main program demonstrating the converter
├── spike_svg_converter.py      # Core converter library
├── example_spike_blocks.svg    # Example SVG file with SPIKE blocks
├── generated_spike_code.py     # Generated Python code output
└── README.md                   # This file
```

## How It Works

1. **SVG Parsing**: Uses BeautifulSoup to parse SVG XML structure
2. **Text Extraction**: Finds text elements containing block descriptions
3. **Position Analysis**: Sorts blocks by their position (top to bottom, left to right)
4. **Block Recognition**: Matches text patterns to known SPIKE block types
5. **Parameter Extraction**: Pulls out numbers, colors, ports, and text from blocks
6. **Code Generation**: Converts blocks to equivalent Python statements
7. **Structure Building**: Creates proper functions, loops, and indentation

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