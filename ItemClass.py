#Gets randrange for the random level if the item
import random

#Gets the Level of the player for item level and gets the functions that change the boosts from items
from PlayerStats import GetLevel
from PlayerStats import DamagePlusChange, HPPlusChange, RangePlusChange


#Correlates the type of item to their location in the EquipedItem list
TypeOfItem = {
  "Weapon":0,
  "Armor":1, 
  "Amulet":2
}


#Sets up the Item class that contains the Item level, name, type, boosts, rarity, and current status
class Item:
  def __init__(self, Level, Name, type, IHP, IDamage, Irange, rarity, AttackType):

    self.Level = Level
    self.Name = Name
    self.Type = type
    self.Attack = AttackType
    if IDamage > 0:
      self.Damage = int(IDamage + max(Level-2, 0)**1.125 + 0.5)
    elif IDamage < 0:
      self.Damage = int(IDamage - max(Level-2, 0)**1.125 + 0.5)
    else:
      self.Damage = IDamage
    if IHP > 0:
      self.HP = int(IHP + max(Level-2, 0)**1.30 + 0.5)
    elif IHP < 0:
      self.HP = int(IHP - max(Level-2, 0)**1.30 + 0.5)
    else:
      self.HP = IHP
      
    self.Range = Irange
    self.Rarity = rarity
    self.Equiped = False

  #Is a manual copy of the Item who's level may or may not change based on what got copied
  def Copy(self):
    if self.Level == 0:
      if GetLevel() <= 2:
        Level = 1
      else:
        Level = random.randrange(max(1, GetLevel()-2), (GetLevel()+3))
    else:
      Level = self.Level
      
    return Item(Level, self.Name, self.Type, self.HP, self.Damage, self.Range, self.Rarity, self.Attack)

  #Appends the given Item to the Inventory list
  def AddToInventory(self):
    global Inventory
    Inventory.append(self)

  #Puts the given Item into the corresponding location in the EquipedItems list and removes the old Item
  #Also updates the boosts provided by equiping Items
  def Equip(self):
    global Inventory
    global EquipedItems
    
    EquipedItems[TypeOfItem[self.Type]].Equiped = False
    HPPlusChange(-EquipedItems[TypeOfItem[self.Type]].HP + self.HP)
    DamagePlusChange(-EquipedItems[TypeOfItem[self.Type]].Damage + self.Damage)
    RangePlusChange(-EquipedItems[TypeOfItem[self.Type]].Range + self.Range)


    self.Equiped = True
    EquipedItems[TypeOfItem[self.Type]] = self

  

    


#List of all Common Items
Commons = [Item(0, "Basic Blade", "Weapon", 0, 4, 0, 0, "Slash"),\
           Item(0, "Basic Armor", "Armor", 4, 0, 0, 0, "None"),\
           Item(0, "Basic Amulet", "Amulet", 2, 2, 0, 0, "None"),\
           Item(0, "Wooden Blade", "Weapon", 0, 5, 0, 0, "Slash"),\
           Item(0, "Wooden Staff", "Weapon", 0, 3, 1, 0, "Burst"),\
           Item(0, "Wooden Armor", "Armor", 5, 0, 0, 0, "None"),\
           Item(0, "Wooden Amulet", "Amulet", 3, 2, 0, 0, "None"),\
           Item(0, "Spiked Club", "Weapon", -1, 6, 0, 0, "None"),\
           Item(0, "Spiked Armor", "Armor", 4, 1, 0, 0, "None"),\
           Item(0, "Spiked Amulet", "Amulet", 3, 3, 0, 0, "None"),\
           Item(0, "Hope Amulet", "Amulet", 7, -3, 0, 0, "None"),\
           Item(0, "Cloth Whip", "Weapon", 0, 3, 2, 0, "Pierce"),\
           ]
#List of all Rare Items
Rares = [Item(0, "Iron Blade", "Weapon", 0, 5, 1, 1, "Slash"), \
         Item(0, "Iron Glaive", "Weapon", 0, 4, 2, 1, "Pierce"),\
         Item(0, "Iron Armor", "Armor", 6, 0, 0, 1, "None"),\
         Item(0, "Iron Amulet", "Amulet", 4, 2, 0, 1, "None"),\
         Item(0, "Lead Blade", "Weapon", 0, 6, 0, 1, "Slash"),\
         Item(0, "Lead Glaive", "Weapon", 0, 5, 1.5, 1, "Pierce"),\
         Item(0, "Lead Armor", "Armor", 5, 1, 0, 1, "None"),\
         Item(0, "Defender's Medal", "Amulet", 6, -1, -0.5, 1, "None"),\
         Item(0, "Cursed Blade", "Weapon", -5, 8, 0, 1, "Slash"),\
         Item(0, "Cursed Armor", "Armor", 8, -5, 0, 1, "None"),\
         Item(0, "Cursed Amulet", "Amulet", 4, 4, -1, 1, "None"),\
         Item(0, "Spiked Shield", "Weapon", 3, 4, 0, 1, "None"),\
         Item(0, "Iron Shield", "Weapon", 6, 2, 0, 1, "None"),\
         Item(0, "Barbed Whip", "Weapon", -1, 5, 2, 1, "Pierce")\
        ]
