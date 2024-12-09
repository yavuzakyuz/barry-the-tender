import threading

EMOTION_ESTIMATION_FRAME = 10
MAX_HISTORY_SIZE = 100

interactionHistory = []
interactionHistory_lock = threading.Lock()

def get_interaction_history():
    with interactionHistory_lock:
        return interactionHistory

def add_interaction_to_history(interaction):
    with interactionHistory_lock:
        interactionHistory.append(interaction)
        if len(interactionHistory) > MAX_HISTORY_SIZE:
            interactionHistory.pop(0)

def clear_interaction_history():
    with interactionHistory_lock:
        interactionHistory.clear()

def get_main_emotion():
    with interactionHistory_lock:
        if len(interactionHistory) < EMOTION_ESTIMATION_FRAME:
            return None

        interactionHistory_0 = [interaction for interaction in interactionHistory if interaction['person'] == 0]
        emotions = [interaction['emotion']
                    for interaction
                    in interactionHistory_0[-EMOTION_ESTIMATION_FRAME:]]
        # print(interactionHistory)
        # print(interactionHistory_0)
    if emotions:
        emotion = max(set(emotions), key=emotions.count)
        return emotion