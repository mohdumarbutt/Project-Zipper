import io
import zipfile
from typing import Iterator

from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

# --- 1. Pydantic Model for Request Body ---
class TreeInput(BaseModel):
    """Defines the structure of the JSON input for the API."""
    tree_structure: str

app = FastAPI(
    title="ProjectZipper",
    description="Generate a downloadable ZIP file from a text-based file tree structure."
)

# --- 2. Root Endpoint (For Health Check and Info) ---
@app.get("/", tags=["Info"])
def read_root():
    return {
        "service": "ProjectZipper API", 
        "status": "Online", 
        "documentation": "/docs"
    }

# --- 3. Core Logic: Parsing and Zipping ---

def parse_and_zip_project(
    tree_lines: list[str], 
    zip_buffer: io.BytesIO
) -> Iterator[bytes]:
    """
    Parses tree lines, creates a zip archive in the in-memory buffer, 
    and returns a generator to stream the data.
    """
    
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_archive:
        
        # Stack to manage directory hierarchy
        current_path_stack = []
        
        # Track created directories to avoid duplicates
        created_dirs = set()
        
        # Extract root directory name from first line
        root_dir_name = extract_root_directory(tree_lines[0]) if tree_lines else "project"

        for line in tree_lines:
            line = line.rstrip() # Remove trailing whitespace

            if not line:
                continue
            
            # --- Robust Parsing: Find the Start of the Name ---
            
            # Find the position where the actual file/folder name starts 
            name_start_index = 0
            for i, char in enumerate(line):
                # Stop searching when we hit an alphanumeric character or a dot
                if char.isalnum() or char in ['.', '/']:
                    break
                name_start_index = i + 1
            
            # The clean name is the remainder of the line, stripped of any leading/trailing space
            clean_name = line[name_start_index:].strip()
            
            if not clean_name:
                continue

            # --- Calculate Indent Level ---
            indent_level = line[:name_start_index].count('│') + line[:name_start_index].count('└') + line[:name_start_index].count('├')
            
            # --- Determine Hierarchy ---
            
            # 1. Update the path stack based on indentation
            while len(current_path_stack) > indent_level:
                current_path_stack.pop()
            
            # 2. Append the current clean name to the stack
            current_path_stack.append(clean_name)
            
            # 3. Construct the full path
            relative_path = "/".join(current_path_stack)

            # --- Improved Directory Detection ---
            
            # Detect directories based on common patterns and structure
            is_directory = (
                clean_name.endswith('/') or
                not '.' in clean_name.split('/')[-1] or
                any(dir_indicator in clean_name.lower() for dir_indicator in 
                    ['src', 'dist', 'examples', 'test', 'docs', 'fixtures', 'workflows', 
                     'issue_template', '.github'])
            )
            
            if is_directory:
                # Directory logic
                dir_path = relative_path.rstrip('/') + "/"
                
                # Only create directory if not already created
                if dir_path not in created_dirs:
                    zip_archive.writestr(dir_path, "")
                    created_dirs.add(dir_path)
                
                # Don't pop from stack - keep for child items
                
            else:
                # File logic - generate appropriate content
                content = generate_file_content(relative_path, clean_name)
                zip_archive.writestr(relative_path, content.encode('utf-8'))
                
                # Pop the file name from the stack immediately after creation
                current_path_stack.pop()

    # --- Finalize Buffer ---
    zip_buffer.seek(0)

    # --- Create Stream Generator ---
    def zip_streamer() -> Iterator[bytes]:
        """Reads the in-memory buffer in chunks for streaming."""
        chunk_size = 8192
        while True:
            chunk = zip_buffer.read(chunk_size)
            if not chunk:
                break
            yield chunk

    return zip_streamer(), root_dir_name

def extract_root_directory(first_line: str) -> str:
    """Extract the root directory name from the first line of the tree structure."""
    # Remove tree structure characters and strip
    clean_line = first_line.strip()
    
    # Find the actual directory name (remove trailing slash if present)
    if '/' in clean_line:
        # Handle cases like "valley-prayer-times/"
        root_name = clean_line.split('/')[0].strip()
    else:
        # Handle cases without trailing slash
        root_name = clean_line.strip()
    
    # Clean up any remaining tree characters
    for char in ['│', '├', '└', '──']:
        root_name = root_name.replace(char, '').strip()
    
    return root_name if root_name else "project"

