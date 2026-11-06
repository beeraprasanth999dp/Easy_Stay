import sqlite3
from booking import Guests,Bookings 
class guestservices():
    def register_guest(self,guest):
        connection=sqlite3.connect("stayeasy.db")
        cursor=connection.cursor()
        cursor.execute("select guest_id from guests where mobile_number=?",(guest.mobile_number(),))
        result=cursor.fetchone()
        if result:
            guest_id=result[0]
            print("guest is already registred")
            connection.close()
            return guest_id
        cursor.execute("""
                       insert into guests(guest_name,mobile_number,email)values(?,?,?)
                       """,(guest.Guest_name(),guest.mobile_number(),guest.email_id()))
        guest_id=cursor.lastrowid
        connection.commit()
        connection.close()
        print("Guest registred successfully!")
        return guest_id
    