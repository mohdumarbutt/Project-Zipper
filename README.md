Project Zipper API

A FastAPI application that generates a downloadable ZIP file from a text-based file tree structure.

Overview
Project Zipper API is a web service that takes a text-based representation of a file tree structure and returns a ZIP file containing the corresponding files and directories. This is useful for creating project templates or demo projects on the fly.

Features
- Accepts a tree-like text structure as input
- Generates an in-memory ZIP file with placeholder content
- Returns the ZIP file as a downloadable response
- Built with FastAPI and Uvicorn for high performance and scalability

Usage
1. Send a POST request to `/generate-zip` with the file tree structure in the request body.
2. The API will return a ZIP file containing the generated project.

Example Input
{
  "tree_structure": "src/\n├── main.js\n├── utils/\n│   ├── helper.js\n│   └── constants.js\n└── index.html",
  "root_dir_name": "my-project"
}

Example Response
A ZIP file containing the generated project.

Deployment
This application is designed to be deployed on Render. See the `render.yaml` file for deployment configuration.

Requirements
- Python 3.9+
- FastAPI
- Uvicorn
- Pydantic

Running Locally
1. Clone the repository and navigate to the project directory.
2. Install dependencies with `pip install -r requirements.txt`.
3. Run the application with `uvicorn main:app --host 0.0.0.0 --port 8000`.

Contributing
Contributions are welcome! Please submit a pull request with your changes.

License
This project is licensed under the MIT License. See the `LICENSE` file for details.