from abc import ABC,abstractmethod
class Room(ABC):
    def __init__(self,room_no,floor):
        self.room_no=room_no
        self.floor=floor
    @abstractmethod
    def get_tarrif(self):
        pass
    @abstractmethod
    def get_max_guest(self):
        pass
    @abstractmethod
    def get_breakfast(self):
        pass
    @abstractmethod
    def get_extra_guest_charge(self):
        pass
    def __str__(self):
        return f"Room No:{self.room_no},Floor:{self.floor}"
    
class StandardRoom(Room):
    def __init__(self, room_no, floor):
        super().__init__(room_no, floor)
    def get_tarrif(self):
        return 2500
    def get_max_guest(self):
        return 2
    def get_breakfast(self):
        return False
    def get_extra_guest_charge(self):
        return 0
class DeluxeRoom(Room):
    def __init__(self, room_no, floor):
        super().__init__(room_no, floor)
    def get_tarrif(self):
        return 4000
    def get_max_guest(self):
        return 3
    def get_breakfast(self):
        return True
    def get_extra_guest_charge(self):
        return 800
class SuitRoom(Room):
    def __init__(self, room_no, floor):
        super().__init__(room_no, floor)
    def get_tarrif(self):
        return 7500
    def get_max_guest(self):
        return 4
    def get_breakfast(self):
        return True
    def get_extra_guest_charge(self):
        return 800

        