import streamlit as st
import google.generativeai as genai
from PIL import Image
from functools import partial

genai.configure(api_key='AIzaSyCnMvBNuAImVy5ezCjp8SKWcDNluZNj2-s')

def click_go_button():
    st.session_state.buttonState = True

st.title("StudyBuddy AI")
st.write("An App to Help you Ace your Exams")
st.text("""Welcome to StudyBuddy AI. This app intends to be 
your one stop shop for all your studying needs. 
You will select what type of help you need, give 
it a prompt and let StudyBuddy do the rest!""")

st.image('studyImage.png')

st.text("""How to use:
    1. Select what type of help you would like to receive. (Test review, Test Preparation, Topic Explanation)
    2. Upload file (If applicable)
    3. Type what you want StudyBuddy to do specifically. (Ex: “Create a practice test for Differential Equations Exam)
    4. Download StudyBuddy response (optional)
    5. ACE YOUR EXAM !!!""")

studyOptions = ["Choose an option","Review a topic", "Practice for exam", "Learn new material"]
studyType = st.selectbox("To begin, select which type of help you need:point_down:", options=studyOptions)

file = st.file_uploader("Upload File (Optional)", type=['png', 'jpg', 'jpeg', 'svg'])

userPrompt = st.text_input("Enter Your Prompt: ", placeholder="Ex: Create an practice test for Calculus 1")

st.button("Go", on_click=click_go_button)

if 'buttonState' not in st.session_state:
	st.session_state.buttonState = False

promptString = ""
if st.session_state.buttonState:
    promptString += f"I need you to help me {studyType}. "
    promptString += userPrompt

    st.write(f'PROMPT: {promptString}')
    response = ""
    if file:
        img = Image.open(file)
        model = genai.GenerativeModel('gemini-pro-vision')
        response = model.generate_content([promptString, img])
        response.resolve()
    else:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(promptString)
        response.resolve()
    st.write("Resubmit prompt to start again.")
    st.header("Results")
    st.write(response.text)
    st.download_button("Download", response.text, type='primary')



