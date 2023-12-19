import streamlit as st
from langchain.llms import OpenAI
import streamlit.components.v1 as components
from openai import OpenAI

#set page layout
st.set_page_config(page_icon="🚀", page_title="PowerPoint Generator")

st.title('Welcome to PowerPoint Generator!')

st.title('🦜🔗 Generate a PPT based on files')
# Input widgets
uploaded_file = st.file_uploader('Upload your relevant documentation')

st.title("🚢 Generate PPT based on URLs")
url = st.text_input("Type relevant URLs")

st.title('🦜🔗 Specify your requirements')

openai_api_key = st.sidebar.text_input('OpenAI API Key', type="password")

def generate_response(input_text):
  llm = OpenAI(temperature=0.7, openai_api_key=openai_api_key)
  st.info(llm(input_text))

with st.form('my_form'):
  text = st.text_area('Enter text:', 'What are the three key pieces of advice for learning how to code?')
  submitted = st.form_submit_button('Submit')
  if not openai_api_key.startswith('sk-'):
    st.warning('Please enter your OpenAI API key!', icon='⚠')
  if submitted and openai_api_key.startswith('sk-'):
    generate_response(text)


st.title('🦜🔗 Upload your PPT template')
# Input widgets
uploaded_file = st.file_uploader('Upload PPT template if you you have')


submit = st.button(label='Generate PowerPoint slides')

st.spinner('Generating awesome slides for you...⏳')

st.title('🎈 Presentation Deck')
components.iframe("https://docs.google.com/presentation/d/e/2PACX-1vSaBx4udmh8hYvD7r8iQPMGpdrOCYPjKTo09pezMX5dyVNHJ0CBu2n8oEX-7DR-j9hGRvB-EBeI9Yaz/embed?start=false&loop=false&delayms=3000", height=480)

text_contents = '''This is some text'''
st.download_button('Download the PPT', text_contents)