# Imported necessary modules
import tkinter as tk
from tkinter import font
from tkinter.constants import END, RIGHT
from typing import Text
import boto3
import os 
import sys
from tempfile import gettempdir
from contextlib import closing

# Available Language
language = {
    'Hindi' : 'hi',
    'English' : 'en',
    'Bengali' : 'bn',
    'Gujarati' : 'gu',
    'Kannada' : 'kn',
    'Malayalam' : 'ml',
    'Marathi' : 'mr',
    'Punjabi' : 'pa',
    'Tamil' : 'ta',
    'Telugu' : 'te'
}

def getText():
    '''Connceting to AWS sevices and the used the translate service to translate the text with boto3 SDK and then place it into translated text area'''
    aws_mgnt_con = boto3.session.Session(profile_name='user1')
    client = aws_mgnt_con.client('translate', region_name="us-east-1")
    result = sourceText.get("1.0","end")
    try:
        translatedText.delete(1.0, END)
        response = client.translate_text(Text=result, SourceLanguageCode=language[clicked1.get()], TargetLanguageCode=language[clicked2.get()])
        text =  response.get('TranslatedText')
        translatedText.insert(1.0, text)
    except:
        translatedText.insert(1.0, "Please firstly Choose your language and Choose the language in which you want to translate!\n")

def clearText():
    '''For clearing the input and output window'''
    sourceText.delete(1.0, END)
    translatedText.delete(1.0, END)

def readText():
    '''Read the translated output'''
    aws_mgnt_con = boto3.session.Session(profile_name='user11')
    client = aws_mgnt_con.client('polly', region_name="us-east-1")
    result = translatedText.get("1.0","end")
    response = client.synthesize_speech(VoiceId='Brian', OutputFormat='mp3', Text=result, Engine='neural', LanguageCode='hi-IN')    
    if "AudioStream" in response:
        with closing(response['AudioStream']) as stream:
            output = os.path.join(gettempdir(),"speech.mp3")
            try:
                with open(output, "wb") as file:
                    file.write(stream.read())
            except IOError as error:
                print(error)
                print(error)
                sys.exit(-1)
    else:
        print("Cloud not find the stream!")
        sys.exit(-1)
    if sys.platform == "win32":
        os.startfile(output)

# Initializing the root
root = tk.Tk()

# Set the size of the window and set the title
root.geometry("800x650")
root.minsize(height=500, width=500)
root.title("Language Translator ")

# Drop Down List
try:
    clicked1 = tk.StringVar()
    clicked1.set('Choose your language')
    drop1 = tk.OptionMenu(root, clicked1,'Hindi', 'English', 'Bengali', 'Gujarati', 'Kannada', 'Malayalam', 'Marathi', 'Punjabi', 'Tamil', 'Telugu')
    drop1.pack()
except:
    tk.Label(text=str(os.error)).pack()
    sys.exit(-1)
    
# Creating Source text area with label
sourceTextLabel = tk.Label(text="Enter the Text")
sourceTextLabel.pack()
sourceText = tk.Text(root, height=15, width=400, font='timesroman')
sourceText.pack()

# Drop Down List
try:
    clicked2 = tk.StringVar()
    clicked2.set('Choose language in which you want to translate')
    drop2 = tk.OptionMenu(root, clicked2, 'Hindi', 'English', 'Bengali', 'Gujarati', 'Kannada', 'Malayalam', 'Marathi', 'Punjabi', 'Tamil', 'Telugu')
    drop2.pack()
except:
    tk.Label(text=str(os.error)).pack()
    sys.exit(-1)

# Creating translated text area with label
translatedTexLabel = tk.Label(text="Translated Text")
translatedTexLabel.pack()
translatedText = tk.Text(root,height=15, width=400)
translatedText.pack()

# Creating the frame for button to put side by side
frame = tk.Frame(root)
frame.pack()

# Creating buttons
btnRead = tk.Button(frame, height=1,width=10, text="Translate", command=getText)
btnRead.pack(side="left")
btnRead = tk.Button(frame, height=1,width=10, text="Read", command=readText)
btnRead.pack(side="left")
clear = tk.Button(frame, height=1,width=10,  text="Clear", command=clearText)
clear.pack(side="left")

root.mainloop()