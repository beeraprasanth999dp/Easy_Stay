
from datetime import datetime,timedelta

class Pricing():
    def caluculate_room_charge(self,room,checkin,checkout,guest_count,breakfast,completed_stays):
        checkin=datetime.strptime(checkin,"%d-%m-%Y").date()
        checkout=datetime.strptime(checkout,"%d-%m-%Y").date()
        nights=(checkout-checkin).days
        total_charge=0
        night_details=[]
        
        for day in range(nights):
            stay_date=checkin+timedelta(days=day)
            room_charge=room.get_tarrif()
            if stay_date.weekday()==4 or stay_date.weekday()==5:
                room_charge= room_charge+(room_charge*0.2)
            total_charge=total_charge+room_charge

            extra_guest_per_night=0
            if guest_count>2:
                extra_guest=guest_count-2
                extra_guest_per_night=extra_guest*room.get_extra_guest_charge()

            breakfast_per_night=0
            if room.get_breakfast()==False and breakfast==True:
                breakfast_per_night=350*guest_count

            night_details.append({
                "stay_date":stay_date.strftime("%d-%m-%Y"),
                "room_charge":room_charge,
                "extra_guest_charge":extra_guest_per_night,
                "breakfast_charge":breakfast_per_night
            })

        weekly_discount=0
        if nights>=7:
            weekly_discount=total_charge*0.1
        total_charge = total_charge - weekly_discount

        loayalty_discount=0
        if completed_stays>=3:
            loayalty_discount=total_charge*0.05
            total_charge = total_charge -loayalty_discount

        extra_guest_charge=0
        if guest_count>2:
            extra_guest=guest_count-2
            extra_guest_charge=extra_guest*room.get_extra_guest_charge()*nights

        breakfast_price=0
        if room.get_breakfast()==False and breakfast==True:
            breakfast_price=350*guest_count*nights

        Gst=0
        if room.get_tarrif()<=7500:
            Gst=total_charge*0.12
        else:
            Gst=total_charge*0.18

        total_amount=total_charge + extra_guest_charge + breakfast_price +Gst

        return total_amount,night_details


