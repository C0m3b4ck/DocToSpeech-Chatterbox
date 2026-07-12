# /////////////////////////////         LIBRARY IMPORTS                 ///////////////////////////////
import pathlib  # for relative paths
import time # for waiting during massive text prints
from datetime import datetime  # for timestamps

import pyfiglet  # for ASCII art in greet()
import torch  # for TTS functionality
from TTS.api import TTS  # for TTS functionality

# /////////////////////////////          USER INTERACTION FUNCTIONS            ////////////////////////////


def greet():
    ASCII_art_greet = pyfiglet.figlet_format("DocToSpeech", font="alphabet")
    print(ASCII_art_greet)
    ASCII_art_credit = pyfiglet.figlet_format("By C0m3b4ck under MPL 2.0")
    print(ASCII_art_credit)

def goodbye():
    ASCII_art_bye = pyfiglet.figlet_format("Goodbye!", font='alphabet')
    print(ASCII_art_bye)
    ASCII_art_credit = pyfiglet.figlet_format("By C0m3b4ck under MPL 2.0")
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

        while len(choice) != 1 or choice not in ("y", "n"):
             choice = input("Treat the inputted doc as text file? y/n: ").lower()
             if choice == "y":
                 print("File already in raw text format! Proceeding to tts option selection...")
                 txt_path = doc_path
             elif choice == "n":
                 print("Unknown file extension. Closing program.")
                 exit()

    get_user_input_tts(txt_path)


def get_user_input_tts(txt_path):
    choice = ""
    choice_timestamp = ""
    cloning_path = ""
    use_cloning = False
    preset_speaker = ""
    tts_initialized = False
    tts = None
    output_path = ""

    output_file_name = input("Output file name (without *.wav): ").strip()
    while (len(choice_timestamp) != 1) and choice_timestamp != "c" and choice_timestamp != "p":
        choice_timestamp = input("Add timestamp to file name? y/n: ")
        choice_timestamp.lower()
        if choice_timestamp == "y":
            # Get current datetime object
            current_datetime = datetime.now()
            # Convert datetime object to timestamp
            current_timestamp = current_datetime.timestamp()
            print("---> Current Timestamp:", current_timestamp)
            output_path = (output_file_name + "_" + str(current_timestamp)) # .wav extention is attached automatically
            print("---> Output file name: ", output_path)
        elif choice_timestamp == "n":
            output_path = output_file_name + ".wav"
            print("---> Not adding timestamp.")
        else:
            print("!!! Please input 'y' or 'n' !!!")
    language = input("Language acronym (en for english): ")

    while (len(choice) != 1) and choice != "c" and choice != "p":
        choice = input("Use cloning voice (c) or preset voice? c/p: ")
        choice.lower()
        if choice == "c":
            cloning_path = input("Input cloning voice .wav relative path: ")
            #os.path.join(os.path.dirname(__file__), cloning_path)
            use_cloning = True
        elif choice == "p":
            tts = make_tts_init(show_speakers=True)
            preset_speaker = input("Input preset speaker name: ")
            use_cloning = False
        else:
            print("!!! Please input 'c' or 'p' !!!")
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
        tts,
        output_path
    )

# /////////////////////         DOCS TO TXT FUNCTIONS           //////////////////////////
def epub_to_text(doc_path):
    # actually implement
    print("Not done yet!")
def pdf_to_text(doc_path):
    # actually implement
    print("Not done yet!")
def docx_to_text(doc_path):
    # actually implement
    print("Not done yet!")
def doc_to_text(doc_path):
    # actually implement
    print("Not done yet!")
def html_to_text(doc_path):
    # actually implement
    print("Not done yet!")
def djvu_to_text(doc_path):
    # actually implement
    print("Not done yet!")
# ////////////////////            TTS FUNCTIONS           /////////////////
def make_tts_init(show_speakers): # initializes tts object
    print("Checking for CUDA/CPU...")
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print("Using device:", device)

    print("Initializing TTS model...")
    tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device) # model that supports both cloning and speakers

    if show_speakers:
        if hasattr(tts, "speakers") and tts.speakers:
            print("Available speakers:")
            for speaker in tts.speakers:
                print("-", speaker)
        else:
            print("This model does not expose a speaker list.")

    return tts

def make_tts_voiceover(
    text_to_say,
    use_cloning,
    preset_voice,
    cloning_audio_relative_path,
    language,
    file_name,
    tts,
    output_path
):
    if (tts is None):
        tts = make_tts_init(show_speakers=False)
    # Run TTS
    # ❗ XTTS supports both, but many models allow only one of the `speaker` and
    # `speaker_wav` arguments

    # TTS with list of amplitude values as output, clone the voice from `cloning_audio_relative_path`
    try:
        if use_cloning:
            tts.tts_to_file(
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
    except Exception as e:
        print("An error occured while trying to generate file: ", e)
    else:
        print("~~~ File made successfully!!! ~~~")
        print("Output file path: ", output_path)
        print("Language: ", language)
        time.sleep(1)
        print("Text read: ", text_to_say)
        goodbye()

# /////////////////////////////////                 MAIN FUNCTION - ENTRY POINT                     //////////////////////////////
if __name__ == "__main__":
    greet()
    get_user_input_docs()
