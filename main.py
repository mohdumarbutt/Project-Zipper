import io
import zipfile
import re
from typing import Iterator, Tuple, List
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

class TreeInput(BaseModel):
    """Defines the structure of the JSON input for the API."""
    tree_structure: str

app = FastAPI(
    title="ProjectZipper",
    description="Generate a downloadable ZIP file from a text-based file tree structure."
)

@app.get("/", tags=["Info"])
def read_root():
    return {
        "service": "ProjectZipper API", 
        "status": "Online", 
        "documentation": "/docs"
    }

def parse_tree_structure(tree_lines: List[str]) -> List[Tuple[str, int, bool]]:
    """
    Parse tree structure lines into (path, depth, is_directory) tuples.
    This handles the tree characters and calculates proper depth.
    """
    parsed_items = []
    
    for line in tree_lines:
        line = line.rstrip()
        if not line:
            continue
            
        # Count the depth based on tree characters
        # Each '├──', '└──', or '│' increases depth, but we need to be careful
        depth = 0
        i = 0
        while i < len(line):
            if line[i] in [' ', '\t']:
                i += 1
                continue
            if line.startswith('├──', i) or line.startswith('└──', i):
                depth += 1
                i += 3
            elif line[i] == '│':
                depth += 1
                i += 1
            else:
                break
        
        # Extract the actual file/directory name
        # Find where the actual name starts (after tree characters)
        name_start = 0
        for i, char in enumerate(line):
            if char not in [' ', '│', '├', '└', '─', '\t']:
                name_start = i
                break
        
        clean_name = line[name_start:].strip()
        if not clean_name:
            continue
            
        # Determine if it's a directory
        is_directory = (
            clean_name.endswith('/') or 
            not '.' in clean_name.split('/')[-1] or
            any(clean_name == dir_name for dir_name in [
                'src', 'dist', 'examples', 'test', 'docs', 'fixtures', 
                'workflows', 'ISSUE_TEMPLATE', '.github'
            ]) or
            any(clean_name.startswith(dir_name) for dir_name in [
                'src/', 'dist/', 'examples/', 'test/', 'docs/', '.github/'
            ])
        )
        
        parsed_items.append((clean_name, depth, is_directory))
    
    return parsed_items

def build_file_hierarchy(parsed_items: List[Tuple[str, int, bool]]) -> List[Tuple[str, bool]]:
    """
    Build the complete file hierarchy from parsed items.
    Returns list of (full_path, is_directory) tuples.
    """
    hierarchy = []
    stack = []
    
    for name, depth, is_directory in parsed_items:
        # Adjust stack based on current depth
        while len(stack) > depth:
            stack.pop()
        
        # Build the full path
        if stack:
            parent_path = stack[-1][0]
            full_path = f"{parent_path}/{name}" if parent_path else name
        else:
            full_path = name
        
        # Add to hierarchy
        hierarchy.append((full_path, is_directory))
        
        # If it's a directory, push to stack for children
        if is_directory:
            stack.append((full_path, depth))
    
    return hierarchy

def parse_and_zip_project(
    tree_lines: list[str], 
    zip_buffer: io.BytesIO
) -> Tuple[Iterator[bytes], str]:
    """
    Main function to parse tree structure and create ZIP archive.
    """
    # Extract project name from first line
    project_name = "project"
    for line in tree_lines:
        line = line.strip()
        if line and not any(c in line for c in ['│', '├', '└', '─']):
            if '/' in line:
                project_name = line.split('/')[0].strip()
            else:
                project_name = line.strip()
            break
    
    # Parse the tree structure
    parsed_items = parse_tree_structure(tree_lines)
    hierarchy = build_file_hierarchy(parsed_items)
    
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_archive:
        created_dirs = set()
        
        for full_path, is_directory in hierarchy:
            if is_directory:
                # Ensure directory path ends with /
                dir_path = full_path.rstrip('/') + '/'
                if dir_path not in created_dirs:
                    zip_archive.writestr(dir_path, '')
                    created_dirs.add(dir_path)
            else:
                # It's a file - generate appropriate content
                content = generate_file_content(full_path)
                zip_archive.writestr(full_path, content)
    
    zip_buffer.seek(0)
    
    def zip_streamer() -> Iterator[bytes]:
        chunk_size = 8192
        while True:
            chunk = zip_buffer.read(chunk_size)
            if not chunk:
                break
            yield chunk

    return zip_streamer(), project_name

