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

    # Reduce history size. Keep the first element as the system message and then the last 6 messages
    if len(messages_array) > 7:
        temp_messages_array = messages_array[:1] + messages_array[-6:]
    else:
        temp_messages_array = messages_array

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=temp_messages_array,
        )
        print(f"Received response from OpenAI: {response}")
        response_message = response.choices[0].message.content
        add_message_to_array("assistant", response_message)
        return response_message.strip()
    except Exception as e:
        print(f"Error communicating with OpenAI: {e}")
        return "Sorry, I couldn't process your request."


def decide_state_gpt(user_input, current_state):
    client = OpenAI()
    prompt = (
        "You are an intent classifier for a bartender. I'll send you both the current context with a keyword like 'greet', 'menu', 'recommend' etc. Based on the following user message, and this state "
        "determine the appropriate NEXT context BE FAST:\n"
        "- If the message is about the drink menu, respond with 'menu'.\n"
        "- If it's about drink recommendations, respond with 'recommend'.\n"
        "- If it doesn't change the current context DO NOT FORGET, YOU'RE GUESSING WHAT THE ROBOT WILL SAY NEXT, IF USER ASKS/WANTS MENU THEN YOU HAVE TO MOVE ON TO MENU CONTEXT, RIGHT?\n"
        f"Current state: {current_state}"
        f"User message: {user_input}"
        "YOU CAN ONLY GIVE ONE OF THESE: [greeting, menu, recommendation]"
    )

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": prompt}],
        )
        intent = response.choices[0].message.content.strip()
        print(f"Intent detected: {intent}")
        return intent
    except Exception as e:
        print(f"Error determining intent with GPT: {e}")
        return current_state  