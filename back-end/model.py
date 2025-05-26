from config import client, MODEL_NAME

def generate_content(messages):
    formatted_messages = [{"role": "system", "content": messages[0]}] + [
        {"role": "user" if i % 2 == 1 else "assistant", "content": msg}
        for i, msg in enumerate(messages[1:], start=1)
    ]

    print("Formatted messages para a API:", formatted_messages)

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=formatted_messages,
        temperature=0.7,
        max_tokens=800
    )
    print("Resposta da API:", response.choices[0].message.content)
    return response.choices[0].message.content
