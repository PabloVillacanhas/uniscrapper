from abc import ABC, abstractmethod


class Scrapper(ABC):

    def __init__(self):
        super(Scrapper, self).__init__()

    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def getData(self):
        pass
