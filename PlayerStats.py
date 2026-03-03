#Is just Player Stats and other Game stats
MHP = 15
HP = MHP
Damage = 5
Range = 1

DashLength = 2
DashCooldownLength = 3


HPPlus = 0
DamagePlus = 0
RangePlus = float(0)

Level = 1
Exp = 0
InventorySize = 10

size = 23
half = int(size/2)


def GetMHP():
  return MHP

def GetHP():
  return HP

def GetDamage():
  return Damage

def GetRange():
  return Range

def GetDashLength():
  return DashLength

def GetDashCooldownLength():
  return DashCooldownLength




def GetHPPlus():
  return HPPlus

def GetDamagePlus():
  return DamagePlus

def GetRangePlus():
  return RangePlus



def GetLevel():
  return Level

def GetInventorySize():
  return InventorySize


def GetSize():
  return size

def GetHalf():
  return half

def MHPChange(amount):
  global MHP
  MHP += amount
  
def HPSet(amount):
  global HP
  HP = amount



def HPChange(amount):
  global HP
  HP = min(HP + amount, GetMHP())

def DamageChange(amount):
  global Damage
  Damage += amount



def DashLengthChange(amount):
  global DashLength
  DashLength += int(amount)



def HPPlusChange(amount):
  global HPPlus
  HPPlus += amount

def DamagePlusChange(amount):
  global DamagePlus
  DamagePlus += amount

def RangePlusChange(amount):
  global RangePlus
  RangePlus += amount




def ExpUp(plusvalue):
  global MHP
  global Level
  global Exp
  global HP
  global Damage
  Exp += plusvalue
  while True:
    if Exp >= Level**1.85*4+10:
      Exp -= Level**1.85*4+10
      Level += 1
      DamageChange(min((Damage/2)**(1+Level/50), Damage*2/3))
      MHPChange(min(int(MHP/2), MHP/8+10))
      HPSet(MHP)
      if Level % int(10+Level/2) == 0:
        DashLengthChange(min(1, max(DashLength-GetHalf()-6, 0)))
    else:
      break
  return



