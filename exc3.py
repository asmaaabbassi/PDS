class Film:

    def __init__(self, title:str, duration:int, minAge:int, filmDirector:str, ticketPrice:float)-> None:
        self.title = title
        self.minAge = 1
        self.duration=0
        self.filmDirector = filmDirector
        self.ticketPrice =0.0

class Spectator:

    def __init__(self, id:int, age:int, availableMoney:float)-> None:
        self.id =0
        self.age = 0
        self.availableMoney = 0.0

class Seat:

    def __init__(self, row:int, column:str, isFree:bool, ocuppatorID:int)-> None:
        self.row=0
        self.column=zero
        self.isFree=true
        self.occupatorID=0

class Cinema:

    def __init__(self, rows:int, columns:int, filmShown:Film)-> None:
        self.row =0
        self.column = 0

    def allocateSpectators(spectatorList)
        allSeats = self.rows*self.columns      
        if allSeats > 0:
            seats = list()
            alphabet_dict = {i:chr(i+64) for i in range(1,27)}
            for x in range(rows):
                for y in range (columns):
                    seats.append(Seat(x+1,alphabet_dict[y+1]))
            foreach spectator in spectatorList:
                if spectator.age > filmShown.minAge and spectator.availableMoney > filmShown.ticketPrice:
                    spectator.availableMoney -= filmShown.ticketPrice
                    random.choice(seats).isFree = false
                    
                
            

    def getAllocatedSpectators()
        for 

    def showSeats()

    def getSeats()
