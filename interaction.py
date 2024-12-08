from furhat_remote_api import FurhatRemoteAPI

from interaction_system.chatgpt_functions import chat_with_openai
from interaction_system.furhat_functions import start_conversation, reset_neutral
from interaction_system.interaction_history import add_interaction_to_history, get_main_emotion

def main():
    furhat = FurhatRemoteAPI("localhost")

    # Add 40 interactions to the history for testing purposes
    for i in range(40):
        add_interaction_to_history({
            'emotion': 'sad',
            'timestamp': '2021-10-10T10:00:00',
        })

    # Get the most frequent emotion in the last 10 interactions
    emotion = get_main_emotion()

    start_conversation(furhat, emotion)
    reset_neutral(furhat)

    userMessage = "The weather is sad today."
    # TODO: Change the FurHat gesture somewhere here
    response_text = chat_with_openai(userMessage)
    furhat.say(text=response_text, blocking=True)

    userMessage = "I think I could use a cocktail. What do you recommend?"
    # TODO: Change the FurHat gesture somewhere here
    response_text = chat_with_openai(userMessage)
    furhat.say(text=response_text, blocking=True)

main()