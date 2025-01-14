from time import sleep

import numpy as np
from furhat_remote_api import FurhatRemoteAPI

from interaction_system.chatgpt_functions import chat_with_openai, decide_state_gpt
from interaction_system.furhat_functions import start_conversation, reset_neutral
from interaction_system.gestures import GESTURE_RESET_NEUTRAL
from interaction_system.interaction_history import add_interaction_to_history, get_main_emotion

class StateManager:
    """State manager singleton"""
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(StateManager, cls).__new__(cls)
            cls._instance.current_state = "greeting"
            cls._instance.state_counters = {}
            cls._instance.state_flow = ["greeting", "menu", "recommend", "order", "bye"]
        return cls._instance

    def transition(self, new_state):
        if new_state not in self.state_counters:
            self.state_counters[new_state] = 0
        elif new_state == self.current_state:
            self.state_counters[new_state] += 1
        else:
            self.state_counters[new_state] = 0

        print(f"Transitioning from {self.current_state} to {new_state}")
        self.current_state = new_state

    def get_current_state(self):
        return self.current_state

    def get_state_counter(self):
        return self.state_counters.get(self.current_state, 0)

    def get_next_state(self):
        try:
            current_index = self.state_flow.index(self.current_state)
            return self.state_flow[current_index + 1]
        except (ValueError, IndexError):
            return None

def greeting_interaction(state_manager, furhat, emotion):
    print("COUNTER " + "of intent " + state_manager.get_current_state() + " EQUALS  =" + str(state_manager.get_state_counter()))
    if state_manager.get_state_counter() == 0:
        furhat.say(text="sorry to keep you waiting, how can I help?", blocking=True)
   
    next_state_intent = intent_grabber(furhat.listen().message, state_manager.get_current_state()) 
    while not next_state_intent:
        response = "sorry, what was that again?"
        next_state_intent = intent_grabber(furhat.listen().message, state_manager.get_current_state()) 
    
    if(next_state_intent == "menu"):
        response = "alright, I'll tell you what we have, just one second"
    elif(next_state_intent == "recommend"):
        response = "we got some fire coctails, let me line them up for you"

    elif(next_state_intent == "greeting"):
        response = "sorry, you were saying?"
    
    state_manager.transition(next_state_intent)
    return response

def menu_interaction(state_manager, furhat, emotion):
    print("COUNTER " + "of intent " + state_manager.get_current_state() + " EQUALS  =" + str(state_manager.get_state_counter()))
    if state_manager.get_state_counter() == 0:
        furhat.say(text="So we have vodka-cran, tequila-lime, jack and coke. What do you like? I can do a custom for you if you like?", blocking=True)
    else:
        user_response = furhat.listen().message
        next_state = state_manager.get_next_state()
        gpt_response = chat_with_openai(f"The user continued the conversation with this (review your past interaction here): '{user_response}'. "
        f" Now if you received an answer you need to move the conversation forward gracefully follow into the next section in conversation, "
        f" which is '{next_state}' ")
        next_state_intent = intent_grabber(user_response, state_manager.get_current_state())
        state_manager.transition(next_state_intent)
        return gpt_response
    
    user_response = furhat.listen().message
    print(f"User response in menu: {user_response}")

    next_state_intent = intent_grabber(user_response, state_manager.get_current_state())
    

    response = "Sorry, what was that again?"
    if next_state_intent == "recommend":
        response = "Okay, let me think of something."
        state_manager.transition("recommend")
    elif next_state_intent == "order":
        response = "Okay, let's take the orders!"
        state_manager.transition("order")
    else:
        response = "Sorry, you were saying?"

    state_manager.transition(next_state_intent)
    return response

def recommend_interaction(state_manager, furhat, emotion):
    print("COUNTER EQUALS  =" + str(state_manager.get_state_counter()))
    next_state = state_manager.get_next_state()
    next_state_intent = ''

    if state_manager.get_state_counter() == 0:
        furhat.say(text="Do you have any preference/allergies?", blocking=True)
        user_response = furhat.listen().message
        if(emotion == "neutral"): 
            gpt_response = chat_with_openai(f"The user continued the conversation with this (review your past interaction here): '{user_response}'. "
            f" You need to recommend a drink to the user based on their preferences and current emotional state (which you have), "
            f" gracefully move conversation to the '{next_state}' DO NOT SAY SINCE YOU'RE FEELING BLABLA, JUST ACT ACCORDINGLY")
            next_state_intent = intent_grabber(user_response, state_manager.get_current_state())
            state_manager.transition(next_state_intent)
            return gpt_response
        elif(emotion == "happy"):
            #furhat.gesture(body=GESTURE_RESET_NEUTRAL)
            gpt_response = chat_with_openai(f"The user continued the conversation with this (review your past interaction here): '{user_response}'. "
            f" You need to recommend a drink to the user based on their preferences, and make a light-hearted joke while you're on it DO NOT SAY SINCE YOU'RE FEELING BLABLA, JUST ACT ACCORDINGLY"
            f" gracefully move conversation to the '{next_state}'")
            next_state_intent = intent_grabber(user_response, state_manager.get_current_state())
            state_manager.transition(next_state_intent)
            return gpt_response
        else:
            gpt_response = chat_with_openai(
                f"The user continued the conversation with this (review your past interaction here): '{user_response}'. "
                f" You need to recommend a drink to the user based on their preferences and current emotional state (which you have), "
                f" gracefully move conversation to the '{next_state}' DO NOT SAY SINCE YOU'RE FEELING BLABLA, JUST ACT ACCORDINGLY")
            next_state_intent = intent_grabber(user_response, state_manager.get_current_state())
            state_manager.transition(next_state_intent)
            return gpt_response

    else:
        user_response = furhat.listen().message
        next_state = state_manager.get_next_state()
        gpt_response = chat_with_openai(f"The user continued the conversation with this (review your past interaction here): '{user_response}'. "
        f" Now if you received an answer you need to move the conversation forward gracefully follow into the next section in conversation, "
        f" which is '{next_state}' Also notice and recommend based on user's emotional state (which you have) DO NOT SAY SINCE YOU'RE FEELING BLABLA, JUST ACT ACCORDINGLY")
        print("next state: " + next_state)
        state_manager.transition(next_state)
        return gpt_response
    
    response = "Sorry, what was that again?"
    if next_state_intent == "order":
        response = "Do you want to order now?"
        state_manager.transition("order")
    else:
        response = "Sorry, you were saying?"

    state_manager.transition(next_state_intent)
    return response

