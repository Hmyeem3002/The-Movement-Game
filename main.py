#Gets clear function for smooth transitions
from replit import clear
#Readkey for a better input function
import readchar
#Random for random stuff
import random


#imports from other files

#Collects all print functions that don't overly affect the main screen
from OtherPrintFunctions import InventoryView, KeyTut, MapInfo

#Collects Player stats for use
from PlayerStats import GetMHP, GetHP, GetRange, GetDashLength, GetDashCooldownLength, GetHPPlus, GetRangePlus, GetLevel, GetSize, GetHalf
from PlayerStats import HPChange

#Collects the Blank Item object so it can be used as a neutral variable
from ItemClass import Blank, EquipedItems

#Collects the functions that Opens crates and Makes crates
from CrateClass import Open, MakeCrate

#Collects the function that Makes bosses
from BossClass import MakeBoss

#Collects the Nothing Enemy object so it can be used as a neutral variable and collects the function that Makes enemies
from EnemyClass import Nothing
from EnemyClass import MakeEnemy

#Collects the function that lets the Enemies and Bosses do stuff
from BadGuys import BadAction

#Collects the function that Makes obstacles
from ObstacleThing import MakeObstacle

#Collects the lists containing Bosses, Enemies, and Obstacles. Also collects the functions that Move things and Checks what things are where
from ExistingEntity import Bosses, Enemies, Obstacles
from ExistingEntity import MoveAway, IsAnyoneThere


#turn variable that remembers how many turns have occured
turn = 1

#Unused
CheckMode = [GetHalf(), GetHalf()]

#Contols what Direction the player is facing.
#0 = Up, 1 = Right, 2 = Down, 3 = Left
Direction = 0
#Controls how far you move when you move
MovementAmount = 1
#Controls the cooldown between dashes
NoDashTime = 0

#dictionary the hold the basic color rarities
Color_Code = {
  0: "\033[38;2;255;255;255m", # Common. White color
  1: "\033[38;2;59;160;255m",  # Rare. Blue color
  2: "\033[38;2;132;0;255m",   # Epic. Purple color
  3: "\033[38;2;186;41;89m",   # Mythic. Pink color
  4: "\033[38;2;255;242;0m"    # LEGENDARY. Yellow color
}

#Function that checks whether a location is in sight
def ConditionOfSight(Vert, Hori):
  Flip = ((Direction > 1)*2)-1
  #Weird Math Stuff. 
  return ((Direction % 2 == 0 and (Vert)*Flip >= (GetHalf()+Flip)*Flip and (Hori)*Flip <= (Vert)*Flip and (Hori)*Flip >= (GetSize()-Vert-1)*Flip)) or ((Direction % 2 == 1 and (Hori)*Flip <= (GetHalf()-Flip)*Flip and (Vert)*Flip >= (Hori)*Flip and (Vert)*Flip <= (GetSize()-Hori-1)*Flip))

#Makes a starting Enemy to fight
MakeEnemy("Melee", [-2, 2])

#Makes a starting Crate to collect
MakeCrate([random.choice([-1, 1])*(random.randrange(GetHalf()-6, GetHalf()))+GetHalf(), random.choice([-1, 1])*(random.randrange(GetHalf()-6, GetHalf()))+GetHalf()], [60, 25, 10, 4], 0, Blank)