def generate_file_content(file_path: str) -> str:
    """
    Generate appropriate content based on file type and path.
    This is a general-purpose content generator.
    """
    filename = file_path.split('/')[-1]
    
    # Common configuration files
    if filename == 'package.json':
        return '''{
  "name": "project",
  "version": "1.0.0",
  "description": "",
  "main": "index.js",
  "scripts": {
    "test": "echo \\"Error: no test specified\\" && exit 1"
  },
  "keywords": [],
  "author": "",
  "license": "ISC"
}'''
    
    elif filename == '.gitignore':
        return '''node_modules/
dist/
build/
*.log
.DS_Store
.env
'''
    
    elif filename == '.eslintrc.json':
        return '''{
  "extends": ["eslint:recommended"],
  "env": {
    "browser": true,
    "node": true,
    "es6": true
  },
  "parserOptions": {
    "ecmaVersion": 2020
  },
  "rules": {}
}'''
    
    elif filename == '.prettierrc':
        return '''{
  "semi": true,
  "singleQuote": true,
  "tabWidth": 2,
  "trailingComma": "es5"
}'''
    
    elif filename == '.npmignore':
        return '''src/
test/
docs/
examples/
*.config.js
'''
    
    # Documentation files
    elif filename == 'README.md':
        return f'''# {file_path.split('/')[0] if '/' in file_path else 'Project'}

Project description goes here.

## Installation

\\`\\`\\`bash
npm install
\\`\\`\\`

## Usage

\\`\\`\\`javascript
// Example usage
console.log("Hello World");
\\`\\`\\`

## License

MIT
'''
    
    elif filename == 'DOCUMENTATION.md':
        return '''# Documentation

Project documentation goes here.

## Features

- Feature 1
- Feature 2
- Feature 3

## API Reference

Coming soon...
'''
    
    elif filename == 'CHANGELOG.md':
        return '''# Changelog

All notable changes to this project will be documented in this file.

## [1.0.0] - YYYY-MM-DD

### Added
- Initial release
'''
    
    elif filename == 'CONTRIBUTING.md':
        return '''# Contributing

We welcome contributions! Please see our guidelines below.

## Code Style

Please follow the existing code style.

## Testing

Make sure all tests pass before submitting a PR.
'''
    
    elif filename == 'CODE_OF_CONDUCT.md':
        return '''# Code of Conduct

## Our Pledge

We pledge to make participation in our project a harassment-free experience for everyone.
'''
    
    elif filename == 'ARCHITECTURE.md':
        return '''# Architecture

## Overview

Project architecture documentation.
'''
    
    elif filename == 'API.md':
        return '''# API Documentation

## Endpoints

- GET /api/v1/endpoint
- POST /api/v1/endpoint
'''
    
    elif filename == 'FAQ.md':
        return '''# Frequently Asked Questions

## Q: Question 1?
A: Answer 1.

## Q: Question 2?
A: Answer 2.
'''
    
    elif filename == 'FORMULAS.md':
        return '''# Formulas

Mathematical formulas and calculations used in this project.
'''
    
    elif filename == 'COMPARISON.md':
        return '''# Comparison

Comparison with similar projects and libraries.
'''
    
    elif filename == 'LICENSE':
        return '''MIT License

Copyright (c) 2024 Project Author

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.'''
    
    # GitHub specific files
    elif filename == 'ci.yml':
        return '''name: CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run tests
        run: npm test
'''
    
    elif filename == 'bug_report.md':
        return '''---
name: Bug report
about: Create a report to help us improve
title: ''
labels: bug
assignees: ''

---

## Describe the bug
A clear and concise description of what the bug is.

## Steps to reproduce
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '....'
3. Scroll down to '....'
4. See error

## Expected behavior
A clear and concise description of what you expected to happen.
'''
    
    elif filename == 'feature_request.md':
        return '''---
name: Feature request
about: Suggest an idea for this project
title: ''
labels: enhancement
assignees: ''

---

## Is your feature request related to a problem? Please describe.
A clear and concise description of what the problem is.

## Describe the solution you'd like
A clear and concise description of what you want to happen.
'''
    
    elif filename == 'PULL_REQUEST_TEMPLATE.md':
        return '''# Description

Please include a summary of the changes and which issue is fixed.

## Type of change

- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Checklist

- [ ] My code follows the style guidelines
- [ ] I have performed a self-review of my code
- [ ] I have added tests that prove my fix is effective
'''
    
    # Code files
    elif file_path.endswith('.js'):
        return f'''// {filename}
// Generated by ProjectZipper

console.log('Hello from {filename}');
module.exports = {{}};
'''
    
    elif file_path.endswith('.jsx'):
        return f'''import React from 'react';

const {filename.replace('.jsx', '').title()} = () => {{
  return (
    <div>
      <h1>{filename.replace('.jsx', '')}</h1>
    </div>
  );
}};

export default {filename.replace('.jsx', '').title()};
'''
    
    elif file_path.endswith('.d.ts'):
        return f'''// TypeScript definitions for {filename}

export interface Example {{
  // Type definitions here
}}
'''
    
    elif file_path.endswith('.dart'):
        return f'''// {filename}

void main() {{
  print('Hello from {filename}');
}}
'''
    
    elif file_path.endswith('.py'):
        return f'''# {filename}

def main():
    print("Hello from {filename}")

if __name__ == "__main__":
    main()
'''
    
    elif file_path.endswith('.json'):
        return '''{
  "name": "example",
  "version": "1.0.0"
}'''
    
    elif file_path.endswith(('.yml', '.yaml')):
        return '''# YAML configuration file

name: "Example"
version: "1.0.0"
'''
    
    # Default content for any other file type
    else:
        return f'# {filename}\n\nThis file was generated by ProjectZipper.\n\nFile path: {file_path}\n'

@app.post("/generate-zip", tags=["Generator"])
async def generate_zip_file(input_data: TreeInput):
    """
    Accepts a tree-like text structure, generates an in-memory ZIP file, 
    and returns it as a downloadable response.
    """
    
    lines = input_data.tree_structure.strip().split('\n')
    
    if not lines or not input_data.tree_structure.strip():
        raise HTTPException(status_code=400, detail="Input tree structure cannot be empty.")

    zip_buffer = io.BytesIO()
    
    try:
        stream, project_name = parse_and_zip_project(lines, zip_buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during zip creation: {str(e)}")

    response = StreamingResponse(
        stream,
        media_type="application/zip",
        headers={
            "Content-Disposition": f"attachment; filename={project_name}.zip",
            "Content-Length": str(zip_buffer.getbuffer().nbytes) 
        }
    )
    return response

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)