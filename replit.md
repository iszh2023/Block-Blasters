# Overview

This is a comprehensive Python application that converts SPIKE Prime visual programming into executable Python code. The system supports both SVG diagrams and native .llsp3 project files, featuring intelligent block analysis, pattern recognition, and automated code generation. The converter bridges the gap between visual block programming and text-based coding, enabling SPIKE Prime developers to work with Python directly.

## Recent Changes (August 17, 2025)
- ✓ Added complete .llsp3 project file support with archive extraction
- ✓ Implemented intelligent pattern matching for block recognition  
- ✓ Created interactive console interface for user-friendly conversion
- ✓ Added comprehensive test suite with real sumobot project
- ✓ Enhanced error handling and robust file processing
- ✓ Integrated both SVG and .llsp3 converters in unified interface

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Core Application Structure
- **Multi-file architecture**: Modular design with specialized components
  - `main.py`: Interactive conversion interface with menu system
  - `llsp3_converter.py`: .llsp3 project file processor with archive handling
  - `spike_svg_converter.py`: SVG diagram converter with spatial analysis
  - `test_llsp3.py`: Automated test suite for .llsp3 conversion
  - `sumobot_test.llsp3`: Real SPIKE Prime project for testing
  - Example files: SVG diagrams and generated Python outputs

## Programming Language
- **Python 3.11**: Modern Python with type hints and advanced features
- **Object-oriented design**: Uses classes for parser functionality and extensibility

## Key Components
- **Dual Format Support**: Handles both .llsp3 archives and SVG diagrams
- **Archive Processing**: ZIP extraction and JSON/SVG data mining from .llsp3 files
- **Pattern Recognition**: Advanced regex-based block type identification
- **Template Engine**: Flexible code generation with parameter substitution
- **Interactive Interface**: User-friendly console application with multiple options
- **Comprehensive Testing**: Automated validation with real SPIKE Prime projects

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
- **zipfile-deflate64**: Enhanced ZIP archive handling for .llsp3 files
- **spike-py**: Official SPIKE Prime Python library for generated code compatibility

## Target Platform
- **SPIKE Prime Hub**: Generated Python code is compatible with LEGO SPIKE Prime programming environment
- **MicroPython**: Code follows MicroPython conventions used in SPIKE Prime