import sqlite3
from room import StandardRoom,DeluxeRoom,SuitRoom
from booking_service import BookingService
from pricing import Pricing
from guest_serive import guestservices
from booking import Guests,Bookings
from reports import ReportService
from room_service import RoomService
from datetime import datetime
from exception import Room_unavailable,Invalid_Date,Booking_NotFound,Invalid_status,Guest_limit,Invalid_input


room_service=RoomService()
booking_service=BookingService()
pricing=Pricing()
guest_service=guestservices()
report_service=ReportService()

rooms=room_service.readcsv("rooms.csv","erros.txt")

def get_booking():
    connection=sqlite3.connect("stayeasy.db")
    cursor=connection.cursor()
    
    cursor.execute("""
                   select room_no,checkin,checkout
                   from bookings where status in('CONFIRMED','CHECK_IN')
                   """)
    bookings=cursor.fetchall()
    connection.close()
    return bookings
def search_availability():
    while True:
        try:
        
            room_type=input("Enter room type (standard/deluxe/suite):").lower()
            
            if room_type not in ["standard","deluxe","suite"]:
                raise Invalid_input("Invalid room type")
            guest_count=int(input("Enter number of guests:"))
            if guest_count<1:
                raise Guest_limit("Guest count must be at least 1:")
            elif room_type=="standard" and guest_count>2:
                raise Guest_limit("Standard room allows macimum 2 guests")
            elif room_type=="deluxe" and guest_count>3:
                raise Guest_limit("Deluxe room allows maximum 3 guests")
            elif room_type=="suite"and guest_count>4:
                raise Guest_limit("Suite allows maximum 4 guests")
            
            checkin=input("Enter check-in date (DD-MM-YYYY):")
            checkout=input("Enter check_out date (DD-MM-YYYY):")
            try:
                checkin_date=datetime.strptime(checkin,"%d-%m-%Y").date()
                checkout_date=datetime.strptime(checkout,"%d-%m-%Y").date()
            except ValueError:
                raise Invalid_Date("Invalid date format use DD-MM-YYYY.")
            today=datetime.today().date()
            if checkin_date < today:
                raise Invalid_Date("Check-in date cannot be in the past!")

            if (checkin_date - today).days > 180:
                raise Invalid_Date("Check-in date cannot be more than 180 days ahead!")

            if checkout_date <= checkin_date:
                raise Invalid_Date("Check-out must be after check-in!")

            if (checkout_date - checkin_date).days > 30:
                raise Invalid_Date("Maximum stay is 30 nights!")
            
            
            bookings=get_booking()
            
            available_rooms=booking_service.get_available_rooms(
                rooms,
                room_type,
                guest_count,
                checkin,
                checkout,
                bookings
            )
            print("\nAvailable rooms:")
            for room in available_rooms:
                print(room)
            if len(available_rooms)==0:
                print("No rooms available!")
            break
        except (Invalid_input,Invalid_Date,Guest_limit,Room_unavailable) as error:
            print(error)
