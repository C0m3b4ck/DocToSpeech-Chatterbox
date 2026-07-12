# /////////////////////////////         LIBRARY IMPORTS                 ///////////////////////////////
import pathlib  # for relative paths
from datetime import datetime  # for timestamps

import pyfiglet  # for ASCII art in greet()
import torch  # for TTS functionality
from TTS.api import TTS  # for TTS functionality

# /////////////////////////////          USER INTERACTION FUNCTIONS            ////////////////////////////


def greet():
    ASCII_art_greet = pyfiglet.figlet_format("DocToSpeech", font="alphabet")
    print(ASCII_art_greet)
    ASCII_art_credit = pyfiglet.figlet_format("By C0m3b4ck under APL 2.0")
    print(ASCII_art_credit)


def get_user_input_docs():
    txt_path = ""
    choice = ""
    file_extention = ""

    print("Currently supported formats: [PDF, EPUB, DOCX, DOC, HTML, DJVU, TXT]")
    doc_path = str(input("Input doc path: "))
    print("Document path:", doc_path)
    file_extention = pathlib.Path(doc_path).suffix.lower()
    print("Document file extention:", file_extention)

    # Convert to .txt, then return .txt path
    if file_extention == ".epub":
        txt_path = epub_to_text(doc_path)
    elif file_extention == ".pdf":
        txt_path = pdf_to_text(doc_path)
    elif file_extention == ".docx":
        txt_path = docx_to_text(doc_path)
    elif file_extention == ".doc":
        txt_path = doc_to_text(doc_path)
    elif file_extention in (".html", ".htm"):
        txt_path = html_to_text(doc_path)
    elif file_extention == ".djvu":
        txt_path = djvu_to_text(doc_path)
    elif file_extention == ".txt":
        print("File already in raw text format! Proceeding to tts option selection...")
        txt_path = doc_path
    else:
        print("Unrecognized extention.")
        return

    while len(choice) != 1 or choice not in ("y", "n"):
        choice = input("Treat the inputted doc as text file? y/n: ").lower()
        if choice == "y":
            print(
                "File already in raw text format! Proceeding to tts option selection..."
            )
            txt_path = doc_path
        elif choice == "n":
            print("Unknown file extention. Closing program.")
            exit()

    get_user_input_tts(txt_path)


def get_user_input_tts(txt_path):
    choice = ""
    cloning_path = ""
    use_cloning = False
    preset_speaker = ""

    output_file_name = input("Output file name: ")
    language = input("Language acronym (en for english): ")

    while (len(choice) != 1) and choice != "c" and choice != "p":
        choice = input("Use cloning voice (c) or preset voice? c/p: ")
        choice.lower()
        if choice == "c":
            cloning_path = input("Input cloning voice .wav relative path: ")
            os.path.join(os.path.dirname(__file__), cloning_path)
            use_cloning = True
        elif choice == "p":
            print("Speakers: ", tts.speakers)
            preset_speaker = input("Input preset speaker name: ")
            use_cloning = False
    with open(txt_path, "r") as file:
        file_contents = file.read()
    print("File contents: ", file_contents)

    # call make_tts_voiceover with all of the arguments
    make_tts_voiceover(
        file_contents,
        use_cloning,
        preset_speaker,
        cloning_path,
        language,
        output_file_name,
    )

# /////////////////////         DOCS TO TXT FUNCTIONS           //////////////////////////
def epub_to_text(doc_path):
def pdf_to_text(doc_path):
def docx_to_text(doc_path):
def doc_to_text(doc_path):
def html_to_text(doc_path):
def djvu_to_text(doc_path):
# ////////////////////            TTS FUNCTIONS           /////////////////
def make_tts_voiceover(
    text_to_say,
    use_cloning,
    preset_voice,
    cloning_audio_relative_path,
    language,
    file_name,
):

    # Get device
    print("Getting device (CUDA/CPU)...")
    device = "cuda" if torch.cuda.is_available() else "cpu"

    # List available TTS models
    # print("Available models: ",TTS().list_models())

    # Initialize TTS
    print("Initializing TTS model...")
    tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)

    # Run TTS
    # ❗ XTTS supports both, but many models allow only one of the `speaker` and
    # `speaker_wav` arguments

    # Get current datetime object
    current_datetime = datetime.now()

    # Convert datetime object to timestamp
    current_timestamp = current_datetime.timestamp()
    print("Current Timestamp:", current_timestamp)
    output_path = file_name + "_" + current_timestamp + ".wav"
    print("Output file name: ", output_path)
    # TTS with list of amplitude values as output, clone the voice from `cloning_audio_relative_path`
    if use_cloning:
        wav = tts.tts(
            text=text_to_say,
            speaker_wav=cloning_audio_relative_path,
            language=language,
            file_path=output_path,
        )
    else:
        # TTS to a file, use a preset speaker
        tts.tts_to_file(
            text=text_to_say,
            speaker=preset_voice,
            language=language,
            file_path=output_path,
        )


# /////////////////////////////////                 MAIN FUNCTION - ENTRY POINT                     //////////////////////////////
if __name__ == "__main__":
    greet()
    get_user_input_docs()
