# ✨ Auto-PPT Agent

You can watch the working demonstration of the Auto-PPT Agent here:

🔗 Google Drive Link:
https://drive.google.com/drive/folders/1pVm5kZgnj4XGQUj9HY12cTHakvQHEdAo?usp=drive_link

📌 What the Demo Shows
End-to-end workflow of the Auto-PPT Agent
Multi-MCP server usage (Web Search, PPT Generator, Filesystem, Image Generator)
Automatic slide creation from a single prompt
Generated PowerPoint output

An autonomous AI agent that **researches any topic and generates beautiful PowerPoint presentations** — complete with themed layouts, images, and structured content — all from a single text prompt.

Built with **LangChain**, **Mistral AI**, **MCP (Model Context Protocol)**, **python-pptx**, and **Streamlit**.

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-Frontend-FF4B4B?logo=streamlit&logoColor=white)
![Mistral](https://img.shields.io/badge/Mistral_AI-LLM-orange)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 🎯 What It Does

1. You enter a **topic** (e.g. _"Artificial Intelligence"_)
2. You pick a **visual template** and **number of slides**
3. The AI agent:
   - 🔍 **Researches** the topic using Wikipedia
   - 📝 **Generates** structured slide content with bullet points
   - 🖼️ **Fetches** relevant images from Unsplash
   - 🎨 **Applies** your chosen color theme and layout
   - 💾 **Saves** a real `.pptx` file to disk
4. You **download** the finished presentation from the browser

> **No copy-pasting. No manual formatting. One click → professional slides.**

---

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- A [Mistral AI API key](https://console.mistral.ai/)

### Installation

```bash
# Clone the repository
git clone https://github.com/your-username/ppt_antigravity.git
cd ppt_antigravity

# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Configuration

Create a `.env` file in the project root:

```env
MISTRAL_API_KEY=your_mistral_api_key_here
```

### Run

```bash
streamlit run app.py
```

The app opens at **http://localhost:8501**. Enter your topic, pick a template, set slide count, and click **🚀 Generate Presentation**.

---

## 🖼️ Screenshots

### Streamlit Dashboard
- Modern sidebar with **template selector** and **slide count slider**
- Live **theme preview** card showing colors before you generate
- One-click **Download** button after generation

### Generated Slides
- **Title slide** with accent band and centered heading
- **Content slides** with proper margins, bullet spacing, and left accent stripe
- **Image slides** with 55/45 two-column layout (text + photo)

---

## 🎨 Available Templates

| Template | Style | Best For |
|----------|-------|----------|
| `modern_minimal` | Light grey, indigo accents | Clean modern decks |
| `dark_tech` | Dark navy, neon teal/purple | Tech & developer talks |
| `startup_pitch` | White + vibrant orange-red | Pitch decks & demos |
| `education_visual` | Warm cream, soft green | Students & classrooms |
| `corporate_professional` | White + deep blue | Business & formal presentations |
| `academic_clean` | Pure white, muted navy | Research & academic talks |

Each template defines: background color, title bar color, title text color, content text color, accent color, title font, and body font.

---

## 📂 Project Structure

```
ppt_antigravity/
├── app.py                      # Streamlit frontend (dashboard UI)
├── agent_ppt.py                # AI agent — native tool-calling loop
├── requirements.txt            # Python dependencies
├── .env                        # API keys (not committed)
├── template.pptx               # Optional base PowerPoint template
├── output.pptx                 # Generated presentation (after running)
│
├── servers/                    # MCP tool servers
│   ├── ppt_mcp_server.py      # PowerPoint generation (slides, themes, images)
│   ├── search_mcp_server.py   # Wikipedia research tool
│   ├── filesystem_mcp_server.py # File system operations
│   ├── image_mcp_server.py    # Image generation/placeholder tool
│   └── templates.py           # Theme/template configuration
│
├── utils/                      # Utility scripts
│   └── create_theme.py        # Script to generate template.pptx
│
├── output/                     # Output artifacts
│   └── img_cache/             # Downloaded slide images (auto-created)
│
└── docs/                       # Documentation
```

---

## ⚙️ Architecture

```
┌──────────────────────────────────────────────────────┐
│                   Streamlit UI (app.py)               │
│  ┌─────────────┐  ┌──────────┐  ┌────────────────┐  │
│  │ Topic Input  │  │ Template │  │  Slide Slider  │  │
│  └──────┬──────┘  └────┬─────┘  └───────┬────────┘  │
└─────────┼──────────────┼────────────────┼────────────┘
          │              │                │
          ▼              ▼                ▼
┌──────────────────────────────────────────────────────┐
│              Agent Loop (agent_ppt.py)                │
│                                                      │
│  Mistral LLM  ←→  Native Tool Calling  ←→  MCP      │
│                                                      │
│  Workflow:                                           │
│  1. search_wikipedia → gather facts                  │
│  2. initialize_presentation → set theme & title      │
│  3. write_slide (×N) → add content + images          │
│  4. save_ppt → physically write .pptx to disk        │
└──────────────────┬───────────────────────────────────┘
                   │
    ┌──────────────┼──────────────────┐
    ▼              ▼                  ▼
┌────────┐  ┌───────────┐  ┌──────────────┐
│ Search │  │    PPT     │  │  Filesystem  │
│ Server │  │  Server    │  │   Server     │
│        │  │            │  │              │
│Wikipedia│ │python-pptx │  │  File I/O    │
│  API   │  │ + Unsplash │  │              │
└────────┘  └───────────┘  └──────────────┘
```

### How It Works

1. **Streamlit** collects the user's topic, template choice, and slide count.
2. **`agent_ppt.py`** spins up MCP server connections and invokes Mistral with **native function/tool calling** (not ReAct text parsing).
3. The LLM decides which tools to call, in what order.
4. **`ppt_mcp_server.py`** maintains a global `Presentation()` object in memory. Each `write_slide` call adds a properly formatted slide. `save_ppt` writes the final `.pptx` to disk with `os.path.exists()` verification.
5. **`app.py`** checks for the output file and presents a download button.

---

## 🛠️ Key Technologies

| Technology | Role |
|-----------|------|
| [Mistral AI](https://mistral.ai/) | LLM with native tool/function calling |
| [LangChain](https://www.langchain.com/) | Message formatting & LLM integration |
| [MCP](https://modelcontextprotocol.io/) | Tool server protocol (stdio transport) |
| [python-pptx](https://python-pptx.readthedocs.io/) | PowerPoint file generation |
| [Streamlit](https://streamlit.io/) | Web UI dashboard |
| [Unsplash](https://unsplash.com/) | Royalty-free slide images |
| [Wikipedia API](https://pypi.org/project/wikipedia/) | Topic research |

---

## 🔧 CLI Usage

You can also run the agent directly from the command line:

```bash
# Default (5 slides, corporate theme)
python agent_ppt.py "Create a presentation on Machine Learning"

# Custom template and slide count
python agent_ppt.py "Quantum Computing" --template dark_tech --slides 7
```

**Available CLI flags:**

| Flag | Default | Description |
|------|---------|-------------|
| `--template` | `corporate_professional` | Theme name |
| `--slides` | `5` | Number of content slides (3–10) |

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| `MISTRAL_API_KEY is not set` | Add your key to `.env` |
| `ReadTimeout` during generation | The 180s timeout should handle most cases. For very large slide counts, try reducing to 5 slides. |
| `Agent finished but no .pptx found` | Check terminal logs for `[DEBUG]` messages. The agent must call `save_ppt` — the strict prompt enforces this. |
| Images not appearing on slides | Unsplash Source API may be rate-limited. The slide will still generate without the image. |
| `ImportError` for langchain | Run `pip install --upgrade langchain langchain-mistralai` |

---

## 📝 Adding Custom Templates

Edit `servers/templates.py` and add a new entry to the `TEMPLATES` dictionary:

```python
"my_custom_theme": {
    "display_name": "My Custom Theme",
    "bg_color": (240, 240, 255),        # Light lavender
    "title_bg": (60, 20, 120),          # Deep purple
    "title_color": (255, 255, 255),     # White
    "content_color": (40, 40, 40),      # Dark grey
    "accent_color": (180, 100, 255),    # Violet
    "font_title": "Georgia",
    "font_body": "Verdana",
    "layout": "light",
},
```

The new template will automatically appear in the Streamlit sidebar dropdown.

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

## 🙏 Acknowledgements

- [Mistral AI](https://mistral.ai/) for the powerful LLM
- [Anthropic's MCP](https://modelcontextprotocol.io/) for the tool protocol standard
- [Unsplash](https://unsplash.com/) for beautiful royalty-free images
- [python-pptx](https://python-pptx.readthedocs.io/) for PowerPoint generation

---

<p align="center">
  Made with ❤️ by <strong>Somasundaram</strong>
</p>
