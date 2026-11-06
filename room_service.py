import csv
import sqlite3
from room import StandardRoom,DeluxeRoom,SuitRoom
class RoomService:
    def readcsv(self,filename,Error):
        roomlist=[]
        room_number=[]
        rooms=["standard","deluxe","suite"]
        file=open(filename,"r")
        error=open(Error,"w")
        next(file)
        lineno=1
        for line in file:
            lineno+=1
            line=line.strip()
            if line=="":
                error.write(f"{lineno}:line is empty\n")
                continue
            colm=line.split(",")
            if len(colm)!=3:
                error.write(f"{lineno}:Invalid colms\n")
                continue
            room_no=int(colm[0].strip())
            room_type=colm[1].strip().lower()
            floor=colm[2].strip()
            if room_no=="":
                error.write(f"{lineno}:room number is empty")
                continue
            if room_type=="":
                error.write(f"{lineno}:room_tupe  is empty")
                continue
            if floor == "":
                error.write(f"{lineno}: floor is empty\n")
                continue
            if room_type not in rooms:
                error.write(f"{lineno}:room type is not valid\n")
                continue
            if room_no in room_number:
                error.write(f"{lineno}: duplicate room number\n")
                continue
            # room_no=int(room_no)
            floor=int(floor)
            if room_type=="standard":
                room=StandardRoom(room_no,floor)
            if room_type=="deluxe":
                room=DeluxeRoom(room_no,floor)
            if room_type=="suite":
                room=SuitRoom(room_no,floor)
            roomlist.append(room)
            room_number.append(room_no)
            print("room added:",room)
        file.close()
        error.close()
        return roomlist
    def export_booking(self):
        connection=sqlite3.connect("stayeasy.db")
        cursor=connection.cursor()
        cursor.execute("""
                        select b.booking_id,g.guest_name,g.mobile_number,g.email,
                        b.room_no,b.room_type,b.checkin,b.checkout,
                        b.guest_count,b.breakfast,b.total_amount,b.status
                        from bookings b
                        join guests g on b.guest_id=g.guest_id 
                    """)
        bookings=cursor.fetchall()
        connection.close()
        if not bookings:
            print("No bookings available to export")
            return
        with open("bookings_export.csv","w",newline="") as file:
            writer=csv.writer(file)
            writer.writerow([
                "Booking ID" , "Guest Name" ,"Mobile Number" , "Email",
                "Room Number" , "Room type" ,"Check-in" , "check-out",
                "Guest count" , "Breakfast" , "Total Amount" , "Status"
                
            ])
            writer.writerows(bookings)
            print("All Bookingd are exported Successfully")
