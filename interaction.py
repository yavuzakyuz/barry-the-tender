from furhat_remote_api import FurhatRemoteAPI

from interaction_system.chatgpt_functions import chat_with_openai
from interaction_system.furhat_functions import start_conversation, reset_neutral
from interaction_system.interaction_history import add_interaction_to_history, get_main_emotion

def main():
    furhat = FurhatRemoteAPI("localhost")

    # Add 40 interactions to the history for testing purposes - will be deleted
    for i in range(40):
        add_interaction_to_history({
            'emotion': 'angry',
            'timestamp': '2021-10-10T10:00:00',
        })

    # Get the most frequent emotion in the last 10 interactions
    emotion = get_main_emotion()

    start_conversation(furhat, emotion)
    reset_neutral(furhat)

    while True:
        user_message = furhat.listen().message;
        emotion = get_main_emotion()
        print(f"User message: {user_message}")

        # TODO: Change the FurHat gesture somewhere here - I would say it should react to the user's emotion like happy-happy, sad-concerned, angry-surprised, etc

        response_text = chat_with_openai(user_message)
        furhat.say(text=response_text, blocking=True)

main()