import os
import pathlib
import sys

from tqdm import tqdm
import time
from datetime import datetime

import pyfiglet
import torch
from TTS.api import TTS

from epub2txt import epub2txt
import pdftotext
import docx2txt
import html2text


# ========================= TERMINAL COLORS =========================

class C:
    RESET   = "\033[0m"
    BOLD    = "\033[1m"
    DIM     = "\033[2m"
    RED     = "\033[91m"
    GREEN   = "\033[92m"
    YELLOW  = "\033[93m"
    CYAN    = "\033[96m"
    MAGENTA = "\033[95m"

def prompt(msg):
    return input(f"{C.CYAN}? {C.RESET}{msg}")

def info(msg):
    print(f"{C.DIM}[*] {msg}{C.RESET}")

def success(msg):
    print(f"{C.GREEN}[+] {msg}{C.RESET}")

def warn(msg):
    print(f"{C.YELLOW}[!] {msg}{C.RESET}")

def error(msg):
    print(f"{C.RED}[!] {msg}{C.RESET}")

def header(msg):
    print(f"\n{C.CYAN}{C.BOLD}--- {msg} ---{C.RESET}")

def divider():
    print(f"{C.DIM}{'-' * 50}{C.RESET}")


# ========================= PATH SAFETY =========================

def safe_resolve(path):
    """Resolve path and reject traversal outside current directory."""
    resolved = os.path.realpath(path)
    if ".." in path.split(os.sep):
        warn(f"Path contains traversal components: {path}")
    return resolved

def validate_path_exists(path, label="path"):
    """Check that a file or directory exists, return resolved path."""
    if not os.path.exists(path):
        error(f"{label} does not exist: {path}")
        return None
    return os.path.realpath(path)


# ========================= USER INTERACTION =========================

def greet():
    ascii_art = pyfiglet.figlet_format("DocToSpeech", font="alphabet")
    print(f"{C.CYAN}{ascii_art}{C.RESET}")
    time.sleep(1)
    credit = pyfiglet.figlet_format("By C0m3b4ck under MPL 2.0")
    print(f"{C.DIM}{credit}{C.RESET}")

def goodbye():
    ascii_art = pyfiglet.figlet_format("Goodbye!", font="alphabet")
    print(f"{C.CYAN}{ascii_art}{C.RESET}")
    time.sleep(1)
    credit = pyfiglet.figlet_format("By C0m3b4ck under MPL 2.0")
    print(f"{C.DIM}{credit}{C.RESET}")


def get_user_input_volume():
    while True:
        choice = prompt("Use single file or directory? (s/d): ").lower().strip()
        if choice == "s":
            get_user_input_docs()
        elif choice == "d":
            get_user_input_dir()
        else:
            warn("Please input 's' or 'd'")
            continue

        again = prompt("Process another document? (y/n): ").lower().strip()
        if again != "y":
            break


