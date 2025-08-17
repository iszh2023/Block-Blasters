#!/usr/bin/env python3
"""
Test script for .llsp3 converter functionality
"""

import os
from llsp3_converter import LLSP3Analyzer


def test_llsp3_converter():
    """Test the .llsp3 converter with the sumobot example"""
    print("Testing LLSP3 to Python Converter")
    print("=" * 40)
    
    analyzer = LLSP3Analyzer()
    
    # Test with the sumobot file
    test_files = [
        'sumobot_test.llsp3',
        'attached_assets/Sumobot CODE 1_1755462521642.llsp3'
    ]
    
    for file_path in test_files:
        if os.path.exists(file_path):
            print(f"\nProcessing: {file_path}")
            print("-" * 30)
            
            try:
                python_code = analyzer.process_llsp3_file(file_path)
                
                print("Generated Python Code:")
                print(python_code)
                
                # Save the output
                output_name = 'sumobot_converted.py'
                with open(output_name, 'w') as f:
                    f.write(python_code)
                print(f"\n✓ Saved converted code to {output_name}")
                
                return True
                
            except Exception as e:
                print(f"Error processing {file_path}: {e}")
                import traceback
                traceback.print_exc()
    
    print("No .llsp3 files found to test")
    return False


if __name__ == "__main__":
    test_llsp3_converter()