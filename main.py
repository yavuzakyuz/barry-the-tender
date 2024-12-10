import threading
import backend
import interaction
import atexit


def main():
    t_interaction = threading.Thread(target=interaction.main_interaction)
    t_backend = threading.Thread(target=backend.emotion_detection)

    t_backend.start()
    t_interaction.start()

    t_interaction.join()
    t_backend.join()
    return 0

if __name__ == "__main__":
    main()

