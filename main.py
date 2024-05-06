from flask import Flask, render_template, request
import speech_recognition as sr
import pyttsx3
from llm_util import LLM

app = Flask(__name__)
llm_obj = LLM()

class SpeechToText:
    def __init__(self, lang='en'):
        self.r = sr.Recognizer()
        self.language = lang
        
    def extract_text_from_speech(self):
        with sr.Microphone() as source2:
            print("Listening....")
            self.r.adjust_for_ambient_noise(source2, duration=0.3)
            audio2 = self.r.listen(source2)
            MyText = self.r.recognize_google(audio2)
            MyText = MyText.lower()
            return MyText
        
class TextToSpeech:
    def __init__(self):
        self.engine = pyttsx3.init()
        
    def text_to_speech(self, command):
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[1].id)
        self.engine.say(command)
        self.engine.runAndWait()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_query', methods=['POST'])
def process_query():
    query = request.form['query']
    response = llm_obj.answer_to_the_question(query)
    tts = TextToSpeech()
    tts.text_to_speech(response)
    return render_template('index.html', query=query, response=response)

@app.route('/speech_to_text', methods=['POST'])
def speech_to_text():
    if request.method == 'POST':
        stt = SpeechToText()
        query = stt.extract_text_from_speech()
        response = llm_obj.answer_to_the_question(query)
        return render_template('index.html', query=query, response=response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
