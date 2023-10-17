from typing import List
from pygame import Surface
from Figure import Figure
from constants import MovementMode


class SingletonMetaclass(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class State(metaclass=SingletonMetaclass):
    def __init__(self):
        self.user_figure: Figure | None = None
        self.figures: List[Figure] = []
        self.screen: Surface | None = None
        self.movement_mode = MovementMode.Linear
        self.game_run = True
