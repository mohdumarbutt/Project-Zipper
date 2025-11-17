## ProjectZipper 🗂️⚡

A FastAPI-based service that converts text-based file tree structures into downloadable ZIP archives. Perfect for quickly generating project skeletons, boilerplate code, or file structure templates.

https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi
https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white
https://img.shields.io/badge/ZIP-Archive-2D5B8A?style=for-the-badge

## ✨ Features

· 🚀 Lightning Fast - Built with FastAPI for high performance
· 📁 Smart Parsing - Understands various tree structure formats
· 🎯 Auto Content - Generates appropriate placeholder content based on file types
· 💾 Streaming Response - Efficient memory usage with streaming ZIP downloads
· 🔧 Fully Typed - Type hints throughout for better development experience
· 🐳 Docker Ready - Easy deployment with containerization

## 🎮 Quick Start

Installation

```bash
# Clone the repository
git clone https://github.com/umarbutt/projectzipper.git
cd projectzipper

# Install dependencies
pip install -r requirements.txt
```

Usage

```python
import requests

# Example request
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

# Save the ZIP file
with open("my_project.zip", "wb") as f:
    f.write(response.content)
```

🛠️ API Reference

POST /generate-zip

Generates a ZIP file from a tree structure.

Request Body:

```json
{
  "tree_structure": "string",
  "root_dir_name": "string"
}
```

Response: ZIP file stream

📦 Supported File Types

File Type Generated Content
.py Python placeholder with comments
.js JavaScript placeholder with console log
.json Basic JSON structure
.txt Simple text placeholder
Others Basic file identifier

🚀 Deployment

Local Development

```bash
python main.py
```

Using Docker

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
├── main.py              # FastAPI application
├── requirements.txt     # Dependencies
├── Dockerfile          # Container configuration
├── README.md           # Project documentation
└── examples/           # Usage examples
    ├── basic_usage.py
    └── advanced_usage.py
```

🤝 Contributing

We love your input! We want to make contributing to ProjectZipper as easy and transparent as possible.

Development Setup

1. Fork the repo
2. Create your feature branch (git checkout -b feature/amazing-feature)
3. Commit your changes (git commit -m 'Add some amazing feature')
4. Push to the branch (git push origin feature/amazing-feature)
5. Open a Pull Request

Reporting Issues

Please use the issue tracker to report any bugs or suggest features.

📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

👨‍💻 Author

Mohd Umar Butt (Umar Butt)

· 💼 Portfolio
· 🐦 Twitter
· 💻 GitHub
· 📝 Blog
· 🔗 LinkedIn

🌟 Support

If you find this project helpful, please consider supporting its development:

☕ Buy Me a Coffee

https://img.shields.io/badge/Buy_Me_A_Coffee-FFDD00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black

Your support helps me continue maintaining and improving this project and creating more open-source tools for the community.

📊 GitHub Stats

https://github-readme-stats.vercel.app/api?username=umarbutt&show_icons=true&theme=radical

https://visitor-badge.laobi.icu/badge?page_id=umarbutt.projectzipper

🛡️ Security

If you discover any security-related issues, please email security@umarbutt.com instead of using the issue tracker.

🙏 Acknowledgments

· FastAPI team for the amazing web framework
· Pydantic for data validation
· Uvicorn for ASGI server implementation
· All contributors and users of this project

---

<div align="center">

⭐ Don't forget to star this repo if you find it useful! ⭐

Made with ❤️ by Umar Butt

https://img.shields.io/badge/GitHub-ProjectZipper-181717?style=for-the-badge&logo=github
https://img.shields.io/twitter/follow/umarbutt?style=social

</div>

📞 Connect With Me

<p align="center">
  <a href="https://buymeacoffee.com/umarbutt">
    <img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" height="50" alt="Buy Me A Coffee">
  </a>
  <a href="https://github.com/mohdumarbutt">
    <img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white" height="50">
  </a>
  <a href="https://www.linkedin.com/in/mohdumarbutt">
    <img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" height="50">
  </a>
  <a href="https://twitter.com/">
    <img src="https://img.shields.io/badge/Twitter-1DA1F2?style=for-the-badge&logo=twitter&logoColor=white" height="50">
  </a>
</p>

---