#Starts the game.
#As long as the Player's total HP doesn't go below 0, the game keeps on playing
while (GetHP()+GetHPPlus()) > 0:
  
  #Clears the screen to make the illusion of smooth animation
  clear()
  #Prints the Turns Made
  print("Turns Made:", turn, end = "")
  #Puts a reasonable amount of space between the turns made and player levels 
  for i in range(GetSize()+5-len(str(turn))-len(str(GetLevel()))):
    print(" ", end = "")
  #Prints the player's level
  print("Level:", GetLevel())
  #Print the board
  for i in range(GetSize()):
    print("[", end = "")
    for o in range(GetSize()):    
      #If the current print spot is in the middle of the map
      if i == GetHalf() and o == GetHalf():
        #Set the player's color based on certain conditions 
        if MovementAmount > 1:
          PlayerColor = "\033[38;2;0;255;221m"
        else:
          PlayerColor = f"\033[38;2;{max(NoDashTime, 0)*85};255;{max(NoDashTime, 0)*85}m"
        #Prints the player with the color set
        print(f"{PlayerColor}O\033[0m", end = "")
      #Is Unused
      elif [i, o] == CheckMode:
        print("⎕", end = "")    
      #If the current print spot is in the Player's line of sight
      elif ConditionOfSight(i, o):

        #Checks what thing is in the current print spot
        SomethingExists, TheThing = IsAnyoneThere(i, o)

        #If it is an Enemy, print a red enemy who's colors fades with their HP 
        if SomethingExists == "Enemy":
          print(f"\033[38;2;{255};{235-(int(TheThing.HP/TheThing.MaxHP)*235)};{235-(int(TheThing.HP/TheThing.MaxHP)*235)}m{TheThing.Name}\033[0m", end = "")

        #If it is a Crate, print a Crate who's color is based on their rarity. (See line 53 for indivisual colors)
        elif SomethingExists == "Crate":
          print(f"{Color_Code[TheThing.Rarity]}☐\033[0m", end = "")

        #If it is a Boss, we are going to have to do some special printing
        elif SomethingExists == "Boss":
          #Print a different icon based on the location is accordance to the Boss. Also make the color fade with HP
          if TheThing.Location == [i, o]:
            ToPrint = TheThing.Name      
          elif TheThing.Location[0] - 1 == i and TheThing.Location[1] == o:
            ToPrint = "⏶"
          elif TheThing.Location[0] == i and TheThing.Location[1] + 1 == o:
            ToPrint = "⏵" 
          elif TheThing.Location[0] == i and TheThing.Location[1] - 1 == o:
            ToPrint = "⏴"
          elif TheThing.Location[0] + 1 == i and TheThing.Location[1] == o:
            ToPrint = "⏷"
          print(f"\033[38;2;{255};{235-(int(TheThing.HP/TheThing.MaxHP)*235)};{235-(int(TheThing.HP/TheThing.MaxHP)*235)}m{ToPrint}\033[0m", end = "")
          
          ToPrint = " "

        #If it is an Obstacle, print a regular tree.
        elif SomethingExists == "Obstacle":
          print("𖠰", end = "")

        #If nothing is there but the location is in place diagonal to the Player, print vision lines to indicate the player's line of vision
        elif ((Direction == 0 or Direction == 3) and i == GetHalf()-1 and o == GetHalf()-1) or ((Direction == 1 or Direction == 2) and i == GetHalf()+1 and o == GetHalf()+1):
          print("⟍", end = "")
        elif ((Direction == 0 or Direction == 1) and i == GetHalf()-1 and o == GetHalf()+1) or ((Direction == 2 or Direction == 3) and i == GetHalf()+1 and o == GetHalf()-1):
          print("⟋", end = "")

        #If nothing is there at all, print a blank visable space icon
        else:
          print(".", end = "")

      #If it is not in the Player's line of sight, print a blank nonvisible space icon
      else:
        print("_", end = "")

      #To keep the grid looking nice, add spaces between icons. But not between icons and the end of the row
      if o < GetSize()-1:
        print(" ", end = "")
    #At the end of the row, print an end bracket to move the print spot to the next row and keep the board nice
    print("]")

  #Prints some inputs that act as a small guide. Also print your HP between the two input option things
  print("Key Info: K", end = "")
  for i in range(13-len(str(int(GetMHP())+GetHPPlus()))-len(str(int(GetHP())+GetHPPlus()))):
    if i == (GetHalf()+1)/2-len(str(int(GetMHP())+GetHPPlus())):
      print(f"Current HP: {int(GetHP())+GetHPPlus()}/{int(GetMHP())+GetHPPlus()}", end = "")
    else:
      print(" ", end = "")
  print("Map Info: M")

  #Gets Player input without use of Enter key
  Selection = readchar.readkey()

  #Movement Related Inputs
  
  #If the Player chose x, either set the Player's movement length to the DashLength or set their movement length back to normal
  if Selection == "x":
    if MovementAmount > 1:
      MovementAmount = 1
      NoDashTime = 0
    elif NoDashTime <= 0:
      MovementAmount = GetDashLength()
      NoDashTime = GetDashCooldownLength()
    else:
      #If the Cooldown isn't over yet, print this
      print("")
      print("Your Dash Cooldown is not over yet.")
      readchar.readkey()
    continue

  #If the readkey collects the left arrow or the "a" button, everything will move one to the right
  elif Selection == "\x1b[D" or Selection == "a":
    if Direction == 3:
      if MoveAway(1, MovementAmount):
        MovementAmount = 1
      else:
        continue
    else:
      Direction = 3
      continue

  #If the readkey collects the right arrow or the "d" button, everything will move one to the left 
  elif Selection == "\x1b[C"or Selection == "d":
    if Direction == 1:
      if MoveAway(1, -MovementAmount):
        MovementAmount = 1
      else:
        continue
    else:
      Direction = 1
      continue

  #If the readkey collects the down arrow or the "s" button, the current coordinates will move one down
  elif Selection == "\x1b[B" or Selection == "s":
    if Direction == 2:
      if MoveAway(0, -MovementAmount):
        MovementAmount = 1
      else:
        continue
    else:
      Direction = 2
      continue

  #If the readkey collects the up arrow or the "w" button, the current coordinates will move one up
  elif Selection == "\x1b[A" or Selection == "w":
    if Direction == 0:
      if MoveAway(0, MovementAmount):
        MovementAmount = 1
      else:
        continue
    else:
      Direction = 0
      continue

