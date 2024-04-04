import pandas as pd
import openai
import matplotlib.pyplot as plt
from openai import OpenAI

openai_api_key="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"


def generate_visualization_gpt4(excel_file, user_prompt, openai_api_key):
    # Step 1: Read the Excel File
    df = pd.read_excel(excel_file)

    # Step 2: Initialize OpenAI client and Process User Prompt with GPT-4
    client = openai.OpenAI(api_key=openai_api_key)

    try:
        response = client.chat.completions.create(
            model="gpt-4",  # Specify the GPT-4 model
            messages=[{"role": "system", "content": "You are a helpful assistant."},
                      {"role": "user", "content": user_prompt}],
            max_tokens=100  # Adjust as necessary
        )
    except Exception as e:
        print(f"Error in calling OpenAI API: {e}")
        return

    # Interpret the response to decide what chart to create
    chart_instructions = interpret_openai_response(response)

    # Step 3: Create Visualization Based on Instructions
    chart = create_chart_based_on_instructions(df, chart_instructions)

    # Step 4: Return or Display the Chart
    return chart

def interpret_openai_response(response):
    # Extract and return the instructions for creating the chart
    try:
        # Assuming the last message in the conversation will contain the chart instructions
        
        return response['choices'][0]['message']['content'].strip()
    except KeyError:
        return ""

def create_chart_based_on_instructions(df, instructions):
    # Create a chart based on the instructions from GPT-4
    # Placeholder implementation
    plt.figure(figsize=(10, 6))
    plt.plot(df[df.columns[0]], df[df.columns[1]])
    plt.xlabel(df.columns[0])
    plt.ylabel(df.columns[1])
    plt.title('Chart based on GPT-4 Instructions')
    plt.show()
    return plt
# # Example usage
# chart = generate_visualization_gpt4('data.xlsx', 'Please create a line plot of the first two columns', 'your-openai-api-key')


generate_visualization_gpt4('tencent_report_extracted_tables.xlsx', 'Please visualize the forth table in a proper way', openai_api_key)
