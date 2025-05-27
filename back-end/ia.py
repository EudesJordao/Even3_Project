from config import client

def generate_content(messages):
    formatted_messages = [{"role": "system", "content": messages[0]}] + [
        {"role": "user" if i % 2 == 1 else "assistant", "content": msg}
        for i, msg in enumerate(messages[1:], start=1)
    ]

    response = client.chat.completions.create(
        model="gpt-4",
        messages=formatted_messages,
        temperature=0.7,
        max_tokens=800
    )
    return response.choices[0].message.content
