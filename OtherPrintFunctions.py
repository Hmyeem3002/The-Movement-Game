#Get clear function for clearing the screen
from replit import clear

#Get readkey function for a better input function
import readchar

#Gets Stats and half of screen
from PlayerStats import GetMHP, GetHP, GetDamage, GetRange, GetDashLength, GetDashCooldownLength, GetHPPlus, GetDamagePlus, GetRangePlus, GetInventorySize, GetHalf
from PlayerStats import HPSet

#Gets neutral Item, Inventory list, and EquipedItems
from ItemClass import Blank, Inventory, EquipedItems

#Gets MakeCrate fuction for the ability to drop Items
from CrateClass import MakeCrate


#Colors for different rarities
Color_Code = {
  0: "\033[38;2;255;255;255m",
  1: "\033[38;2;59;160;255m",
  2: "\033[38;2;132;0;255m",
  3: "\033[38;2;186;41;89m",
  4: "\033[38;2;255;242;0m"
}

#Names of the different attack types
Names = {
  "None": "Regular",
  "Slash": "Slash",
  "Pierce": "Pierce",
  "Burst": "Explosion"
}

#Shows the Player's Stats, Equiped Items, and Inventory.
def InventoryView():

  location = 0
  while True:
    clear()
    #Shows Stats
    print("Player Stats:")
    print(f"HP: {int(GetHP()+GetHPPlus())}/{int(GetMHP()+GetHPPlus())}")
    print(f"Damage: {int(GetDamage()+GetDamagePlus()+0.5)}")
    print(f"Range: {GetRange()+GetRangePlus()}")
    print(f"Attack Type: {Names[EquipedItems[0].Attack]}")
    print("")
    #Shows Equiped Items
    print("Equiped Items: ")
    print(f"Weapon Slot: {Color_Code[EquipedItems[0].Rarity]}{EquipedItems[0].Name}\033[0m")
    print(f"Armor Slot: {Color_Code[EquipedItems[1].Rarity]}{EquipedItems[1].Name}\033[0m")
    print(f"Amulet Slot: {Color_Code[EquipedItems[2].Rarity]}{EquipedItems[2].Name}\033[0m")
    print("")
    #Shows Inventory in a checkbox list showing the Item's name, rarity color, level, and equiped status
    print("Inventory: ")
    for ilit, item in enumerate(Inventory):

      if location == ilit:
        print("■", end = " ")
      else:
        print("□", end = " ")

      print(f"{Color_Code[item.Rarity]}{item.Name}  {Color_Code[0]}Level: {item.Level}\033[0m", end = "  ")

      if item.Equiped:
        print("Equiped")
      else:
        print("")

    print("")
    #Warns the Player that their Inventory is full
    if len(Inventory) >= GetInventorySize():
      print("Your Inventory is full. Please drop an Item before picking up another one.")
      print("")
    #Gives small introduction about the avaliable player inputs
    print("Press Up or W to check the Item above.")
    print("Press Down or S to check the Item bellow.")
    print("Press Q to look at the Item's stats.")
    print("Press P or Enter to stop looking at your Inventory.")
    #Gets input
    Selection = readchar.readkey()

    if Selection == "q":
      clear()
      #Clears the screen and replaces it with the Item's name, Item type, Stat boosts, and input options
      print(f"{Color_Code[Inventory[location].Rarity]}{Inventory[location].Name}\033[0m")
      print("")
      print(f"Type of Item: {Inventory[location].Type}")
      print(f"HP Boost: {Inventory[location].HP}")
      print(f"Damage Boost: {Inventory[location].Damage}")
      print(f"Range Boost: {Inventory[location].Range}")
      if Inventory[location].Type == "Weapon":
        print(f"Attack Type: {Names[Inventory[location].Attack]}")
      print("")
      if Inventory[location].Equiped:
        print("Unequip Item: E")
      else:
        print("Equip Item: E")
      print("Drop Item: D")
      print("Stop Looking: Any Other key")
      #Gets another input
      Selection = readchar.readkey()
      if Selection == "e":
        #Either unequips the item or equips it based in it's status
        if Inventory[location].Equiped:
          TempBlank = Blank.Copy()
          TempBlank.Type = Inventory[location].Type
          TempBlank.Equip()
          #HP will have a minimum in case you die from unequiping a health boosting Item
          if GetHP() + GetHPPlus() <= 0:
            HPSet(1-GetHPPlus())
          Inventory[location].Equiped = False

        else:
          #If the HP boost would set you below 0, stop the Player from equipping the Item
          if (GetHP()+GetHPPlus())+Inventory[location].HP <= 0:
            print("You cannot equip this item as you have too little HP.")
            print("Please Heal before you Equip this Item.")
            input("Press Enter to stop reading.")
            print("")
          else:
            Inventory[location].Equip()
            if GetHP() + GetHPPlus() <= 0:
              HPSet(1-GetHPPlus())
      #Makes a Crate who's Item is the selected Item
      elif Selection == "d":
        #Can't drop an Item that is equipped
        if Inventory[location].Equiped:
          print("You cannot Drop this Item as it is currently Equiped.")
          print("Please Unequip this Item before Dropping it.")
          input("Press Enter to stop reading.")
          print("")
        else:
          MakeCrate([GetHalf(), GetHalf()], [0, 0, 0, 0], Inventory[location].Rarity, Inventory[location])
          Inventory.pop(location)

    #Leave loop.
    elif Selection == "p" or Selection == "\n":
      break

    #Go up/down
    elif Selection == "\x1b[B" or Selection == "s":
      location += 1
    elif Selection == "\x1b[A" or Selection == "w":
      location -= 1
    location %= max(1, len(Inventory))
    
  return





