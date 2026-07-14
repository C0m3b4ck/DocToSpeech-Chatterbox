# DocToSpeech (Chatterbox)
https://github.com/C0m3b4ck/DocToSpeech-Chatterbox/blob/main/icon.png
[![MPL 2.0](https://img.shields.io/badge/License-MPL%202.0-brightgreen.svg)](LICENSE)
[![Pinokio](https://img.shields.io/badge/Platform-Pinokio-FF6B35.svg?style=for-the-badge&logo=pinokio&logoColor=white)](https://pinokio.computer)

One-click Pinokio launcher for DocToSpeech with Resemble Chatterbox TTS.

## Included Model

| Model | VRAM | Cloning | Languages | Presets |
|-------|------|---------|-----------|---------|
| Chatterbox | ~2-4 GB | Yes | English (+23 via Multilingual V3) | No |

350M parameter model with paralinguistic tags and voice cloning.

## Requirements

- Python 3.11
- 8 GB RAM minimum, 16 GB+ recommended
- 2-4 GB GPU VRAM
- Pinokio

## Install

1. Open Pinokio
2. Click **Discover**
3. Search for **DocToSpeech (Chatterbox)**
4. Click **Download** then **Install**

Or manually copy this folder to your Pinokio `api/` directory.

## Usage

After installation, Pinokio will show a **Start** button. Click it to launch the Gradio web UI at `http://localhost:7860`.

## Other Versions

| Launcher | Models | Venv |
|----------|--------|------|
| [DocToSpeech (Coqui)](https://github.com/C0m3b4ck/DocToSpeech-coqui) | XTTS v2, Bark, VITS, YourTTS, StyleTTS 2 | Shared |
| **DocToSpeech (Chatterbox)** (this one) | Resemble Chatterbox | Separate |
| [DocToSpeech (Tortoise)](https://github.com/C0m3b4ck/DocToSpeech-Tortoise) | Tortoise TTS | Separate |
| [DocToSpeech (OpenVoice)](https://github.com/C0m3b4ck/DocToSpeech-OpenVoice) | OpenVoice V2 | Separate |
| [DocToSpeech (CSM)](https://github.com/C0m3b4ck/DocToSpeech-CSM) | Sesame CSM-1B | Separate |

## Full Documentation

For CLI usage, batch processing, Ollama sanitization, and more, see the [main DocToSpeech repository](https://github.com/C0m3b4ck/DocToSpeech).

## Credits

Started on July 12th, 2026 by [C0m3b4ck](https://github.com/C0m3b4ck).

### TTS Engine
- [Chatterbox](https://github.com/resemble-ai/chatterbox) by Resemble AI -- [MIT License](https://github.com/resemble-ai/chatterbox/blob/main/LICENSE)

### Document Processing
- [epub2txt](https://github.com/aaronsw/html2text)
- [pdftotext](https://github.com/jalan/pdftotext)
- [docx2txt](https://github.com/ankushshah893/docx2txt)
- [html2text](https://github.com/Alir3z4/html2text)

### Other
- [pyfiglet](https://github.com/pwaller/pyfiglet) -- ASCII art
- [tqdm](https://github.com/tqdm/tqdm) -- Progress bars
- [Ollama](https://ollama.com) -- Local LLM for text sanitization

MPL 2.0 License.
