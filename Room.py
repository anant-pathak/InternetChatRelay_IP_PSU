import json
import copy
import Message

class Room:
    def __init__(self, name):
        self.name = name
        self.messages = []
        self.members = []

    def addMessage(self, Message):
        self.messages.append(Message)
    
    def returnDict(self):
        dict = copy.deepcopy(self.__dict__)
        dict['messages'] = []
        for i in self.messages:
            dict['messages'].append(i.__dict__)
        return dict