#Gets randrange and choice functions from random
import random

#Gets the Player's level and the map sizes
from PlayerStats import GetLevel, GetSize, GetHalf

#Gets the BadGuy class to be a parent class
from BadGuys import BadGuy

#Gets the Bosses list for updates
from ExistingEntity import Bosses



#Initiates the Boss class who's only goal is to be part of the BadGuy class with the "Boss" tag

class Boss(BadGuy):
  def __init__(self, Name, BCoordinates, BLevel, BHP, BDamage, BRange, BSpeed, EXPrange, ChestRarity):
    BadGuy.__init__(self, "Boss", Name, BCoordinates, BLevel, BHP, BDamage, BRange, BSpeed, EXPrange, ChestRarity, 1)

#Is a Manual copy of the Boss object
  def Copy(self):
    return Boss(self.Name, self.Location, self.Level, self.MaxHP, self.Damage, self.Range, self.Speed, self.EXP, self.ChestPotential)
    

#Holds the different types of Bosses
Typing = {
  "Melee": Boss("O", [0, 0], random.randrange(max(1, GetLevel()-2), GetLevel()+2), 50, 7, 1.5, 1, [75, 100], [0, 0, 80, 15]),
  "Ranged": Boss("0", [0, 0], random.randrange(max(1, GetLevel()-2), GetLevel()+2), 30, 5, 5, 1, [75, 100], [0, 0, 70, 20]),
  "Speed": Boss("⬮", [0, 0], random.randrange(max(1, GetLevel()-2), GetLevel()+2), 40, 3, 1, 3, [75, 100], [0, 0, 75, 18])
}

  
#Makes a Boss
def MakeBoss(Type, Outside = [2, 5]):

  #Sets up the random creation of the Boss's location outside the screen.
  Coordinate = [0, 0]

  Axis = random.randrange(0, 2)
  extra = random.randrange(Outside[0], Outside[1])

  Coordinate[Axis] = random.randrange(-extra, GetSize()+extra)

  if Coordinate[Axis] >= 0 and Coordinate[Axis] <= GetSize():
    Coordinate[not Axis] = (random.choice([-1, 1])*random.randrange(GetHalf()+Outside[0], GetHalf()+Outside[1]))+GetHalf()

  else:
    extra = random.randrange(Outside[0], Outside[1])
    Coordinate[not Axis] = random.randrange(-extra, GetSize()+extra)

  #Then make a Boss who's stats are based on the tye of Boss.
  #Then make the location of the newborn Boss to be the one we set up
  new = Typing[Type].Copy()
  new.Location = Coordinate

  
  Bosses.append(new)







