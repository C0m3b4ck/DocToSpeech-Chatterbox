# /////////////////////////////         LIBRARY IMPORTS                 ///////////////////////////////
import os # for relative paths
from pathlib import Path  # for relative paths
import io # for streams, including pdf_stream
import pathlib # for misc path-related stuff, including extentions
import time # for waiting during massive text prints
from datetime import datetime # for timestamps

import pyfiglet  # for ASCII art in greet()
import torch  # for TTS functionality
from TTS.api import TTS  # for TTS functionality

from epub2txt import epub2txt # for epub to txt
import pdftotext # for pdf to txt
import docx2txt # for docx to txt
import html2text # for html to txt

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
    txt_string = ""
    # output as a list of chapters
    ch_list = epub2txt(doc_path, outputlist=True) # chapter titles will be available as epub2txt.content_titles if available
    # convert .epub to disinfected string
    try:
        txt_string = epub2txt(doc_path)
    except Exception as e:
        print("!!! An error occurred while converting file: ", e)
        print("Please select different file.")
        get_user_input_docs()
    else:
        print("Succesfully converted .epub to .txt!")

    # save disinfected string into .txt file
    try:
        save_text = open((doc_path + ".txt"), "w")
        save_text.write(txt_string)
        save_text.close
    except Exception as e:
        print("!!! An error occurred while saving .txt: ", e)
        print("---> Please check write permissions in this directory.")
        time.sleep(3)
        print("Returning to file selection.")
        get_user_input_docs()
    else:
        print("Successfully saved file!")
    txt_file = doc_path + ".txt"
    print("---> Finished text file: ", txt_file)
    return txt_file
def pdf_to_text(doc_path):
    choice = ""
    password = ""
    pdf = ""
    txt_file = ""
    while (len(choice) != 1) and choice != "y" and choice != "n":
        choice = input("Is PDF password-protected? y/n: ")
        choice.lower()
        if choice == "y":
            password = input("Input PDF password: ")
            try:
                # If it's password-protected
                with open(doc_path, "rb") as f:
                    pdf = pdftotext.PDF(f, password)
            except Exception as e:
                print("!!! An exception occurred while opening PDF: ",e)
                time.sleep(3)
                print("Returning to file selection.")
                get_user_input_docs()
            else:
                print("PDF opened succesfully!")
        elif choice == "n":
            try:
                # Load your PDF
                #with open(doc_path, "rb") as f:
                #    pass
                doc_path_abs = os.path.abspath(doc_path)
                print("CWD: ", os.getcwd())
                print("Resolved path: ", doc_path_abs)
                print("Exists: ", os.path.isfile(doc_path_abs))
                with open(doc_path_abs, "rb") as f:
                    pdf_bytes = f.read()
                pdf_stream = io.BytesIO(pdf_bytes)
                pdf = pdftotext.PDF(pdf_stream)
            except Exception as e:
                print("!!! An exception occurred while opening PDF: ",e)
                time.sleep(3)
                print("Returning to file selection.")
                get_user_input_docs()
            else:
                print("PDF opened succesfully!")
        else:
            print("!!! Please input 'y' or 'n' !!!")

    # How many pages?
    print("PDF pages: ", len(pdf))

    while (len(choice) != 1) and choice != "c" and choice != "p":
        choice = input("Show all PDF pages? y/n: ")
        choice.lower()
        if choice == "y":
            # Iterate over all the pages
            for page in pdf:
                print(page)
        elif choice == "n":
            print("Not showing.")
        else:
            print("Unknown input - defaulting to not printing.")


    # Read all the text into one string
    txt_string = "\n\n".join(pdf)

    # save disinfected string into .txt file
    try:
        txt_file = doc_path + ".txt"
        save_text = open((doc_path + ".txt"), "w")
        save_text.write(txt_string)
        save_text.close
    except Exception as e:
        print("!!! An error occurred while saving .txt: ", e)
        print("---> Please check write permissions.")
        time.sleep(3)
        print("Returning to file selection.")
        get_user_input_docs()
    else:
        print("Successfully saved file: ", txt_file)
        return txt_file
def docx_to_text(doc_path):
    txt_string = docx2txt.process(doc_path)
    # save disinfected string into .txt file
    try:
        txt_file = doc_path + ".txt"
        save_text = open((doc_path + ".txt"), "w")
        save_text.write(txt_string)
        save_text.close
    except Exception as e:
        print("!!! An error occurred while saving .txt: ", e)
        print("---> Please check write permissions. ")
        time.sleep(3)
        print("Returning to file selection.")
        get_user_input_docs()
    else:
        print("Successfully saved file: ", txt_file)
        return txt_file
def doc_to_text(doc_path):
    # actually implement
    print("Not done yet! Will require .doc to .docx conversion.")
def html_to_text(doc_path):
    html_contents = ""

    # open html file
    try:
        with open(doc_path, 'r') as file:
            html_contents = file.read()
    except Exception as e:
        print("!!! An error occurred while opening HTML: ", e)
        print("---> Please check read permissions in this directory.")
        time.sleep(3)
        print("Returning to file selection.")
        get_user_input_docs()
    else:
        print("Succesfully read HTML file.")

    # convert html contents
    try:
        h = html2text.HTML2Text()
        h.ignore_links = True # ignore links
        txt_string = h.handle(html_contents)
    except Exception as e:
        print("!!! An error occurred while saving .txt: ", e)
        print("---> Please check write permissions in this directory.")
        time.sleep(3)
        print("Returning to file selection.")
        get_user_input_docs()
    else:
        print("Succesfully sanitized HTML contents.")
    # save disinfected string into .txt file
    try:
        txt_file = doc_path + ".txt"
        save_text = open((doc_path + ".txt"), "w")
        save_text.write(txt_string)
        save_text.close
    except Exception as e:
        print("!!! An error occurred while saving .txt: ", e)
        print("---> Please check write permissions in this directory.")
        time.sleep(3)
        print("Returning to file selection.")
        get_user_input_docs()
    else:
        print("Successfully saved file: ", txt_file)
        return txt_file
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
        print("!!! An error occured while trying to generate file: ", e)
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
