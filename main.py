#!/usr/bin/env python3
"""
Spike Block Code SVG to Python Converter - Main Program

This program demonstrates the SVG to Python converter for Spike block code.
"""

from spike_svg_converter import SpikeBlockParser


def main():
    """Main program to demonstrate the Spike SVG converter"""
    print("Spike Block Code SVG to Python Converter")
    print("=" * 45)
    print()
    
    # Create converter instance
    converter = SpikeBlockParser()
    
    # Convert the example SVG file
    try:
        print("Converting example_spike_blocks.svg to Python...")
        python_code = converter.parse_svg_file('example_spike_blocks.svg')
        
        print("Generated Python Code:")
        print("-" * 30)
        print(python_code)
        print("-" * 30)
        print()
        
        # Save the generated code to a file
        with open('generated_spike_code.py', 'w') as f:
            f.write(python_code)
        print("✓ Saved generated code to 'generated_spike_code.py'")
        
    except FileNotFoundError:
        print("Error: example_spike_blocks.svg not found")
        print("Please ensure the SVG file exists in the current directory")
    except Exception as e:
        print(f"Error during conversion: {e}")
    
    print()
    
    # Test with complex example if it exists
    try:
        print("Converting complex_example.svg to Python...")
        complex_code = converter.parse_svg_file('complex_example.svg')
        print("Complex Example Generated Code:")
        print("-" * 35)
        print(complex_code)
        print("-" * 35)
        
        # Save the complex example
        with open('complex_generated_code.py', 'w') as f:
            f.write(complex_code)
        print("✓ Saved complex example to 'complex_generated_code.py'")
        
    except FileNotFoundError:
        print("Note: complex_example.svg not found (optional)")
    except Exception as e:
        print(f"Error with complex example: {e}")
    
    print()
    print("Usage Instructions:")
    print("1. Create or save your Spike block diagram as an SVG file")
    print("2. Use: converter.parse_svg_file('your_file.svg')")
    print("3. The generated Python code works with SPIKE Prime hub")
    print()
    print("Supported block types:")
    print("- When program starts")
    print("- Motor run/stop commands")
    print("- LED color settings")
    print("- Wait/sleep commands")
    print("- Print/say statements")
    print("- Sound/beep commands")
    print("- Repeat loops")
    print("- Forever loops")
    print("- Variable assignments")


if __name__ == "__main__":
    main()