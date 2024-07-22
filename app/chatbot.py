import openai

openai.api_key = 'sk-proj-D4WcxqGAVE5GyrVRXkk2T3BlbkFJOsWR1x40PpznTaUvnKhh'

def generate_response(question, tml_data):
    prompt = f"""
    TML File Content:
    {tml_data}

    User Question: {question}

    Provide insights about the TML file based on the question:
    """

    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=150
    )

    return response.choices[0].text.strip()