def create_bookings():
    try:
        guest_name=input("Enter guest Name: ").strip()

        if guest_name=="":
            raise Invalid_input("Guest name cannot be empty")

        mobile=input("Enter mobile number:").strip()

        if len(mobile)!=10 or not mobile.isdigit() or mobile[0] not in "6789":
            raise Invalid_input("Invalid mobile number!")

        email=input("Enter email:").strip()

        if "@" not in email or "." not in email or " " in email:
            raise Invalid_input("Invalid email address!")

        guest=Guests(guest_name,mobile,email)
        guest_id=guest_service.register_guest(guest)

        room_type=input("Enter room type (standard/deluxe/suite): ").lower()

        if room_type not in ["standard", "deluxe", "suite"]:
            raise Invalid_input("Invalid room type")

        guest_count=int(input("Enter number of guests: "))

        if guest_count<1:
            raise Guest_limit("Guest count must be at least 1")

        if room_type=="standard" and guest_count>2:
            raise Guest_limit("Standard room allows maximum 2 guests")

        elif room_type=="deluxe" and guest_count>3:
            raise Guest_limit("Deluxe room allows maximum 3 guests")

        elif room_type=="suite" and guest_count > 4:
            raise Guest_limit("Suite allows maximum 4 guests")

        checkin=input("Enter check-in date (DD-MM-YYYY): ")
        checkout=input("Enter check-out date (DD-MM-YYYY): ")

        try:
            checkin_date = datetime.strptime(checkin, "%d-%m-%Y").date()
            checkout_date = datetime.strptime(checkout, "%d-%m-%Y").date()
        except ValueError:
            raise Invalid_Date("Invalid date format! Use DD-MM-YYYY.")
        today = datetime.today().date()

        if checkin_date<today:
            raise Invalid_Date("Check-in date cannot be in the past!")

        if (checkin_date-today).days>180:
            raise Invalid_Date("Check-in date cannot be more than 180 days ahead!")

        if checkout_date <= checkin_date:
            raise Invalid_Date("Check-out must be after check-in!")

        if (checkout_date - checkin_date).days > 30:
            raise Invalid_Date("Maximum stay is 30 nights!")

        breakfast=False

        if room_type=="standard":
            answer=input("Do you want breakfast (yes/no): ").lower()

            if answer not in ["yes","no"]:
                raise Invalid_input("Please enter yes or no")
            if answer=="yes":
                breakfast=True
        bookings=get_booking()

        available_rooms=booking_service.get_available_rooms(
            rooms,room_type,guest_count,checkin,checkout,bookings
        )

        selected_room=booking_service.select_room(available_rooms)

        if selected_room is None:
            raise Room_unavailable("No rooms available for the selected dates!")

        connection = sqlite3.connect("stayeasy.db")
        cursor = connection.cursor()
        cursor.execute("""
            SELECT COUNT(*)
            FROM bookings
            WHERE guest_id = ? AND status = 'CHECK_OUT'
        """, (guest_id,))

        completed_stays=cursor.fetchone()[0]
        connection.close()
        total_amount, night_details = pricing.caluculate_room_charge(
            selected_room, checkin, checkout, guest_count,
            breakfast, completed_stays
        )
        print("\nSelected room:",selected_room)
        print("Total Amount:",total_amount)

        answer=input("Confirm booking (yes/no):").lower()

        if answer not in ["yes","no"]:
            raise Invalid_input("Please enter yes or no")

        if answer=="yes":
            room_type_name = room_type.capitalize()

            booking_service.save_bookings(
                guest_id, selected_room, room_type_name,
                checkin, checkout, guest_count, breakfast,
                total_amount, bookings, night_details
            )
        else:
            print("Booking cancelled by user.")
    except (Invalid_input, Invalid_Date, Guest_limit, Room_unavailable) as error:
        print(error)
    except ValueError:
        print("Please enter a valid number!")
    except sqlite3.Error as error:
        print("Database error:", error)   
def Check_in():
    try:
        booking_id=int(input("Enter booking ID:"))
        if booking_id<=0:
            raise Invalid_input("Invalid Booking ID:")
        booking_service.check_in(booking_id)
    except(Exception) as error:
        print(error)
    except ValueError:
        print("Booking ID must be a number")
def check_out():
    try:
        booking_id=int(input("Enter Booking Id:"))
        if booking_id<=0:
            raise Invalid_input("Invalid Booking ID")
       
        booking_service.check_out(booking_id)
    except ValueError:
        print("Booking ID msut be a number")
def Cancel_booking():
    try:
        while True:
            Booking_id=int(input("Enter Booking ID: "))
            if Booking_id>0:
                break
            print("Invalid_input ID enter agin: ")
        booking_service.cancel_booking(Booking_id)
    except ValueError:
        print("Booking ID must be a number")
def View_booking_details():
    try:
        while True:
            booking_id=int(input("Enter Booking ID:"))
            if booking_id>0:
                break
            print("Invalid Booking Id Enter again")
        booking_service.view_bookings(booking_id)
    except ValueError:
        print("Inavlid integer")
def Guest_stay_history():
    
        while True:
            mobile_number=input("Enter Mobile number: ")
            if not mobile_number.isdigit() or len(mobile_number)==10:
                break
            print("Booking Id not be negative or number not registered")
        booking_service.Guest_history(mobile_number)
        
      
def ocuupancy_report():
    try:
        checkin=input("Enter start date (DD-MM-YYYY):")
        checkout=input("Enter end date date (DD-MM-YYYY)")
        
        report_service.occupancy_report(
            rooms,
            checkin,
            checkout
            )
    except ValueError:
        print("Invalid date format use DD-MM-YYYY")
    except Invalid_Date as error:
        print(error)
        
def revenue_report():
    report_service.revenue_report()
    
while True:
    print("\n========== STAYEASY HOTEL ==========")
    print("1. Search Room Availability")
    print("2. Create Booking")
    print("3. Check In")
    print("4. Check Out")
    print("5. Cancel Booking")
    print("6. View Booking Details")
    print("7. Guest Stay History")
    print("8. Occupancy Report")
    print("9. Revenue Report")
    print("10. Export All Bookings to CSV")
    print("11. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        search_availability()

    elif choice == "2":
        create_bookings()

    elif choice == "3":
        Check_in()

    elif choice == "4":
        check_out()

    elif choice == "5":
         Cancel_booking()

    elif choice == "6":
        View_booking_details()

    elif choice == "7":
        Guest_stay_history()

    elif choice == "8":
        ocuupancy_report()

    elif choice == "9":
        revenue_report()

    elif choice == "10":
        room_service.export_booking()

    elif choice == "11":
        print("Thank you for using StayEasy!")
        break

    else:
        print("Invalid choice! Try again.")