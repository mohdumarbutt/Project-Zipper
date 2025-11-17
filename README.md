# ProjectZipper 🗂️⚡

A **FastAPI-based service** that converts plain text-based file tree structures into instantly downloadable ZIP archives. It is perfect for quickly generating project skeletons, boilerplate code, or template file structures.

\<div align="center"\>

[](https://fastapi.tiangolo.com/)
[](https://www.python.org/)
[](https://en.wikipedia.org/wiki/Zip_\(file_format\))

\</div\>

-----

## ✨ Features

  * **🚀 Lightning Fast** - Built with FastAPI for high-performance ZIP generation.
  * **📁 Smart Parsing** - Understands and correctly interprets various textual file tree formats.
  * **🎯 Auto Content** - Generates appropriate placeholder content based on recognized file extensions (e.g., Python comments, JavaScript console logs).
  * **💾 Streaming Response** - Uses efficient memory usage by streaming the ZIP file for large archives.
  * **🔧 Fully Typed** - Leverages Python type hints throughout for better code quality and developer experience.
  * **🐳 Docker Ready** - Easy and consistent deployment using containerization.

-----

## 🎮 Quick Start

### Installation

Clone the repository and install the dependencies:

```bash
# Clone the repository
git clone https://github.com/umarbutt/projectzipper.git
cd projectzipper

# Install dependencies
pip install -r requirements.txt
```

### Usage

You can use the service by sending a `POST` request with the file structure text.

```python
import requests

# Example file structure input
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

# Save the downloaded ZIP file
if response.status_code == 200:
    with open("my_project.zip", "wb") as f:
        f.write(response.content)
    print("Successfully generated my_project.zip")
else:
    print(f"Error: {response.status_code}, {response.text}")
```

-----

## 🛠️ API Reference

### `POST /generate-zip`

Generates a ZIP file from the provided file tree structure.

| Field | Type | Description |
| :--- | :--- | :--- |
| `tree_structure` | `string` | The text representation of the file directory tree. |
| `root_dir_name` | `string` | The name of the top-level directory inside the generated ZIP file. |

**Request Body Example:**

```json
{
  "tree_structure": "string",
  "root_dir_name": "string"
}
```

**Response:** ZIP file stream (`application/zip`)

-----

## 📦 Supported File Types

| File Type | Generated Content |
| :--- | :--- |
| **`.py`** | Python placeholder with comments (`# Your code here...`) |
| **`.js`** | JavaScript placeholder with a console log (`console.log('// File:');`) |
| **`.json`** | Basic JSON structure (`{}`) |
| **`.txt`** | Simple text placeholder (`This is a placeholder file.`) |
| **Others** | Basic file identifier |

-----

## 🚀 Deployment

### Local Development

Run the FastAPI application directly:

```bash
python main.py
```

### Using Docker

For containerized deployment:

```bash
docker build -t projectzipper .
docker run -p 8000:8000 projectzipper
```

### Production with Uvicorn

Use Uvicorn with multiple worker processes for optimal performance:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

-----

## 🏗️ Project Structure

```
projectzipper/
├── main.py              # Core FastAPI application
├── requirements.txt     # Python dependencies
├── Dockerfile           # Docker container configuration
└── examples/            # Usage examples
    ├── basic_usage.py
    └── advanced_usage.py
```

-----

## 🤝 Contributing

We welcome your input\! We aim to make contributing to ProjectZipper as easy and transparent as possible.

### Development Setup

1.  Fork the repository.
2.  Create your feature branch: `git checkout -b feature/amazing-feature`
3.  Commit your changes: `git commit -m 'feat: Add amazing feature'`
4.  Push to the branch: `git push origin feature/amazing-feature`
5.  Open a **Pull Request**.

### Reporting Issues

Please use the [GitHub issue tracker](https://www.google.com/search?q=https://github.com/umarbutt/projectzipper/issues) to report any bugs or suggest new features.

-----

## 📄 License

This project is licensed under the **MIT License** - see the `LICENSE` file for details.

-----

## 👨‍💻 Author

**Mohd Umar Butt (Umar Butt)**

| Link | Handle |
|:---:|:---:|
| 💻 [GitHub](https://github.com/mohdumarbutt) | 🔗 [LinkedIn](https://www.linkedin.com/in/mohdumarbutt) |
| 🐦 [Twitter](https://www.google.com/search?q=https://twitter.com/umarbutt) | 💼 [Portfolio / Blog](https://umarbutt.com) |

-----

## 🌟 Support

If you find this project helpful, please consider supporting its development:

[](https://buymeacoffee.com/umarbutt)

Your support helps me continue maintaining and improving this project and creating more open-source tools for the community.

-----

## 📊 Project Metrics

\<div align="center"\>

| GitHub Stats | Visitor Count |
| :---: | :---: |
| [](https://www.google.com/search?q=https://github.com/umarbutt) |  |

\</div\>

-----

## 🛡️ Security

If you discover any security-related issues, please email **security@umarbutt.com** instead of using the public issue tracker.

-----

## 🙏 Acknowledgments

  * The **FastAPI** team for the amazing web framework.
  * **Pydantic** for robust data validation.
  * **Uvicorn** for the high-performance ASGI server implementation.
  * All contributors and users of this project\!

-----

\<div align="center"\>

## ⭐ Don't forget to star this repo if you find it useful\! ⭐

Made with ❤️ by Umar Butt

<br>

| Follow Me | Project Badge |
| :---: | :---: |
| [](https://www.google.com/search?q=https://twitter.com/umarbutt) | [](https://www.google.com/search?q=https://github.com/umarbutt/projectzipper) |

\</div\>