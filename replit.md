# Overview

This is a comprehensive Python application that converts SVG diagrams of SPIKE Prime block code into executable Python programs. The system includes a sophisticated parser that recognizes visual programming blocks and generates equivalent Python code compatible with SPIKE Prime robots. The project serves as a bridge between visual block programming and text-based coding.

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Core Application Structure
- **Multi-file architecture**: Modular design with specialized components
  - `main.py`: Demonstration program and CLI interface
  - `spike_svg_converter.py`: Core converter library with SpikeBlockParser class
  - `example_spike_blocks.svg`: Sample SVG file for testing
  - `generated_spike_code.py`: Output file containing converted Python code

## Programming Language
- **Python 3.11**: Modern Python with type hints and advanced features
- **Object-oriented design**: Uses classes for parser functionality and extensibility

## Key Components
- **SVG Parser**: BeautifulSoup-based XML/SVG processing
- **Block Recognition**: Pattern matching for SPIKE block identification
- **Code Generator**: Template-based Python code generation
- **Position Analysis**: Spatial sorting of blocks for proper code order

## Design Patterns
- **Parser Pattern**: Structured parsing of SVG elements
- **Template Method**: Code generation using predefined templates
- **Strategy Pattern**: Different handling for different block types

# External Dependencies

## Runtime Requirements
- **Python 3.11+**: The application requires modern Python interpreter
- **SPIKE Prime Hub**: Generated code is designed for SPIKE Prime robotics platform

## Third-party Libraries
- **beautifulsoup4**: XML/SVG parsing and DOM manipulation
- **lxml**: Fast XML parsing backend for BeautifulSoup
- **xml-python**: Additional XML processing utilities

## Target Platform
- **SPIKE Prime Hub**: Generated Python code is compatible with LEGO SPIKE Prime programming environment
- **MicroPython**: Code follows MicroPython conventions used in SPIKE Prime