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
    
    def addMember(self, member):
        self.members.append(member)
    
    def removeMember(self, member):
        self.members.remove(member)
    
    def returnDict(self):
        dict = copy.deepcopy(self.__dict__)
        dict['messages'] = []
        for i in self.messages:
            dict['messages'].append(i.__dict__)
        return dict