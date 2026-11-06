from datetime import datetime
from room_service import RoomService
import sqlite3
from pricing import Pricing
from exception import Room_unavailable,Invalid_Date,Booking_NotFound,Invalid_status,Guest_limit,Invalid_input 
class BookingService:
    def check_room_type(self, rooms, room_type, guest_count):
        rooms_available=[]
        for room in rooms:
            if room_type=="standard":
                if room.get_max_guest()!=2:
                    continue
            elif room_type=="deluxe":
                if room.get_max_guest()!=3:
                    continue
            elif room_type=="suite":
                if room.get_max_guest()!=4:
                    continue
            if guest_count > room.get_max_guest():
                continue
            rooms_available.append(room)
        return rooms_available
    
    def check_room_availability(self,rooms,checkin,checkout,bookings):
        availabale_rooms=[]
        checkin=datetime.strptime(checkin,"%d-%m-%Y").date()
        checkout=datetime.strptime(checkout,"%d-%m-%Y").date()
        for room in rooms:
            available=True
            for booking in bookings:
                if room.room_no==booking[0]:
                    old_checkin=datetime.strptime(booking[1],"%d-%m-%Y").date()
                    old_checkout=datetime.strptime(booking[2],"%d-%m-%Y").date()
                    if checkin <old_checkout and checkout>old_checkin:
                        available=False
                        break
            if available:
                availabale_rooms.append(room)
        return availabale_rooms
    def get_available_rooms(self,rooms,room_type,guest_count,checkin,checkout,bookings):
        room_list=self.check_room_type(rooms,room_type,guest_count)
        available_rooms=self.check_room_availability(
            room_list,checkin,checkout,bookings
        )
        return available_rooms
    def select_room(self,rooms):
        if len(rooms)==0:
            print("No rooms available")
            return None
        select_room=rooms[0]
        for room in rooms:
            if room.room_no<select_room.room_no:
                select_room=room
        return select_room
    def save_bookings(self,guest_id,room,room_type,checkin,checkout,guest_count,breakfast,total_amount,bookings,night_details):
        available_rooms = self.check_room_availability(
            [room], checkin, checkout, bookings
        )

        if len(available_rooms)==0:
            print("Room is already booked!")
            return
        connection=sqlite3.connect("stayeasy.db")
        cursor =connection.cursor()
        cursor.execute("""
            insert into bookings
            (guest_id,room_no,room_type,checkin,checkout,
            guest_count,breakfast,total_amount,status)
            values (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            guest_id,
            room.room_no,
            room_type,
            checkin,
            checkout,
            guest_count,
            breakfast,
            total_amount,
            "CONFIRMED"
        ))
        
        booking_id=cursor.lastrowid
        print("Your Bookinf ID:",booking_id)

        for night in night_details:
            cursor.execute("""
                insert into booking_nights
                (booking_id,stay_date,room_charge,extra_guest_charge,
                breakfast_charge,discount,gst)
                vakues(?, ?, ?, ?, ?, ?, ?)
            """, (
                booking_id,
                night["stay_date"],
                night["room_charge"],
                night["extra_guest_charge"],
                night["breakfast_charge"],
                0,
                0
            ))
        connection.commit()
        connection.close()
        print("Booking saved successfully")
    def check_in(self,booking_id):
            connection=sqlite3.connect("stayeasy.db")
            cursor=connection.cursor()  
            cursor.execute("""
                           select checkin,status from bookings where booking_id=?
                           """,(booking_id,))
            booking=cursor.fetchone()
            if booking is None:
                print("Booking ID not found")
                connection.close()
                return
            check_in=datetime.strptime(booking[0],"%d-%m-%Y").date()
            status=booking[1]
            if status != "CONFIRMED":
                print("only confirmed booking can be checked in")
                connection.close()
                return
            if check_in!=datetime.today().date():
                print("check-in is allowed only on the booking date")
                connection.close()
                return
            cursor.execute("""
                           update bookings set status=? where booking_id=?
                           """,("CHECK_IN",booking_id))
            connection.commit()
            connection.close()  
            print("Guest checked in sucessfully")
    def check_out(self,booking_id):
        connection=sqlite3.connect("stayeasy.db")
        cursor=connection.cursor()
        
        cursor.execute("""
                       select b.booking_id,b.guest_id,b.room_no,b.room_type,
                        b.checkin,b.checkout,b.guest_count,
                        b.total_amount,b.status,
                        g.guest_name,g.mobile_number,g.email
                        from bookings b
                        join guests g ON b.guest_id=g.guest_id
                        where b.booking_id=?
                       """,(booking_id,))
        booking=cursor.fetchone()
        if booking is None:
            print("Booking Id not found")
            connection.close()
            return
        if booking[8]!="CHECK_IN":
            print("only checked_in bookings can check out")
            connection.close()
            return
        

        cursor.execute("""
                       select stay_date,room_charge,extra_guest_charge,
                       breakfast_charge,discount,gst
                       from booking_nights where booking_id=? """,(booking_id,))  
        nights=cursor.fetchall()
        
        invoice_file="invoices/BK"+str(booking_id)+".txt"
        file=open(invoice_file,"w")
        file.write("========== STAYEASY HOTEL ==========\n")
        file.write("              INVOICE\n")
        file.write("====================================\n\n")
        file.write("Booking ID:"+str(booking[0])+"\n")
        file.write("Guest Name:"+booking[9]+"\n")
        file.write("Mobile Number:"+booking[10]+"\n")
        file.write("Email:"+booking[11]+"\n")
        file.write("Room Number:"+str(booking[2])+"\n")
        file.write("Room Type:"+booking[3]+"\n")
        file.write("Check-in:"+booking[4]+"\n")
        file.write("Check-out:"+booking[5]+"\n")
        file.write("Guest Count:"+str(booking[6])+"\n")
        file.write("\n========== NIGHT DETAILS ==========\n")
        for night in nights:
            file.write("\nStay Date:"+night[0]+"\n")
            file.write("Room Charge Rs:"+str(night[1])+"\n")
            file.write("Extra Guest Charge Rs:"+str(night[2])+"\n")
            file.write("Breakfast Charge Rs:"+str(night[3])+"\n")
            file.write("Discount:"+str(night[4])+"\n")
            file.write("GST: Rs"+str(night[5])+"\n")
        file.write("\n========== BILL SUMMARY ==========\n")
        file.write("Total Amount Paid: Rs"+str(booking[7])+"\n")
        file.write("====================================\n")
        file.close()
        cursor.execute("update bookings set status=? where booking_id=?",("CHECK_OUT",booking_id))
        connection.commit()
        print("Guest checked out successfully!")
        print("Invoice generated:",invoice_file)
        connection.close()
    def cancel_booking(self,booking_id):
        connection=sqlite3.connect("stayeasy.db")
        cursor=connection.cursor()
        cursor.execute("""
                    select checkin,total_amount,status from bookings where booking_id=?
                    """,(booking_id,))
        booking=cursor.fetchone()
        if booking is None:
            print("booking ID nto found")
            connection.close()
            return
        checkin_date=datetime.strptime(booking[0],"%d-%m-%Y").date()
        total_amount=booking[1]
        status=booking[2]
        if status!="CONFIRMED":
            print("Only confirmed bookings can be cancelled")
            connection.close()
            return
        day_before=(checkin_date-datetime.today().date()).days
        if day_before>=7:
            refund=total_amount
        elif day_before>=2:
            refund=total_amount*0.50
        else:
            refund=0
        retained_amount=total_amount-refund
        cursor.execute("""
                    update bookings set status=? where booking_id=?
                    """,("CANCELLED",booking_id))
        connection.commit()
        connection.close()
        print("Booking cancelled suceessfully")
        print("Total amount:" ,total_amount)
        print("Refund amount:",refund)
        print("Amount retianed:",retained_amount)
    
    def view_bookings(self,booking_id):
        connection=sqlite3.connect("stayeasy.db")
        cursor=connection.cursor()
        cursor.execute("""
                    select b.booking_id,g.guest_name,g.mobile_number,g.email,
                    b.room_no,b.room_type,b.checkin,b.checkout,
                    b.guest_count,b.breakfast,b.total_amount,b.status
                    from bookings b
                    join guests g ON b.guest_id=g.guest_id
                    where b.booking_id=?
                       """,(booking_id,))
        booking=cursor.fetchone()
        if booking is None:
            print("Booking ID not found")
            connection.close()
            return
        print("\n========== BOOKING DETAILS ==========")
        print("Booking ID:",booking[0])
        print("Guest name:",booking[1])
        print("Mobile number:",booking[2])
        print("Email:",booking[3])
        print("Room number:",booking[4])
        print("Room type:",booking[5])
        print("Check-in date:",booking[6])
        print("Check-out date:",booking[7])
        print("Guest count:",booking[8])

        if booking[9]==1:
            print("breakfast: Yes")
        else:
            print("breakfast: No")
        print("Total Amount:",booking[10])
        print("Booking Status:",booking[11])

        connection.close()
    def Guest_history(self,mobile_number):
        connection=sqlite3.connect("stayeasy.db")
        cursor=connection.cursor()
        cursor.execute("""
            select b.booking_id,b.room_no,b.room_type,b.checkin,
            b.checkout,b.total_amount,b.status
            from guests g
            join bookings b on g.guest_id=b.guest_id
            where g.mobile_number=?""",(mobile_number,))
        bookings=cursor.fetchall()
        connection.close()
        if not bookings:
            print("No bookings available with number")
            return
        print("\n=========== GUEST STAY HISTORY ==============")
        for booking in bookings:
            print("\nBooking ID:",booking[0])
            print("Room Number:",booking[1])
            print("Room type:",booking[2])
            print("Check-in:",booking[3])
            print("Check-out",booking[4])
            print("Total Amount:",booking[5])
            print("Status:",booking[6])
            print("-"*30)
