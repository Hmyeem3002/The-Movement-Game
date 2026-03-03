#Gets randrange and choice for randomly making Obstacle positions
import random

#Gets half the screen and the whole screen for making Obstacle positions
from PlayerStats import GetSize, GetHalf 

#Gets the Obstacles list for updating and the EveryThing list to make sure newly made Obstacles don't overlap other things
#Also gets the Entity class because I see no reason to make an Obstacle class
from ExistingEntity import Obstacles, EveryThing
from ExistingEntity import Entity




#Different biomes for the Obstacles
ObstacleBiome = {
  0:[1, 4],   #Lone Obstacle
  1:[5, 10],   #Group of some Obstacles
  2:[7, 20]   #Forest of Obstacles

}


#Makes a whole biome's worth of Obstacles. *Location turns all inputs into one big tuple
def MakeObstacle(*Location):
  global Obstacles
  
  #Selects a random biome
  Biome = ObstacleBiome[random.randrange(len(ObstacleBiome))]

  #Converts Location into a list
  Location = list(Location)

  #If Location is empyty (No inputs were given), then create a random Location
  if len(Location) == 0:
    Location = [0, 0]
    while True:
      #Chooses a random axis to start on then randomly select a number for that first axis to become
      Axis = random.randrange(0, 2)
      extra = random.randrange(5, 10)
      
      Location[Axis] = random.randrange(-extra, GetSize()+extra)
      
      #Based on what that first number is, that will dictate the range of the second number
      if Location[Axis] >= 0 and Location[Axis] <= GetSize():
        Location[not Axis] = (random.choice([-1, 1])*random.randrange(GetHalf()+5, GetHalf()+10))+GetHalf()
  
      else:
        extra = random.randrange(5, 10)
        Location[not Axis] = random.randrange(-extra, GetSize()+extra)

      #Checks to see if the final Location is too close to other Obstacles. If it is, then try the Location creation again 
      for Tree in Obstacles:
        if abs(Location[0]-Tree.Location[0]) < GetHalf()+10 or abs(Location[1]-Tree.Location[1]) < GetHalf()+10:
          break
      else:
        break

  #Start making multiple Obstacles based on the bione type
  for Repeats in range(random.randrange(Biome[0], Biome[1])):
    Obstacles.append(Entity(Location))
    while True:
      #Prepares a temporary location that will have a small amount of change compared to the previous location
      Temp = Location.copy()

      firstMove = random.randrange(1, 3)
      firstDirection = random.randrange(2)
      Temp[firstDirection] += random.choice([-1, 1]) * firstMove

      if firstMove <= 2 and random.randrange(2) == 0:
        Temp[not firstDirection] += random.choice([-1, 1]) * random.randrange(1, 4-firstMove)

      #Checks if this temporary is already in use. If it is, try again. Otherwise, move on
      for Type in EveryThing:
        for Thing in Type:
          if Thing.Location == Temp:
            break
        else:
          continue
        break
      else:
        break
        
    Location = Temp.copy()

#Calls the creation once
MakeObstacle()


