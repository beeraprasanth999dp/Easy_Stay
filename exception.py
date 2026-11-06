class StayEasy(Exception):
    pass
class Room_unavailable(StayEasy):
    pass
class Invalid_Date(StayEasy):
    pass
class Booking_NotFound(StayEasy):
    pass
class Invalid_status(StayEasy):
    pass
class Guest_limit(StayEasy):
    pass
class Invalid_input(StayEasy):
    pass