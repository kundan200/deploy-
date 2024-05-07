import streamlit as st
import speech_recognition as sr
import pyttsx3
from llm_util import LLM

llm_obj = LLM()

class SpeechToText:
    def __init__(self, lang='en'):
        self.r = sr.Recognizer()
        self.language = lang
        
    def extract_text_from_speech(self):
        with sr.Microphone() as source2:
            st.write("Listening....")
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

def main():
    st.title('Your Streamlit App Title')

    query = st.text_input('Enter your query here:')
    
    if st.button('Submit'):
        response = llm_obj.answer_to_the_question(query)
        tts = TextToSpeech()
        tts.text_to_speech(response)
        st.write('Response:', response)

    if st.button('Speech to Text'):
        stt = SpeechToText()
        query = stt.extract_text_from_speech()
        response = llm_obj.answer_to_the_question(query)
        st.write('Query:', query)
        st.write('Response:', response)

if __name__ == '__main__':
    main()
