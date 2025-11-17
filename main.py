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
    root_name: str, 
    zip_buffer: io.BytesIO
) -> Iterator[bytes]:
    """
    Parses tree lines, creates a zip archive in the in-memory buffer, 
    and returns a generator to stream the data. This version uses robust 
    parsing to strip structural characters (│, ├──, etc.).
    """
    
    # --- Step 3b & 3c (Setup Archive) ---
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_archive:
        
        # Stack to manage directory hierarchy
        current_path_stack = []
        
        # Base path for zipping (e.g., 'valley-prayer-times/')
        base_path = f"{root_name}" 
        
        # Add the root folder itself to the ZIP
        zip_archive.writestr(f"{base_path}/", "")

        for line in tree_lines:
            line = line.rstrip() # Remove trailing whitespace

            if not line:
                continue
            
            # --- 3c (Robust Parsing: Find the Start of the Name) ---
            
            # Find the position where the actual file/folder name starts 
            # by looking for the first alphanumeric character or dot.
            name_start_index = 0
            for i, char in enumerate(line):
                # Stop searching when we hit an alphanumeric character or a dot (start of filename)
                if char.isalnum() or char in ['.', '/']:
                    break
                name_start_index = i + 1
            
            # The clean name is the remainder of the line, stripped of any leading/trailing space.
            clean_name = line[name_start_index:].strip()
            
            if not clean_name:
                continue

            # --- Calculate Indent Level ---
            # Calculate the indent level based on the number of structural symbols present 
            # before the name. This helps manage the stack.
            indent_level = line[:name_start_index].count('│') + line[:name_start_index].count('└') + line[:name_start_index].count('├')
            
            # --- Determine Hierarchy ---
            
            # 1. Update the path stack based on indentation
            while len(current_path_stack) > indent_level:
                current_path_stack.pop()
            
            # 2. Append the current clean name to the stack
            current_path_stack.append(clean_name)
            
            # 3. Construct the full path
            relative_path = "/".join(current_path_stack)
            full_zip_path = f"{base_path}/{relative_path}"

            # --- 3c (Write to Archive) ---
            
            # Heuristic: If path ends with / or has no period/extension, treat as directory
            if full_zip_path.endswith('/') or not '.' in full_zip_path.split('/')[-1]:
                
                # Directory logic:
                dir_path = full_zip_path.rstrip('/') + "/"
                zip_archive.writestr(dir_path, "")
                
                # The directory name stays on the stack until the next line decreases indentation.
                # However, if the current item is definitively a directory (e.g., 'src/'), 
                # we pop it off to prevent duplication in the next step's relative_path calculation.
                current_path_stack.pop()
                
            else:
                # File logic:
                
                # Generate simple placeholder content (slightly expanded)
                if full_zip_path.endswith(('.js', '.jsx', '.d.ts')):
                    content = f'// File: {relative_path}\nconsole.log("Project Zipper generated this file.");'
                elif full_zip_path.endswith(('.py', '.dart', '.md')):
                    content = f'# File: {relative_path}\n# This content is a placeholder.'
                elif full_zip_path.endswith(('.json', '.yml')):
                    content = '{\n  "generated_by": "ProjectZipper"\n}'
                else:
                    content = f'File: {relative_path} content.'
                    
                zip_archive.writestr(full_zip_path, content.encode('utf-8'))
                
                # Pop the file name from the stack immediately after creation
                current_path_stack.pop()

    # --- 3d (Finalize Buffer) ---
    zip_buffer.seek(0) # Rewind the buffer to the beginning

    # --- 4 (Create Stream Generator) ---
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
    
    lines = input_data.tree_structure.strip().split('\n')
    
    if not lines or not input_data.tree_structure.strip():
        raise HTTPException(status_code=400, detail="Input tree structure cannot be empty.")

    # --- 3a (Initialize Buffer) ---
    zip_buffer = io.BytesIO()
    
    try:
        stream = parse_and_zip_project(lines, input_data.root_dir_name, zip_buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during zip creation: {str(e)}")

    # --- 4 (Construct Streaming Response) ---
    response = StreamingResponse(
        stream,
        media_type="application/zip",
        headers={
            "Content-Disposition": f"attachment; filename={input_data.root_dir_name}.zip",
            "Content-Length": str(zip_buffer.getbuffer().nbytes) 
        }
    )
    return response

# --- 5. Local Development Run Command ---
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