#Gives tutorial about input options
def KeyTut():
  clear()
  print("Change Direction: Arrow Keys or WASD")
  print("Use the key that corresponds with your current direction to move that direction.")
  print("")
  print("Dash: X")
  print(f"It allows you to move more spaces than normal. But it has a cooldown of {GetDashCooldownLength()} turns.")
  print(f"When you have to ability to dash, your character will be \033[38;2;0;255;21mgreen{Color_Code[0]}.\033[0m")
  print(f"When is Dash Mode, your character will turn \033[38;2;31;251;255mcyan{Color_Code[0]}.\033[0m")
  print(f"You can currently dash {GetDashLength()} tiles.")
  print("Attack: Z")
  print("Heal: H")
  print("Inventory: E")

  input("Press Enter to stop reading.")
  print("")







def MapInfo():
  clear()
  #Gives the names of things and an example of what they look like
  print("Your character: O")
  print("Your character changes colors based on when it is able to dash.")
  print("")
  print("Your line of sight: ⟍ ⟋")
  print("If something has the same location as one of the lines,")
  print("that line will not show so the other thing can be seen.")
  print("")
  print("Empty space that you are looking at: .")
  print("")
  print("Item crate: □")
  #Also gives descriptions when there is more info
  print("Crates have different colors based on their rarities.")
  print("As the rarity increases, all items of lower ranks won't appear.")
  #Showing Examples of the different colors that represent crate rarities
  print(f"{Color_Code[0]}Common: ☐   Rare: {Color_Code[1]}☐   {Color_Code[0]}Epic: {Color_Code[2]}☐   {Color_Code[0]}Mythic: {Color_Code[3]}☐   {Color_Code[0]}LEGENDARY: {Color_Code[4]}☐\033[0m")
  print("")
  print(f"{Color_Code[0]}Melee Enemy: \033[38;2;255;0;0mO   {Color_Code[0]}Ranged Enemy: \033[38;2;255;0;0m0  {Color_Code[0]}Speed Enemy: \033[38;2;255;0;0m⬮\033[0m")
  print("Enemies lose their color as their Health Points decrease.")
  print("When they die, they have a chance of dropping item crates.")

  print("              \033[38;2;255;0;0m⏶                    ⏶                   ⏶\033[0m")
  print(f"{Color_Code[0]}Melee Boss: \033[38;2;255;0;0m⏴ O ⏵   {Color_Code[0]}Ranged Boss: \033[38;2;255;0;0m⏴ 0 ⏵   {Color_Code[0]}Speed Boss: \033[38;2;255;0;0m⏴ ⬮ ⏵\033[0m")
  print("              \033[38;2;255;0;0m⏷                    ⏷                   ⏷\033[0m")
  print("Bosses also lose their color an their Health Points decrease.")
  print("Bosses are guarenteed to drop a Crate with the Epic rarity or higher.")
  print("")
  print("Obstacles: 𖠰")
  print("Unbreakable obstacles that block movement. They typically appear in clusters.")
  print("")
  print("Space that you are not looking at: _")
  input("Press Enter to stop reading.")
  print("")
