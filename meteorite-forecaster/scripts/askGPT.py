import openai
openai.api_key =


def prompt(text):
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": text}]
    )

    return response.choices[0].message.content.strip()
