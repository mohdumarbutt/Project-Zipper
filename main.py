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
    root_dir_name: str = "project" # Default name for the downloadable ZIP and root folder

app = FastAPI(
    title="ProjectZipper",
    description="Generate a downloadable ZIP file from a text-based file tree structure."
)

# --- 2. Root Endpoint (Added to pass Render Health Check) ---
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
    root_name: str, 
    zip_buffer: io.BytesIO
) -> Iterator[bytes]:
    """
    Parses tree lines, creates a zip archive in the in-memory buffer, 
    and returns a generator to stream the data.
    """
    
    # --- Step 3b & 3c (Setup Archive) ---
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_archive:
        
        # A simple stack to keep track of current directories (context for nested files)
        current_path_stack = []
        
        # Determine the base path for zipping (e.g., 'project/')
        base_path = f"{root_name}" 
        
        # Add the root folder itself to the ZIP
        zip_archive.writestr(f"{base_path}/", "")

        for line in tree_lines:
            line = line.strip()
            if not line:
                continue

            # --- Step 3c (Parsing: Identify Indentation and Name) ---
            
            # Count leading non-alphanumeric characters (indicators of indentation)
            # This is a robust way to handle tree lines like "├── file" or "│   file"
            indent_level = len(line) - len(line.lstrip('|- '))
            
            # The clean name is the text after the indentation indicators
            clean_name = line.lstrip('|- ').lstrip('└──').lstrip('├──').strip()
            
            if not clean_name:
                continue

            # --- Step 3c (Determine Hierarchy) ---
            
            # 1. Update the path stack based on indentation
            # Pop elements from the stack if indentation decreases
            while len(current_path_stack) > indent_level:
                current_path_stack.pop()
            
            # 2. Add the current name to the stack
            current_path_stack.append(clean_name)
            
            # 3. Construct the final relative path within the ZIP (e.g., 'src/main.js')
            relative_path = "/".join(current_path_stack)
            
            # 4. Construct the full ZIP path (e.g., 'project/src/main.js')
            full_zip_path = f"{base_path}/{relative_path}"


            if full_zip_path.endswith('/') or not '.' in full_zip_path.split('/')[-1]:
                # Treat as a directory if ends with / or has no file extension heuristic
                dir_path = full_zip_path.rstrip('/') + "/"
                zip_archive.writestr(dir_path, "") # Write empty string for a directory entry
                
                # Crucial: If it was identified as a directory, remove the last element from stack 
                # (the directory name itself) because we are relying on the indentation level 
                # to manage the hierarchy, and the next line will be a child of this directory.
                # If we leave it, the path will be duplicated (e.g., 'src/src/file').
                # We handle the hierarchy via `current_path_stack` length, not the explicit path strings.
                
                # The simple path parsing provided above is sufficient for your basic example:
                # project/
                # ├── src/
                # ...
                
                # However, for robustness, if the name ends with '/', remove it from the stack 
                # to prevent path duplication when the children are processed.
                if current_path_stack and current_path_stack[-1].endswith('/'):
                    current_path_stack[-1] = current_path_stack[-1].rstrip('/') # Clean up the stack entry
                
            else:
                # --- Step 3c (File Content Generation) ---
                
                # Generate simple placeholder content based on the extension
                if full_zip_path.endswith('.js'):
                    content = f'// File: {relative_path}\nconsole.log("Project Zipper generated this file.");'
                elif full_zip_path.endswith(('.py', '.txt')):
                    content = f'# File: {relative_path}\n# This content is a placeholder.'
                elif full_zip_path.endswith(('.json')):
                    content = '{\n  "generated_by": "ProjectZipper"\n}'
                else:
                    content = f'File: {relative_path} content.'
                    
                zip_archive.writestr(full_zip_path, content.encode('utf-8'))
                
                # Pop the file name from the stack immediately after creation
                current_path_stack.pop()

    # --- Step 3d (Finalize Buffer) ---
    zip_buffer.seek(0) # Rewind the buffer to the beginning

    # --- Step 4 (Create Stream Generator) ---
    def zip_streamer() -> Iterator[bytes]:
        """Reads the in-memory buffer in chunks for streaming."""
        chunk_size = 8192  # 8KB
        while True:
            chunk = zip_buffer.read(chunk_size)
            if not chunk:
                break
            yield chunk

    # Return the generator function
    return zip_streamer()


# --- 4. FastAPI Endpoint (POST /generate-zip) ---

@app.post("/generate-zip", tags=["Generator"])
async def generate_zip_file(input_data: TreeInput):
    """
    Accepts a tree-like text structure, generates an in-memory ZIP file, 
    and returns it as a downloadable response.
    """
    
    # Pre-process the input lines
    lines = input_data.tree_structure.strip().split('\n')
    
    if not lines or not input_data.tree_structure.strip():
        raise HTTPException(status_code=400, detail="Input tree structure cannot be empty.")

    # --- Step 3a (Initialize Buffer) ---
    zip_buffer = io.BytesIO()
    
    # Perform the parsing and zipping
    try:
        # --- Call Core Logic ---
        stream = parse_and_zip_project(lines, input_data.root_dir_name, zip_buffer)
    except Exception as e:
        # Catch any unexpected errors during zipping
        raise HTTPException(status_code=500, detail=f"Error during zip creation: {str(e)}")

    # --- Step 4 (Construct Streaming Response) ---
    response = StreamingResponse(
        stream,
        media_type="application/zip",
        headers={
            # Forces download and sets the filename
            "Content-Disposition": f"attachment; filename={input_data.root_dir_name}.zip",
            # Provides the client with the final file size for progress bar display
            "Content-Length": str(zip_buffer.getbuffer().nbytes) 
        }
    )
    return response

# --- 5. Local Development Run Command ---
if __name__ == "__main__":
    import uvicorn
    # Host 0.0.0.0 is needed for Pydroid/Android access
    uvicorn.run(app, host="0.0.0.0", port=8000)
