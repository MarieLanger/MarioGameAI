"""
Todo: This file is redundant but for now I leave it here
"""

from abc import ABC
from abc import abstractmethod

class BasicController(ABC):

    @abstractmethod
    def test(self):
        pass


class HumanController(BasicController):
    def __init__(self):
        print("Class created")

    #overriding abstract method
    def test(self):
        return 0


