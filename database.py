import sqlite3
connection = sqlite3.connect("stayeasy.db")
cursor = connection.cursor()
cursor.execute("""
    create table if not exists guests(
        guest_id integer primary key autoincrement,
        guest_name text not null,
        mobile_number text not null check(
            length(mobile_number) = 10 and
            (
                mobile_number like '6%' or
                mobile_number like '7%' or
                mobile_number like '8%' or
                mobile_number like '9%'
            )
        ),
        email text not null
    )
""")

cursor.execute("""
    create table if not exists bookings(
        booking_id integer primary key autoincrement,
        guest_id integer not null,
        room_no integer not null,
        room_type text not null,
        checkin text not null,
        checkout text not null,
        guest_count integer not null,
        breakfast integer not null,
        total_amount real not null,
        status text not null,

        foreign key (guest_id)
        references guests(guest_id)
    )
""")

cursor.execute("""
    create table if not exists booking_nights(
        night_id integer primary key autoincrement,
        booking_id integer not null,
        stay_date text not null,
        room_charge real not null,
        extra_guest_charge real not null,
        breakfast_charge real not null,
        discount real not null,
        gst real not null,

        foreign key (booking_id)
        references bookings(booking_id)
    )
""")


connection.commit()
connection.close()

print("All tables created successfully")
