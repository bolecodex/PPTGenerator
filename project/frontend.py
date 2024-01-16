import os
from openai import OpenAI
import streamlit as st
import requests as req
from utils import read_word_file
import streamlit.components.v1 as components

openai_api_key = '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'
# text = "The New Year is the time or day at which a new calendar year begins and the calendar's year count increments by one. Many cultures celebrate the event in some manner.[1] In the Gregorian calendar, the most widely used calendar system today, New Year occurs on January 1 (New Year's Day, preceded by New Year's Eve). This was also the first day of the year in the original Julian calendar and the Roman calendar (after 153 BC).[2] Other cultures observe their traditional or religious New Year's Day according to their own customs, typically (though not invariably) because they use a lunar calendar or a lunisolar calendar. Chinese New Year, the Islamic New Year, Tamil New Year (Puthandu), and the Jewish New Year are among well-known examples. India, Nepal, and other countries also celebrate New Year on dates according to their own calendars that are movable in the Gregorian calendar. During the Middle Ages in Western Europe, while the Julian calendar was still in use, authorities moved New Year's Day, depending upon locale, to one of several other days, including March 1, March 25, Easter, September 1, and December 25. Since then, many national civil calendars in the Western World and beyond have changed to using one fixed date for New Year's Day, January 1—most doing so when they adopted the Gregorian calendar."

def generate_response(input_text):
    api_gateway_ep = "https://7j7chla9ih.execute-api.us-east-1.amazonaws.com/test/text-summarization"
    headers = {"accept": "application/json", "Content-Type": "application/json"}
    data = {"text": input_text}
    resp = req.post(api_gateway_ep, headers=headers, json=data)
    st.info(resp.text)

st.caption('📃Upload a word file')
# Input widgets
uploaded_file = st.file_uploader('Upload your word documentation')
st.caption('🔗🚀Word file summarization')
st.info(generate_response(read_word_file(uploaded_file)))

st.caption('🔗Write down the urls')

# with st.form('my_form'):
#   text = st.text_area("Please enter the text")
#   submitted = st.form_submit_button('Submit')
#   generate_response(text)


st.caption("💬 Chatbot to optimize the ouput")
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    client = OpenAI(api_key=openai_api_key)
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    response = client.chat.completions.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
    msg = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)
    
st.title('🎈 Presentation Deck')
components.iframe("https://docs.google.com/presentation/d/11zGuEQ73hmZJRW6Spo9v1TpcrJCgos4w/edit?usp=drivesdk&ouid=109567901216249287883&rtpof=true&sd=true", height=480)
