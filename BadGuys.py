#Gets the randrange function for the chance of a crate
import random

#Gets the players damage and half the screen for ranges. Also allows the change of HPs and EXP
from PlayerStats import GetDamage, GetDamagePlus, GetHalf
from PlayerStats import HPChange, ExpUp

#Gets the default Crate item drop
from ItemClass import Blank

#Gets the Entity class to be a parent class, gets the Bosses and Enemies lists for illiteration, and the CannotWalk list to stop BadGuys from overlapping
from ExistingEntity import Entity, Bosses, Enemies, CannotWalk


#Starts the BadGuy Class that hold the object type(Enemy or Boss), Name(what they'll look like on screen), HP, Damage, Range, Speed, Ect.

class BadGuy(Entity):
  def __init__(self, Class, Name, Coordinates, Level, MaxHP, Damage, Range, Speed, EXPrange, ChestPotential, DropChance):
    self.Class = Class
    self.Name = Name
    self.Level = Level
    Entity.__init__(self, Coordinates)
    self.MaxHP = int(MaxHP + Level**1.70 - Level/2 + 0.5)
    self.HP = int(MaxHP + Level**1.70 - Level/2 + 0.5)
    self.Damage = int(Damage + Level**1.50 -Level/2 + 0.5)
    self.Range = Range
    self.Speed = Speed
    if isinstance(EXPrange, int):
      self.EXP = EXPrange
    else:
      Smallest = int(EXPrange[0] + Level**1.7 - Level/2 + 0.5)
      Biggest = int(EXPrange[1] + Level**1.5 - Level/2 + 0.5)
      if Biggest == Smallest:
        Biggest += 1
      self.EXP = random.randrange(min(Smallest, Biggest), max(Smallest, Biggest))
      
    self.ChestPotential = ChestPotential
    self.DropChance = max(int(DropChance-Level**0.75), 1)


  #Makes the BadGuy attack the Player. The amount of hits corresponds to the Speed of the BadGuy
  def AttackPlayer(self, UsedTurns = 0):
    for Attacks in range(self.Speed-UsedTurns):
      HPChange(-self.Damage)

  #Makes the BadGuy take Damage from the Player.
  def ChangeHP(self):
    from CrateClass import MakeCrate
    self.HP -= (GetDamage()+GetDamagePlus())
    #When killed, have a chance to spawn a Crate
    if self.HP <= 0:
      if random.randrange(0, self.DropChance) == 0:
        rarity = random.randrange(0, 100)
        #Make a Crate with a rarity based on a random chance
        if rarity < self.ChestPotential[0]:
          RarityPoint = 0
        elif rarity < self.ChestPotential[0]+self.ChestPotential[1]:
          RarityPoint = 1
        elif rarity < self.ChestPotential[0]+self.ChestPotential[1]+self.ChestPotential[2]:
          RarityPoint = 2
        elif rarity < self.ChestPotential[0]+self.ChestPotential[1]+self.ChestPotential[2]+self.ChestPotential[3]:
          RarityPoint = 3
        else:
          RarityPoint = 4
  
        for Rarities in range(RarityPoint):
          if RarityPoint < 4:
            self.ChestPotential[RarityPoint] += self.ChestPotential[Rarities]
          self.ChestPotential[Rarities] = 0
  
        MakeCrate(self.Location, self.ChestPotential, RarityPoint, Blank)

      #Give EXP to the Player
      ExpUp(self.EXP)

      #Remove the dead BadGuy from their list
      if self.Class == "Enemy":
        Enemies.remove(self)
      elif self.Class == "Boss":
        Bosses.remove(self)


  #If the BadGuy is too far to Attack the Player, it needs to get closer.
  def ComeCloser(self): 

    for Repeat in range(self.Speed):
      #If the BadGuy is now in range to attack and still has turns left, switch to Attacking the Player
      if ((GetHalf() - self.Location[0])**2 + (GetHalf() - self.Location[1])**2)**0.5 <= self.Range:
        self.AttackPlayer(Repeat)
        return

      #Check if the vertical difference between the BadGuy and Player is longer than the horizontal difference
      if abs(self.Location[0]-GetHalf()) >= abs(self.Location[1]-GetHalf()) and self.Location[0] != GetHalf():
        #If so, check if anything is blocking the path and move if nothing is blocking
        for Type in CannotWalk:
          for Creature in Type:
            if Creature.Location[1] == self.Location[1] and Creature.Location[0]+((self.Location[0]>GetHalf())*2-1) == self.Location[0]:
              break
              
          else:
            continue
          #If something is blocking, the loop should end artificially and we will try again with the other dimension of travel
          break

        #If nothing was blocking, then that means all the loops ended naturally and this code should run
        else:
          self.Location[0] -= ((self.Location[0] > GetHalf())*2-1)
          continue

            
      #Next, try moving the BadGuy in the horizontal dimension.
      #This is OK because this code can only run if: the horizontal difference between Player&BadGuy is greater than the Vertical difference or the BadGuy couldn't move vertical
      for Type in CannotWalk:
        for Creature in Type:
          if Creature.Location[1] + ((self.Location[1] > GetHalf())*2-1) == self.Location[1] and Creature.Location[0] == self.Location[0]:
            break
        #Uses same logic as the previous one
        else:
          continue

        break

      else:
        self.Location[1] -= ((self.Location[1] > GetHalf())*2-1)
        continue

        
      #If the horizontal difference was greater than the vertical difference and the prior attempt to move horizontally didn't work, try to move horizontally
      if abs(self.Location[0]-GetHalf()) <= abs(self.Location[1]-GetHalf()) and self.Location[1] != GetHalf():

        for Type in CannotWalk:
          for Creature in Type:
            if Creature.Location[1] == self.Location[1] and Creature.Location[0]+((self.Location[0] > GetHalf())*2-1) == self.Location[0]:
              break
          #Uses same logic as the original one
          else:
            continue
            
          break
          
        else:
          self.Location[0] -= ((self.Location[0] > GetHalf())*2-1)
          continue



#Illiterates through the Enemies and Bosses lists to give each one a chance to move/attack
def BadAction():
  for EnemyThing in Enemies:
    if ((GetHalf() - EnemyThing.Location[0])**2 + (GetHalf() - EnemyThing.Location[1])**2)**0.5 <= EnemyThing.Range:
      HPChange(-EnemyThing.Damage)
      
    #Enemies have a range on how far they can view the Player
    elif ((GetHalf() - EnemyThing.Location[0])**2 + (GetHalf() - EnemyThing.Location[1])**2)**0.5 <= GetHalf()+GetHalf()/3:
      EnemyThing.ComeCloser()
      
    #If the Player is too far away, just let the Enemy move idlely
    else:
      for Amount in range(EnemyThing.Speed):
        EnemyThing.Move(random.randrange(0,2), random.choice([-1, 1]))

  for BossThing in Bosses:
    if ((GetHalf() - BossThing.Location[0])**2 + (GetHalf() - BossThing.Location[1])**2)**0.5 <= BossThing.Range:
      HPChange(-BossThing.Damage)
    #Bosses ALWAYS know where the Player is
    else:
      BossThing.ComeCloser()

