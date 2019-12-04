import enum

class MessageType(enum.Enum):
    CreateRoom = 1
    ListAllRooms = 2
    JoinRoom = 3
    LeaveRoom = 4
    ListMembersForRoom = 5
    SendMsgRoom = 6
    CheckForARoom = 7
    InitUsername = 8


class Message:
    def __init__(self, msg_type, sender, destination, message):
        self.msg_type = msg_type
        self.sender = sender
        self.destination = destination
        self.message = message



    