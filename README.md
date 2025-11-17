ProjectZipper 🗂️⚡

<div align="center">

https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi
https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white
https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white

A high-performance FastAPI service that converts text-based file trees into downloadable ZIP archives

https://img.shields.io/github/issues/umarbutt/projectzipper
https://img.shields.io/badge/License-MIT-yellow.svg
https://img.shields.io/badge/python-3.8+-blue.svg

</div>

✨ Features

· 🚀 Lightning Fast - Built with FastAPI for high-performance ZIP generation
· 📁 Smart Parsing - Interprets various textual file tree formats with intelligent structure detection
· 🎯 Auto Content Generation - Creates appropriate placeholder content based on file extensions
· 💾 Streaming Response - Efficient memory usage with direct ZIP streaming for large archives
· 🔧 Fully Typed - Comprehensive Python type hints for better code quality and developer experience
· 🐳 Docker Ready - Containerized deployment for consistent environments

🎮 Quick Start

Installation

```bash
# Clone the repository
git clone https://github.com/umarbutt/projectzipper.git
cd projectzipper

# Install dependencies
pip install -r requirements.txt
```

Basic Usage

```python
import requests

# Example file structure
tree_structure = """
project/
├── src/
│   ├── main.py
│   └── utils.py
├── tests/
│   └── test_main.py
├── requirements.txt
└── README.md
"""

response = requests.post(
    "http://localhost:8000/generate-zip",
    json={
        "tree_structure": tree_structure,
        "root_dir_name": "my_project"
    }
)

# Save the generated ZIP
if response.status_code == 200:
    with open("my_project.zip", "wb") as f:
        f.write(response.content)
    print("✅ Successfully generated my_project.zip")
else:
    print(f"❌ Error: {response.status_code}, {response.text}")
```

🛠️ API Reference

POST /generate-zip

Generates a ZIP archive from the provided file tree structure.

Request Body:

```json
{
  "tree_structure": "string",
  "root_dir_name": "string"
}
```

Parameters:

Field Type Required Description
tree_structure string ✅ Text representation of directory tree
root_dir_name string ✅ Top-level directory name in ZIP

Response: application/zip stream with generated archive

📦 Supported File Types

File Type Generated Content
.py Python file with comments and basic structure
.js JavaScript file with console log statement
.json Empty JSON object {}
.txt Simple text placeholder
.md Markdown file with basic header
.html Basic HTML5 template
.css CSS file with reset styles
Others Generic placeholder text

🚀 Deployment

Local Development

```bash
python main.py
# Server runs on http://localhost:8000
```

Docker Deployment

```bash
docker build -t projectzipper .
docker run -p 8000:8000 projectzipper
```

Production with Uvicorn

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

🏗️ Project Structure

```
projectzipper/
├── main.py                 # FastAPI application entry point
├── requirements.txt        # Python dependencies
├── Dockerfile             # Container configuration
├── README.md              # Project documentation
└── examples/              # Usage examples
    ├── basic_usage.py     # Simple implementation
    └── advanced_usage.py  # Complex use cases
```

🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create feature branch: git checkout -b feature/amazing-feature
3. Commit changes: git commit -m 'feat: Add amazing feature'
4. Push to branch: git push origin feature/amazing-feature
5. Open a Pull Request

Reporting Issues

Use the GitHub Issues to report bugs or request features.

📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

👨‍💻 Author

Mohd Umar Butt

<div align="center">

https://img.shields.io/badge/GitHub-mohdumarbutt-181717?style=for-the-badge&logo=github
https://img.shields.io/badge/LinkedIn-Mohd_Umar_Butt-0077B5?style=for-the-badge&logo=linkedin
https://img.shields.io/badge/Email-Mohdumar2724@gmail.com-D14836?style=for-the-badge&logo=gmail

</div>

🌟 Support

If this project helps you, consider supporting its development:

<div align="center">

https://img.shields.io/badge/Buy_Me_A_Coffee-FFDD00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black

</div>

Your support helps maintain and improve this project! ❤️

🛡️ Security

For security-related issues, please email Mohdumar2724@gmail.com instead of using the public issue tracker.

🙏 Acknowledgments

· FastAPI team for the excellent web framework
· Pydantic for robust data validation
· Uvicorn for high-performance ASGI server
· All contributors and users of this project

---

<div align="center">

⭐ Don't forget to star this repo if you find it useful!

Made with ❤️ by Umar Butt

https://img.shields.io/github/followers/mohdumarbutt?style=social

</div>

---

📊 Project Status

https://img.shields.io/github/last-commit/umarbutt/projectzipper
https://img.shields.io/github/repo-size/umarbutt/projectzipper

Last Updated: 25/10/2025

---

<div align="center">

https://img.shields.io/badge/Powered_by-FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white
https://img.shields.io/badge/Made_with-Python-3776AB?style=for-the-badge&logo=python&logoColor=white

</div>