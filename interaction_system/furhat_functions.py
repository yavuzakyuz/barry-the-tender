from interaction_system.chatgpt_functions import add_message_to_array
from interaction_system.gestures import GESTURE_BIG_SMILE, GESTURE_RESET_NEUTRAL
from interaction_system.scripts import STARTER_TEXT_NEUTRAL, STARTER_TEXT_SURPRISED, STARTER_TEXT_ANGRY, \
    STARTER_TEXT_SAD, STARTER_TEXT_HAPPY


def start_conversation(furhat, emotion):
    if emotion == 'happy':
        starter_text = STARTER_TEXT_HAPPY
    elif emotion == 'sad':
        starter_text = STARTER_TEXT_SAD
    elif emotion == 'angry':
        starter_text = STARTER_TEXT_ANGRY
    elif emotion == 'surprised':
        starter_text = STARTER_TEXT_SURPRISED
    else:
        starter_text = STARTER_TEXT_NEUTRAL

    starter_gesture = GESTURE_BIG_SMILE

    # TODO: Might also want to add a different gesture based on the emotion
    furhat.gesture(body=starter_gesture)
    furhat.say(text=starter_text, blocking=True)
    add_message_to_array('assistant', starter_text)


def reset_neutral(furhat):
    furhat.gesture(body=GESTURE_RESET_NEUTRAL)
    furhat.say_stop()

def react_to_emotion(furhat, emotion):
    if emotion == 'happy':
        react_gesture = "BigSmile"
    elif emotion == 'sad':
        react_gesture = "BrowFrown"
    elif emotion == 'angry':
        react_gesture = "Surprised"
    elif emotion == 'surprised':
        react_gesture = "BrowRaise"

    furhat.gesture(name=react_gesture)