#!/usr/bin/env python3
"""
SPIKE Prime Block Code Converter - Main Program

This program converts both SVG diagrams and .llsp3 project files to Python code.
It provides an interactive interface for processing SPIKE Prime projects.
"""

import os
from spike_svg_converter import SpikeBlockParser
from llsp3_converter import LLSP3Analyzer


def main():
    """Main program with interactive interface"""
    print("SPIKE Prime Block Code to Python Converter")
    print("=" * 50)
    print()
    print("This tool can convert:")
    print("1. SVG diagrams of SPIKE blocks")
    print("2. LEGO SPIKE Prime .llsp3 project files")
    print()
    
    while True:
        print("Choose conversion type:")
        print("1. Convert SVG file")
        print("2. Convert .llsp3 project file")
        print("3. Demo with included examples")
        print("4. Quit")
        
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == '1':
            convert_svg_file()
        elif choice == '2':
            convert_llsp3_file()
        elif choice == '3':
            demo_examples()
        elif choice == '4':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")
        
        print("\n" + "=" * 50)


def convert_svg_file():
    """Convert SVG file to Python"""
    converter = SpikeBlockParser()
    
    file_path = input("Enter path to SVG file: ").strip()
    
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found.")
        return
    
    try:
        print(f"\nConverting {file_path}...")
        python_code = converter.parse_svg_file(file_path)
        
        print("\nGenerated Python Code:")
        print("-" * 40)
        print(python_code)
        print("-" * 40)
        
        # Ask if user wants to save
        save = input("\nSave to file? (y/n): ").strip().lower()
        if save in ['y', 'yes']:
            output_name = os.path.splitext(file_path)[0] + '_converted.py'
            with open(output_name, 'w') as f:
                f.write(python_code)
            print(f"✓ Saved to {output_name}")
        
    except Exception as e:
        print(f"Error converting SVG: {e}")


def convert_llsp3_file():
    """Convert .llsp3 file to Python"""
    analyzer = LLSP3Analyzer()
    
    file_path = input("Enter path to .llsp3 file: ").strip()
    
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found.")
        return
    
    try:
        print(f"\nAnalyzing .llsp3 project: {file_path}")
        print("Extracting blocks from project data...")
        
        python_code = analyzer.process_llsp3_file(file_path)
        
        print("\nGenerated Python Code:")
        print("-" * 40)
        print(python_code)
        print("-" * 40)
        
        # Ask if user wants to save
        save = input("\nSave to file? (y/n): ").strip().lower()
        if save in ['y', 'yes']:
            output_name = os.path.splitext(file_path)[0] + '_converted.py'
            with open(output_name, 'w') as f:
                f.write(python_code)
            print(f"✓ Saved to {output_name}")
        
    except Exception as e:
        print(f"Error converting .llsp3: {e}")


def demo_examples():
    """Demo with included example files"""
    print("\nRunning demo with included examples...")
    
    # Demo SVG conversion
    converter = SpikeBlockParser()
    
    print("\n1. SVG Example Conversion:")
    print("-" * 30)
    
    try:
        if os.path.exists('example_spike_blocks.svg'):
            python_code = converter.parse_svg_file('example_spike_blocks.svg')
            print("Simple example result:")
            print(python_code[:300] + "..." if len(python_code) > 300 else python_code)
        else:
            print("example_spike_blocks.svg not found")
    except Exception as e:
        print(f"Error with SVG demo: {e}")
    
    print("\n2. .llsp3 Example Conversion:")
    print("-" * 30)
    
    # Check for any .llsp3 files in current directory or attached_assets
    llsp3_files = []
    
    # Check current directory
    for file in os.listdir('.'):
        if file.endswith('.llsp3'):
            llsp3_files.append(file)
    
    # Check attached_assets directory
    if os.path.exists('attached_assets'):
        for file in os.listdir('attached_assets'):
            if file.endswith('.llsp3'):
                llsp3_files.append(os.path.join('attached_assets', file))
    
    if llsp3_files:
        analyzer = LLSP3Analyzer()
        test_file = llsp3_files[0]
        print(f"Testing with: {test_file}")
        
        try:
            python_code = analyzer.process_llsp3_file(test_file)
            print("Conversion result:")
            print(python_code[:400] + "..." if len(python_code) > 400 else python_code)
        except Exception as e:
            print(f"Error processing {test_file}: {e}")
    else:
        print("No .llsp3 files found for demo")
    
    print("\nDemo complete!")

if __name__ == "__main__":
    main()