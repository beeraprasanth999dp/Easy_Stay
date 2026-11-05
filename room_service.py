import csv
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
    
# serices=RoomService()

# serices.readcsv("rooms.csv","erros.txt")
