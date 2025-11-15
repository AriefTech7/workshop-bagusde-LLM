from config import client

# function untuk respon dari ai yang ada animasi 
def respon_stream(history):
    response = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=history,
        stream=True
    )
    full_response = ""
    print("AI: ", end="")
    for chunk in response:
        if chunk.choices[0].delta.content is not None:
            content = chunk.choices[0].delta.content
            full_response += content
            
        print(content, end="", flush=True)
    print()
    return full_response