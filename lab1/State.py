from typing import List
from pygame import Surface
from Figure import Figure

class State():
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(State, cls).__new__(cls, *args, **kwargs)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if not self._initialized:
            self.user_figure: Figure | None = None
            self.figures: List[Figure] = []
            self.screen: Surface | None = None
            self._initialized = True