def get_user_input_dir():
    header("Directory Mode")

    output_dir = prompt("Output directory: ")
    output_dir = validate_path_exists(output_dir, "Output directory")
    if output_dir is None:
        return

    doc_dir = prompt("Document directory: ")
    doc_dir = validate_path_exists(doc_dir, "Document directory")
    if doc_dir is None:
        return

    while True:
        try:
            number = int(prompt("Number of extensions to convert (0 = all supported): "))
            if number < 0:
                warn("Please input a non-negative number")
                continue
            break
        except ValueError:
            warn("Please input a number")

    default_extentions = [".txt", ".pdf", ".html", ".docx", ".epub"]
    extention_list = []
    if number > 0:
        for x in range(1, number + 1):
            ext = prompt(f"Extension {x}/{number} (e.g. '.pdf'): ").lower().strip()
            if not ext.startswith("."):
                ext = "." + ext
            extention_list.append(ext)
    else:
        info("Using default extension list")
        extention_list = default_extentions

    header("Scanning files")
    file_list = [
        f for f in os.listdir(doc_dir)
        if os.path.isfile(os.path.join(doc_dir, f))
        and f.endswith(tuple(extention_list))
    ]

    if not file_list:
        warn("No matching files found in directory")
        return

    info(f"Found {C.BOLD}{len(file_list)}{C.RESET}{C.DIM} file(s){C.RESET}")
    for f in file_list:
        print(f"  {C.DIM}>{C.RESET} {f}")
    divider()

    epub_chapter_choice = ""
    if any(f.endswith(".epub") for f in file_list):
        while epub_chapter_choice not in ("y", "n"):
            epub_chapter_choice = prompt("Split epub files into separate chapters? (y/n): ").lower()

    header("Converting to .txt")
    txtfile_list = []
    for filename in tqdm(file_list, desc="Converting", bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}]"):
        full_path = os.path.join(doc_dir, filename)
        file_ext = pathlib.Path(filename).suffix.lower()
        try:
            if file_ext == ".epub":
                txt_paths = epub_to_text(full_path, epub_chapter_choice)
                txtfile_list.extend(txt_paths)
            elif file_ext == ".pdf":
                txt_path = pdf_to_text(full_path)
                txtfile_list.append(txt_path)
            elif file_ext == ".docx":
                txt_path = docx_to_text(full_path)
                txtfile_list.append(txt_path)
            elif file_ext == ".doc":
                warn(f".doc not implemented yet: {filename}")
            elif file_ext in (".html", ".htm"):
                txt_path = html_to_text(full_path)
                txtfile_list.append(txt_path)
            elif file_ext == ".djvu":
                warn(f".djvu not implemented yet: {filename}")
        except Exception as e:
            error(f"Failed to convert {filename}: {e}")

    if not txtfile_list:
        warn("No files were successfully converted")
        return

    success(f"Converted {C.BOLD}{len(txtfile_list)}{C.RESET}{C.GREEN} file(s){C.RESET}")
    divider()

    header("TTS Options")
    language = prompt("Language code (e.g. 'en'): ")

    choice = ""
    cloning_path = ""
    use_cloning = False
    preset_speaker = ""
    while choice not in ("c", "p"):
        choice = prompt("Voice type: cloning (c) or preset (p)? ").lower()
        if choice == "c":
            cloning_path = prompt("Path to .wav clone voice: ")
            use_cloning = True
        elif choice == "p":
            preset_speaker = prompt("Preset speaker name: ")
            use_cloning = False
        else:
            warn("Please input 'c' or 'p'")

    tts = make_tts_init(show_speakers=(choice == "p"))

    header("Generating audio")
    info(f"Processing {C.BOLD}{len(txtfile_list)}{C.RESET}{C.DIM} file(s)...{C.RESET}")
    for txt_path in txtfile_list:
        with open(txt_path, "r") as file:
            text_to_say = file.read()
        output_filename = os.path.basename(txt_path).rsplit('.', 1)[0] + ".wav"
        output_path = os.path.join(output_dir, output_filename)
        make_tts_voiceover(text_to_say, use_cloning, preset_speaker, cloning_path, language, tts, output_path)

    success("All files processed!")


def get_user_input_docs():
    while True:
        header("Single File Mode")
        info("Supported formats: PDF, EPUB, DOCX, DOC, HTML, DJVU, TXT")

        doc_path = prompt("Document path: ")
        doc_path = validate_path_exists(doc_path, "Document")
        if doc_path is None:
            continue

        file_ext = pathlib.Path(doc_path).suffix.lower()
        info(f"Extension: {C.BOLD}{file_ext}{C.RESET}")

        try:
            if file_ext == ".epub":
                txt_paths = epub_to_text(doc_path)
                for txt_path in txt_paths:
                    get_user_input_tts(txt_path)
            elif file_ext == ".pdf":
                txt_path = pdf_to_text(doc_path)
                get_user_input_tts(txt_path)
            elif file_ext == ".docx":
                txt_path = docx_to_text(doc_path)
                get_user_input_tts(txt_path)
            elif file_ext == ".doc":
                warn("Not implemented yet (requires .doc to .docx conversion)")
                continue
            elif file_ext in (".html", ".htm"):
                txt_path = html_to_text(doc_path)
                get_user_input_tts(txt_path)
            elif file_ext == ".djvu":
                warn("Not implemented yet")
                continue
            elif file_ext == ".txt":
                info("File is already plain text, proceeding to TTS...")
                get_user_input_tts(doc_path)
            else:
                warn(f"Unrecognized extension: {file_ext}")
                choice = prompt("Treat as plain text? (y/n): ").lower()
                if choice == "y":
                    info("Treating as plain text, proceeding to TTS...")
                    get_user_input_tts(doc_path)
                else:
                    info("Returning to file selection")
                    continue
        except Exception as e:
            error(f"Something went wrong: {e}")
            retry = prompt("Try again? (y/n): ").lower()
            if retry != "y":
                break
            continue

        break


