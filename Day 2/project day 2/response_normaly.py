from config import client

# function untuk respon dari ai yang normal
def respon_normaly(history):
    response = client.chat.completions.create(
    model='gpt-4o-mini',
    messages=history
    )
    print(f"AI: {response.choices[0].message.content}")
    return response.choices[0].message.content