from PyPDF2 import PdfFileReader

from tkinter import *
from tkinter import filedialog
from tkinter.messagebox import showinfo

from google.cloud import texttospeech
import os
from google.cloud import storage


filename = ""
file_counter = 0

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'YOUR GOOGLE JSON CREDENTIALS PATH'


def convert_to_audio(text):
    client = texttospeech.TextToSpeechClient()
    synthesis_input = texttospeech.SynthesisInput(text=f"{text}")

    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    global file_counter
    file_counter += 1

    with open(f"audiobook{file_counter}.mp3", "wb") as out:
        out.write(response.audio_content)

    showinfo(
        title='File saved',
        message=f'Audio content written to file "audiobook{file_counter}.mp3"'
    )


def read_pdf():
    if filename == "":

        showinfo(
            title='Wrong or no file',
            message=f"No file selected"
        )

    else:

        document = PdfFileReader(stream=filename)
        pages = document.getNumPages()
        print(pages)
        text = ""

        for num in range(pages):

            page = document.getPage(num)
            text += page.extractText()

        convert_to_audio(text)


def select_file():
    filetypes = (
        ('PDF files', '*.pdf'),
    )

    global filename
    filename = filedialog.askopenfilename(
        title='Open a file',
        initialdir='/',
        filetypes=filetypes)

    if filename != "":
        showinfo(
            title='Selected File',
            message=f"Selected file: {filename.split('/')[-1]}"
        )


window = Tk()
window.title("PDF to audio converter")
window.geometry('300x150')

open_button = Button(text='Choose a file', command=select_file)
open_button.pack(expand=True)

convert_button = Button(text='Convert file', command=read_pdf)
convert_button.pack(expand=True)





window.mainloop()
