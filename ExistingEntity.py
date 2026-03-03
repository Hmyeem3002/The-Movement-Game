#Gets half the screen for calculation of distance between the Player and each CannotWalk object
from PlayerStats import GetHalf

#Create a class that gives it's objects a location and movement is responce to the Player's input
class Entity:
  def __init__(self, Coordinates):
    self.Location = Coordinates

  #Moves the objects away to give the illusion of movement
  def Move(self, Direction, Distance):
    self.Location[Direction] += Distance


#Make lists for each object that will be a part of the Entity class
Crates = []
Bosses = []
Enemies = []
Obstacles = []

#Special lists that reflect the main lists. They are used for locating things
CannotWalk = [Obstacles, Bosses, Enemies]
EveryThing = [Crates, Bosses, Enemies, Obstacles]


#A fuction that will give the illusion of a Player moving
def MoveAway(Direction, Distance):
  #Checks if anything is blocking the way of the Player's movement and does calculations accordingly
  for Type in CannotWalk:
    for Thing in Type:
      if Thing.Location[not Direction] == GetHalf() and abs(GetHalf() - Thing.Location[Direction]) <= abs(Distance) and ((GetHalf() - Thing.Location[Direction]) >= 0) == (Distance >= 0):
        Distance = (GetHalf() - Thing.Location[Direction]) - (((Distance>0)*2)-1)
  #If the Player was completely unable to move, refund the turn and let the Player choose a different action 
  if Distance == 0:
    return False

  #Else, move all the objects
  for Type in EveryThing:
    for Thing in Type:
      Thing.Move(Direction, Distance)

  #Then let the turn end
  return True

#Checks if anything has the same location as the one provided
def IsAnyoneThere(Vert, Hori):
  Coordinate = [Vert, Hori]

  #Returns the objects and it's type
  for i in Enemies:
    if Coordinate == i.Location:
      return "Enemy", i
  
  for i in Crates:
    if Coordinate == i.Location:
      return "Crate", i
  
  for i in Bosses:
    if (Vert <= i.Location[0] + 1 and Vert >= i.Location[0] - 1 and Hori == i.Location[1]) or (Hori <= i.Location[1] + 1 and Hori >= i.Location[1] - 1 and Vert == i.Location[0]):
      for o in Bosses:
        if o.Location == [Vert, Hori]:
          return "Boss", o
      return "Boss", i
      
  for i in Obstacles:
    if Coordinate == i.Location:
      return "Obstacle", i
      
  return "Nothing", 0