def order_interaction(state_manager, furhat, emotion):
    print("COUNTER " + "of intent " + state_manager.get_current_state() + " EQUALS  =" + str(state_manager.get_state_counter()))
    if state_manager.get_state_counter() == 0:
        furhat.say(text="Alright, let me write down the order.", blocking=True)
    else:
        user_response = furhat.listen().message
        next_state = state_manager.get_next_state()
        gpt_response = chat_with_openai(f"The user continued the conversation with this (review your past interaction here): '{user_response}'. "
        f" Now if you received an answer you need to move the conversation forward gracefully follow into the next section in conversation, "
        f" which is '{next_state}' ")
        next_state_intent = intent_grabber(user_response, state_manager.get_current_state())
        state_manager.transition(next_state_intent)
        return gpt_response
    
    user_response = furhat.listen().message
    print(f"User response in menu: {user_response}")

    next_state_intent = intent_grabber(user_response, state_manager.get_current_state())
    print(f"Detected intent: {next_state_intent}")

    response = "Sorry, what was that again?"
    if next_state_intent == "recommend":
        response = "Okay, let me think of something."
        state_manager.transition("recommend")
    elif next_state_intent == "order":
        response = "Okay, let's take the orders!"
        state_manager.transition("order")
    else:
        response = "Sorry, you were saying?"

    state_manager.transition(next_state_intent)
    return response

def intent_grabber(user_response, current_state):
    print("Intent grabber trying with user response: " + user_response + "\n")
    if("menu" in user_response.lower()):
        print(f"Detected intent: menu. Moving: " + current_state + " -> " + "menu")
        return "menu"
    elif("recommend" in user_response.lower()):
        print(f"Detected intent: recommend. Moving: " + current_state + " -> " + "recommend")
        return "recommend"
    elif("order" in user_response.lower()): 
        print(f"Detected intent: order. Moving: " + current_state + " -> " + "order")
        return "order"
    else:
        interpreted_next_state = decide_state_gpt(user_response, current_state)
        print(f"GPT Detected intent: {interpreted_next_state}. Moving: " + current_state + " -> " + interpreted_next_state)
        return interpreted_next_state


def script_interaction(state_manager, furhat, emotion, user_input):
    gpt_response = chat_with_openai(user_input)
    return gpt_response


def main_interaction():
    furhat = FurhatRemoteAPI("localhost")
    furhat.say(text="I'll see you in a sec, mate!", blocking=True)
    state_manager = StateManager()

    # Add 40 interactions to the history for testing purposes - will be deleted
    # for i in range(40):
    #     add_interaction_to_history({
    #         'emotion': 'happy',
    #         'timestamp': '2021-10-10T10:00:00',
    #         'person': 0,
    #     })

    while get_main_emotion() is None:
        sleep(0.2)

    emotion = get_main_emotion()
    start_conversation(furhat, emotion)
    reset_neutral(furhat)

    while True:
        current_state = state_manager.get_current_state()
        emotion = get_main_emotion()
        response = "could you repeat that?"

        #print(f"Emotion: {emotion}")
        #print(f"User message: {user_message}")

        # TODO: Change the FurHat gesture somewhere here - I would say it should react to the user's emotion like happy-happy, sad-concerned, angry-surprised, etc
        
        # user_input = furhat.listen().message
        # response = script_interaction(state_manager, furhat, emotion, user_input)
        # furhat.say(text=response, blocking=True)

        if current_state == "greeting":
             furhat.say(text=greeting_interaction(state_manager, furhat, emotion), blocking=True)

        elif current_state == "menu":
            furhat.say(text=menu_interaction(state_manager, furhat, emotion), blocking=True)

        elif current_state == "recommend":
             furhat.say(text=recommend_interaction(state_manager, furhat, emotion), blocking=True)
        
        elif current_state == "order":
             furhat.say(text=order_interaction(state_manager, furhat, emotion), blocking=True)

if __name__ == "__main__":
    main_interaction()