#List of all Epic Items
Epics = [Item(0, "Steel Blade", "Weapon", 0, 8, 0.5, 2, "Slash"),\
         Item(0, "Steel Armor", "Armor", 8, 0, 0, 2, "None"),\
         Item(0, "Steel Amulet", "Amulet", 4, 4, 0.5, 2, "None"),\
         Item(0, "Diamond Staff", "Weapon", 0, 6, 2, 2, "Burst"),\
         Item(0, "Golden Blade", "Weapon", 0, 9, 0, 2, "Slash"),\
         Item(0, "Golden Armor", "Armor", 9, 0, 0, 2, "None"),\
         Item(0, "Golden Amulet", "Amulet", 5, 3, 0.5, 2, "None"),\
         Item(0, "Focus Amulet", "Amulet", 1, 5, 3, 2, "None"),\
         Item(0, "Range Amulet", "Amulet", 1, 1, 4, 2, "None"),\
         Item(0, "Infinite Bow and Arrows", "Weapon", 0, 5, 4, 2, "None")\
         
        ]
#List of all Mythic Items
Mythics = [Item(0, "Blessed Blade", "Weapon", 1, 12, 1, 3, "Slash"),\
           Item(0, "Blessed Armor", "Armor", 12, 2, 0, 3, "None"),\
           Item(0, "Blessed Amulet", "Amulet", 6, 6, 1, 3, "None"),\
           Item(0, "Blessed Staff", "Weapon", 2, 10, 2, 3, "Burst"),\
           Item(0, "Titanium Blade", "Weapon", 0, 15, 0.5, 3, "Slash"),\
           Item(0, "Titanium Armor", "Armor", 15, 0, 0, 3, "None"),\
           Item(0, "Titanium Amulet", "Amulet", 7, 6, 2, 3, "None"),\
           Item(0, "Chaotic Whip", "Weapon", -5, 17, 3, 3, "Pierce"),\
           Item(0, "Chaotic Blade", "Weapon", -4, 18, 1, 3, "Slash"),\
           Item(0, "Chaotic Armor", "Armor", 18, -5, 0, 3, "None"),\
           Item(0, "Chaotic Amulet", "Amulet", 7, 7, -2, 3, "None"),\
           Item(0, "Wizard's Amulet", "Amulet", 3, 3, 5, 3, "None"),\
           Item(0, "Infinite Crossbow and Bolts", "Weapon", 0, 8, 5, 3, "None")\
          ]

#Names of Mythological Items or Items from another game
Legendaries = [Item(0, "Zenith", "Weapon", 5, 20, 1, 4, "Slash"),\
               Item(0, "Achilles's Armor", "Armor", 20, 5, 1, 4, "None"),\
               Item(0, "Dragon's Teeth Necklace", "Amulet", 5, 15, 2, 4, "None"),\
               Item(0, "Excalibur", "Weapon", 0, 25, 0.5, 4, "Slash"),\
               Item(0, "Kavacha", "Armor", 25, 0, 0, 4, "None"),\
               Item(0, "Celestial Shell", "Amulet", 12, 12, 1, 4, "None"),\
               Item(0, "Anhk Amulet", "Amulet", 35, -10, 2, 4, "None"),\
               Item(0, "Phylactery Amulet", "Amulet", -10, 35, 2, 4, "None"),\
               Item(0, "Sorcerrer's Emblem", "Amulet", 10, 10, 3, 4, "None"),\
               Item(0, "Lens of the Stars", "Amulet", 7, 7, 6, 4, "None"),\
               Item(0, "Ruyi Jingu Bang Staff", "Weapon", 2, 15, 7, 4, "Pierce")
               
              ]

#A default variable used as a control Items
Blank = Item(0, "Empty", "All", 0, 0, 0, 0, "None")

#The list that contains the info of all Items that the Player has currently collected
Inventory = []

#The list that contains the info of all Items that the Player has currently Equiped
EquipedItems = [Blank, Blank, Blank]


