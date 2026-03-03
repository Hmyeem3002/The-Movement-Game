#Gets the randrange and choice functions from random
import random

#Get the sizes of the map and the level of the player
from PlayerStats import GetLevel, GetSize, GetHalf

#Gets the BadGuy class to be a parent class
from BadGuys import BadGuy

#Gets the Enemies list for updates
from ExistingEntity import Enemies



#Initiates an Enemy class who's only goal is to be part of the BadGuy class with the "Enemy" tag

class Enemy(BadGuy):
  def __init__(self, EName, ECoordinates, ELevel, EMaxHP, EDamage, ERange, ESpeed, EXPrange, Potential, DropChance):
    BadGuy.__init__(self, "Enemy", EName, ECoordinates, ELevel, EMaxHP, EDamage, ERange, ESpeed, EXPrange, Potential, DropChance)

#Is a Manual copy of the Enemy object
  def Copy(self):
    return Enemy(self.Name, self.Location, self.Level, self.MaxHP, self.Damage, self.Range, self.Speed, self.EXP, self.ChestPotential, self.DropChance)


#A Variable for a neutral Enemy
Nothing = Enemy("O", [-1, -1], 1, -1, -1, -1, -1, [-1, 1], [0,0,0,0], 1)

#Holds the different types of Enemies.
Typing = {
  "Melee":Enemy("O", [0, 0], random.randrange(max(GetLevel()-2, 1), GetLevel()+2), 10, 4, 1, 1, [5, 20], [50, 30, 15, 4], 5),
  "Ranged":Enemy("0", [0, 0], random.randrange(max(GetLevel()-2, 1), GetLevel()+2), 5, 2, 4, 1, [10, 35], [40, 30, 18, 9], 4),
  "Speed":Enemy("⬮", [0, 0], random.randrange(max(GetLevel()-2, 1), GetLevel()+2), 8, 2, 1, 2, [7, 25], [49, 27, 18, 5], 5)
}

#Makes an Enemy
def MakeEnemy(Type, Outside = [4, 10]):

  #Sets up the random creation the Enemy's location outside the screen.
  Coordinate = [0, 0]

  Axis = random.randrange(0, 2)
  extra = random.randrange(Outside[0], Outside[1])
  
  Coordinate[Axis] = random.randrange(-extra, GetSize()+extra)
  
  if Coordinate[Axis] >= 0 and Coordinate[Axis] <= GetSize():
    Coordinate[not Axis] = (random.choice([-1, 1])*random.randrange(GetHalf()+Outside[0], GetHalf()+Outside[1]))+GetHalf()
  
  else:
    extra = random.randrange(Outside[0], Outside[1])
    Coordinate[not Axis] = random.randrange(-extra, GetSize()+extra)

  #Make the new Enemy who's stats are based on the type of Enemy. 
  #Then make the location of the newborn Enemy to be the one we set up
  new = Typing[Type].Copy()
  new.Location = Coordinate

  
  Enemies.append(new)
