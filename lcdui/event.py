from enum import Enum


class EventType(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3
    ACTION = 4
    BACK = 5
    INPUT = 6


class Event:
    def __init__(self, type):
        self.type = type


class InputEvent:
    def __init__(self, value):
        self.type = EventType.INPUT
        self.value = value
