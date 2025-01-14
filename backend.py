import cv2
import torch
from feat import Detector
from sklearn.svm import SVC
import pickle
import time
import logging
import warnings 

logging.getLogger('cv2').setLevel(logging.ERROR)
logging.getLogger('torch').setLevel(logging.ERROR)
logging.getLogger().setLevel(logging.ERROR)
logging.getLogger('feat').setLevel(logging.ERROR)
logging.getLogger('torch').setLevel(logging.ERROR)

# Suppress warnings
warnings.filterwarnings("ignore")

from interaction_system.interaction_history import add_interaction_to_history, get_main_emotion

emotion = {
    "angry": 0,
    "disgust": 1,
    "fear": 2,
    "happy": 3,
    "sad": 4,
    "surprise": 5,
    "neutral": 6
}

with open('model_svc.pkl', 'rb') as f:
    model = pickle.load(f)
detector = Detector(device='cuda' if torch.cuda.is_available() else 'cpu')

def emotion_detection():
    cam = cv2.VideoCapture(0)

    while True:
        check, frame = cam.read()
        if not check:
            cam.release()
            break

        new_frame, aus, em = feeling(frame, True, True)
        for n, emotion_person in enumerate(em):
            print(f"Emotion of person {n}: {emotion_person}")
            add_interaction_to_history({
                'emotion': emotion_person,
                'person': n,
                'timestamp': time.time(),
            })

            # Tuple if you want to detect more people
            # add_interaction_to_history((emotion_person, n))
        print(get_main_emotion())

    cam.release()


def feeling(image, enable_aus=False, enable_emotion=False):
    face = detector.detect_faces(image)

    aus = None
    emotion_str = None

    if enable_emotion or enable_aus:
        landmark = detector.detect_landmarks(image, face)
        if enable_aus:
            aus = detector.detect_aus(image, landmark)
        if enable_emotion:
            emotion_str = model.predict(aus[0])

    return image, aus, emotion_str

if __name__ == "__main__":
    emotion_detection()