import os
import json
import openai
from openai import OpenAI
import streamlit as st
import streamlit.components.v1 as components
from generate_ppt import generate_ppt
from ppt_to_json import ppt_to_json
from text_summarization import text_summarization
from upload_ppt_to_google_drive import upload_ppt_to_google_drive
from web_scraping import web_scraping,validate_url
from generate_json import generate_json
from read_word_file import read_word_file
from change_extension import change_extension

OPENAI_API_KEY='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'
st.title("Intelligent PPT Generator")
# text = "The New Year is the time or day at which a new calendar year begins and the calendar's year count increments by one. Many cultures celebrate the event in some manner.[1] In the Gregorian calendar, the most widely used calendar system today, New Year occurs on January 1 (New Year's Day, preceded by New Year's Eve). This was also the first day of the year in the original Julian calendar and the Roman calendar (after 153 BC).[2] Other cultures observe their traditional or religious New Year's Day according to their own customs, typically (though not invariably) because they use a lunar calendar or a lunisolar calendar. Chinese New Year, the Islamic New Year, Tamil New Year (Puthandu), and the Jewish New Year are among well-known examples. India, Nepal, and other countries also celebrate New Year on dates according to their own calendars that are movable in the Gregorian calendar. During the Middle Ages in Western Europe, while the Julian calendar was still in use, authorities moved New Year's Day, depending upon locale, to one of several other days, including March 1, March 25, Easter, September 1, and December 25. Since then, many national civil calendars in the Western World and beyond have changed to using one fixed date for New Year's Day, January 1—most doing so when they adopted the Gregorian calendar."
st.caption('🔗Write down the urls')

container = st.container()
with container:
    url = st.text_input("URL: ", key="input")
    is_valid_url = validate_url(url)
    if not is_valid_url:
        st.write('Please input valid url')
    else:
        content = web_scraping(url)
        text=text_summarization(content)
        st.info(text)
        st.session_state['text'] = text
        st.session_state['output_file_name'] = "output.pptx"
st.caption('📃Upload a word file')
# Input widgets
uploaded_file = st.file_uploader('Upload your word documentation')


if (uploaded_file is not None) & ('Executed' not in st.session_state):
    st.caption('🔗🚀Word file summarization')
    text=json.loads(text_summarization(read_word_file(uploaded_file)))
    st.session_state['text'] = text
    st.info(text)
    slides_data = generate_json(word_content=text)
    output_file_name = change_extension(uploaded_file.name, "pptx")
    st.session_state['output_file_name'] = output_file_name
    generate_ppt(slides_data=slides_data, output_file_name=output_file_name)
    webViewLink = upload_ppt_to_google_drive(credentials_path='service-account-credentials.json', file_path=str(output_file_name), file_name=str(output_file_name))
    
    st.info('🎈 Presentation Deck of '+ output_file_name)
    components.iframe(webViewLink, height=480)
    st.session_state['Executed'] = True


st.caption("💬 Chatbot to optimize the ouput")
    
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    st.chat_message("user").write(prompt)
    text = st.session_state['text']
    output_file_name = st.session_state['output_file_name']
    slideDeck = ppt_to_json(output_file_name)
    print(slideDeck)
    slides_data = generate_json(word_content=text, prompt=prompt, slideDeck=slideDeck)
    generate_ppt(slides_data=slides_data, output_file_name=output_file_name)
    webViewLink = upload_ppt_to_google_drive(credentials_path='service-account-credentials.json', file_path=str(output_file_name), file_name=str(output_file_name))
    msg = "The PPT has already updated"
    st.chat_message("assistant").write(msg)
    
    st.title('🎈 New Presentation Deck of '+ output_file_name)
    components.iframe(webViewLink, height=480)
    
# if prompt := st.chat_input():
#     # client = OpenAI(api_key=OPENAI_API_KEY)
#     st.session_state.messages.append({"role": "user", "content": prompt})
#     st.chat_message("user").write(prompt)

#     slideDeck = ppt_to_json(output_file_name)
#     print(slideDeck)
#     slides_data = generate_json(word_content=text, prompt=prompt, slideDeck=slideDeck)
#     generate_ppt(slides_data=slides_data, output_file_name=output_file_name)
#     webViewLink = upload_ppt_to_google_drive(credentials_path='service-account-credentials.json', file_path=str(output_file_name), file_name=str(output_file_name))
#     msg = "The PPT has already updated"
#     st.session_state.messages.append({"role": "assistant", "content": msg})
#     st.chat_message("assistant").write(msg)

    # response = client.chat.completions.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
    # msg = response.choices[0].message.content
    # st.session_state.messages.append({"role": "assistant", "content": msg})
    # st.chat_message("assistant").write(msg)