def generate_file_content(relative_path: str, clean_name: str) -> str:
    """Generate appropriate placeholder content based on file type."""
    if relative_path.endswith(('.js', '.jsx')):
        return f'''// {clean_name}
// Generated by ProjectZipper

function main() {{
    console.log("Hello from {clean_name}");
}}

module.exports = {{ main }};
'''
    elif relative_path.endswith('.d.ts'):
        return f'''// TypeScript definitions for {clean_name}
// Generated by ProjectZipper

export interface PrayerTimes {{
    fajr: string;
    sunrise: string;
    dhuhr: string;
    asr: string;
    maghrib: string;
    isha: string;
}}

export declare function calculatePrayerTimes(date: Date, latitude: number, longitude: number): PrayerTimes;
'''
    elif relative_path.endswith('.py'):
        return f'''# {clean_name}
# Generated by ProjectZipper

def main():
    print("Hello from {clean_name}")

if __name__ == "__main__":
    main()
'''
    elif relative_path.endswith('.dart'):
        return f'''// {clean_name}
// Generated by ProjectZipper

void main() {{
    print('Hello from {clean_name}');
}}
'''
    elif relative_path.endswith('.md'):
        return f'''# {clean_name}

This file was generated by ProjectZipper.

## Description

Placeholder content for {clean_name}.
'''
    elif relative_path.endswith('.json'):
        return f'''{{
  "generated_by": "ProjectZipper",
  "file": "{clean_name}",
  "description": "Placeholder configuration file"
}}
'''
    elif relative_path.endswith(('.yml', '.yaml')):
        return f'''# {clean_name}
# Generated by ProjectZipper

name: "Project Configuration"
version: "1.0.0"
description: "Placeholder YAML configuration"
'''
    elif relative_path in ['LICENSE', 'LICENSE.md']:
        return '''MIT License

Copyright (c) 2024 Project Author

Permission is hereby granted...
'''
    elif relative_path == 'package.json':
        return '''{
  "name": "valley-prayer-times",
  "version": "1.0.0",
  "description": "Prayer times calculation library",
  "main": "dist/vpt.min.js",
  "scripts": {
    "build": "node build.js",
    "test": "jest",
    "lint": "eslint src/"
  },
  "keywords": ["prayer", "times", "islamic", "calculation"],
  "author": "Your Name",
  "license": "MIT"
}
'''
    elif relative_path in ['.gitignore', '.npmignore']:
        return '''node_modules/
dist/
*.log
.DS_Store
.env
'''
    elif relative_path in ['.eslintrc.json']:
        return '''{
  "extends": ["eslint:recommended"],
  "env": {
    "node": true,
    "es6": true
  },
  "parserOptions": {
    "ecmaVersion": 2020
  }
}
'''
    elif relative_path in ['.prettierrc']:
        return '''{
  "semi": true,
  "singleQuote": true,
  "tabWidth": 2
}
'''
    else:
        return f'''# {clean_name}

This file was generated by ProjectZipper.

File: {relative_path}
'''

# --- 4. FastAPI Endpoint (POST /generate-zip) ---

@app.post("/generate-zip", tags=["Generator"])
async def generate_zip_file(input_data: TreeInput):
    """
    Accepts a tree-like text structure, generates an in-memory ZIP file, 
    and returns it as a downloadable response.
    """
    
    lines = input_data.tree_structure.strip().split('\n')
    
    if not lines or not input_data.tree_structure.strip():
        raise HTTPException(status_code=400, detail="Input tree structure cannot be empty.")

    # Initialize Buffer
    zip_buffer = io.BytesIO()
    
    try:
        stream, root_dir_name = parse_and_zip_project(lines, zip_buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during zip creation: {str(e)}")

    # Construct Streaming Response
    response = StreamingResponse(
        stream,
        media_type="application/zip",
        headers={
            "Content-Disposition": f"attachment; filename={root_dir_name}.zip",
            "Content-Length": str(zip_buffer.getbuffer().nbytes) 
        }
    )
    return response

# --- 5. Local Development Run Command ---
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)