#Get randrange and choice functions for randomly selecting an Item
import random

#Gets half the screen to check if a Crate is overlapping the Player
from PlayerStats import GetHalf

#Gets the Entity class to act as a parent class and get the Crates list for updating
from ExistingEntity import Entity, Crates

#Get the lists of different rarity Items for selection and the neutral Item for checking
from ItemClass import Commons, Rares, Epics, Mythics, Legendaries, Blank


#Starts the Crate Class who's parent class is Entity
class Crate(Entity):
  def __init__(self, ECoordinate, chances, rarity, PreItem):
    Entity.__init__(self, ECoordinate)
    #If a preselected Item wasn't given, randomly select a rarity and then randomly select an Item in that raritty's list
    if PreItem == Blank:
      randomChance = random.randrange(100)
      if randomChance < chances[0]:
        self.ItemDrop = random.choice(Commons).Copy()
      elif randomChance < chances[0]+chances[1]:
        self.ItemDrop = random.choice(Rares).Copy()
      elif randomChance < chances[0]+chances[1]+chances[2]:
        self.ItemDrop = random.choice(Epics).Copy()
      elif randomChance < chances[0]+chances[1]+chances[2]+chances[3]:
        self.ItemDrop = random.choice(Mythics).Copy()
      else:
        self.ItemDrop = random.choice(Legendaries).Copy()
    #If a preselected Item was given, then make the ItemDrop equal to the PreItem
    else:
      self.ItemDrop = PreItem

    self.Rarity = rarity



#Checks through every Crate in the Crates list and if a Crate is overlapping the Player, put the Item in the Inventory and destroy the Crate
def Open():
  global Crates
  for Indivisual in Crates:
    if Indivisual.Location == [GetHalf(), GetHalf()]:
      Indivisual.ItemDrop.AddToInventory()
      Crates.remove(Indivisual)



#Adds a Crate object to the Crates list
def MakeCrate(CCoordinates, CItemPotential, CRarity, MaybePreItem = Blank):
  Crates.append(Crate(CCoordinates, CItemPotential, CRarity, MaybePreItem))


