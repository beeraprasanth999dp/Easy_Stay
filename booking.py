class Guests:
    def __init__(self, guest_name, mobile_number, email):
        self.__guest_name = guest_name
        self.__mobile_number = mobile_number
        self.__email = email
    def Guest_name(self):
        return self.__guest_name
    def mobile_number(self):
        return self.__mobile_number
    def email_id(self):
        return self.__email
    def __str__(self):
        return f"Guest Name: {self.__guest_name}, Mobile: {self.__mobile_number}"
class Bookings:
    def __init__(self, booking_id, guest_id, room_no, room_type,
                 checkin, checkout, guest_count, breakfast,
                 total_amount, status="CONFIRMED"):

        self.__booking_id = booking_id
        self.__guest_id = guest_id
        self.__room_no = room_no
        self.__room_type = room_type
        self.__checkin = checkin
        self.__checkout = checkout
        self.__guest_count = guest_count
        self.__breakfast = breakfast
        self.__total_amount = total_amount
        self.__status = status

    def get_booking_id(self):
        return self.__booking_id
    def get_guest_id(self):
        return self.__guest_id
    def get_room_no(self):
        return self.__room_no
    def get_room_type(self):
        return self.__room_type
    def get_checkin(self):
        return self.__checkin
    def get_checkout(self):
        return self.__checkout
    def get_guest_count(self):
        return self.__guest_count
    def get_breakfast(self):
        return self.__breakfast
    def get_total_amount(self):
        return self.__total_amount
    def get_status(self):
        return self.__status
    def set_status(self, status):
        self.__status = status

    def __str__(self):
        return f"Booking ID: {self.__booking_id}, Room: {self.__room_no}, Status: {self.__status}"