def get_user_input_tts(txt_path):
    header("TTS Configuration")

    output_file_name = prompt("Output filename (without .wav): ").strip()

    choice_timestamp = ""
    while choice_timestamp not in ("y", "n"):
        choice_timestamp = prompt("Add timestamp to filename? (y/n): ").lower()

    if choice_timestamp == "y":
        ts = datetime.now().timestamp()
        output_path = f"{output_file_name}_{ts}.wav"
        info(f"Output: {C.BOLD}{output_path}{C.RESET}")
    else:
        output_path = output_file_name + ".wav"
        info(f"Output: {C.BOLD}{output_path}{C.RESET}")

    language = prompt("Language code (e.g. 'en'): ")

    choice = ""
    cloning_path = ""
    use_cloning = False
    preset_speaker = ""
    tts = None
    while choice not in ("c", "p"):
        choice = prompt("Voice type: cloning (c) or preset (p)? ").lower()
        if choice == "c":
            cloning_path = prompt("Path to .wav clone voice: ")
            use_cloning = True
        elif choice == "p":
            tts = make_tts_init(show_speakers=True)
            preset_speaker = prompt("Preset speaker name: ")
            use_cloning = False
        else:
            warn("Please input 'c' or 'p'")

    with open(txt_path, "r") as file:
        file_contents = file.read()

    preview = file_contents[:200] + ("..." if len(file_contents) > 200 else "")
    info(f"Text preview: {C.DIM}{preview}{C.RESET}")

    make_tts_voiceover(file_contents, use_cloning, preset_speaker, cloning_path, language, tts, output_path)


# ========================= DOC -> TXT =========================

def epub_to_text(doc_path, chapter_choice=None):
    if chapter_choice not in ("y", "n"):
        while True:
            chapter_choice = prompt("Split epub into separate chapters? (y/n): ").lower()
            if chapter_choice in ("y", "n"):
                break

    try:
        chapter_list = epub2txt(doc_path, outputlist=True)
    except Exception as e:
        error(f"Failed to read epub: {e}")
        raise

    info(f"Read {C.BOLD}{len(chapter_list)}{C.RESET}{C.DIM} chapter(s){C.RESET}")

    base_name = doc_path.rsplit('.', 1)[0]
    txt_files = []

    if chapter_choice == "y":
        for i, chapter in enumerate(chapter_list):
            chapter_file = f"{base_name}_chapter_{i + 1}.txt"
            with open(chapter_file, "w") as f:
                f.write(chapter)
            txt_files.append(chapter_file)
        del chapter_list
        success(f"Saved {len(txt_files)} chapter files")
    else:
        full_txt = "\n\n".join(chapter_list)
        del chapter_list
        txt_file = doc_path + ".txt"
        with open(txt_file, "w") as f:
            f.write(full_txt)
        del full_txt
        txt_files.append(txt_file)
        success(f"Saved: {txt_file}")

    return txt_files


