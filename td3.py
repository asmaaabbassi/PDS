import random
class Film:
    def __init__(self, title, duration, min_age, film_dir, ticket_price) -> None:
        self.title=title
        self.duration=duration
        self.min_age=min_age
        self.film_dir=film_dir
        self.ticket_price=ticket_price


class Spectator: 
    def __init__(self, id:int, age:int, available_money:float)->None:
       self.id=id
       self.age=age
       self.available_money=available_money


class Seat:
   def __init__(self, row: str, column:str)->None:
       self.row=row
       self.column=column


class Cinema:
    def __init__(self,r,c,film)->None:
        self.film=film
        self.numberofrows=r
        self.numberofcolumns=c
        self.spectators=set()
        self.seats=list()

    def getSeats(self):
        seats=list()
        for i in range (1,self.numberofrows+2):
            for j in range (ord('A'), ord('A')+self.numberofcolumns):
                seats.append(Seat(str(i), chr(j)))
        return seats

    def getrandseat(self):
         a,b= random.randint(1, self.numberofrows), random.randint(ord('A'),self.numberofcolumns+ord('A'))
         return a,b
    
    def allocateSpectators(self,spectatorList):
        for i in spectatorList:
            if len(spectatorList) < self.numberofcolumns*self.numberofrows:
                if self.film.ticket_price <= i.available_money and i.age>= self.film.min_age:
                    a,b= self.getrandseat()
                    for s in self.seats:
                        if str(a)==s.row and b==ord(s.column):
                            s.column='*' + str(i.id)
                            s.row='*S'
                            self.spectators.add(i)

    def getAllocatedSpectators(self):
        return self.spectators

    def showSeats(self):
        s=0
        for i in self.seats:
            if s==self.numberofcolumns:
                print()
                s=0
            print([i.row, i.column], end="")
            s+=1
            


film=Film('Titanic', 90, 15, 'bob', 6.5)
cinema= Cinema(8,8, film)
cinema.seats=cinema.getSeats()
spec1= Spectator(988, 18, 180)
spec2 = Spectator(900, 13, 56)
spec3= Spectator(899, 56, 4)
spec4= Spectator(677, 45, 70.6)
cinema.allocateSpectators([spec1, spec2, spec3, spec4])
cinema.showSeats()



