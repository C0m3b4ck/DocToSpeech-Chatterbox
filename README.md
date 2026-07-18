# DocToSpeech 
[![Ollama](https://img.shields.io/badge/Ollama-%23D97757.svg?style=for-the-badge&logo=ollama&logoColor=white)](https://ollama.com) [![Coqui TTS](https://img.shields.io/badge/Coqui%20TTS-%233EA8A8.svg?style=for-the-badge&logo=coqui&logoColor=white)](https://github.com/idiap/coqui-ai-TTS)[![Agentic](https://img.shields.io/badge/Agentic-AI-%23FF6B6B.svg?style=for-the-badge&logo=openai&logoColor=white)](agent.md)[![XTTS v2](https://img.shields.io/badge/XTTS%20v2-%233EA8A8.svg?style=flat-square&logo=coqui&logoColor=white)](https://github.com/idiap/coqui-ai-TTS)[![Bark](https://img.shields.io/badge/Bark-%23F9A825.svg?style=flat-square&logo=suno&logoColor=white)](https://github.com/suno-ai/bark)[![VITS](https://img.shields.io/badge/VITS-%237B1FA2.svg?style=flat-square&logo=pytorch&logoColor=white)](https://github.com/jaywalnut310/vits)[![YourTTS](https://img.shields.io/badge/YourTTS-%2300897B.svg?style=flat-square&logo=coqui&logoColor=white)](https://github.com/Edresson/YourTTS)[![StyleTTS 2](https://img.shields.io/badge/StyleTTS%202-%23E91E63.svg?style=flat-square&logo=style&logoColor=white)](https://github.com/yl4579/StyleTTS2)[![Chatterbox](https://img.shields.io/badge/Chatterbox-%23FF5722.svg?style=flat-square&logo=resemble&logoColor=white)](https://github.com/resemble-ai/chatterbox) [![Tortoise](https://img.shields.io/badge/Tortoise%20TTS-%23795548.svg?style=flat-square&logo=tortoise&logoColor=white)](https://github.com/neonbjb/tortoise-tts)[![OpenVoice](https://img.shields.io/badge/OpenVoice%20V2-%232196F3.svg?style=flat-square&logo=myshell&logoColor=white)](https://github.com/myshell-ai/OpenVoice) [![Sesame CSM](https://img.shields.io/badge/Sesame%20CSM--1B-%239C27B0.svg?style=flat-square&logo=speech&logoColor=white)](https://github.com/SesameAILabs/csm) 

Convert documents (EPUB, PDF, DOCX, HTML, TXT) to speech using local AI text-to-speech models. No API keys required — everything runs on your hardware.

## Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| Python | 3.10+ | 3.11 |
| RAM | 8 GB | 16 GB+ |
| GPU VRAM | 2 GB (VITS) | 6 GB+ (XTTS, Chatterbox) |
| GPU | Any CUDA-capable | NVIDIA RTX 3060+ |
| Disk | 5 GB | 20 GB+ (models are large) |
| OS | Linux, macOS, Windows | Linux (best CUDA support) |

**Note:** CPU-only mode works but is 5-10x slower than GPU. Some models (Tortoise, Sesame CSM) require a GPU. Use Python 3.11 for all venvs — Python 3.14 is not supported by torch 2.6.0 (required by Chatterbox).

### IMPORTANT COMPATIBILITY NOTE - READ BEFORE USE

**Poppler** is required for PDF text extraction on all platforms. If you plan to process PDF files, you must install Poppler separately — it is **not** included with pip dependencies.

| Platform | Install Command |
|----------|-----------------|
| **Linux (Debian/Ubuntu)** | `sudo apt install poppler-utils` |
| **Linux (Fedora/RHEL)** | `sudo dnf install poppler-utils` |
| **Linux (Arch)** | `sudo pacman -S poppler` |
| **macOS** | `brew install poppler` |
| **Windows** | Download from [poppler-windows releases](https://github.com/oschwartz10612/poppler-windows/releases), extract, and add the `Library/bin` folder to your system PATH |

After installing, verify with: `pdftotext -v`

Without Poppler, PDF documents will fail to load in the Gradio web UI and CLI.

## Features

- Convert EPUB, PDF, DOCX, HTML, TXT to audio
- Single file or batch directory processing
- 9 TTS engines with voice cloning support
- Gradio web UI for browser-based access
- Ollama-powered text sanitization for cleaner output
- Customizable agent prompts for text cleanup
- Pinokio 1-click launchers for each model
- PDF OCR for scanned documents (via Tesseract)

## Supported Document Formats

| Format | Status |
|--------|--------|
| EPUB | Supported (split by chapter or full text) |
| PDF | Supported (with optional password, OCR for scanned docs) |
| DOCX | Supported |
| HTML | Supported |
| TXT | Supported (passthrough) |
| DOC | Not yet implemented |
| DJVU | Not yet implemented |

## TTS Models

### Coqui TTS Models (same venv)

These models all come from `coqui-tts` and run in the same environment.

| Model | VRAM | GPU | CPU | Cloning | Languages | Install |
|-------|------|-----|-----|---------|-----------|---------|
| [![XTTS v2](https://img.shields.io/badge/XTTS%20v2-%233EA8A8.svg?style=flat-square&logo=coqui&logoColor=white)](https://github.com/idiap/coqui-ai-TTS) | ~4 GB | Recommended | Slow | Yes | 17 (en, es, fr, de, it, pt, pl, tr, ru, nl, cs, ar, zh, ja, hu, ko, bg) | [requirements-coqui.txt](requirements-coqui.txt) |
| [![Bark](https://img.shields.io/badge/Bark-%23F9A825.svg?style=flat-square&logo=suno&logoColor=white)](https://github.com/suno-ai/bark) | ~4-12 GB | Recommended | Very slow | No | Multi-lingual (en, de, es, fr, it, ja, ko, pl, pt, ru, zh, hi, ar, tr) | [requirements-coqui.txt](requirements-coqui.txt) |
| [![VITS](https://img.shields.io/badge/VITS-%237B1FA2.svg?style=flat-square&logo=pytorch&logoColor=white)](https://github.com/jaywalnut310/vits) | ~2-4 GB | Works on CPU | Yes | No | English (preset speakers) | [requirements-coqui.txt](requirements-coqui.txt) |
| [![YourTTS](https://img.shields.io/badge/YourTTS-%2300897B.svg?style=flat-square&logo=coqui&logoColor=white)](https://github.com/Edresson/YourTTS) | ~3-5 GB | Recommended | Possible | Yes | Multi-lingual (en, pt, fr, de, it, es, nl, pl, tr, ru, cs, ar, zh, ja, hu, ko) | [requirements-coqui.txt](requirements-coqui.txt) |

### Optional Models (add-on or separate venv)

| Model | VRAM | GPU | CPU | Cloning | Languages | Install | Venv |
|-------|------|-----|-----|---------|-----------|---------|------|
| [![StyleTTS 2](https://img.shields.io/badge/StyleTTS%202-%23E91E63.svg?style=flat-square&logo=style&logoColor=white)](https://github.com/yl4579/StyleTTS2) | ~4-8 GB | Recommended | Slow | Yes | English | [requirements-styletts2.txt](requirements-styletts2.txt) | Same as coqui |
| [![Chatterbox](https://img.shields.io/badge/Chatterbox-%23FF5722.svg?style=flat-square&logo=resemble&logoColor=white)](https://github.com/resemble-ai/chatterbox) | ~2-4 GB | Recommended | Possible | Yes | English (+ 23 via V3) | [requirements-chatterbox.txt](requirements-chatterbox.txt) | **Separate** |
| [![Tortoise](https://img.shields.io/badge/Tortoise%20TTS-%23795548.svg?style=flat-square&logo=tortoise&logoColor=white)](https://github.com/neonbjb/tortoise-tts) | ~4-6 GB | Required | No | Yes | English | [requirements-tortoise.txt](requirements-tortoise.txt) | **Separate** |
| [![OpenVoice](https://img.shields.io/badge/OpenVoice%20V2-%232196F3.svg?style=flat-square&logo=myshell&logoColor=white)](https://github.com/myshell-ai/OpenVoice) | ~4 GB | Recommended | Possible (3-4x slower) | Yes | Multi-lingual (via MeloTTS) | [requirements-openvoice.txt](requirements-openvoice.txt) | **Separate** |
| [![Sesame CSM](https://img.shields.io/badge/Sesame%20CSM--1B-%239C27B0.svg?style=flat-square&logo=speech&logoColor=white)](https://github.com/SesameAILabs/csm) | ~4.5 GB | CUDA required | 8.5 GB VRAM | Yes | English | [requirements-csm.txt](requirements-csm.txt) | **Separate** |

### Why Separate Venvs?

| Conflict | Models Affected | Reason |
|----------|----------------|--------|
| `torch` version | Chatterbox | Uses torch==2.6.0, coqui-tts may lag behind |
| `transformers` version | Tortoise | Needs `==4.31`, coqui-tts needs `>=4.43` |
| `transformers` version | Sesame CSM | Needs `>=4.45`, may conflict with coqui 0.25.x |
| Python version | All | Use Python 3.11 — torch 2.6.0 has no wheels for Python 3.14 |

## Installation

### Base install (4 Coqui models)

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements-coqui.txt
```

### Add StyleTTS 2 (same venv)

```bash
pip install -r requirements-styletts2.txt
```

### Chatterbox (separate venv)

```bash
python3.11 -m venv venv-chatterbox
source venv-chatterbox/bin/activate

# Must be done in order — torch first, then chatterbox with --no-deps:
pip install torch==2.6.0 torchaudio==2.6.0
pip install chatterbox-tts --no-deps
pip install numpy librosa s3tokenizer transformers==5.2.0 diffusers==0.29.0
pip install resemble-perth conformer==0.3.2 safetensors==0.5.3
pip install spacy-pkuseg pykakasi==2.3.0 pyloudnorm omegaconf
pip install epub2txt docx2txt pdftotext html2text pyfiglet tqdm rich ollama
```

### Tortoise (separate venv)

```bash
python3.11 -m venv .venv-tortoise
source .venv-tortoise/bin/activate
pip install -r requirements-tortoise.txt
```

### Sesame CSM (separate venv)

```bash
python3.11 -m venv .venv-csm
source .venv-csm/bin/activate
pip install -r requirements-csm.txt
huggingface-cli login
```

### OpenVoice (separate venv)

```bash
python3.11 -m venv .venv-openvoice
source .venv-openvoice/bin/activate
pip install -r requirements-openvoice.txt
git clone https://github.com/myshell-ai/OpenVoice.git
cd OpenVoice && pip install -e . && cd ..
pip install git+https://github.com/myshell-ai/MeloTTS.git
python -c "from huggingface_hub import snapshot_download; snapshot_download(repo_id='myshell-ai/OpenVoiceV2', local_dir='checkpoints_v2')"
python -m unidic download
```

## Usage

### CLI

```bash
python doctospeech.py
```

1. Choose single file or directory mode
2. Provide document path(s)
3. (Optional) Sanitize text with Ollama
4. Select TTS model
5. Configure voice (cloning or preset)
6. Audio files are generated as `.wav`

### Gradio Web UI

```bash
python app.py
```

Opens a browser-based interface at `http://localhost:7860`:

- Upload documents (PDF, EPUB, DOCX, HTML, TXT) or paste text
- Select TTS model from dropdown (unavailable models are greyed out with install instructions)
- Configure voice type (cloning or preset), language, output filename
- Optional Ollama text sanitization
- Generate and play/download audio directly in the browser

The web UI automatically detects which models are installed and warns about models that need a separate venv.

### Pinokio (1-Click Launch)

Pinokio launchers are provided for each model group. Copy the desired launcher folder to your Pinokio `api/` directory:

| Launcher | Models | Venv |
|----------|--------|------|
| `pinokio/` | XTTS v2, Bark, VITS, YourTTS, StyleTTS 2 | Shared coqui venv |
| `pinokio-chatterbox/` | Chatterbox | Separate |
| `pinokio-tortoise/` | Tortoise TTS | Separate |
| `pinokio-openvoice/` | OpenVoice V2 | Separate |
| `pinokio-csm/` | Sesame CSM-1B | Separate |

```bash
# Example: install the Coqui launcher
cp -r pinokio ~/.pinokio/api/DocToSpeech
```

## Optional: Ollama Text Sanitization

Before TTS, you can clean extracted text using a local Ollama model:

1. Install and run [Ollama](https://ollama.com)
2. Pull a model: `ollama pull llama3.1`
3. The script will prompt you to sanitize — it fixes OCR errors, removes artifacts, normalizes whitespace
4. You can provide a custom `agent.md` prompt for domain-specific cleanup

## Project Structure

```
DocToSpeech/
  doctospeech.py              # Main CLI script
  app.py                      # Gradio web UI
  agent.md                    # Ollama sanitization prompt (editable)
  template.py                 # Standalone Ollama sanitizer
  requirements-coqui.txt      # Base install (4 coqui models + gradio)
  requirements-styletts2.txt  # Add-on for same venv
  requirements-chatterbox.txt # Separate venv
  requirements-tortoise.txt   # Separate venv
  requirements-csm.txt        # Separate venv
  requirements-openvoice.txt  # Separate venv
  requirements-gradio.txt     # Gradio-only install
  pinokio/                    # Pinokio launcher (Coqui + StyleTTS2)
  pinokio-chatterbox/         # Pinokio launcher (Chatterbox)
  pinokio-tortoise/           # Pinokio launcher (Tortoise)
  pinokio-openvoice/          # Pinokio launcher (OpenVoice)
  pinokio-csm/                # Pinokio launcher (CSM)
```
## Known bugs
* "Failed to load Resemble Chatterbox: 'NoneType' object is not callable" error when TTS generation is initiated for Chatterbox
 

## Credits

Started on July 12th, 2026 by C0m3b4ck.

### TTS Engines
- [Coqui TTS](https://github.com/idiap/coqui-ai-TTS) (XTTS v2, Bark, VITS, YourTTS) — [CPML License](https://coqui.ai/cpml)
- [Chatterbox](https://github.com/resemble-ai/chatterbox) by Resemble AI — [MIT License](https://github.com/resemble-ai/chatterbox/blob/main/LICENSE)
- [Tortoise TTS](https://github.com/neonbjb/tortoise-tts) by James Betker — [Apache 2.0 License](https://github.com/neonbjb/tortoise-tts/blob/main/LICENSE)
- [StyleTTS 2](https://github.com/yl4579/StyleTTS2) by Yuanhao Yi — [MIT License](https://github.com/yl4579/StyleTTS2/blob/main/LICENSE)
- [OpenVoice](https://github.com/myshell-ai/OpenVoice) by MyShell AI — [MIT License](https://github.com/myshell-ai/OpenVoice/blob/main/MIT_LICENSE)
- [Sesame CSM](https://github.com/SesameAILabs/csm) by Sesame AI — [Apache 2.0 License](https://github.com/SesameAILabs/csm/blob/main/LICENSE)

### Document Processing
- [epub2txt](https://github.com/aaronsw/html2text)
- [pdftotext](https://github.com/jalan/pdftotext)
- [docx2txt](https://github.com/ankushshah893/docx2txt)
- [html2text](https://github.com/Alir3z4/html2text)

### Other
- [pyfiglet](https://github.com/pwaller/pyfiglet) — ASCII art
- [tqdm](https://github.com/tqdm/tqdm) — Progress bars
- [Ollama](https://ollama.com) — Local LLM for text sanitization

MPL 2.0 License.
