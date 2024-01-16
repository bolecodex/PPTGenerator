from typing import Any
from fastapi import Body, FastAPI
from mangum import Mangum
from openai import OpenAI
import json
import os

app = FastAPI()

@app.get("/")
def hello_world():
    return {'message': 'Hello from FastAPI'}


@app.get("/hello/{name}")
def hello(name: str):
    return {"message": f'Hello from FastAPI, {name}!'}

@app.post("/ask")
def ask(payload: Any = Body(None)):
    client = OpenAI()

    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
        {"role": "user", "content": payload["question"]}
    ]
    )

    response_message = completion.choices[0].message.content
    return  response_message

@app.post("/ppt-content")
def generate_ppt(payload: Any = Body(None)):
    client = OpenAI()
    slide_number="1"
    # prompt="Generate a PPT of 3 slides related to Albert Einstein"
    word_content=""
    slideDeck={"slide_number": float(slide_number), "title": "", "content": "", "narration": ""}
    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
            {"role": "system", "content": "User will ask you to create or update text content for some slides"+(" based on the aforementioned Input Article" if word_content else "")+". The response format should be a valid json format structured as this: [{\"slide_number\": <Float>, \"title\": \"<String>\", \"content\": \"<String>\", \"narration\": \"<String>\"},{\"slide_number\": <Float>, \"title\": \"<String>\", \"content\": \"<String>\", \"narration\": \"<String>\"}] \n content field in the response comprehensive enough as it is the main text of each slide. \n For content use a mix of bullet points and text when applicable. \n If you are modifying an existing slide leave the slide number unchanged but if you are adding slides to the existing slides, use decimal digits for the slide number. for example to add a slide after slide 2, use slide number 2.1, 2.2, ... \n If user asks to remove a slide, set its slide number to negative of its current value because slides with negative slide number will be excluded from presentation. \n The existing slides are as follows: "+json.dumps(slideDeck)},
            {"role": "system", "content": "For each slide the content field is the main body of the slide while the narration field is just an example transcript of the presentation of the content field. \n Never mention the slide number in the transcript."},
            {"role": "system", "content": "For each slide, the content field should be the default field to modify if modification is demanded by the user for the slide, not the narration field. "},
            {"role": "system", "content": "For each slide, the narration field should only be populated if explicitely asked in user prompt, otherwise should be left empty. "},
            {"role": "system", "content": "Response should be valid json in the format described earlier. slide_number, title,and content are mandatory keys."},
            {"role": "user", "content": payload["prompt"]}
    ]
    )

    response_message = completion.choices[0].message.content
    slides_data = json.loads(completion.choices[0].message.content)

    print(slides_data)
    return  slides_data

@app.post("/chat_gpt4")
def chat_gpt4(payload: Any = Body(None)):
    client = OpenAI()

    completion = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "You are an assistant."},
        {"role": "user", "content": payload["question"]}
    ]
    )

    response_message = completion.choices[0].message.content
    return  response_message

handler = Mangum(app)
