# -*- coding: utf-8-*-
from sys import maxint
import random

WORDS = []

PRIORITY = -(maxint + 1)


def handle(text, mic, profile):
    """
        Reports that the user has unclear or unusable input.

        Arguments:
        text -- user-input, typically transcribed speech
        mic -- used to interact with the user (for both input and output)
        profile -- contains information related to the user (e.g., phone
                   number)
    """

    messages = ["I'm sorry, could you repeat that sir?",
                "My apologies, could you try saying that again, sir?",
                "Say that again, i am having trouble hearing you?", "I beg your pardon, microphone input is low?"]

    message = random.choice(messages)

    mic.say(message)


def isValid(text):
    return True
