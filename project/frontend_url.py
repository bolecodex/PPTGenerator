import streamlit as st
from streamlit_chat import message
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    SystemMessage,
    HumanMessage,
    AIMessage
)
from langchain.callbacks import get_openai_callback
from langchain.prompts import PromptTemplate
from langchain.chains.summarize import load_summarize_chain
from langchain.text_splitter import RecursiveCharacterTextSplitter

import requests, json, os
from bs4 import BeautifulSoup
from urllib.parse import urlparse
ALB_BACKEND_URL="http://PPTGeneratorALB-1552944092.ap-northeast-1.elb.amazonaws.com"
OPENAI_API_KEY="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"
openai_api_key="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"


def init_page():
    st.set_page_config(
        page_title="PPT Generator",
        page_icon="🤗"
    )
    st.header("PPT Generator 🤗")
    st.sidebar.title("Options")


def init_messages():
    clear_button = st.sidebar.button("Clear Conversation", key="clear")
    if clear_button or "messages" not in st.session_state:
        st.session_state.messages = [
            SystemMessage(content="You are a helpful assistant.")
        ]
        st.session_state.costs = []


def select_model():
    model = st.sidebar.radio("Choose a model:", ("GPT-3.5", "GPT-4"))
    if model == "GPT-3.5":
        model_name = "gpt-3.5-turbo"
        st.session_state.model_name = "gpt-3.5-turbo-0613"
    else:
        model_name = "gpt-4"
        st.session_state.model_name = "gpt-4"
    # 300: 本文以外の指示のtoken数 (決めうちの雑な実装です…)
    st.session_state.max_token = OpenAI.modelname_to_contextsize(st.session_state.model_name) - 300
    return ChatOpenAI(temperature=0, model_name=model_name)


def get_url_input():
    url = st.text_input("URL: ", key="input")
    return url


def validate_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


def get_content(url):
    try:
        with st.spinner("Fetching Content ..."):
            # response = requests.get(url)
            # soup = BeautifulSoup(response.text, 'html.parser')
            r = requests.get(url)
            soup = BeautifulSoup(r.content, 'html.parser')
            # fetch text from main (change the below code to filter page)
            if soup.main:
                return soup.main.get_text()
            elif soup.article:
                return soup.article.get_text()
            else:
                return soup.body.get_text()
    except:
        st.write('something wrong')
        return None


def build_prompt(content, n_chars=3000):
    return f"""Summarize the below web content to about {n_chars} words.

========

{content}

========

Please writen in Chinese!
"""

def build_ppt_from_summary(page_number, summary):
    return f"""generate {page_number} slides base on the content below:

========

{summary}

========

Please writen in Chinese!
"""

def get_answer(llm, messages):
    print("messages:")
    print(messages)
    with get_openai_callback() as cb:
        answer = llm(messages)
    return answer.content, cb.total_cost

def summarize(llm, docs):
    prompt_template = """Write a Chinese summary of the following web content.

{text}

Please writen in Chinese
"""
    PROMPT = PromptTemplate(template=prompt_template, input_variables=["text"])

    with get_openai_callback() as cb:
        chain = load_summarize_chain(
            llm,
            chain_type="map_reduce",
            verbose=True,
            map_prompt=PROMPT,
            combine_prompt=PROMPT
        )
        response = chain(
            {
                "input_documents": docs,
                # token_max を指示しないと、GPT3.5など通常の
                # モデルサイズに合わせた内部処理になってしまうので注意
                "token_max": st.session_state.max_token
            },
            return_only_outputs=True
        )

    return response['output_text'], cb.total_cost

def main():
    init_page()
    backend_url = os.getenv('ALB_BACKEND_URL')
    llm = select_model()
    init_messages()

    container = st.container()
    response_container = st.container()

    with container:
        url = get_url_input()
        is_valid_url = validate_url(url)
        if not is_valid_url:
            st.write('Please input valid url')
            answer = None
        else:
            content = get_content(url)
            if content:
                prompt = build_prompt(content)
                st.session_state.messages.append(HumanMessage(content=prompt))
                with st.spinner("ChatGPT is typing ..."):
                    # answer, cost = get_answer(llm, st.session_state.messages)
                    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
                        model_name=st.session_state.model_name,
                        chunk_size=st.session_state.max_token,
                        chunk_overlap=0,
                    )
                    splits = text_splitter.split_text(content)
                    texts = text_splitter.create_documents(splits)
                    print(texts)
                    answer, cost = summarize(llm, texts)
                st.session_state.costs.append(cost)
            else:
                answer = None

    if answer:
        with response_container:
            st.markdown("## Summary")
            st.write(answer)
            url = backend_url + '/ppt-content'
            post_data = {"prompt": "\""+build_ppt_from_summary(8,answer)+"\""}
            print(build_ppt_from_summary(8,answer))
            print (post_data)
            print(type(post_data))
            result = requests.post(url, json = post_data)
            st.markdown("---")
            print(result)
            st.markdown("## PPT Contents")
            print(result.text)
            st.write(result.text)
            url = backend_url + '/ppt-file'
            post_data = result.text
            print(post_data)
            print(type(post_data))
            # 报错json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)
            ppt_generation_result = requests.post(url, json = json.loads(post_data))
            print(ppt_generation_result.text)
            ppt_file_data = json.loads(ppt_generation_result.text)
            st.markdown("---")
            st.markdown("## Generated PPT File Download")
            st.link_button(ppt_file_data["ppt_file_name"], ppt_file_data["download_url"])
            st.markdown("---")
            st.markdown("## Original Text")
            st.write(content)

    costs = st.session_state.get('costs', [])
    st.sidebar.markdown("## Costs")
    st.sidebar.markdown(f"**Total cost: ${sum(costs):.5f}**")
    for cost in costs:
        st.sidebar.markdown(f"- ${cost:.5f}")

if __name__ == '__main__':
    main()