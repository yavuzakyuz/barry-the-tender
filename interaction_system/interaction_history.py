EMOTION_ESTIMATION_FRAME = 10
MAX_HISTORY_SIZE = 100

interactionHistory = []

def get_interaction_history():
    return interactionHistory

def add_interaction_to_history(interaction):
    interactionHistory.append(interaction)
    if len(interactionHistory) > MAX_HISTORY_SIZE:
        interactionHistory.pop(0)

def clear_interaction_history():
    interactionHistory.clear()

def get_main_emotion():
    emotions = [interaction['emotion'] for interaction in interactionHistory[-EMOTION_ESTIMATION_FRAME:]]
    emotion = max(set(emotions), key=emotions.count)
    return emotion