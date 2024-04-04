import os
from getpass import getpass

import pandas as pd
from IPython.display import Markdown, display
from langchain.agents import create_csv_agent
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI


os.environ["OPENAI_API_KEY"] = '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'

df = pd.read_csv("btc-daily-price.csv")

agent = create_csv_agent(
    ChatOpenAI(temperature=0, model_name="gpt-4"), "btc-daily-price.csv", verbose=True
)

print(agent.run("Draw a graph of overall price trend"))