def pdf_to_text(doc_path):
    choice = ""
    password = None
    pdf = None

    while choice not in ("y", "n"):
        choice = prompt("Is this PDF password-protected? (y/n): ").lower()

    try:
        with open(doc_path, "rb") as f:
            if choice == "y":
                password = prompt("Enter PDF password: ")
                pdf = pdftotext.PDF(f, password)
            else:
                pdf = pdftotext.PDF(f)
    except Exception as e:
        error(f"Failed to open PDF: {e}")
        raise
    finally:
        password = None

    info(f"PDF has {C.BOLD}{len(pdf)}{C.RESET}{C.DIM} page(s){C.RESET}")

    show = ""
    while show not in ("y", "n"):
        show = prompt("Show all pages? (y/n): ").lower()
    if show == "y":
        for page in pdf:
            print(page)

    txt_file = doc_path + ".txt"
    try:
        with open(txt_file, "w") as save_text:
            for i, page in enumerate(pdf):
                if i > 0:
                    save_text.write("\n\n")
                save_text.write(page)
        del pdf
    except Exception as e:
        error(f"Failed to save txt: {e}")
        raise

    success(f"Saved: {txt_file}")
    return txt_file


def docx_to_text(doc_path):
    txt_string = docx2txt.process(doc_path)
    txt_file = doc_path + ".txt"

    try:
        with open(txt_file, "w") as save_text:
            save_text.write(txt_string)
        del txt_string
    except Exception as e:
        error(f"Failed to save txt: {e}")
        raise

    success(f"Saved: {txt_file}")
    return txt_file


def doc_to_text(doc_path):
    warn("Not implemented yet -- requires .doc to .docx conversion")


def html_to_text(doc_path):
    try:
        with open(doc_path, 'r') as file:
            html_contents = file.read()
    except Exception as e:
        error(f"Failed to read HTML: {e}")
        raise

    try:
        h = html2text.HTML2Text()
        h.ignore_links = True
        txt_string = h.handle(html_contents)
        del html_contents
    except Exception as e:
        error(f"Failed to convert HTML: {e}")
        raise

    txt_file = doc_path + ".txt"
    try:
        with open(txt_file, "w") as save_text:
            save_text.write(txt_string)
        del txt_string
    except Exception as e:
        error(f"Failed to save txt: {e}")
        raise

    success(f"Saved: {txt_file}")
    return txt_file


def djvu_to_text(doc_path):
    warn("Not implemented yet")


# ========================= TTS =========================

def make_tts_init(show_speakers):
    header("Initializing TTS Model")

    device = "cuda" if torch.cuda.is_available() else "cpu"
    info(f"Device: {C.BOLD}{device}{C.RESET}")

    start = time.time()
    tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)
    elapsed = time.time() - start
    success(f"Model loaded in {C.BOLD}{elapsed:.1f}s{C.RESET}")

    if show_speakers:
        if hasattr(tts, "speakers") and tts.speakers:
            info(f"Available speakers ({len(tts.speakers)}):")
            for speaker in tts.speakers:
                print(f"  {C.DIM}>{C.RESET} {speaker}")
        else:
            info("This model does not expose a speaker list")

    return tts


def make_tts_voiceover(text_to_say, use_cloning, preset_voice, cloning_audio_path, language, tts, output_path):
    if tts is None:
        tts = make_tts_init(show_speakers=False)

    info(f"Generating: {C.BOLD}{output_path}{C.RESET}")
    start = time.time()

    try:
        if use_cloning:
            tts.tts_to_file(
                text=text_to_say,
                speaker_wav=cloning_audio_path,
                language=language,
                file_path=output_path,
            )
        else:
            tts.tts_to_file(
                text=text_to_say,
                speaker=preset_voice,
                language=language,
                file_path=output_path,
            )
        elapsed = time.time() - start
        success(f"Done in {C.BOLD}{elapsed:.1f}s{C.RESET}")
        preview = text_to_say[:200] + ("..." if len(text_to_say) > 200 else "")
        info(f"Preview: {C.DIM}{preview}{C.RESET}")
    except Exception as e:
        error(f"TTS generation failed: {e}")
        raise


# ========================= MAIN =========================

if __name__ == "__main__":
    try:
        greet()
        get_user_input_volume()
        goodbye()
    except KeyboardInterrupt:
        print()
        warn("Interrupted")
        sys.exit(1)
    except Exception as e:
        error(f"Fatal: {e}")
        sys.exit(1)