#Action Keys: 

  
  #If the readkey collects the z button, search for something that has a coordinate in range of the player and lower it's HP
  elif Selection == "z":
    Closest = Nothing
    for i in set(Enemies).union(set(Bosses)):
      Distance = ((GetHalf()-i.Location[0])**2 + (GetHalf()- i.Location[1])**2)**0.5
      if ConditionOfSight(i.Location[0], i.Location[1]) and Distance <= GetRange()+GetRangePlus() and Distance < ((GetHalf() - Closest.Location[0])**2+(GetHalf() - Closest.Location[1])**2)**0.5:
          Closest = i
          break

    
    if Closest != Nothing:
      AtType = EquipedItems[0].Attack
      if AtType == "Slash":
        for i in set(Enemies).union(set(Bosses)): 
          if i.Location[Direction%2] == Closest.Location[Direction%2] and abs(i.Location[(Direction-1)%2] - Closest.Location[(Direction-1)%2]) <= 1:
            i.ChangeHP()
            
      elif AtType == "Pierce":
        YDiff = (Closest.Location[1]-GetHalf())
        XDiff = (Closest.Location[0]-GetHalf())
        
        for i in set(Enemies).union(set(Bosses)):
          Distance = ((GetHalf()-i.Location[0])**2 + (GetHalf()- i.Location[1])**2)**0.5
          
          if Distance <= GetRange()+GetRangePlus():
            if (YDiff == 0 and i.Location[1] == Closest.Location[1]) or (XDiff == 0 and i.Location[0] == Closest.Location[0]):
              i.ChangeHP()
              continue
            #I seperated them so that the slope code wouldn't make a ZeroDivisionError
            elif ((i.Location[1]-GetHalf()) == YDiff/XDiff*(i.Location[0]-GetHalf())):
              i.ChangeHP()

      
      elif AtType == "Burst":
        for i in set(Enemies).union(set(Bosses)): 
          if abs(i.Location[0] - Closest.Location[0]) <= 1 and abs(i.Location[1] - Closest.Location[1]) <= 1:
            i.ChangeHP()

      else:
        Closest.ChangeHP()
    

    else:
      continue


  #If the readkey collects the h button, let the HP go up by 1
  elif Selection == "h":
    HPChange(1)

  
  #If the readkey collects the k button, open the function that describes what keys do
  elif Selection == "k":
    KeyTut()
    continue

  #If the readkey collects the m button, open the function that describes what each symbol means
  elif Selection == "m":
    MapInfo()
    continue

  #If the readkey collects the e button, open the function that shows your inventory
  elif Selection == "e":
    InventoryView()
    continue

  #If the readkey doesn't get a regonized input, restart the loop as if nothing has happened
  else:
    continue
    

  #After the Player Input is collected

  #Check if the Player is standing on any Crates. Open the said Crates which will destroy them and add an Item to the inventory
  Open()


  #All Creation Actions
  
  #Every 10 turns, have a 1 in 20 chance to spawn a Crate at a random location
  if turn % 10 == 0 and random.randrange(0, 20) == 0:
    Coordinate = [0, 0]

    #Setting up a way to have a nice random location outside the Player's screen. 
    Axis = random.randrange(0, 2)
    extra = random.randrange(2, 5)

    Coordinate[Axis] = random.randrange(-extra, GetSize()+extra)

    if Coordinate[Axis] >= 0 and Coordinate[Axis] <= GetSize():
      Coordinate[not Axis] = (random.choice([-1, 1])*random.randrange(GetHalf()+2, GetHalf()+5))+GetHalf()

    else:
      extra = random.randrange(2, 5)
      Coordinate[not Axis] = random.randrange(-extra, GetSize()+extra)

    MakeCrate(Coordinate, [60, 25, 10, 4], 0, Blank)
    

  #Every few turns, have a 1 in something chance to spawn a Melee Enemy at a random location
  if turn % max(20 - int(turn/10 + 0.5), 3) == 0 and random.randrange(0, max(5-int(turn/20), 2)) == 0:
    MakeEnemy("Melee", [4, 10])

  #Every few turns, have a 1 in something chance to spawn a Speed Enemy at a random location
  if turn % max(30 - int(turn/12 + 0.5), 3) == 0 and random.randrange(0, max(2, 10-int(turn/30))) == 0:
    MakeEnemy("Speed", [4, 10])

  #Every few turns, have a 1 in something chance to spawn a Ranged Enemy at a random location
  if turn % max(50 - int(turn/14 + 0.5), 3) == 0 and random.randrange(0, max(2, 11-int(turn/50))) == 0:
    MakeEnemy("Ranged", [4, 10])

  #Every few turns, have a 1 in something chance to spawn a random Boss at a random location
  if turn % max(100 - int(turn/30 + 0.5), 50) == 0 and random.randrange(0, max(2, 10-int(turn/100))) == 0:
    BossType = random.randrange(0, 3)
    BossChart = {
      0:"Melee",
      1:"Ranged",
      2:"Speed"
    }
    
    MakeBoss(BossChart[BossType], [2, 5])


  #If you aren't nearby any Obstacles, randomly spawn a new Obstacle biome
  for Tree in Obstacles:
    if abs(Tree.Location[0]-GetHalf()) <= GetHalf()+20 and abs(Tree.Location[1]-GetHalf()) <= GetHalf()+20:
      break

  else:
    MakeObstacle()


  #Lets all the Bad Guys do their turn. They will either go towards you or attack you based on how close they are.
  BadAction()


  #Update the turns and Dash Cooldown
  NoDashTime -= 1
  turn += 1


#If the while loop ended, that means you died. =)
print("You Died.")

