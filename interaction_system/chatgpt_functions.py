import os
from dotenv import load_dotenv
from openai import OpenAI

from interaction_system.interaction_history import get_main_emotion

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

messages_array = [
    {"role": "system", "content": "You are role-playing as a friendly bartender. Try to maintain conversation about how the client feels. Don't give very long responses. I will also provide information about how the user feels, keep that into account."},
]

def add_message_to_array(role, content):
    """
    Adds a message to the messages_array.
    """
    messages_array.append({"role": role, "content": content})

def get_last_message():
    """
    Returns the last message in the messages_array.
    """
    return messages_array[-1]["content"]

def chat_with_openai(user_input):
    """
    Sends user input to OpenAI's ChatGPT API and returns the response.
    """
    client = OpenAI()

    user_emotion = get_main_emotion()

    user_input = f"[User feels: {user_emotion}] User message: {user_input}"

    add_message_to_array("user", user_input)
    print(f"Sending messages to OpenAI: {messages_array}")

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages_array,
        )
        print(f"Received response from OpenAI: {response}")
        response_message = response.choices[0].message.content
        add_message_to_array("assistant", response_message)
        return response_message.strip()
    except Exception as e:
        print(f"Error communicating with OpenAI: {e}")
        return "Sorry, I couldn't process your request."